import json
import requests

from tnzapi.base.functions import Functions

class SMSReplyResult(object):

    def __init__(self,**kwargs):

        self.SMSReceived = []

        for key, value in kwargs.items():
            
            if key == "response":
                print(key)
                self.ParseResponse(value)
            
            if key == "error":
                self.Result = "Error"
                self.Message = value

    def ParseResponse(self, r):

        if r.text:

            #print(r.text)

            response = Functions.__parsejson__(self,r.text)

            if "Result" in response:
                self.Result = response["Result"]

            if "Status" in response:
                self.Result = response["Status"]

            if "MessageID" in response:
                self.MessageID = response["MessageID"]

            if self.Result == "Success" and "Data" in response:

                for key in response["Data"]:
                    if key == "JobNum":
                        self.JobNum = response["Data"][key]
                    if key == "Account":
                        self.Account = response["Data"][key]
                    if key == "SubAccount":
                        self.SubAccount = response["Data"][key]
                    if key == "Department":
                        self.Department = response["Data"][key]
                    if key == "SMSSent":
                        self.SMSSent = SMSSent(response["Data"][key])
                    if key == "SMSReceived":
                        for message in response["Data"][key]:
                            self.SMSReceived.append(message)

            else:
                if "ErrorMessage" in response:
                    self.Message = response["ErrorMessage"]
                else:
                    self.Message = ""

    """ Data """
    @property
    def Data(self):

        if self.Result == "Success":

            return {
                "Result": self.Result,
                "MessageID": self.MessageID,
                "Data": {
                    "JobNum": self.JobNum,
                    "Account": self.Account,
                    "SubAccount": self.SubAccount,
                    "Department": self.Department,
                    "SMSSent": {
                        "Date": self.SMSSent.Date,
                        "Destination": self.SMSSent.Destination,
                        "MessageText": self.SMSSent.MessageText
                    },
                    "SMSReceived": self.SMSReceived
                }
            }

        if self.Result == "Failed":
            return {
                "Result": self.Result,
                "Message": self.Message
            }
        
        return {
            "Result": self.Result,
            "Message": self.Message
        }

    """ Getters/Setters """
    @property
    def Result(self):
        return self.__result

    @Result.setter
    def Result(self,val):
        self.__result = val
    
    @property
    def SMSReceived(self):
        return self.__sms_received
    
    @SMSReceived.setter
    def SMSReceived(self, message):
        self.__sms_received = message

    def __repr__(self):
        return Functions.__pretty__(self, self.Data)

    def __str__(self):
        return 'SMSReplyResult()'

class SMSReplyMessage(object):

    def __init__(self, received):

        if received["Date"]:
            self.Date = received["Date"]
        
        if received["From"]:
            self.From = received["From"]
        
        if received["MessageText"]:
            self.MessageText = received["MessageText"]

class SMSSent(object):

    def __init__(self, message):

        if message["Date"]:
            self.Date = message["Date"]
        
        if message["Destination"]:
            self.Destination = message["Destination"]
        
        if message["MessageText"]:
            self.MessageText = message["MessageText"]
