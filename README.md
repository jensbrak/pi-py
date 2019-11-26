# PIP-Py

**PIP-Py: Public IP PYthon-script**

Simple Python script to update external IP for dynamic DNS - but only when IP has changed. 
Primary IP check using SSH to router. Alternative method also provided, using external web page of choice.

# Platform

Tested and used on Linux (Debian Buster), however Python runs on multiplatform so it is multiplatform since only dependency is Python with some Python libs.
If you try this script on other platforms, let me know!

# Dependencies

**Software dependencies**

1.  Python (https://www.python.org/)
2.  Invoke (https://www.pyinvoke.org/) - needed by Fabric)
3.  Paramiko (https://www.paramiko.org/) - needed by Fabric)
4.  Fabric (http://www.fabfile.org/) - needed by PIP-Py for SSH
  
**Other dependendies**

1.  A script or URL for updating the external IP for the dynamic DNS provider used 
2.  A router with SSH access enabled (alternatively an URL for a web page providing external IP information)
3.  A (Linux) system to run PIP-Py from 

# Installation
**NOTE: Make sure you understand the script somewhat before using it**

1.  Dependencies: If missing - install the dependencies for PIP-Py 
2.  Script: Download PIP-Py.py script (pippy.py) and place it in a folder where it should be run (eg /usr/bin/, /usr/local/bin/ or ~/bin/)
3.  Script permissions: Make sure PIP-Py has proper permissions set (eg chmod 755 pippy.py) 
4.  Settings selection: Download pippy.router.json or pippy.externalpage.json (deprnding on what kind of provider you choose to use) and place it in a folder of choice (eg /etc/ or ~/.PIP-Py/) 
5.  Settings editing: Edit selected .json file to suit your selected provider (see Settings below for details)
6.  Directory permissions: Make sure the paths pointed out in .json file is accessible and directories exists (see Settings below for details).
7.  Script editing: Make sure path pointed out in pippy.py for settings file (pippy.*.json is accessible and directories exists (see Settings below for details).
8.  Script testing: Test the script by calling it directly, until it works as desired (eg ./pippy) Hint: remove file "pippy.save" to simulate IP change
9.  Script scheduling: Add row to crontab to run the script as often as desired (see crontab on the web for instructions)

# Description
PIP-Py is pretty basic: it will load settings from a json file and based on the settings use a provider to get external IP. 
If IP has changed since last check, an action is performed - once again as defined in settings.
Two versions of the settings file is provided, one if using the script as indended by checking router, and another one if external page is used. 
See them as examples of the two approaches, you still need to edit and understand them. :)
Basic logging is provided using a log file. Debug logging also provided. (See Settings below for details)

# Settings (pippy.*.json)
Details of the different settings in pippy.*.json and how they work below.
Note: pippy.*.json denote either pippy.router.json or pippy.externalpage.json and should either be renamed to pippy.json or referenced by actual name in pippy.py

`server: string:`

*URI including 'http' OR an IP address*

If 'server' starts with "http" PIP-Py will assume it represents a working address to a web page that prints the external IP.

If 'server' does not start with "http" PIP-Py will assume it represents a valid internal IP to a router with SSH access enabled.

`port: int`

*SSH port used by router*

Only relevant if 'server' represents IP to a router with SSH.

`user: string`

*Username for SSH admin*

Only relevant if 'server' represents IP to a router with SSH.

`password: string`

*Password for SSH admin*

Only relevant if 'server' represents IP to a router with SSH.

`matchip: string`

*Regexp for IP match OR shell command(s) for getting IP*

If 'server' represents IP to arouter with SSH, PIP-Py will use 'matchip' as a command (possibly using pipes) to ask router for external IP.

If 'server' represents an adress to a web page, PIP-Py will use 'matchip' as a regexp to parse the web page for external IP.
Note: regexp needs to have double backslash.

`action: string`

*URI including 'http' OR a valid shell command*

The action to use in order to update dyndns provider with new IP.

If 'action' starts with "http" PIP-Py will assume 'action' is a web page URI that will update dyndns provider with the new IP. 

If 'action' does not start with "http" PIP-Py will assume 'action' is a script (with fully qualified path) that will update dyndns provider with the new IP.

Note: The web page or script functionality is NOT covered here, but remain the core functionality of PIP-Py. The dyndns provider should have API or other means to update its records.
PIP-Py only provide functionality to get external IP and calling the selected update method given by the dyndns provider.

*Example: I use Free DNS (http://freedns.afraid.org) and they provide personal URL (if you have account) that will update their records with a new IP.
It looks something like this: http://freedns.afraid.org/dynamic/update.php?abcdef (just an example, non working I hope). This is what I use as action with PIP-Py!*

`logfile: string`

*Fully qualified path to logfile*

PIP-Py will write IP changes to this file.
If file is missing it will be created, but missing directories or failed access is not handled and will cause error.

`changeonly: bool`

*If IP changes shall be logged only*

What to log: 
If true: only IP changes shall be logged in logfile
If false: even checks with no change shall be logged in logfile (not recommended)

`debug: bool` 

*If debug messages shall be printed*

What to print:
If true: print debugg info to stdout (will not be printed in logfile)
If false: don't print debug info (nothing will be printed part from logging to logfile or whatever action as console command will print)

# NOTES

*  **IMPORTANT**: Use at own risk. I made it to fit my purposes but made it available so that you can make it fit yours.  
*  **IMPORTANT**: Make sure you ONLY use this in a settig where you can protect your router credentials. If PIP-Py.json can be read by others, you will expose your router admin credentials.
*  If your router does not support SSH, you can use PIP-Py with the external web page support. However, there may be other options to consider if that's the case. Main purpose with PIP-Py is to use SSH to router.
*  If you choose to log everything (settings file option 'changeonly' set to false), the log WILL grow. Use logrotate or something, or you will produce large logfiles with rather meaningless contents that will fill your disk.
*  I encourage (and appreciate) you to let me know you have use for this script, especially if you adopt it to other platforms or in anyway enhance it. Pull requests are most welcome too!
*  While I can't guarantee to provide any support using the script, you are welcome to contact me with if you have questions or thoughts.
  