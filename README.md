# HackingTools

[![PyPI version](https://badge.fury.io/py/hackingtools.svg)]
![PyPI - Downloads](https://img.shields.io/pypi/dm/hackingtools)
![GitHub issues](https://img.shields.io/github/issues/Luiggy/hackingtoolsgui?color=purple&style=plastic)

![](https://blog.pentestinglab.es/wp-content/uploads/2019/11/HackingTools.png)

HackingTools is a recopilation of my own created modules in Python for automating the Hacking and Security Developer's life.

  - This proyect is a Django GUI for creating modules for the hackingtools library
  - Easy to use and automatically file and folder structure is generated for not corrupting this personal framework when creating a Module or any new Category
  - Already developing this framework, so I could say it's an Alpha Version.

# Installing Django Environment for Developing

First of all download this repository and be sure you have Python 3.7.X installed and well configured in your PATH.

You can install the environment into your Anaconda Environment (automatically set's the name to "ht" in your environment):

```sh
./install_gui.sh
```
Or:

```sh
conda env create -f=environment.yml
```

Or install requirements.txt with pip:

```sh
$ pip install -r requirements.txt -U
```

Once installed anything for loading the Django, try loading de GUI:

If you have created a Virtual Environment for this project, you have to activate it before continuing:

```sh
$ activate envname
```
In case you have installed it with the environment.yml file, you could use:

```sh
$ activate ht
```

And now we can start the Django project:

```sh
$ python manage.py runserver
```

If it loads, visit the URL Django tells at the end of loading the library and the debug messages.
Now you can start traying some functions, modules and also develop and create new modules and categories.
It's as simple as the Django GUI shows on visiting it.

# Installing Library from PyPi

```sh
$ pip install hackingtools -U
```

# Use of hackingtools

Now, you have installed the library, so you can import it as a Module and start hacking with all the modules created.

```sh
>>> import hackingtools as ht
>>> print(ht.getModulesNames()) # Return all the Modules Names for calling them later
```
This prints all the modules loaded names. Now, if we want to see what function names are available for a Module, we should do this:
```sh
>>> my_nmap = ht.getModule('ht_nmap') # Return a module loaded into the variable
>>> my_nmap.help() # Prints a help with the Functions Names for that Module
```
Or simply:
```sh
>>> ht.getModule('ht_nmap').help() # It's the same that last, but without a variable
```

Once we have the functions for a Module, we can call them like this:
```sh
>>> my_shodan = ht.getModule('ht_shodan') # Load Module
>>> my_shodan.getIPListfromServices('apache') # Call a function
```
