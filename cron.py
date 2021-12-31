import traceback
from src.http.nines_api import NinesApi
from src.flow_manager import FlowManager
from multiprocessing import Process
from src.util.alerter import KafkaProducer

def cron():
    try:
        nines_api = NinesApi()
        flow_names = nines_api.get_flow_schedule()
        flow_manager = FlowManager()
        controller_map = flow_manager.get_controller_map()
        workers = []
        for flow_name in flow_names:
            if not controller_map.get(flow_name):
                continue
            object = controller_map.get(flow_name).get('object')()
            worker = Process(target=object.run)
            workers.append(worker)
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join()
    except Exception:
        KafkaProducer.publish('cron', traceback.format_exc())

if __name__ == '__main__':
    cron()
