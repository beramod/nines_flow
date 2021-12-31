import os
import importlib
import inspect
import time
import datetime
import re
from src.flow.controller import Controller
from src.util.html_logger import HtmlLogger
from define import BASE_DIR

class FlowManager:
    def run_flow(self, flow_name, argument_map):
        html_logger = HtmlLogger('nines_flow')
        controller_map = self.get_controller_map()
        if flow_name in controller_map:
            html_logger.info('start {}'.format(flow_name))
            t = time.time()
            object = controller_map.get(flow_name).get('object')()
            object.set_arguments(argument_map)
            res = object.run('manual')
            html_logger.info('success {}. {}'.format(flow_name, time.time() - t))
            return res
        else:
            html_logger.error('failed. not exist flow: {}'.format(flow_name))
            return False

    def parse_arguments(self, arguments_string):
        argument_map = {}
        pattern = "[^@]+=\'.+\'|[^@]+"
        regex = re.compile(pattern)
        args = regex.findall(arguments_string)
        for arg in args:
            arg = arg.replace('\'', '')
            parsed_arg = arg.split('=')
            argument_map[parsed_arg[0]] = parsed_arg[1]
        return argument_map

    def get_controller_map(self):
        package_path = os.path.join(BASE_DIR, 'src', 'flow', 'controller')
        modules = self.get_modules_in_package(package_path)

        get_controller_map = {}

        for module_name in modules:
            if '.pyc' in module_name:
                continue
            module_package_name = os.path.join(package_path, module_name)
            files = os.listdir(module_package_name)
            for file in files:
                if self.is_common_package_file(file) or file[-3:] != '.py':
                    continue

                module_name = self.make_module_name(BASE_DIR, file, module_package_name)
                for name, cls in inspect.getmembers(importlib.import_module(module_name, package=__name__), inspect.isclass):
                    if cls.__module__ != module_name or not issubclass(cls, Controller):
                        continue
                    if cls.FLOW_NAME is not None:
                        handlers = []
                        for each in cls.HANDLERS:
                            handlers.append(list(map(lambda el: {'handlerName': el.HANDLER_NAME, 'description': el.DESCRIPTION}, each)))
                        get_controller_map.update({cls.FLOW_NAME: {'description': cls.DESCRIPTION, 'object': cls, 'handlers': handlers}})
        return get_controller_map

    def get_modules_in_package(self, package_path):
        packeges = os.listdir(package_path)
        modules = []
        for package in packeges:
            if self.is_common_package_file(package):
                continue
            modules.append(package)
        return modules

    def is_common_package_file(self, file) -> bool:
        if file in ['__init__.py', '__pycache__']:
            return True
        return False

    def make_module_name(self, base_dir: str, file: str, module_package_name: str) -> str:
        file_name = file[:-3]
        module_name = os.path.join(module_package_name, file_name)
        module_name = module_name.replace(base_dir + os.sep, '')
        module_name = module_name.replace(os.sep, '.')
        return module_name

    def get_refined_now(self):
        now = datetime.datetime.now()
        minute = int(now.strftime('%M'))
        hour = int(now.strftime('%H'))
        day = int(now.strftime('%d'))
        month = int(now.strftime('%m'))
        weekday = now.weekday() + 1
        refined_time = [minute, hour, day, month, weekday]
        return refined_time
