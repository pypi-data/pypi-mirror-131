import json
import requests

from tnzapi.base.functions import Functions

class SMSReceivedResult(object):

    def __init__(self,**kwargs):

        self.SMSReceived = []

        for key, value in kwargs.items():
            
            if key == "response":
                print(key)
                self.ParseResponse(value)
            
            if key == "error":
                self.Result = "Error"
                self.ErrorMessage = value

    def ParseResponse(self, r):

        if r.text:

            response = Functions.__parsejson__(self,r.text)

            if "Result" in response:
                self.Result = response["Result"]

            if "Status" in response:
                self.Result = response["Status"]

            if self.Result == "Success" and "Data" in response:
                if response["Data"]["SMSReceived"]:
                    for key in response["Data"]["SMSReceived"]:
                        self.SMSReceived.append(key)
            else:
                self.Message = response["Message"]

    """ Data """
    @property
    def Data(self):

        if self.Result == "Success":
            return {
                "Result": self.Result,
                "SMSReceived": self.SMSReceived
            }

        if self.Result == "Failed":
            return {
                "Result": self.Result,
                "ErrorMessage": self.ErrorMessage
            }
        
        return {
            "Result": self.Result,
            "ErrorMessage": self.ErrorMessage
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
        return self.__smsreceived
    
    @SMSReceived.setter
    def SMSReceived(self, message):
        self.__smsreceived = message

    def __repr__(self):
        return Functions.__pretty__(self, self.Data)

    def __str__(self):
        return 'SMSReceivedResult()'

class SMSReceivedMessage(object):

    def __init__(self, received):

        if received["Date"]:
            self.Date = received["Date"]
        
        if received["From"]:
            self.From = received["From"]
        
        if received["MessageText"]:
            self.MessageText = received["MessageText"]
