#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os, time, sys, json, threading, queue
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackingtoolsgui.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def checkPackages():
    # If Windows NT
    extra_packages = {
        "nt" : ['pywin32', 'pywin32-ctypes', 'opencv-python'],
        "linux" : ['opencv-python'],
    }
    for system in extra_packages:
        if system in os.name:
            for package in extra_packages[system]:
                if not package in sys.modules:
                    pipmain(['install', package])

restart_flag = False
def restartServerDjango():
    restart = False
    with open(os.path.join(os.path.dirname(__file__), 'core' , '__auto_restart_flag__.json')) as json_data_file:
        restart = json.load(json_data_file)["restart"]
    
    if restart:
        print('Restarting automatically the server')

        new_conf = { "restart" : False }
        with open(os.path.join(os.path.dirname(__file__), 'core' , '__auto_restart_flag__.json'), 'w', encoding='utf8') as outfile:  
            json.dump(new_conf, outfile, indent=4, ensure_ascii=False)

        restart_flag = True
        sys.exit(1)
        raise KeyboardInterrupt

if __name__ == '__main__':
    checkPackages()

    import threading
    import queue

    # t1 = threading.Thread(target=restartServerDjango)
    # t1.start()
    # t1.join()

    class myThread(threading.Thread):
        def __init__(self, name, queue):
            threading.Thread.__init__(self)
            self.queue = queue
        def run(self):
            process_data(self.queue)

    def process_data(q):
        while True:
            try:
                restartServerDjango()
            except:
                raise
            time.sleep(3)
        import sys 
        sys.exit()
    try:
        que = queue.Queue()
        thread = myThread("restart-auto-checker", que)
        thread.start()

        main()
    except Exception as e:
        sys.exit(e)
