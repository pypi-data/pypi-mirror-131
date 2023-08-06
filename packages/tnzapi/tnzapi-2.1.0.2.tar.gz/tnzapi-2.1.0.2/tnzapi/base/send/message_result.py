import json

from tnzapi.base.functions import Functions

class MessageResult(object):

    def __init__(self, **kwargs):

        self.Result = ""
        self.MessageID = ""
        self.ErrorMessage = ""

        for key, value in kwargs.items():
            
            if key == "response":
                print(key)
                self.ParseResponse(value)
            
            if key == "error":
                self.Result = "Error"
                self.ErrorMessage = value

    def ParseResponse(self, r):

        if r.text:

            self.__response_string__ = r.text

            response = Functions.__parsejson__(self,r.text)

            for key in response:

                if key == "Result":
                    self.Result = response[key]
                
                if key == "MessageID":
                    self.MessageID = response[key]
                
                if key == "ErrorMessage":
                    self.ErrorMessage = response[key]

    """ Data """
    @property
    def Data(self):

        if self.Result == "Success":
            return {
                "Result": self.Result,
                "MessageID": self.MessageID,
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
        return 'MessageResult('+ self.__response_string__ +')'

    