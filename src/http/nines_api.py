from src.http import HttpRequests
from src.model.flow_job import FlowJob
from src.api import settings


class NinesApi(HttpRequests):
    def __init__(self):
        super().__init__()
        self._api_key = '{api key}'
        self._env = settings.ENV
        if self._env == 'PROD':
            self._api_server_url = '{api uri}'
        else:
            self._api_server_url = 'http://127.0.0.1:11001'

    def get_flow_schedule(self):
        res = self.get('/api/v1/flow/schedule', {})
        if not res:
            return []
        return res.get('result')

    def create_flow_job(self, flow_job: FlowJob):
        res = self.post('/api/v1/flow/job', {}, flow_job.json())
        if res.get('code') != 200:
            return None
        return res.get('result')

    def update_flow_job_fail(self, job_id, message):
        self.put('/api/v1/flow/job/fail', {}, {'job_id': job_id, 'message': message})

    def update_flow_job_complete(self, job_id):
        self.put('/api/v1/flow/job/complete', {'job_id': job_id}, {})

    def update_flow_job_handler_run(self, job_id, handler_name):
        self.put('/api/v1/flow/job/handler/run', {'job_id': job_id, 'handler_name': handler_name,}, {})

    def update_flow_job_handler_fail(self, job_id, handler_name, message):
        body = {
            'job_id': job_id,
            'handler_name': handler_name,
            'message': message
        }
        self.put('/api/v1/flow/job/handler/fail', {}, body)

    def update_flow_job_handler_complete(self, job_id, handler_name):
        query = {
            'job_id': job_id,
            'handler_name': handler_name
        }
        res = self.put('/api/v1/flow/job/handler/complete', query, {})

    def run_flow_sync(self):
        res = self.post('/api/v1/flow/sync', {}, {})
        return res.get('result')
