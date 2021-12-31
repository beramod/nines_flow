from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from src.api.database.mongodb import get_client
from main import main
from test import test

flow_control_router = InferringRouter()

@cbv(flow_control_router)
class FLowControlController:
    @flow_control_router.get("/run", tags=[])
    async def run_flow(self, flow_name):
        hot_db = get_client('hot')
        flow_db = hot_db['flow']
        flow_col = flow_db.get_collection('flow')
        flow_doc = await flow_col.find_one({'flowName': flow_name})
        if not flow_doc:
            return {'result': None, 'message': 'Not exist flow [{}]'.format(flow_name), 'code': 400}
        res = main(['', flow_name])
        return {'result': res, 'message': '', 'code': 200}

    @flow_control_router.get("/run/test", tags=[])
    async def run_flow_test(self, flow_name):
        hot_db = get_client('hot')
        flow_db = hot_db['flow']
        flow_col = flow_db.get_collection('flow')
        flow_doc = await flow_col.find_one({'flowName': flow_name})
        if not flow_doc:
            return {'result': None, 'message': 'Not exist flow [{}]'.format(flow_name), 'code': 400}
        res = test(['', flow_name])
        return {'result': res, 'message': '', 'code': 200}
