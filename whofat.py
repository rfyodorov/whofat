#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import datetime

def getPidMemUser():
    proc_list = os.popen("ps -eo pid,rss,vsz,user").read()
    proc_cmd_list = os.popen("ps -eo cmd").read()

    # create list from string
    proc_list = proc_list.split()
    # find step for split string
    split_step = len(proc_list)/4

    # create four lists from string
    list_row_user = []
    list_row_vsz = []
    list_row_rss = []
    list_row_pid = []

    for i in range(1,split_step+1):
        list_row_user.append(proc_list[(i*4)-1])
        list_row_vsz.append(proc_list[(i*4)-2])
        list_row_rss.append(proc_list[(i*4)-3])
        list_row_pid.append(proc_list[(i*4)-4])
        #print list_row_pid[i-1], list_row_rss[i-1], list_row_vsz[i-1], list_row_user[i-1]

    # remove titile (PID RSS VSZ USER)
    list_row_user.pop(0)
    list_row_vsz.pop(0)
    list_row_rss.pop(0)
    list_row_pid.pop(0)

    #for i in range(0, len(list_row_rss)):
    #    print "Pid:" , list_row_pid[i], "RAM:" , int(list_row_rss[i])/1024, "Mb"

    return list_row_pid, list_row_rss, list_row_vsz, list_row_user, proc_cmd_list

def getPidCmd(proc_cmd_list):
    cmd_list = proc_cmd_list
    #cmd_list = os.popen("ps -eo cmd").read()

    list_cmd = []
    for line in  cmd_list.split('\n'):
        list_cmd.append(line)

    list_cmd.pop(0)

    return list_cmd

def getPidJava(cmd, str_pattern):
    favor_pid = []
    favor_cmd = []

    for item in range(0, len(cmd)):
        if "java" in cmd[item]:
            favor_pid.append(pid[item])

            str = cmd[item]
            str = str.split(" ")
            #print str

            for j in str:
                if str_pattern in j:
                    favor_cmd.append(j)
                    #print "PID:", pid[item], "RAM:", int(rss[item])/1024,"MB", "JAVA:", j

    return favor_pid, favor_cmd

def writeLog(str_log):
    f = open('fat.log', 'a')
    f.write(str(str_log) + "\n")
    f.close()

# --- start ---

pid, rss, vsz, user, proc_cmd_list = getPidMemUser()
cmd = getPidCmd(proc_cmd_list)

str_pattern = "-Didea.platform.prefix="
java_pid, java_cmd = getPidJava(cmd, str_pattern)

# Print result
str_log = str(datetime.now())
writeLog(str_log)
for item in range(0, len(java_pid)):
    for j in range(0, len(pid)):
        if pid[j] == java_pid[item]:
            str_log = "PID:", java_pid[item], "RAM:", int(rss[j])/1024, "MB", "JAVA:", java_cmd[item]
            writeLog(str_log)


