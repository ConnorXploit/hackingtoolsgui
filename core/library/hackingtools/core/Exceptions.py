class IndexError(Exception):

    def __init__(self, message):
        super().__init__(message)

class ConnectionTimeout(Exception):

    def __init__(self, message):
        super().__init__(message)

class InvalidValue(Exception):

    def __init__(self, message):
        super().__init__(message)

class QueryError(Exception):

    def __init__(self, message):
        super().__init__(message)

class ParameterRequired(Exception):

    def __init__(self, message):
        super().__init__(message)

class NotFoundException(Exception):

    def __init__(self, message="", code=404):
        super().__init__(f'{message}, Code:{code}')

class AnyException(Exception):

    def __init__(self, message="", code=500):
        super().__init__(f'{message}, Code:{code}')
    
    @staticmethod
    def default(response_text, status_code):
        return AnyException('Response code is {status_code}. Body: {response_text}. Something went wrong. Please report issue.'.format(response_text=response_text, status_code=status_code), status_code)

class AuthException(Exception):
    def __init__(self, message = "", code = 401):
        super().__init__(f'{message}, Code:{code}')