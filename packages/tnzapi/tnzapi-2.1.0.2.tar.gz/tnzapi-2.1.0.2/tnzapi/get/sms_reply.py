import requests
import json
import asyncio

from tnzapi.get._common import Common
from tnzapi.base import SMSReplyResult

class SMSReply(Common):

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
            "Type": "SMSReply",
            "MessageID" : self.MessageID
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/get/sms/reply", data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return SMSReplyResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return SMSReplyResult(error=str(e))

        return SMSReplyResult(response=r)

    """ Private async function to POST message to TNZ REST API """
    async def __PostMessageAsync(self):

        return self.__PostMessage()

    """ Function to send message """
    def Poll(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)

        """ Checking validity """
        if not self.Sender :
            return SMSReplyResult(error="Missing Sender")
        
        if not self.APIKey :
            return SMSReplyResult(error="Missing APIKey")
        
        if not self.MessageID:
            return SMSReplyResult(error="Missing MessageID")
        
        return self.__PostMessage()

    """ Function to send message """
    async def PollAsync(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)
        
        """ Checking validity """
        if not self.Sender :
            return SMSReplyResult(error="Missing Sender")
        
        if not self.APIKey :
            return SMSReplyResult(error="Missing APIKey")
        
        if not self.MessageID:
            return SMSReplyResult(error="Missing MessageID")
        
        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'SMSReply(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'