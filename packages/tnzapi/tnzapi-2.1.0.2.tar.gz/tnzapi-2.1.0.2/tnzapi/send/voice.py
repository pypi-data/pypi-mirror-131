import requests
import base64
import json
import asyncio

from tnzapi.send._common import Common

from tnzapi.base import MessageResult
from tnzapi.base import Keypad

class Voice(Common):

    CallerID    = ""
    Options     = ""

    BillingAccount = ""

    NumberOfOperators   = 0
    RetryAttempts       = 0
    RetryPeriod         = 1

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

        self.MessageToPeople             = ""
        self.MessageToAnswerPhones       = ""
        self.CallRouteMessageToPeople    = ""
        self.CallRouteMessageToOperators = ""
        self.CallRouteMessageOnWrongKey  = ""

        self.ReportTo    = ""
        self.Keypads     =[]

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
            
            if key == "MessageToPeople":
                self.AddMessageData(key,value)
            
            if key == "MessageToAnswerPhones":
                self.AddMessageData(key,value)
            
            if key == "CallRouteMessageToPeople":
                self.AddMessageData(key,value)
            
            if key == "CallRouteMessageToOperators":
                self.AddMessageData(key,value)
            
            if key == "CallRouteMessageOnWrongKey":
                self.AddMessageData(key,value)
            
            if key == "Recipients":
                self.Recipients = value
            
            if key == "ReportTo":
                self.ReportTo = value

    """ API Data """
    @property
    def APIData(self):
        return {
            "Sender": self.Sender,
            "APIKey": self.APIKey,
            "MessageType": "Voice",
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
                "BillingAccount": self.BillingAccount,
                "Department": self.Department,
                "ChargeCode": self.ChargeCode,
                "ReportTo": self.ReportTo,

                "CallerID": self.CallerID,

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

    """ Add Message Data """
    def AddMessageData(self, type, file):

        content = file

        if open(file,"rb").read():
            content = base64.b64encode(open(file,"rb").read()).decode("utf-8")
        
        if type == "MessageToPeople":
            self.MessageToPeople = content
        elif type == "MessageToAnswerPhones":
            self.MessageToAnswerPhones = content
        elif type == "CallRouteMessageToPeople":
            self.CallRouteMessageToPeople = content
        elif type == "CallRouteMessageToOperators":
            self.CallRouteMessageToOperators = content
        elif type == "CallRouteMessageOnWrongKey":
            self.CallRouteMessageOnWrongKey = content
    
    """ Add Keypad """
    def AddKeypad(self, **kwargs):

        keypad = Keypad(**kwargs)

        if keypad.Play == "" and keypad.PlayFile != "":
            keypad.Play = base64.b64encode(open(keypad.PlayFile,"rb").read()).decode("utf-8")

        self.Keypads.append(
        {
            "Tone": keypad.Tone,
            "RouteNumber": keypad.RouteNumber,
            "Play": keypad.Play,
            "PlayFile": keypad.PlayFile
        })


    """ Private function to POST message to TNZ REST API """
    def __PostMessage(self):

        try:
            r = requests.post(self.APIURL+"/send/voice", data=json.dumps(self.APIData), headers=self.APIHeaders)
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
            return MessageResult(error="Empty APIKey")

        if self.WebhookCallbackURL and not self.WebhookCallbackFormat :
            return MessageResult(error="Missing WebhookCallbackFormat - JSON or XML")
        
        if not self.Recipients:
            return MessageResult(error="Empty Recipient(s)")

        if not self.MessageToPeople:
            return MessageResult(error="Missing MessageToPeople")
        
        """
        if len(self.Keypads) > 0:
            for keypad in self.Keypads:
                if keypad["PlayFile"] == "" and keypad["Play"] != "":
                    err_msg = "Keypad " + str(keypad["Tone"]) + str(": Use PlayFile='[file name]' instead of Play=xxx.")
                    return MessageResult(error=err_msg)
        """

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
            return MessageResult(error="Missing MessageToPeople")
        
        """
        if len(self.Keypads) > 0:
            for keypad in self.Keypads:
                if keypad["PlayFile"] == "" and keypad["Play"] != "":
                    err_msg = "Keypad " + str(keypad["Tone"]) + str(": Use PlayFile='[file name]' instead of Play=xxx.")
                    return MessageResult(error=err_msg)
        """

        return await asyncio.create_task(self.__PostMessageAsync())

    def __repr__(self):
        return self.__pretty__(self.APIData)

    def __str__(self):
        return 'Voice(Sender='+self.Sender+', APIKey='+str(self.APIKey)+ ')'