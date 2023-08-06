class BaseResponse:
    def __init__(self, status: str = "SUCCESS", message: str = "") -> None:
        self._status = status
        self._message = message

    def __str__(self):
        return '{} : {}'.format(self._status, self._message)

class SmsResponse(BaseResponse):
    def __init__(self, status: str = "SUCCESS", message: str = "", data: dict = {}):
        super().__init__(status, message)
        self._uid = data.get('uid')
        self._receiver = data.get('to', None)
        self._sender = data.get('from', None)
        self._text = data.get('message', None)
        self._text_status = data.get('status', None)
        self._cost = data.get('cost', None)
        self._data = {}
        
    @property
    def status(self):
        return self._status
    
    @property
    def message(self):
        return self._message
        
    @property
    def uid(self):
        return self._uid

    @property
    def receiver(self):
        return self._receiver

    @property
    def sender(self):
        return self._sender

    @property
    def text(self):
        return self._text

    @property
    def delivery_status(self):
        return self._text_status

    @property
    def cost(self):
        return self._cost   
    
    @property
    def data(self):
        return self._data
    
    def add_data(self, key: str, value: str):
        self._data[key] = value
    
    