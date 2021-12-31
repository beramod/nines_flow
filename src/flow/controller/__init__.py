import time
import traceback
from datetime import datetime
from threading import Thread
from multiprocessing import Process, Manager
from typing import List
from src.flow.handler import Handler
from src.util.html_logger import HtmlLogger
from src.util.script_lock import ScriptLock
from src.http.nines_api import NinesApi
from src.model.flow_job import FlowJob
from src.util.ses_mail_sender import SESMailSender
from src.util.alerter import KafkaProducer

class Controller:
    FLOW_NAME = 'base_controller'
    DESCRIPTION = 'base controller'
    HANDLERS: List[List[Handler]] = []
    PARALLEL_MODE = 'fork'

    def __init__(self):
        self._arguments = {}
        self._html_logger: HtmlLogger = None
        self._script_lock = ScriptLock(self.FLOW_NAME)
        self._nines_api = NinesApi()
        self._flow_job: FlowJob = FlowJob()
        self._flow_job.flow_name = self.FLOW_NAME

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self, job_type='schedule'):
        self._html_logger = HtmlLogger(self.FLOW_NAME)
        self._flow_job.start_time = datetime.now()
        if not self.create_flow_job(job_type):
            self.failed_flow_job('failed create flow job')
            return False
        try:
            t = time.time()
            self._html_logger.info('start')
            self._run()
            self.complete_flow_job()
            self._html_logger.info('success: {}'.format(time.time() - t))
            return True
        except BaseException:
            error = traceback.format_exc()
            KafkaProducer.alert(self._flow_job.flow_name, f'Abort: {error}')
            self.failed_flow_job(error)
            self._html_logger.info('fail. {}'.format(error))
            return False

    ## override
    def _run(self):
        shared_data = Manager().dict()
        for handler_classes in self.HANDLERS:
            workers = []
            handler_names = []
            for handler_class in handler_classes:
                handler_names.append(handler_class.HANDLER_NAME)
                obj = handler_class(self._flow_job.flow_name, self._flow_job.job_id, shared_data)
                if self._arguments:
                    obj.set_arguments(self._arguments)
                worker = None
                if self.PARALLEL_MODE == 'fork':
                    worker = Process(target=obj.run)
                else:
                    worker = Thread(target=obj.run)
                workers.append(worker)
                worker.start()
            for worker in workers:
                worker.join()
            for handler_name in handler_names:
                if shared_data.get(handler_name).get('state') == 'failed':
                    KafkaProducer.alert(self._flow_job.flow_name, f'{handler_name} failed!')
                    raise Exception('Handler Failed')

    def test(self):
        try:
            t = time.time()
            print('----------------------[CONTROLLER] {} start----------------------'.format(self.FLOW_NAME))
            res = self._test()
            print('----------------------[CONTROLLER] {}: {}, {}----------------------'.format(self.FLOW_NAME, 'success' if res else 'failed', time.time() - t))
            return res
        except Exception:
            error = traceback.format_exc()
            print('----------------------[CONTROLLER] {}: failed(exception) {}----------------------'.format(self.FLOW_NAME, error))
            return False

    ## override
    def _test(self):
        shared_data = Manager().dict()
        for handler_classes in self.HANDLERS:
            workers = []
            handler_names = []
            for handler_class in handler_classes:
                obj = handler_class(self._flow_job.flow_name, self._flow_job.job_id, shared_data)
                handler_names.append(handler_class.HANDLER_NAME)
                if self._arguments:
                    obj.set_arguments(self._arguments)
                worker = None
                if self.PARALLEL_MODE == 'fork':
                    worker = Process(target=obj.test)
                else:
                    worker = Thread(target=obj.test)
                workers.append(worker)
                worker.start()
            for worker in workers:
                worker.join()
            for handler_name in handler_names:
                if shared_data.get(handler_name).get('state') == 'failed':
                    return False
        return True

    def check_run(self, refined_now):
        if self._script_lock.check_lock():
            return False
        return True

    def create_flow_job(self, job_type='schedule') -> bool:
        self._flow_job.job_type = job_type
        for handler_classes in self.HANDLERS:
            for handler_class in handler_classes:
                self._flow_job.add_handler_run_time(handler_class.HANDLER_NAME)
        res = self._nines_api.create_flow_job(self._flow_job)
        if not res:
            return False
        self._flow_job.job_id = res.get('jobId')
        self._flow_job.start_time = datetime.strptime(res.get('startTime'), '%Y-%m-%dT%H:%M:%S.%f')
        return True

    def failed_flow_job(self, message = ''):
        self._nines_api.update_flow_job_fail(self._flow_job.job_id, message)

    def complete_flow_job(self):
        self._nines_api.update_flow_job_complete(self._flow_job.job_id)