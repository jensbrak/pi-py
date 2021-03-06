# ##############################################################################
# ### System dependencies
import sys
import json
import subprocess
import datetime
import re

# ##############################################################################
# ### Directory suggestions/settings from settings file
# ###	pippy.py[this]: /usr/bin/
# ###	pippy.json:		/etc/pippy/      see 'settingspath' below
# ###	pippy.log:      /var/log/        see 'logfile' in pippy.json
# ###	pippy.save:     /var/lib/pippy/  see 'savedipfile' in pippy.json

# ##############################################################################
# ### loadsettings(): Read global variables from a settings file
def loadsettings():
    settingspath = "." 
    #settingspath = "/etc/pippy" 

    global pippysettings, settings
    global server, port, user, password
    global savedipfile, logfile
    global matchip, action, debug, changeonly

    #pippysettings = settingspath + "/" + "pippy.externalpage.json"
    pippysettings = settingspath + "/" + "pippy.router.json"
    
    with open(pippysettings) as settingsfile:
        settings = json.load(settingsfile)
    server = settings['server']
    port = settings['port']
    user = settings['user']
    password = settings['password']
    matchip = settings['matchip']
    savedipfile = settings['savedipfile']
    action = settings['action']
    logfile = settings['logfile']
    debug = settings['debug']
    changeonly = settings['changeonly']

# ##############################################################################
# ### Helpers
# ##############################################################################
    
# ### info(txt, lvl): generic message printing with some formatting for pippy
# ###	'txt'	- text to print
# ###	'lvl'	- text representing loglevel, like 'DEBUG', 'INFO', etc 
def info(txt, lvl=""):
    msg = "[pippy"
    if lvl != "":
        msg += " " + lvl
    msg += "] " + txt
    print(msg)

# ### fail(txt, halt): print error message with possibility to
# ###   abort program after
# ###	'txt'	- text describing failure
# ###	'halt'	- set to True will force the script to terminate immediately
def fail(txt, halt=True):
    info(txt, "ERROR")
    if halt:
        info("terminating!", "ERROR")
        exit(1)

# ### dbg(txt): print debug message 
# ###	'txt'	- text describing debug information, but only if global setting 
# ###			  'debug' is set to True (read from settings file)
def dbg(txt):
    if debug:
        info(txt, "DEBUG")

# ### log(txt): log message to file where full path to file is set by
# ###			global setting 'logfile' (read from settings file)
# ###	'txt'	- text to log
def log(txt):
    if logfile != "":
        dbg("Logging to: " + logfile + ", text: " + txt)
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        msg = ts + ": " + txt + "\n"
        try:
            with open(logfile, "a") as file:
                file.write(msg)
        except Exception as e:
            fail("Failed to write logifle: " + logfile + ", reason: " + str(e), halt=False)
    else:
        dbg("Not logged (empty logfile path): , text: " + txt)

# ##############################################################################
# ### IP change functions
# ##############################################################################

# ### onipchanged(): called when IP change occur. Calls whatever action the
# ###   global variable 'action' (read from settings file) is set to.
# ###	This function can be seen as the actual callback to update DNS provider
# ###	with a new external IP.
# ###
# ###   Note: if 'action' starts with "http" the action is assumed to be a
# ###	page/script accessable on the web and is called as such. Result code 
# ###	will be HTTP result, ie 200 for ok
# ###
# ###	If 'action' does NOT start with "http" it is assumed to be a shell command
# ###	and will be called using a spawned shell process. Result code will be a
# ###	code from the shell, ie 0 for success
def onipchanged():
    if action.startswith("http"):
        from urllib import request
        result = request.urlopen(action)
        code = str(result.getcode())
        dbg("URL action returned code: " + code)
    else:
        args = action.split(" ")
        result = subprocess.run(args)
        code = str(result.returncode)
        dbg("CMD action returned code: " + code)

    return code
        
# ### getipexternal(): called to get external IP. Two supported methods:
# ###	1. if 'server' starts with "http" the server is assumed to be an external
# ###   web page that will print external IP somewhere. The page will be
# ###   retrieved and 'matchip' will be used as a regexp to get the IP from the
# ###   html from the web page
# ###
# ###	2. if 'server' does not start with "http" it is assumed it's an ip to a
# ###   router. A SSH client will be used to connect to the router and
# ###   'matchip' will be used as the command to run on the router to get the IP.
def getipexternal():
    if server.startswith("http"):
        # Get ip from external page
        dbg("getipexternal: getting ip from external page=" + server)
        
        from urllib import request
        result = request.urlopen(server)
        code = result.getcode()
        html = str(result.read())

        regex = matchip.replace("\\\\", "\\")
        match = re.search(regex, html)

        if match == None:
            ip = ""
        else:
            ip = match.group()
            
        dbg("getipexternal: got result=" + str(code) + " and ip=" + ip)
        return ip
    else:
        # Get ip from router
        dbg("getipexgternal: getting ip from router=" + server)
        
        from fabric import Connection
        ssh = Connection(
            host=server,
            port=str(port),
            user=user,
            connect_kwargs={"password": password}
        )

        result = ssh.run(matchip, hide=True)
        code = result.exited
        ip = result.stdout.strip()

        dbg("getipexternal: got result=" + str(code) + " and ip=" + ip)
        return ip

# ### setipsaved(ip): save a given P to file. If save file does not exist, 
# ###	create it. Used to pickup result from previous check.
# ###	'ip'	- the ip to save, as string
def setipsaved(ip):
    with open(savedipfile, "w") as file:
        file.write(ip)
    dbg("setipsaved: " + ip)

# ### getipsaved(): read a saved IP and return it. If save file does not exist
# ###	try creating it with setsavedip() using '0.0.0.0' as IP, forcing a call
# ###	to 'action' since IP will be considered to have changed (first time use)
def getipsaved():
    try:
        with open(savedipfile) as file:
            ipold = file.read()
    except IOError:
        dbg("getipsaved: file not found: " + savedipfile)
        ipold = "0.0.0.0"
        setipsaved(ipold)
    dbg("getipsaved: " + ipold)
    return ipold

# ### pipmain(): Main function of pip: in short...
# ###   Get old IP, get new IP, act if IP has changed
# ###
# ###	Note: if external IP is empty, it indicates internet is unreachable
# ###	If so, no action will be called until internet is reachable again (ie
# ###	IP changed from empty to a non empty IP)
def pipmain():
    try:
        loadsettings()
        dbg("Settings file loaded: " + pippysettings + " = " + str(settings))
    except Exception as e:
        fail("Could not read settings file: " + pippysettings + ", reason: " + str(e))
    
    ipold = getipsaved()
    ipnew = getipexternal()

    if ipold != ipnew:
        msg = "ip changed: '" + ipold + "' -> '" + ipnew + "'"
        log(msg)
        setipsaved(ipnew)
        if ipnew != "":
            result = onipchanged()
            msg = "action returned: '" + result + "'"
        else:
            msg = "internet unreachable, no action called"
        log(msg)
    else:
        if changeonly:
            dbg("ip unchanged: '" + ipnew + "', no logging done")
        else:
            log("ip unchanged: '" + ipnew + "'")

pipmain()

# ##############################################################################
# ### End of file
# ##############################################################################
