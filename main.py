import sys
from src.flow_manager import FlowManager

def main(args):
    flow_manager = FlowManager()
    flow_name = args[1]
    argument_map = None
    if len(args) > 2:
        arguments_string = args[2]
        argument_map = flow_manager.parse_arguments(arguments_string)
    res = flow_manager.run_flow(flow_name, argument_map)
    return res

if __name__ == '__main__':
    main(sys.argv)
