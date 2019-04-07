import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--production', action='store_true')
parser.add_argument('-d', '--development', action='store_true')
args = parser.parse_args()

if args.production:
    from config.production import *
else:
    from config.development import *
