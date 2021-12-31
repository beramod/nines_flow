from functools import reduce
from src.db.soul import SoulDB
from src.flow.controller import Controller
from src.flow.handler.test.test1_handler import Test1Handler
from src.flow.handler.test.test2_handler import Test2Handler
from src.flow.handler.test.test3_handler import Test3Handler

class TestParallelController(Controller):
    FLOW_NAME = 'testParallel'
    DESCRIPTION = 'test parallel'
    HANDLERS = [
        [Test1Handler, Test2Handler],
        [Test3Handler]
    ]

    def _test(self):
        print('test code!')