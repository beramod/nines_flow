import time
import traceback
from datetime import datetime
from src.util.html_logger import HtmlLogger
from src.util.script_lock import ScriptLock
from src.http.nines_api import NinesApi

class Handler:
    LOCK = False
    HANDLER_NAME = 'base_handler'
    DESCRIPTION = ''

    def __init__(self, flow_name, job_id, shared_data):
        self._flow_name = flow_name
        self._job_id = job_id
        self._shared_data = shared_data
        self._arguments = {}
        self._html_logger: HtmlLogger = None
        self._script_lock = ScriptLock(self.HANDLER_NAME)
        self._nines_api = NinesApi()
        self._start_time = None
        self._mode = ''

    def set_arguments(self, arguments):
        self._arguments = arguments

    def run(self):
        self._mode = 'real'
        self._html_logger = HtmlLogger(self.HANDLER_NAME)
        try:
            self.start_handler_job()
            self._start_time = datetime.now()
            t = time.time()
            self._html_logger.info('start FLOW: {}, HANDLER: {}'.format(self._flow_name, self.HANDLER_NAME))
            self._run()
            self._html_logger.info('FLOW: {}, HANDLER: {}, success: {}'.format(self._flow_name, self.HANDLER_NAME, time.time() - t))
            self.complete_handler_job()
            return True
        except Exception:
            error = traceback.format_exc()
            self.failed_handler_job(error)
            self._html_logger.info('FLOW: {}, HANDLER: {}, fail. {}'.format(self._flow_name, self.HANDLER_NAME, error))
            print(error)
            return False

    ## override
    def _run(self):
        pass

    def test(self):
        self._mode = 'test'
        try:
            self.start_handler_job()
            self._start_time = datetime.now()
            t = time.time()
            print('[HANDLER] {} start'.format(self.HANDLER_NAME))
            result = self._test()
            print('[HANDLER] {}: sucess, {}'.format(self.HANDLER_NAME, time.time() - t))
            self.complete_handler_job()
            return result
        except Exception:
            error = traceback.format_exc()
            self.failed_handler_job(error)
            print('[HANDLER] {}: failed, {}'.format(self.HANDLER_NAME, error))
            return False

    ## override
    def _test(self):
        pass

    def check_run(self, refined_now):
        if self.LOCK and self._script_lock.check_lock():
            return False
        return True

    def start_handler_job(self):
        if self._mode == 'real':
            self._nines_api.update_flow_job_handler_run(self._job_id, self.HANDLER_NAME)
        self._shared_data[self.HANDLER_NAME] = {
            'start_time': self._start_time,
            'state': 'run'
        }

    def failed_handler_job(self, message):
        if self._mode == 'real':
            self._nines_api.update_flow_job_handler_fail(self._job_id, self.HANDLER_NAME, message)
        end_time = datetime.now()
        run_time = (end_time - self._start_time).total_seconds()
        self._shared_data[self.HANDLER_NAME] = {
            'start_time': self._start_time,
            'end_time': end_time,
            'run_time': run_time,
            'state': 'failed'
        }

    def complete_handler_job(self):
        if self._mode == 'real':
            self._nines_api.update_flow_job_handler_complete(self._job_id, self.HANDLER_NAME)
        end_time = datetime.now()
        run_time = (end_time - self._start_time).total_seconds()
        self._shared_data[self.HANDLER_NAME] = {
            'start_time': self._start_time,
            'end_time': end_time,
            'run_time': run_time,
            'state': 'completed'
        }