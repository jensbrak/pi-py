# pippy

**pippy: Public IP PYthon-script**

Simple Python script to update external IP for dynamic dns but only when IP has changed and only by checking router via SSH or using external web page.

# Dependencies

**Software dependencies**

1.  Python (https://www.python.org/)
2.  Invoke (https://www.pyinvoke.org/) - needed by Fabric)
3.  Paramiko (https://www.paramiko.org/) - needed by Fabric)
4.  Fabric (http://www.fabfile.org/) - needed by pippy for SSH
  
**Other dependendies**

1.  A script or url for updating the external IP for the dynamic dns provider used
2.  A router with SSH access enabled OR an external IP providing site
3.  A linux system to run pippy from 

# Installation
**NOTE: Make sure you understand the script somewhat before using it**

1.  If missing - install the dependencies for pippy, 
2.  Download pippy script and place it in a folder where it should be run (eg /usr/bin/, /usr/local/bin/ or ~/bin/)
3.  Make sure pippy has proper permissions set (eg chmod 755 pippy) 
4.  Download pippy.router.json or pippy.externalpage.json (depnding on what kind of provider you choose to use) and place it in a folder of choice (eg /etc/ or ~/.pippy/) 
5.  Edit selected .json file to suit your selected provider (see Desciption below for details)
6.  Make sure the paths pointed out in .json file is accessable and directories exists (see Description below for details).
7.  Make sure path pointed out in pippy for .json is accessible and directories exists (see Description below for details).
8.  Test the script by calling it directly, until it works as desired (eg ./pippy) Hint: remove file "pippy.save" to simulate IP change
9.  Add row to crontab to run the script as often as desired (see crontab on the web for instructions)

# Description
pippy is pretty basic: it will load settings from a json file and based on the settings use a provider to get external IP. 
If IP has changed since last check, an action is performed - once again as defined in settings.

Details of the different settings in pippy.*.json and how they work:

**server**

`string: URI including 'http' OR an IP address`

If `server` starts with `'http'` pippy will try to get external IP from is an external web page. 
Assumption is that an IP is presented on that page representing external IP.

If `server` does not start with `'http'` pippy will try to get external IP from a router. 
Assumption is that the setting is a local IP that points to a SSH enabled router from which to get the external IP from.

**action**

`int: SSH port to router`

Port to use for SSH connection (usually 22)
Only relevant if `server` is a router with SSH.

**user**

`string: username for SSH`

The username for the admin of the router.
Only relevant if `server` is a router with SSH.

**password**

`string: password for SSH`

The password for the admin of the router.
Only relevant if `server` is a router with SSH.

**matchip**

`string: regexp for IP match OR shell command(s) for getting IP`

If `server`is a web page, pippy will use `matchip` as a regexp to parse the web page for external IP.
Assumption is that `matchip` is a valid AND double quoted (double backslash) regexp.

If `server`is a router with SSH, pippy will use `matchip` as a command (possibly using pipes) to ask router for external IP.
Assumption is that `matchip` is a valid command or series of commands supported by the router using SSH connection.

**action**

`string: URI including 'http' OR a valid shell command`

If `action` starts with `'http'` pippy will call the web page given by `action` as a result of a change of external IP.

If `action`does not start with `'http'` pippy will run the comand given by `action` in a local shell as a result of a change of external IP.

Assumption is that `action` is whatever is needed to actually update the dyndns provider with a new external IP.
In other words: he key component for actually updating a dyndns provider with new IP is NOT covered here. 

Example: I use Free DNS (http://freedns.afraid.org) and they provide personal URL (if you have account) that will update their records with a new IP.
It looks something like this: http://freedns.afraid.org/dynamic/update.php?abcdef (just an example, non working I hope). This is what I use as action with pippy!

**logfile**

`string: fully qualified path to logfile`

pippy will write IP changes to this file.
If file is missing it will be created, but missing directories is not handled and will cause error.

**changeonly**

`bool: if IP changes shall be logged only` 

What to log: 
If `true`: only IP changes shall be logged in `logfile`
If `false`: even checks with no change shall be logged in `logfile` (not recommended)

**debug**

`bool: if debug messages shall be printed

What to print:
If `true`: print debugg info to stdout (will not be printed in `logfile`)
If `false`: don't print debug info (nothing will be printed part from logging to `logfile` or whatever `action` as console command will print)

# NOTES
*  **IMPORTANT**: Make sure you ONLY use this in a settig where you can protect your router credentials. If pippy.json can be read by others, you will expose your router admin credentials.
*  If your router does not support SSH, you're out of luck here. Or modify the script to parse an external page that will show IP.
*  If you choose to log everything (settings file option 'changeonly' set to false), the log WILL grow. Use logrotate or something, or you will produce large logfiles with rather meaningless contents that will fill your disk.
*  **IMPORTANT**: Use at own risk. No support, no guarantees. I made it to fit my purposes, you are free to make it yours but that's up to you. :)  
