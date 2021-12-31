from src.flow.handler import Handler
from src.http.nines_api import NinesApi
from datetime import datetime
from src.db.soul import SoulDB
from src.flow_manager import FlowManager

class SyncHandler(Handler):
    HANDLER_NAME = 'sync_handler'
    DESCRIPTION = 'NINES Flow의 코드상의 Controller와 서버상의 Flow 정보들의 Sync를 맞추는 Handler'

    def _run(self):
        flow_manager = FlowManager()
        flow_map = flow_manager.get_controller_map()

        for flow_name in flow_map:
            flow_map.get(flow_name).pop('object')

        prod_db = SoulDB.get_prod_db()
        flow_db = prod_db.database('flow')
        key_value_col = flow_db.get_collection('keyValue')
        now = datetime.now()
        key_value_col.update({'key': 'flowMap'}, {
            '$set': {
                'value': flow_map,
                'updatedAt': now
            }
        })
        nines_api = NinesApi()
        res = nines_api.run_flow_sync()
        self._html_logger.highlight('SYNC RESULT: {}'.format(str(res[1])))

    def _test(self):
        flow_manager = FlowManager()
        flow_map = flow_manager.get_controller_map()

        for flow_name in flow_map:
            flow_map.get(flow_name).pop('object')

        print('[HANDLER-Logic Check] {}: {}'.format(self.HANDLER_NAME, str(flow_map)))
        return True