import requests
import json
import asyncio

from tnzapi.send._common import Common
from tnzapi.base import MessageResult

class Email(Common):

    EmailSubject    = ""
    MessagePlain    = ""
    MessageHTML     = ""

    SMTPFrom        = ""
    From            = ""
    FromEmail       = ""
    ReplyTo         = ""

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        self.SetArgsChild(kwargs)
    
    """ Destructor """
    def __del__(self):
        self.EmailSubject    = ""
        self.MessagePlain    = ""
        self.MessageHTML     = ""

        self.SMTPFrom        = ""
        self.From            = ""
        self.FromEmail       = ""
        self.ReplyTo         = ""
    
    """ Set Args """
    def SetArgsChild(self, kwargs):

        #super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "EmailSubject":
                self.EmailSubject = value
            
            if key == "MessagePlain":
                self.MessagePlain = value
            
            if key == "MessageHTML":
                self.MessageHTML = value

            if key == "SMTPFrom":
                self.SMTPFrom = value

            if key == "From":
                self.From = value
            
            if key == "FromEmail":
                self.FromEmail = value
            
            if key == "ReplyTo":
                self.ReplyTo = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "MessageType": "Email",
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
                "EmailSubject": self.EmailSubject,
                "SMTPFrom": self.SMTPFrom,
                "From": self.From,
                "FromEmail": self.FromEmail,
                "ReplyTo": self.ReplyTo,
                "MessagePlain": self.MessagePlain,
                "MessageHTML": self.MessageHTML,
                "Destinations" : self.Recipients,
                "Files": self.Attachments
            }
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/send/email", data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return MessageResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return MessageResult(error=str(e))
        
        return MessageResult(response=r)

    """ Private async function to POST message to TNZ REST API """
    async def __PostMessageAsync(self):

        return self.__PostMessage()

    """ Function to send message """
    def SendMessage(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)


        if not self.Sender :
            return MessageResult(error="Empty Sender")
        
        if not self.APIKey :
            return MessageResult(error="Empty API Key")

        if self.WebhookCallbackURL and not self.WebhookCallbackFormat :
            return MessageResult(error="Missing WebhookCallbackFormat - JSON or XML")

        if not self.EmailSubject :
            return MessageResult(error="Missing EmailSubject")

        if not self.MessagePlain and not self.MessageHTML:
            return MessageResult(error="Missing MessagePlain and MessageHTML")

        if not self.Recipients:
            return MessageResult(error="Missing Recipient(s)")

        return self.__PostMessage()

    """ Async Function to send message """
    async def SendMessageAsync(self, **kwargs):

        if kwargs != None and len(kwargs) > 0:
            self.__init__(kwargs)

        if not self.Sender :
            return MessageResult(error="Empty Sender")
        
        if not self.APIKey :
            return MessageResult(error="Empty API Key")

        if self.WebhookCallbackURL and not self.WebhookCallbackFormat :
            return MessageResult(error="Missing WebhookCallbackFormat - JSON or XML")

        if not self.MessagePlain and not self.MessageHTML:
            return MessageResult(error="Missing MessagePlain and MessageHTML")

        if not self.Recipients:
            return MessageResult(error="Missing Recipient(s)")

        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Email(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'
    