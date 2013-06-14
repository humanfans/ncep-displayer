#! /usr/bin/env python
# -*- coding: utf-8


from __future__ import unicode_literals
import SocketServer
from time import ctime
import os
import logging
from commands import getoutput

HOST=""
PORT=12777
ADDR=(HOST,PORT)

def loginfo(info,level):
        logger = logging.getLogger()
        handler = logging.FileHandler('server.log')
        logflt = logging.Formatter("%(levelname)s [%(asctime)s]: %(message)s","%Y-%m-%d %H:%M:%S")
        handler.setFormatter(logflt)
        logger.addHandler(handler)
        levels = {"CRITICAL":50,"ERROR":40,"WARNING":30,"INFO":20,"DEBUG":10}
        for key in levels:
                if level == key:
                        logger.setLevel(levels[key])
                        eval("logging."+key.lower()+"("+'"'+info+'"'+")")
        logger.removeHandler(handler)


#loginfo('some error info...','ERROR')


class commands():
        def __init__(self,cmd):
                self.cmd = cmd
        
        def check_cmds(self):
                if self.cmd == "getsysinfo":
                        return self.get_sysinfo()
                elif self.cmd =="help":
                        return "::Valid commands are: getsysinfosystem help bye"
                elif "system" in self.cmd:
                        return self.system(self.cmd.split('system'))
                elif self.cmd == "":
                        return ''
                else:
                        return "::Please input legal command!"
        
        def get_sysinfo(self):
                r = '\r\n'
                issue = self.get_issue()
                os = getoutput('uname -o')
                machine = getoutput('uname -m')
                kernel = getoutput('uname -r')
                return issue+r+os+r+machine+r+kernel
        
        def get_hardware(self):
                pass
                
        
        def system(self,parms):
                if parms[1] != "":
                        if "rm" in parms[1]:
                                return "Dangerous! Make sure **current path**.\r\n"+getoutput(parms[1])
                        return getoutput(parms[1])
                else:
                        return ""
                
        def get_issue(self):
                issue_file = '/etc/issue'
                if not os.path.exists(issue_file):
                        return getoutput('uname -o')
                f = open(issue_file)
                lines = f.readlines()
                f.close()
                for line in lines:
                        if 'Arch' in line:
                                return "ArchLinux"
                        elif 'CentOS' in line:
                                return "CentOS"
                        elif 'Ubuntu' in line:
                                return "Ubuntu"
                        elif 'Fedora' in line:
                                return 'Fedora'


class MyRequestHandler(SocketServer.BaseRequestHandler):
        
        def handle(self):
                login = False
                while login != True:
                        try:
                                self.request.send('Password: ')
                        except Exception,e:
                                loginfo('%s:%s Send failed! %s' % (self.client_address[0],self.client_address[0],e),'ERROR')
                                break
                        data = self.request.recv(10240)
                        if data.strip() == "password":
                                try:
                                        self.request.send("login_sucess\r\n")
                                except Exception,e:
                                        loginfo('%s:%s Send failed! %s' % (self.client_address[0],self.client_address[0],e),'ERROR')
                                login = True
                        else:
                                login = False
                                loginfo('%s has input wrong password: [ %s ]' % (self.client_address[0],data.strip()),'CRITICAL')
                                self.finish()
                                
                print '::connected from: ',self.client_address
                loginfo("Connected from: %s:%s" %(str(self.client_address[0]),str(self.client_address[1])),'INFO')
                while True:
                        data = self.request.recv(10240)
                        if data.strip() == 'byebye':
                                try:
                                        self.request.send("seeyou!")
                                except Exception,e:
                                        loginfo('%s:%s Send failed! %s' % (self.client_address[0],self.client_address[0],e),'ERROR')
                                print("::%s:%s Leaving server.\r\n" % (str(self.client_address[0]),str(self.client_address[1])))
                                loginfo("%s:%s Leaving server." % (str(self.client_address[0]),str(self.client_address[1])),'INFO')
                                self.finish()
                                break
                        if data.strip() == 'sendfile':
                                continue
                        cmd_output = commands(data.strip())
                        try:
                                self.request.send('%s\n' % (cmd_output.check_cmds()))
                        except Exception,e:
                                loginfo('%s:%s Send failed! %s' % (self.client_address[0],self.client_address[0],e),'ERROR')
                                self.finish()
                                break


# Server can reuse listened address
SocketServer.ThreadingTCPServer.allow_reuse_address = True
tcpServ = SocketServer.ThreadingTCPServer(ADDR,MyRequestHandler)
print '::waiting for connecting...'
tcpServ.serve_forever()

