from typing import Dict
from datetime import datetime

class HandlerRunTime:
    def __init__(self):
        self.start_time: datetime = None
        self.end_time: datetime = None
        self.run_time: float = 0
        self.state: str = 'ready'
        self.message: str = ''

    def json(self):
        return {
            'startTime': self.start_time if self.start_time is None else str(self.start_time),
            'endTime': self.end_time if self.end_time is None else str(self.end_time),
            'runTime': self.run_time if self.run_time is None else str(self.run_time),
            'state': self.state,
            'message': self.message
        }

class FlowJob:
    def __init__(self):
        self.flow_name: str = ''
        self.job_id: str = ''
        self.job_type: str = 'schedule'
        self.state: str = 'ready'
        self.start_time: datetime = None
        self.end_time: datetime = None
        self.run_time: float = 0
        self.handlers_run_time: Dict[str, HandlerRunTime] = {}
        self.message: str = ''

    def add_handler_run_time(self, handler_name):
        handler_run_time_obj: HandlerRunTime = HandlerRunTime()
        self.handlers_run_time[handler_name] = handler_run_time_obj

    def json(self):
        handler_run_time = {}
        for handler_name in self.handlers_run_time:
            handler_run_time[handler_name] = self.handlers_run_time.get(handler_name).json()
        doc = {
            'flowName': self.flow_name,
            'jobId': self.job_id,
            'jobType': self.job_type,
            'state': self.state,
            'startTime': str(self.start_time),
            'endTime': self.end_time if self.end_time is None else str(self.end_time),
            'runTime': self.run_time,
            'handlersRunTime': handler_run_time,
            'message': self.message
        }
        return doc
