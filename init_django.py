import subprocess, time

p = None
want_exit = False
while not want_exit:
    try:
        if not p:
            print('Initiating Django Server!')
            p = subprocess.call(['python', 'manage.py', 'runserver', '0.0.0.0:2222'])
        time.sleep(2)
    except KeyboardInterrupt:
        res = input('[DJANGO AUTO-RESTARTER] - Want to close autoloader? (N/y): ')
        if res == 'y':
            want_exit = True