from functools import reduce
from src.db.soul import SoulDB
from src.flow.controller import Controller
from src.flow.handler.test.test1_handler import Test1Handler
from src.flow.handler.test.test2_handler import Test2Handler
from src.flow.handler.test.test3_handler import Test3Handler

class TestBasicController(Controller):
    FLOW_NAME = 'testBasic'
    DESCRIPTION = 'test basic'
    HANDLERS = [
        [Test1Handler],
    ]

    def _run(self):
        for jobs in self.HANDLERS:
            for each in jobs:
                each.set_arguments({'test'})

    def _test(self):
        print(self._arguments)
        print('test code!')