import json

from tnzapi.base.functions import Functions

class SetRequestResult(object):

    def __init__(self, **kwargs):

        self.Result = ""
        self.MessageID = ""
        self.ErrorMessage = ""

        for key, value in kwargs.items():
            
            if key == "response":
                self.ParseResponse(value)
            
            if key == "error":
                self.Result = "Error"
                self.ErrorMessage = value

    def ParseResponse(self, r):

        if r.text:

            self.__response_string__ = r.text

            response = Functions.__parsejson__(self,r.text)

            if response["Result"]:
                self.Result = response["Result"]

            if response["MessageID"]:
                self.MessageID = response["MessageID"]

            if self.Result == "Success":

                for key in response["Data"]:
                    if key == "Status":
                        self.Status = response["Data"][key]
                    if key == "JobNum":
                        self.JobNum = response["Data"][key]
                    if key == "Action":
                        self.Action = response["Data"][key]

            else:
                if "ErrorMessage" in response:
                    self.ErrorMessage = response["ErrorMessage"]
                else:
                    self.ErrorMessage = ""

    """ Data """
    @property
    def Data(self):

        if self.Result == "Success":
            return {
                "Result": self.Result,
                "MessageID": self.MessageID,
                "Data": {
                    "Status": self.Status,
                    "JobNum": self.JobNum,
                    "Action": self.Action
                }
            }

        if self.Result == "Failed":
            return {
                "Result": self.Result,
                "MessageID": self.MessageID,
                "ErrorMessage": self.ErrorMessage
            }
        
        return {
            "Result": self.Result,
            "ErrorMessage": self.ErrorMessage
        }
    
    @property
    def Result(self):
        return self.__Result
    
    @Result.setter
    def Result(self,val):
        self.__Result = val

    @property
    def MessageID(self):
        return self.__MessageID
    
    @MessageID.setter
    def MessageID(self,val):
        self.__MessageID = val
    
    @property
    def ErrorMessage(self):
        return self.__ErrorMessage
    
    @ErrorMessage.setter
    def ErrorMessage(self,val):
        self.__ErrorMessage = val

    def __repr__(self):
        return Functions.__pretty__(self, self.Data)

    def __str__(self):
        return 'SetRequestResult('+ self.__response_string__ +')'

    