import argparse
import re

'''

A basic class for setup config,
it can automatically add params 
and parse params by cmd

'''

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def config_parse(config:object):
    attrs=[]
    for name in dir(config):
        if callable(getattr(config, name)):continue
        if re.match('__.*__',name):continue
        attrs.append(name)

    parser = argparse.ArgumentParser()
    # start to parse
    for name in attrs:
        value = getattr(config, name)
        if isinstance(value, list):
            parser.add_argument(f'--{name}', type=type(value[0]), nargs='*', default=value)
        elif isinstance(value, bool):
            parser.add_argument(f'--{name}', type=str2bool, default=value)
        else:
            parser.add_argument(f'--{name}', type=type(value), default=value)

    args = parser.parse_args()

    # update config
    for name, value in vars(args).items():
        setattr(config, name, value)

    return config

