import argparse
import json
import sys


# Add a config subparser to the parser passed in
# add a --config option that overwrites the defaults
# and is overwritten by the passed in arguments
class ArgumentConfig:
    def __init__(self, parser: argparse.ArgumentParser):
        self.parser = parser

        self.parser.add_argument('--config', '-c',
                                 nargs='?',
                                 metavar='FILENAME')

        # TODO: put this in subparser
        self.parser.add_argument('--write_config', '-wc',
                                 nargs='?',
                                 metavar='FILENAME',
                                 const='stdout')

    def parse_args(self, *args, **kwargs):

        # parse an empty list to get the defaults
        defaults = vars(self.parser.parse_args([]))

        passed_args = vars(self.parser.parse_args(*args, **kwargs))

        # Only keep the args that aren't the default
        passed_args = {key: value for (key, value) in passed_args.items()
                       if (key in defaults and defaults[key] != value)}

        config_path = passed_args.pop('config', None)
        if config_path:
            with open(config_path, 'r') as config_file:
                configargs = json.load(config_file)
        else:
            configargs = dict()

        # override defaults with config with passed args
        options = {**defaults, **configargs, **passed_args}

        # remove the config options from options. They're not needed any more
        # and we don't want them serialized
        options.pop('config', None)
        options.pop('write_config', None)

        # print the options (to file) if needed
        config_dst = passed_args.pop('write_config', None)
        if config_dst:
            print(json.dumps(options, sort_keys=True, indent=4))
            if config_dst != 'stdout':
                with open(config_dst, 'w', encoding='utf-8') as config_file:
                    print(json.dumps(options, sort_keys=True, indent=4), file=config_file)
                    print('Current options saved to: %r' % config_dst)
            sys.exit(0)

        return argparse.Namespace(**options)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--integers', metavar='N', type=int, nargs='+',
                    default=[1, 2, 3],
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const='sum', default='max',
                    help='sum the integers (default: find the max)')

options = ArgumentConfig(parser)

o = options.parse_args()

print(o)

# defaults = parser.parse_args([])
# print(defaults)

# args = parser.parse_args()
# print(args)
# print(args.accumulate(args.integers))
