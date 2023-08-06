from abc import ABCMeta, abstractmethod

class IApp(metaclass=ABCMeta):
    @abstractmethod
    def get_headers():
        """
        Return the headers to use.
        Returns:
            dict -- The headers.
        """
        pass
        

class App(IApp):
    
    __instance = None
    
    def __init__(self, token: str, secret: str):
        """
        Initialize the App.
        Arguments:
            token {str} -- The token to use.
            secret {str} -- The secret to use.
        Raises:
            ValueError: If token or secret is None.
            Exception: If initialization happend twice.
        """
        if App.__instance is not None:
            raise Exception("This class is a singleton!")
        self.token = token
        self.secret = secret
        self.url = "https://sms.send.lk/api/v3/"
        App.__instance = self
    
    @staticmethod
    def get_instance():
        """
        Get the instance of the App.
        Raises:
            ValueError: If the instance is not initialized.

        Returns:
            App: The instance. 
        """
        if App.__instance is None:
            raise ValueError("App not initialized.")
        else:
            return App.__instance
    
    @staticmethod
    def get_headers() -> dict:
        headers = {
            "Authorization": "Bearer " + App.__instance.token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return headers
