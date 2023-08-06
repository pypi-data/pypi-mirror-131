import requests
import json
import asyncio

from tnzapi.set._common import Common
from tnzapi.base import SetRequestResult

class Pacing(Common):

    NumberOfOperators   = 0

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        self.SetArgsChild(kwargs)

    """ Update Data """
    def SetArgsChild(self, kwargs):

        #super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "NumberOfOperators":
                self.NumberOfOperators = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "APIVersion": self.APIVersion,
            "Type": "Pacing",
            "MessageID" : self.MessageID,
            "NumberOfOperators": self.NumberOfOperators
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/set/pacing", data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return SetRequestResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return SetRequestResult(error=str(e))

        return SetRequestResult(response=r)

    """ Private async function to POST message to TNZ REST API """
    async def __PostMessageAsync(self):

        return self.__PostMessage()

    """ Function to send message """
    def SendRequest(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)

        if not self.Sender :
            return SetRequestResult(error="Empty Sender")
        
        if not self.APIKey :
            return SetRequestResult(error="Empty API Key")
        
        if not self.MessageID:
            return SetRequestResult(error="Empty Message ID")

        if not self.NumberOfOperators:
            return SetRequestResult(error="Empty Number of Operators")
        
        return self.__PostMessage()

    """ Async Function to send message """
    async def SendRequestAsync(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)

        if not self.Sender :
            return SetRequestResult(error="Empty Sender")
        
        if not self.APIKey :
            return SetRequestResult(error="Empty API Key")
        
        if not self.MessageID:
            return SetRequestResult(error="Empty Message ID")

        if not self.NumberOfOperators:
            return SetRequestResult(error="Empty Number of Operators")
        
        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Pacing(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'