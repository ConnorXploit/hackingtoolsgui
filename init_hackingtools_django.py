#!/usr/bin/env python
import subprocess, sys
import argparse

parser = argparse.ArgumentParser(description='Script for init the server of Django. It allows to automatically STOP and START the server, because HackingToolsGUI needs to restarts literally for auto create the Views of the new modules you create. If you are going to use normally, execute \'python manage.py runserver 0.0.0.0:2222\' with your favorite port. Instead of been looking at the console and those things, use this script :)')

parser.add_argument('--port', metavar='-p', type=int, default=2222, help='a port for the server (default: 2222)')

def initServer(port=2222):
    return subprocess.Popen([sys.executable, 'manage.py 0.0.0.0:{p}'.format(p=port)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    args = vars(parser.parse_args())
    if args:
        port = 2222
        if 'port' in args or 'p' in args:
            port = int(args['port']) if 'port' in args else int(args['p'])
        
