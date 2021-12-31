from functools import reduce
from src.db.soul import SoulDB
from src.flow.controller import Controller
from src.flow.handler.test.test1_handler import Test1Handler
from src.flow.handler.test.test2_handler import Test2Handler
from src.flow.handler.test.test3_handler import Test3Handler

class TestParallelCustomController(Controller):
    FLOW_NAME = 'testParallelCustom'
    DESCRIPTION = 'test parallel custom logic'

    HANDLERS = [
        [Test1Handler, Test2Handler],
        [Test3Handler]
    ]

    def _run(self):
        for handler_classes in self.HANDLERS:
            for handler_class in handler_classes:
                handler_obj = handler_class()
                if handler_obj.HANDLER_NAME == 'test2_handler':
                    handler_obj.set_arguments(self._arguments)
                handler_obj.run()

    def _test(self):
        print('test code!')