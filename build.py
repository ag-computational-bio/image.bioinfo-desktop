#!/usr/bin/env python
import yaml
from subprocess import call
import os

stream = file('config.yaml', 'r')
config = yaml.load(stream)

image_name = config['name'] + '-' + config['version'] + '.qcow2'
architecture = config['dib']['architecture']
elements = config['dib']['elements']
packages = config['dib']['packages']

cli = 'disk-image-create'
if architecture:
    cli += ' -a ' + architecture

cli += ' -o ' + image_name
if packages:
    for p in packages:
        cli += ' -p ' + p

if elements:
    for e in elements:
        cli += ' ' + e

print("Executing: " + cli)
os.system(cli)
