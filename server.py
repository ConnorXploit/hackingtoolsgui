import subprocess, time, argparse, os, requests, sys

if not os.name == 'nt':
    if not os.geteuid() == 0:
        sys.exit("\nOnly root can run this script\n")

parser = argparse.ArgumentParser()
   
parser.add_argument('-p', '--port', help="set django server port")

args = parser.parse_args()

port = int(os.environ.get('PORT', 2222))
if args.port:
    port = int(args.port)

menu = """
    ==============================
    | Welcome to HackingToolsGUI |
    |----------------------------|
    |  Initiating Django Server  |
    |----------------------------|
    |   http://127.0.0.1:{p}/{spaces}|
    ==============================
""".format(p=port, spaces='       '[len(str(port)):])

p = None
want_exit = False
want_update = False
while not want_exit:
    if want_update:
        print('Updating...')
        p = subprocess.call(['bash', 'update_server.sh'])
        
    try:
        if not p:
            print(menu)
            p = subprocess.call(['python3', 'manage.py', 'runserver', '0.0.0.0:{p}'.format(p=port)])
        time.sleep(2)
    except KeyboardInterrupt:
        res = input('[DJANGO AUTO-RESTARTER] - Want to close autoloader or update? (N/y/u): ')
        # Create a function for upload to pypi automatically and change versions
        if res == 'y':
            want_exit = True
        if res == 'u':
            want_update = True