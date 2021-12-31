import sys
from src.flow_manager import FlowManager

def test(args):
    flow_manager = FlowManager()
    controller_map = flow_manager.get_controller_map()
    flow_name = args[1]
    argument_map = None
    if len(args) > 2:
        arguments_string = args[2]
        argument_map = flow_manager.parse_arguments(arguments_string)
    object = controller_map.get(flow_name).get('object')()
    object.set_arguments(argument_map)
    result = object.test()
    return result

if __name__ == '__main__':
    test(sys.argv)