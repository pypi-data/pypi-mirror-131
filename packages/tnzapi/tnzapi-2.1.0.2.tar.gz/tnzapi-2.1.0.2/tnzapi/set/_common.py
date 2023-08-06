from tnzapi import _config
from tnzapi.base.functions import Functions

class Common:

    Sender          = _config.__Sender__
    APIKey          = _config.__APIKey__
    APIVersion      = _config.__APIVersion__
    APIURL          = _config.__APIURL__
    APIHeaders      = _config.__APIHeaders__

    MessageID       = ""

    """ Constructor """
    def __init__(self,kwargs):

        self.Sender          = _config.__Sender__
        self.APIKey          = _config.__APIKey__
        self.APIVersion      = _config.__APIVersion__
        self.APIURL          = _config.__APIURL__
        self.APIHeaders      = _config.__APIHeaders__

        self.MessageID      = ""

        self.SetArgsCommon(kwargs)

    """ Destructor """
    def __del__(self):
        self.Sender          = ""
        self.APIKey          = ""
        self.APIVersion      = ""
        self.APIURL          = ""
        self.APIHeaders      = ""

        self.MessageID       = ""

    """ Set Args """
    def SetArgsCommon(self, kwargs):

        if "Sender" in kwargs:
            self.Sender = _config.__Sender__ = kwargs.pop("Sender")

        if "APIKey" in kwargs:
            self.APIKey = _config.__APIKey__ = kwargs.pop("APIKey")
        
        if "MessageID" in kwargs:
            self.MessageID = kwargs.pop("MessageID")
    
    def __pretty__(self,obj):
        
        return Functions.__pretty__(self,obj)