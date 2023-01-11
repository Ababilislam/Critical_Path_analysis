#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 23:38:35 2023

@author: ab
"""
line = list() #contains a single line
single_element = list()
tasks = dict() #contains all the tasks
number = 0
cpmdata = open('/home/ab/Documents/cpm_data.txt') #TWO FILES: cpm.txt and cpm1.txt

for line in cpmdata: #slide the file line by line
    single_element=(line.split(',')) #split a line in subparts
    number += 1
    for i in range(len(single_element)): #creating the single task element
        tasks['task'+ str(single_element[0])]= dict()
        tasks['task'+ str(single_element[0])]['id'] = single_element[0]
        tasks['task'+ str(single_element[0])]['name'] = single_element[1]
        tasks['task'+ str(single_element[0])]['duration'] = single_element[2]
        if(single_element[3] != "\n"):
            tasks['task'+ str(single_element[0])]['dependent'] = single_element[3].strip().split(';')
        else:
            tasks['task'+ str(single_element[0])]['dependent'] = ['-1']
        tasks['task'+ str(single_element[0])]['ES'] = 0
        tasks['task'+ str(single_element[0])]['EF'] = 0
        tasks['task'+ str(single_element[0])]['LS'] = 0
        tasks['task'+ str(single_element[0])]['LF'] = 0
        tasks['task'+ str(single_element[0])]['float'] = 0
        tasks['task'+ str(single_element[0])]['isCritical'] = False

# =============================================================================
# FORWARD PASS
# =============================================================================
for task_fw in tasks:
    if('-1' in tasks[task_fw]['dependent']): #checks if it's the first task
        tasks[task_fw]['ES'] = 1
        tasks[task_fw]['EF'] = (tasks[task_fw]['duration'])
    else: #not the first task
        for task_key in tasks.keys():
            for dependent_task in tasks[task_key]['dependent']: #to check all the dependency in a single task
                #print('taskname' + task_fw + ' k '+ k + ' dependent_task ' +dependent_task)
                if(dependent_task != '-1' and len(tasks[task_key]['dependent']) == 1): #if the task k has only one dependency
                    tasks[task_key]['ES'] = int(tasks['task'+ dependent_task]['EF']) +1
                    tasks[task_key]['EF'] = int(tasks[task_key]['ES']) + int(tasks[task_key]['duration']) -1
                elif(dependent_task !='-1'): #if the task k has more dependency
                    if(int(tasks['task'+dependent_task]['EF']) > int(tasks[task_key]['ES'])):
                        tasks[task_key]['ES'] = int(tasks['task'+ dependent_task]['EF']) +1
                        tasks[task_key]['EF'] = int(tasks[task_key]['ES']) + int(tasks[task_key]['duration']) -1

forward_list = list() #list of task keys
for element in tasks.keys():
    forward_list.append(element)

backtrack_list = list() #reversed list of forward list.
while len(forward_list) > 0:
    backtrack_list.append(forward_list.pop())
    
# ================================
# BACKTRACK For finging critical path
# ================================
for task_backward in backtrack_list:
    if(backtrack_list.index(task_backward) == 0): #check if it's the last task (if  no more task can easily stop)
        tasks[task_backward]['LF']=tasks[task_backward]['EF']
        tasks[task_backward]['LS']=tasks[task_backward]['ES']
        
    for dependent_task in tasks[task_backward]['dependent']: #slides all the dependency in a single task
        if(dependent_task != '-1'): #check if it's not the last task
            if(tasks['task'+ dependent_task]['LF'] == 0): #check if the the dependency is already analyzed
                tasks['task'+ dependent_task]['LF'] = int(tasks[task_backward]['LS']) -1
                tasks['task'+ dependent_task]['LS'] = int(tasks['task'+ dependent_task]['LF']) - int(tasks['task'+ dependent_task]['duration']) +1
                tasks['task'+ dependent_task]['float'] = int(tasks['task'+ dependent_task]['LF']) - int(tasks['task'+ dependent_task]['EF'])
            if(int(tasks['task'+ dependent_task]['LF']) >int(tasks[task_backward]['LS']) ): #put the minimun value of LF for the dependent of a task
                tasks['task'+ dependent_task]['LF'] = int(tasks[task_backward]['LS']) -1
                tasks['task'+ dependent_task]['LS'] = int(tasks['task'+ dependent_task]['LF']) - int(tasks['task'+ dependent_task]['duration']) +1
                tasks['task'+ dependent_task]['float'] = int(tasks['task'+ dependent_task]['LF']) - int(tasks['task'+ dependent_task]['EF'])


# ================
# Display task info
# ================
print('task id, task name, predesessor ,  duration,   ES   ,   EF  , LS  , LF  , Slack, isCritical')
for task in tasks:
    if(tasks[task]['float'] == 0):
        tasks[task]['isCritical'] = True
    print(str(tasks[task]['id']) +',         '+str(tasks[task]['name']) +',         '+str(tasks[task]['dependent'])+',         '+str(tasks[task]['duration']) +
          ',       '+str(tasks[task]['ES']) +',    '+str(tasks[task]['EF']) +
          ',    '+str(tasks[task]['LS']) +',    '+str(tasks[task]['LF']) +
          ',    '+str(tasks[task]['float']) +',    '+str(tasks[task]['isCritical']))
    