from flask import jsonify
from app import rapi
import paramiko
import re
import time

# commands available to retrive and set information
commands = {
    'terminal': 'terminal length 0\n',
	'enable': 'enable',
	'config': 'configure terminal\n',
	'show': 'show interfaces %s',
	'interface': 'interface %s\n',
	'set': 'bandwidth %d\n'
}

# credentials
router_username = rapi.config ['USERNAME']
router_password = rapi.config ['PASSWORD']
router_interace = rapi.config ['INTERFACE']
router_port     = rapi.config ['PORT']

#def get_all_routers_info ():
#    command = commands.get ('show') % "1"
#    return command

# return bw info from router identified by ip param
def get_router_info (ip):
    ssh = paramiko.SSHClient ()
    ssh.load_system_host_keys ()
    ssh.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
    ssh.connect (ip, router_port, router_username, router_password, look_for_keys=False)

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command (commands.get ('show') % router_interace)
    output = ssh_stdout.readlines ()
    ssh.close ()

    text = ""
    for line in output:
        text += line

    match = re.search (r"BW\s\d+\s", text)
    return match.group ()

# set bw specified in param to router identified by ip param
def set_bw (ip, bw):
    ssh = paramiko.SSHClient ()
    ssh.load_system_host_keys ()
    ssh.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
    ssh.connect (ip, router_port, router_username, router_password, look_for_keys=False)

    try:
        chan =  ssh.invoke_shell ()
        chan.send (commands.get ('terminal'))
        time.sleep (1)
        print (chan.recv (9999))
        
        chan.send (commands.get ('config'))
        time.sleep (1)
        print (chan.recv (9999))
        
        chan.send (commands.get ('interface') % router_interace)
        time.sleep (1)
        print (chan.recv (9999))
        
        chan.send (commands.get ('set') % bw)
        time.sleep (1)
        print (chan.recv (9999))

        chan.close ()
        ssh.close ()
    except:
        return False


    return True