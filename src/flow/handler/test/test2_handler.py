from src.flow.handler import Handler

class Test2Handler(Handler):
    HANDLER_NAME = 'test2_handler'
    DESCRIPTION = 'test2 handler description'

    def _run(self):
        result = {
            'handlerName': self.HANDLER_NAME,
            'description': self.DESCRIPTION,
            'arguments': self._arguments
        }
        print(result)