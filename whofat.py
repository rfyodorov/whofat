#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta
import time

def getUsedMemAsPercent():
    free_list = os.popen("free -m").read()
    free_list = free_list.split(" ")

    # Remove enpty items
    for i in range(len(free_list), 0, -1):
        if free_list[i-1] == '':
            free_list.pop(i-1)

    mem_total = int(free_list[6])
    mem_free = free_list[14]
    str_pos = mem_free.rfind("\n")
    mem_free = int(mem_free[:str_pos])

    mem_free_percent = mem_free * 100 / mem_total
    mem_used_percent = 100 - mem_free_percent

    return mem_used_percent

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

    return list_row_pid, list_row_rss, list_row_vsz, list_row_user, proc_cmd_list

def getPidCmd(proc_cmd_list):
    cmd_list = proc_cmd_list

    list_cmd = []
    for line in  cmd_list.split('\n'):
        list_cmd.append(line)

    list_cmd.pop(0)

    return list_cmd

def getPidJava(cmd, str_pattern):
    favor_pid = []
    favor_cmd = []

    for item in range(0, len(cmd)):
        if str_pattern in cmd[item]:
            favor_pid.append(pid[item])

            str = cmd[item]
            str = str.split(" ")

            for j in str:
                if str_pattern in j:
                    favor_cmd.append(j)
                    #print "PID:", pid[item], "RAM:", int(rss[item])/1024,"MB", "JAVA:", j

    return favor_pid, favor_cmd

def writeLog(str_log):
    f = open(LOG_FILENAME, 'a')
    f.write(str(str_log) + "\n")
    f.write("\n")
    f.close()

# --- start point ---

print "Start script. Please press Ctrl+C to exit"

STR_PATTERN = "-Didea.platform.prefix="
WARN_PERCENT = 0
LOG_FILENAME = "fat.log"

# Delay if the process uses a lot of memory for a long time
time_stamp = datetime.now() - timedelta(minutes=1)
#print "1st:", time_stamp

while True:
    try:
        mem_used_per = getUsedMemAsPercent()
        time.sleep(10)

        if mem_used_per >= WARN_PERCENT: # >= 70

            time_stamp_current = datetime.now()
            time_stamp_delta = timedelta(minutes=1)

            # If delay between current time and previously check is over, write log
            if time_stamp_current > (time_stamp + time_stamp_delta):
                time_stamp = time_stamp_current

                pid, rss, vsz, user, proc_cmd_list = getPidMemUser()
                cmd = getPidCmd(proc_cmd_list)

                java_pid, java_cmd = getPidJava(cmd, STR_PATTERN)

                # Print result
                str_log = str(datetime.now()) + " - Used memory=" + str(mem_used_per) + "%"
                writeLog("\n")
                writeLog((str_log)
                for item in range(0, len(java_pid)):
                    for j in range(0, len(pid)):
                        if pid[j] == java_pid[item]:
                            str_log = "PID:", java_pid[item], "RAM:", int(rss[j])/1024, "MB", "JAVA:", java_cmd[item]
                            writeLog(str_log)

    except KeyboardInterrupt:
        print "^C received, shutting down script"
        break
