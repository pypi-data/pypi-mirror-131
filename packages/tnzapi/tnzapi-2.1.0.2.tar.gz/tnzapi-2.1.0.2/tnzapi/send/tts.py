import requests
import json
import asyncio

from tnzapi.send._common import Common

from tnzapi.base import MessageResult
from tnzapi.base import Keypad

class TTS(Common):

    CallerID    = ""
    Options     = ""

    BillingAccount = ""

    NumberOfOperators   = 0
    RetryAttempts       = 0
    RetryPeriod         = 1

    TTSVoiceType                = "Female2"
    MessageToPeople             = ""
    MessageToAnswerPhones       = ""
    CallRouteMessageToPeople    = ""
    CallRouteMessageToOperators = ""
    CallRouteMessageOnWrongKey  = ""

    ReportTo    = ""
    Keypads     =[]

    """ Constructor """
    def __init__(self, kwargs):

        super().__init__(kwargs)

        self.SetArgsChild(kwargs)

    """ Destructor """
    def __del__(self):

        self.CallerID    = ""
        self.Options     = ""

        self.BillingAccount = ""

        self.NumberOfOperators   = 0
        self.RetryAttempts       = 0
        self.RetryPeriod         = 1

        self.TTSVoiceType                = "Female2"
        self.MessageToPeople             = ""
        self.MessageToAnswerPhones       = ""
        self.CallRouteMessageToPeople    = ""
        self.CallRouteMessageToOperators = ""
        self.CallRouteMessageOnWrongKey  = ""

    """ Set Args """
    def SetArgsChild(self, kwargs):

        #super().SetArgs(kwargs)

        for key, value in kwargs.items():

            if key == "CallerID":
                self.CallerID = value
            
            if key == "Options":
                self.Options = value

            if key == "BillingAccount":
                self.BillingAccount = value

            if key == "NumberOfOperators":
                self.NumberOfOperators = value
            
            if key == "RetryAttempts":
                self.RetryAttempts = value
            
            if key == "RetryPeriod":
                self.RetryPeriod = value
            
            if key == "TTSVoiceType":
                self.TTSVoiceType = value
            
            if key == "MessageToPeople":
                self.MessageToPeople = value

            if key == "MessageToAnswerPhones":
                self.MessageToAnswerPhones = value
            
            if key == "CallRouteMessageToPeople":
                self.CallRouteMessageToPeople = value

            if key == "CallRouteMessageToOperators":
                self.CallRouteMessageToOperators = value
            
            if key == "CallRouteMessageOnWrongKey":
                self.CallRouteMessageOnWrongKey = value

            if key == "ReportTo":
                self.ReportTo = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "MessageType": "TextToSpeech",
            "APIVersion": self.APIVersion,
            "MessageData" :
            {
                "Mode": self.SendMode,
                "MessageID" : self.MessageID,

                "ErrorEmailNotify": self.ErrorEmailNotify,
                "WebhookCallbackURL": self.WebhookCallbackURL,
                "WebhookCallbackFormat": self.WebhookCallbackFormat,

                "CallerID": self.CallerID,
                "Reference": self.Reference,
                "SendTime": self.SendTime,
                "TimeZone": self.Timezone,
                "SubAccount": self.SubAccount,
                "BillingAccount": self.BillingAccount,
                "Department": self.Department,
                "ChargeCode": self.ChargeCode,
                "ReportTo": self.ReportTo,

                "Voice": self.TTSVoiceType,
                "MessageToPeople": self.MessageToPeople,
                "MessageToAnswerphones": self.MessageToAnswerPhones,
                "CallRouteMessageToPeople": self.CallRouteMessageToPeople,
                "CallRouteMessageToOperators": self.CallRouteMessageToOperators,
                "CallRouteMessageOnWrongKey": self.CallRouteMessageOnWrongKey,

                "Keypads": self.Keypads,

                "NumberOfOperators": self.NumberOfOperators,
                "RetryAttempts": self.RetryAttempts,
                "RetryPeriod": self.RetryPeriod,
                "Options": self.Options,

                "Destinations" : self.Recipients
            }
        }

    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/send/tts", data=json.dumps(self.APIData), headers=self.APIHeaders)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return MessageResult(response=r)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            return MessageResult(error=str(e))

        return MessageResult(response=r)

    """ Private async function to POST message to TNZ REST API """
    async def __PostMessageAsync(self):

        return self.__PostMessage()

    """ AddKeypad Function """
    def AddKeypad(self, **kwargs):

        keypad = Keypad(**kwargs)

        self.Keypads.append(
        {
            "Tone": keypad.Tone,
            "RouteNumber": keypad.RouteNumber,
            "Play": keypad.Play
        })

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

        if not self.MessageToPeople:
            return MessageResult(error="Empty MessageToPeople")

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

        if not self.MessageToPeople:
            return MessageResult(error="Empty MessageToPeople")

        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'TTS(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'