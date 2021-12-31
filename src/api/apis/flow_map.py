import subprocess
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from src.api.database.mongodb import get_client

flow_map_router = InferringRouter()

@cbv(flow_map_router)
class FLowMapController:
    @flow_map_router.get("/", tags=[])
    async def get_flow_map(self):
        hot_db = get_client('hot')
        flow_db = hot_db['flow']
        key_value_col = flow_db.get_collection('keyValue')
        cursor = key_value_col.find({'key': 'flowMap'})
        result = []
        async for document in cursor:
            document.pop('_id')
            result.append(document)
        await cursor.close()
        return {'result': result[0], 'message': '', 'code': 200}
