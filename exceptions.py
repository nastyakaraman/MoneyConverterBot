class ConvertionException(Exception):
    pass

class InputDataException(ConvertionException):
    pass

class ServerResponseException (ConvertionException):
    pass