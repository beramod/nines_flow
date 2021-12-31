from src.flow.handler import Handler

class Test3Handler(Handler):
    HANDLER_NAME = 'test3_handler'
    DESCRIPTION = 'test3 handler description'

    def _run(self):
        result = {
            'handlerName': self.HANDLER_NAME,
            'description': self.DESCRIPTION,
            'arguments': self._arguments
        }
        print(result)