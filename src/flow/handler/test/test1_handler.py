from src.flow.handler import Handler

class Test1Handler(Handler):
    HANDLER_NAME = 'test1_handler'
    DESCRIPTION = 'test1 handler description'

    def _run(self):
        result = {
            'handlerName': self.HANDLER_NAME,
            'description': self.DESCRIPTION,
            'arguments': self._arguments
        }
        print(result)