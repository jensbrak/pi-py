# pippy

**pippy: Public IP PYthon-script**

Simple Python script to update external IP for dynamic dns but only when IP has changed and only by checking router via SSH.

# Dependencies

** Software dependencies **

1.  Python (https://www.python.org/)
2.  Invoke (https://www.pyinvoke.org/) - needed by Fabric)
3.  Paramiko (https://www.paramiko.org/) - needed by Fabric)
4.  Fabric (http://www.fabfile.org/) - needed by pippy for SSH
  
** Other dependendies **

1.  A script or url for updating the external IP for the dynamic dns provider used
2.  A router with SSH access enabled
3.  A linux system to run pippy from 
 
# Installation
** NOTE: If you don't know or understand the dependencies for this script, you should not use it. :) **

1.  If missing - install the dependencies for pippy, 
2.  Download pippy script and place it in a folder where it should be run (eg /usr/bin/, /usr/local/bin/ or ~/bin/)
3.  Make sure pippy has proper flags set (eg chmod 755 pippy)
4.  Download pippy.json and place it in a folder of choice (eg /etc/ or ~/.pippy/) and update pippy variable 'settingspath' to point to this folder
5.  Edit pippy.json to suit your router and dynamic dns provider (see Desciption below for details)
6.  Make sure the paths pointed out in pippy.json is accessable and directories exists (see Description below for details).
7.  Test the script by calling it directly, until it works as desired (eg ./pippy) Tips: remove file "pippy.save" to simulate IP change
8.  Add row to crontab to run the script as often as desired (see crontab on the web for instructions)

# Description
pippy is pretty basic: it will load settings from a json file, use them to connect via SSH to a router pointed out in settings, using the credentials given. 
Using the SSH connection, the external IP is read using some console commands (ifconfig, grep, awk, sed). The interface is a parameter in settings too (eg eth0)
If the external IP has changed since last call, the action pointed out in settings is called.

Details of the different settings in pippy.json and how they work:

`
*  server (string): local IP for the router to use
*  port (int): SSH port to router
*  user (string): username for admin of router
*  password (string): password for admin of router
*  interface (string): name of interface that will give external IP using ifconfig (eth0 for the one I used)
*  savedipfile (string): full path (including filename) to file that will store last IP retrieved (note: all directories must exist, but file will be automatically created)
*  action (string): full URI to web page/script to call for dyndns update OR command to use in console (eg call script locally to do dynds update). See section 'Action' for details
*  logfile (string): full path (including filename) to file that will be used for logging (note: all directories must exist, but file will be automatically created)
*  debug (boolean): true if debug print should be used, false otherwise. Intended to be used when setting things up
*  changeonly (boolean): true if only changes of IP should be logged (recommended), false if checks with no change should be logged as well
`

# Action
The key component for actually updating a dyndns provider with new IP is NOT covered here. I use afraid.org and it provides a personal URI pointing to a script that will update afraid.org to know my new IP. You should create your own one and use.

The way pippy checks how 'action' should be called is utterly simple: if the action setting begin with 'http' it is assumed to be an URI and it will load the URI as a web page, ignoring the result but returning the HTTP code.
If the action does not start with 'http', it is assumed the action is a local script, ie a fully qualified name of the script to call when IP change occur.

The only "magic" pippy does is to use predefined libs to SSH into a router.

# NOTES

*  ** IMPORTANT **: Make sure you ONLY use this in a settig where you can protect your router credentials. If pippy.json can be read by others, you will expose your router admin credentials.
*  If your router does not support SSH, you're out of luck here. Or modify the script to parse an external page that will show IP.
*  If you choose to log everything (settings file option 'changeonly' set to false), the log WILL grow. Use logrotate or something, or you will produce large logfiles with rather meaningless contents that will fill your disk.
*  ** IMPORTANT **: Use at own risk. No support, no guarantees. I made it to fit my purposes, you are free to make it yours but that's up to you. :)  
