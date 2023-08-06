class Get(object):

    def __init__(self):
        self._status = None
        self._sms_received = None
        self._sms_reply = None
        self._result = None

    def Status(self,**kwargs):

        from tnzapi.get.status import Status

        if self._status != None:
            del(self._status)
            
        self._status = Status(kwargs)

        return self._status
    
    def SMSReceived(self,**kwargs):

        from tnzapi.get.sms_received import SMSReceived

        if self._sms_received != None:
            del(self._sms_received)
            
        self._sms_received = SMSReceived(kwargs)

        return self._sms_received

    def SMSReply(self, **kwargs):

        from tnzapi.get.sms_reply import SMSReply

        if self._sms_reply != None:
            del(self._sms_reply)

        self._sms_reply = SMSReply(kwargs)

        return self._sms_reply
    
    def Result(self, **kwargs):

        from tnzapi.get.result import Result

        if self._result != None:
            del(self._result)
            
        self._result = Result(kwargs)

        return self._result