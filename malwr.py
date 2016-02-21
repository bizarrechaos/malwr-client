#! /usr/bin/env python
"""malwr.py

Usage:
  malwr.py init <apikey>
  malwr.py add <file> [options]
  malwr.py status <uuid> [options]

Options:
  -a KEY, --api-key KEY   This will override the api key in the config file.
  -s, --shared            Will share the added binary file with the community.
  -f, --force             Forces processing even if the sample is already analyzed.
  -h, --help              Show this screen.
  -v, --version           Show version.
"""
import json
import os

import ConfigParser
import requests

from docopt import docopt


requests.packages.urllib3.disable_warnings()


def jprint(jsondoc):
    print json.dumps(jsondoc, sort_keys=True, indent=2, separators=(',', ': '))


def createconfig(apikey):
    HOME = os.path.expanduser('~')
    CONFIG = HOME + '/.malwr.cfg'
    parser = ConfigParser.SafeConfigParser()
    parser.add_section('malwr')
    parser.set('malwr', 'apikey', apikey)
    with open(CONFIG, 'w') as fout:
        parser.write(fout)


def readconfig():
    HOME = os.path.expanduser('~')
    CONFIG = HOME + '/.malwr.cfg'
    parser = ConfigParser.SafeConfigParser()
    parser.read(CONFIG)
    return parser.get('malwr', 'apikey')


def addfile(payload):
    url = 'https://malwr.com/api/analysis/add/'
    r = requests.post(url, data=payload)
    jprint(r.json())


def checkstatus(payload):
    url = 'https://malwr.com/api/analysis/status/'
    r = requests.post(url, data=payload)
    jprint(r.json())


def argparse(a):
    if a['init']:
        createconfig(a['<apikey>'])
    else:
        if a['--api-key'] is not None:
            key = a['--api-key']
        else:
            key = readconfig()
            if key is None:
                exit(1)
        payload = {}
        payload['api_key'] = key
        if a['add']:
            payload['file'] = open(a['<file>'], 'rb')
            if a['--shared']:
                payload['shared'] = 'yes'
            if a['--force']:
                payload['force'] = 'yes'
            addfile(payload)
        elif a['status']:
            payload['uuid'] = a['<uuid>']
            checkstatus(payload)
        else:
            exit(1)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='malwr.py 0.1b')
    argparse(arguments)
