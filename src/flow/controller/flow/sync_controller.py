from src.flow.controller import Controller
from src.flow.handler.flow.sync_handler import SyncHandler


class SyncController(Controller):
    FLOW_NAME = 'flow_sync'
    DESCRIPTION = 'Code - Server Flow sync를 맞추는 flow'
    HANDLERS = [
        [SyncHandler]
    ]
