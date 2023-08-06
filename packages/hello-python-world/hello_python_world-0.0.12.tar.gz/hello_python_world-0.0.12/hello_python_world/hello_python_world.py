class HelloPythonWorld:

    def __init__(self, message: str = ''):
        self._message = message

    def message(self) -> str:
        message = self._message
        if not message:
            message = 'Python'
        return f'Hello {message} World'