import requests
import json
import asyncio

from tnzapi.send._common import Common
from tnzapi.base import MessageResult

class Fax(Common):

    Resolution          = "high"
    CSID                = ""
    StampFormat		    = ""
    WatermarkFolder     = ""
    WatermarkFirstPage  = "No"
    WatermarkAllPages   = "No"
    RetryAttempts	    = 0
    RetryPeriod		    = 0

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        self.SetArgsChild(kwargs)

    """ Destructor """
    def __del__(self):
        self.Resolution         = "high"
        self.CSID               = ""
        self.StampFormat		= ""
        self.WatermarkFolder    = ""
        self.WatermarkFirstPage = "No"
        self.WatermarkAllPages  = "No"
        self.RetryAttempts	    = 0
        self.RetryPeriod		= 0

    """ Update Data """
    def SetArgsChild(self, kwargs):

        #super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "Resolution":
                self.Resolution = value
            
            if key == "CSID":
                self.CSID = value
            
            if key == "StampFormat":
                self.StampFormat = value
            
            if key == "WatermarkFolder":
                self.WatermarkFolder = value
            
            if key == "WatermarkFirstPage":
                self.WatermarkFirstPage = value
            
            if key == "WatermarkAllPages":
                self.WatermarkAllPages = value
            
            if key == "RetryAttempts":
                self.RetryAttempts = value
            
            if key == "RetryPeriod":
                self.RetryPeriod = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "MessageType": "Fax",
            "APIVersion": self.APIVersion,
            "MessageData" :
            {
                "Mode": self.SendMode,
                "MessageID" : self.MessageID,
                
                "ErrorEmailNotify": self.ErrorEmailNotify,
                "WebhookCallbackURL": self.WebhookCallbackURL,
                "WebhookCallbackFormat": self.WebhookCallbackFormat,

                "Reference": self.Reference,
                "SendTime": self.SendTime,
                "TimeZone": self.Timezone,
                "SubAccount": self.SubAccount,
                "Department": self.Department,
                "ChargeCode": self.ChargeCode,
                "Resolution": self.Resolution,
                "CSID": self.CSID,
                "StampFormat": self.StampFormat,
                "WatermarkFolder": self.WatermarkFolder,
                "WatermarkFirstPage": self.WatermarkFirstPage,
                "WatermarkAllPages": self.WatermarkAllPages,
                "Destinations" : self.Recipients,
                "Files": self.Attachments
            }
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/send/fax", data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return MessageResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return MessageResult(error=str(e))

        return MessageResult(response=r)

    """ Private function to POST message to TNZ REST API """
    async def __PostMessageAsync(self):

        return self.__PostMessage()

    """ Function to send message """
    def SendMessage(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)

        if not self.Sender :
            return MessageResult(error="Empty Sender")
        
        if not self.APIKey :
            return MessageResult(error="Empty APIKey")

        if self.WebhookCallbackURL and not self.WebhookCallbackFormat :
            return MessageResult(error="Missing WebhookCallbackFormat - JSON or XML")
        
        if not self.Recipients:
            return MessageResult(error="Empty Recipient(s)")

        if not self.Attachments:
            return MessageResult(error="Empty Attachment(s)")

        return self.__PostMessage()

    """ Async Function to send message """
    async def SendMessageAsync(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)

        if not self.Sender :
            return MessageResult(error="Empty Sender")
        
        if not self.APIKey :
            return MessageResult(error="Empty APIKey")

        if self.WebhookCallbackURL and not self.WebhookCallbackFormat :
            return MessageResult(error="Missing WebhookCallbackFormat - JSON or XML")
        
        if not self.Recipients:
            return MessageResult(error="Empty Recipient(s)")

        if not self.Attachments:
            return MessageResult(error="Empty Attachment(s)")

        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Fax(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'