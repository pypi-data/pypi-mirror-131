class Send(object):

    def __init__(self):
        self._email = None
        self._fax = None
        self._sms = None
        self._tts = None
        self._voice = None

    def Email(self,**kwargs):

        from tnzapi.send.email import Email

        if self._email != None:
            del(self._email)
        
        self._email = Email(kwargs)

        return self._email
    
    def Fax(self,**kwargs):

        from tnzapi.send.fax import Fax

        if self._fax != None:
            del(self._fax)
            
        self._fax = Fax(kwargs)

        return self._fax

    def SMS(self,**kwargs):

        from tnzapi.send.sms import SMS

        if self._sms != None:
            del(self._sms)
            
        self._sms = SMS(kwargs)

        return self._sms

    def TTS(self,**kwargs):

        from tnzapi.send.tts import TTS

        if self._tts != None:
            del(self._tts)
            
        self._tts = TTS(kwargs)
        
        return self._tts
    
    def Voice(self,**kwargs):

        from tnzapi.send.voice import Voice

        if self._voice != None:
            del(self._voice)
            
        self._voice = Voice(kwargs)

        return self._voice