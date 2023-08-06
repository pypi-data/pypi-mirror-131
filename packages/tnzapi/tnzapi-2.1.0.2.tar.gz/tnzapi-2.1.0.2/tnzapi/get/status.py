import requests
import json
import asyncio

from tnzapi.get._common import Common
from tnzapi.base import StatusRequestResult

class Status(Common):

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        #self.SetArgs(kwargs)

    """ Set Args """
    #def SetArgs(self, kwargs):
        
        #super().SetArgs(kwargs)

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "APIVersion": self.APIVersion,
            "Type": "Status",
            "MessageID" : self.MessageID
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/get/status", data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return StatusRequestResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return StatusRequestResult(error=str(e))

        return StatusRequestResult(response=r)

    """ Private async function to POST message to TNZ REST API """
    async def __PostMessageAsync(self):

        return self.__PostMessage()

    """ Function to send message """
    def Poll(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)

        if not self.Sender :
            return StatusRequestResult(error="Missing Sender")
        
        if not self.APIKey :
            return StatusRequestResult(error="Missing APIKey")
        
        if not self.MessageID:
            return StatusRequestResult(error="Missing MessageID")
        
        return self.__PostMessage()

    """ Function to send message """
    async def PollAsync(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)

        if not self.Sender :
            return StatusRequestResult(error="Missing Sender")
        
        if not self.APIKey :
            return StatusRequestResult(error="Missing APIKey")
        
        if not self.MessageID:
            return StatusRequestResult(error="Missing MessageID")
        
        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Status(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'