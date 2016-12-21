#!/usr/bin/env python
import argparse
import os
import yaml
from subprocess import call

# parse arguments
parser = argparse.ArgumentParser(description='Build image from configuration yaml file')
parser.add_argument('-c', '--config', default='config.yaml')
args = parser.parse_args()

# read yaml
stream = file(args.config, 'r')
config = yaml.load(stream)

# check mandatory fields
mandatory_fields = ['name', 'version', ['dib','architecture'], ['dib', 'elements']]
for field in mandatory_fields:
    if isinstance(field, list):
        if not config[field[0]][field[1]]:
            raise Exception("Mandatory field '"+field[0] +"."+field[1]+"' not specified in config file")
    else:
        if not config[field]:
            raise Exception("Mandatory field '"+field+"' not specified in config file")

# build commandline
image_name = config['name'] + '-' + config['version'] + '.qcow2'
architecture = config['dib']['architecture']
elements = config['dib']['elements']
packages = config['dib']['packages']

cli = 'disk-image-create'
if architecture:
    cli += ' -a ' + architecture

cli += ' -o ' + image_name
if packages:
    cli += ' -p '
    cli += ','.join(packages)

if elements:
    for e in elements:
        cli += ' ' + e

# Execute diskimage builder
if 'ELEMENTS_PATH' in os.environ:
    os.environ['ELEMENTS_PATH'] = os.getcwd() + '/elements:' + os.environ['ELEMENTS_PATH']
else:
    os.environ['ELEMENTS_PATH'] = os.getcwd() + '/elements'

print("Executing: " + cli)
os.system(cli)
