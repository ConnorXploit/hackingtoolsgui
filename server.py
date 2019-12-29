import subprocess, time, argparse, os, requests

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
while not want_exit:
    try:
        if not p:
            print(menu)
            p = subprocess.call(['python3', 'manage.py', 'runserver', '0.0.0.0:{p}'.format(p=port)])
        time.sleep(2)
    except KeyboardInterrupt:
        res = input('[DJANGO AUTO-RESTARTER] - Want to close autoloader? (N/y): ')
        # Create a function for upload to pypi automatically and change versions
        if res == 'y':
            want_exit = True