#!/usr/bin/python

'''
install python e.g. conda

https://pandas.pydata.org/pandas-docs/stable/install.html

Pip install pandas
pip install xlutils
pip install xlwt
pip install xlrd
pip install openpyxl
pip install beautifulsoup4 #https://www.crummy.com/software/BeautifulSoup/bs4/doc/

'''

# (base) bherudek-ltm1:testpythonbuildxml bherudek$ chmod ugo=rwx *
# (base) bherudek-ltm1:testpythonbuildxml bherudek$  python generatebuildxml.py -d . -e intPR -a realdeployandtest -p FSM
# called in jenkins, potentially with a shell wrapper script
# params -t(arget) targetenv -a(ction) [checkdeploy|checkdeployandtest|realdeployandtest] 
# input fix: config file choosetests.xls
# input variable: path, where the files coming from gut jenkins were copied locally, we read them and use as index to choosetext.xls
# output file fix: build.xml
# params p for project e.g. FSM team is optional and for future use: 
    # depending on the team that jenkins identified, different tests will run
# params n for number of user story or bugis optional and for future use: 
    # with user number we go to targy tab task to retrieve required tests and write them to choosetests.txt permanently

## TO DO: too many imports probably
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys, getopt
import pathlib
from pathlib import PurePath
from pathlib import PurePosixPath
from pathlib import Path
import os
import requests
from bs4 import BeautifulSoup
import json 
import datetime

## example usages
##python updatePRFromJenkins.py -t INT -e PULL_REQUEST -s TEST_FAILED -u 33306 -p 12345 -l THISMIGHTBECOMEAPATH
##python updatePRFromJenkins.py -t STAGING -e DEPLOY -s TEST_SUCCESS -u 33306 -p 12345 -l THISMIGHTBECOMEAPATH

def main(argv):
    
    correct_usage = 'python updatePRFromJenkins.py -t <[INT|STAGING|DEV|INT|PROD]> -e <[PULL_REQUEST|DEPLOY]> -s <[TEST_FAILED|DEPLOY_FAILED|TEST_SUCCESS|DEPLOY_SUCCESS]> -u <userstoryID> -p <pullrequestid> -l <logmessage>';
    logfile = 'choosetests.xlsx'
    
    try:
        opts, args = getopt.getopt(argv,"t:e:s:u:p:l:",["target", "event=","status=","userstory","pullrequestid", "logmessage"])
    except getopt.GetoptError:
        print (correct_usage )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (correct_usage )
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
            if target not in {"INT","STAGING", "DEV"}:
                print ('event: ' + str(action))
                print ('Pls set correct event.\n') 
                print (correct_usage )
                sys.exit()
        elif opt in ("-e", "--event"):
            event = arg
            if event not in {"PULL_REQUEST","DEPLOY"}:
                print ('event: ' + str(action))
                print ('Pls set correct event.\n') 
                print (correct_usage )
                sys.exit()
        elif opt in ("-s", "--status"):
            status = arg
            if status not in {"TEST_FAILED","DEPLOY_FAILED", "TEST_SUCCESS", "DEPLOY_SUCCESS"}:
                print ('action: ' + str(action))
                print ('Pls set correct action.\n') 
                print (correct_usage )
                sys.exit()
        elif opt in ("-u", "--userstory"):
            userstory = arg 
        elif opt in ("-p", "--pullrequest"):
            PRID = arg
            PRURL = 'https://github.com/konecorp/SFDC-MAIN/pull/' + PRID
        ## this might become a fill path
        elif opt in ("-l", "--logmessage"):
            logmessage = arg
        ## we might add a branch for more logic
        #elif opt in ("-b", "--branch"):
        #    logmessage = arg    

    
    #target = 'INT' # STAGING DEV INT PROD ?
        #branch = 'INT' # INT / RELEASEBRANCH / UATFIX ## --> we might use later
    #event = 'PULL_REQUEST' # DEPLOY / Pull_Request
    #status = 'TEST_FAILED' #DEPLOY_FAILED / TEST_FAILED / TEST_SUCCESS / DEPLOY_SUCCESS
    #userstory = '33306'
    #PRID = '12345'
    #PRURL = 'https://github.com/konecorp/SFDC-MAIN/pull/' + PRID
    #logmessage = 'TESTLOGHERE' # could be a file name, see generatebuildxml.py for example file open
    
    ## TO DO replace with generic bot user    
    username = 'bherudek@salesforce.com'
    password = 'Tanzen03'
    top_level_url = 'https://kone.tpondemand.com'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    urlpostcomments = top_level_url + '/api/v1/comments'
    urlgettask = top_level_url + '/api/v1/tasks'
    urlposttasks = urlgettask
    urlpostcomments = top_level_url + '/api/v1/comments'
    urlpostUS = top_level_url + '/api/v1/UserStories/' 
    urlgetUS = urlpostUS
    joke_url = 'https://geek-jokes.sameerkumar.website/api' ## https://www.programmableweb.com/category/humor/api
    
    now = datetime.datetime.now()
    ## name of the task, per convention, where the test plan is defined. From here we get the contact person
    testtask = 'APEXTESTS'

    ## GET OUR CONTACT PERSON for Comments
    where = '?where=(name eq \'APEXTESTS\') and (UserStory.Id eq \''+ userstory+ '\')'
    #print(where)
    urlgetsearchtask = urlgettask + where
    r = requests.get(urlgetsearchtask, headers=headers, auth=(username, password), stream=True)
    ownersoup = BeautifulSoup(r.content,  'html.parser') #'lxml')
    
    #print(soup.prettify())
    ownerfirstname = str(ownersoup.owner.firstname).replace('firstname','').replace('<','').replace('>','').replace('/','')
    ownerlastname = str(ownersoup.owner.lastname).replace('lastname','').replace('<','').replace('>','').replace('/','')
    ownerlogin = str(ownersoup.owner.login).replace('login','').replace('<','').replace('>','').replace('/','')
    


    ## CREATE A BACK REPORT TASK
    '''
    one timer here
    GET to /api/v1/userstories/194?include=[Project] (to know ID of the project)
    urlget = 'https://kone.tpondemand.com/api/v1/UserStories/' + userstory + '?include=[Project]'
    r = requests.get(urlget, headers=headers, auth=(username, password), stream=True)
    print(r)
    print(r.content) --> Project ID is9121
    '''

    payloadtask = '{Name:' + '\"' + target + ' ' +event + ' ' + status + ' ' + str(now) + '\", Description:' + '\"' + logmessage + '\", Project:{Id:9121}, UserStory:{Id:' + userstory + '}}'
    #print(payloadtask)
    
    r = requests.post(urlposttasks, data=payloadtask, headers=headers, auth=(username, password))
    #print(r)
    #print(r.content)
    tasksoup = BeautifulSoup(r.content,  'html.parser') #'lxml')
    #print(tasksoup)
    taskid = tasksoup.task['id']
    #print(taskid)
    taskidurl = top_level_url + '/entity/' + taskid
    
    ## On success we post to the user story

    ## On failure, we post to the task
    if status == 'TEST_FAILED' or status == 'DEPLOY_FAILED':
        #print(urlpost)
        addressee = 'Hey @user:' + ownerlogin +'[' + ownerfirstname + ' ' + ownerlastname + ']'
        todo = ', please check the failed testscripts for Pull Request: ' + PRURL
        joke = requests.get(joke_url, headers=headers, stream=True)
        #print(joke.json())
        cheerup = '\nNever give up, here is a joke to cheer you up:' + str(joke.json())
        comment = addressee + todo + cheerup #str(joke.json())
        #print(comment)
        #comment = 'test'
        payloadcomment = '{Description:' + '\"' + comment + '\", General:{Id:' + taskid + '}}'
        #print(payloadcomment)
        r = requests.post(urlpostcomments, data=payloadcomment, headers=headers, auth=(username, password))
        
        '''
        ## one timer, or use when status changes to get IDs
        
        #change state for Task ID#219
        #GET to /api/v1/tasks/219?include=[EntityState[NextStates]] (to know ID of the state)
        #POST to /api/v1/tasks/219 payload {EntityState:{Id:87}}
        
        #urlgetstates = top_level_url + '/api/v1/tasks/' + taskid + '?include=[EntityState[NextStates]]'
        #urlgetstates = top_level_url + '/api/v1/tasks/' + str(33682) + '?include=[EntityState[NextStates]]'
        
        #r = requests.get(urlgetstates, headers=headers, auth=(username, password), stream=True)
        #print(r.content)
        #<EntityState ResourceType="EntityState" Id="901" Name="Active">\
        # <EntityState ResourceType="EntityState" Id="902" Name="To Re-estimate">
        #<EntityState ResourceType="EntityState" Id="904" Name="In Development">
        #<EntityState ResourceType="EntityState" Id="905" Name="In Testing">\r\n  
        # EntityState ResourceType="EntityState" Id="906" Name="Closed" --> 1st place to in testing, then close
        '''
        urlposttasks = urlposttasks+'/'+taskid
        payloadustaskstatus = '{EntityState:{ID:906}}' ## Closed, we can close directly in API. UI requires 1st test status
        r = requests.post(urlposttasks, data=payloadustaskstatus, headers=headers, auth=(username, password))
      
    elif status == 'TEST_SUCCESS' or status == 'DEPLOY_SUCCESS':
        ## if successful we can change the US status

        '''
        ## one timer, or use when status changes to get IDs
        #urlgetstates = 'https://kone.tpondemand.com/api/v1/UserStories/' + userstory + '?include=[EntityState[NextStates]]'

        #r = requests.get(urlgetstates, headers=headers, auth=(username, password), stream=True)
        #print(r.content)

        <EntityState ResourceType="EntityState" Id="896" Name="New">        
        <EntityState ResourceType="EntityState" Id="1031" Name="Grooming Done">        
        <EntityState ResourceType="EntityState" Id="1097" Name="Reviewed by Test Team">       
        <EntityState ResourceType="EntityState" Id="1539" Name="Design in Progress">
        <EntityState ResourceType="EntityState" Id="1049" Name="Design Blocked">
        <EntityState ResourceType="EntityState" Id="1116" Name="Design In Review">
        <EntityState ResourceType="EntityState" Id="897" Name="Ready for Dev">
        <EntityState ResourceType="EntityState" Id="1425" Name="Needs Work">
        <EntityState ResourceType="EntityState" Id="943" Name="Blocked">
        <EntityState ResourceType="EntityState" Id="1115" Name="Ready for Review">
        <EntityState ResourceType="EntityState" Id="1327" Name="Dev Completed">
        <EntityState ResourceType="EntityState" Id="1099" Name="Testing Blocked">
        <EntityState ResourceType="EntityState" Id="942" Name="Deployed to INT">
        <EntityState ResourceType="EntityState" Id="1540" Name="Test OK INT">
        <EntityState ResourceType="EntityState" Id="1541" Name="Deployed to FULL">
        <EntityState ResourceType="EntityState" Id="1426" Name="Test OK FULL">
        <EntityState ResourceType="EntityState" Id="899" Name="Done">
        '''

        urlpostUSstates = urlpostUS + str(userstory)

        comment = '@user:' + ownerlogin +'[' + ownerfirstname + ' ' + ownerlastname + ']' + ' Woohoo - all tests passed (see Task ' + taskidurl + ' and Pull Request ' + PRURL + ')'
        ## Per environment =target stausses and messages can get refined
        payloadusstatus = ''
        if target == 'INT':
            comment = comment + '. Please verify the status, initiate a code review (yes, we trust 4 eyes more than 2!) and inform the Test Team.'
            payloadusstatus = '{EntityState:{ID:942}}' ## DEPLOYED to INT. for INT we might also say immediately ready for test and make a comment to initiate review
        elif target == 'FULL':
            comment = comment + '. You good to go! Pls inform the Test Team to start rolin\' too.'
            payloadusstatus = '{EntityState:{ID:1541}}' ## DEPLOYED to FULL. for INT we might also say immediately ready for test and make a comment to initiate review
        #print(urlpostUSstates)
        #print(payloadusstatus)
        r = requests.post(urlpostUSstates, data=payloadusstatus, headers=headers, auth=(username, password))
        ## make a comment into the user story
        #print(urlpost)
       
        payloadcomment = '{Description:' + '\"' + comment + '\", General:{Id:' + userstory + '}}'
        r = requests.post(urlpostcomments, data=payloadcomment, headers=headers, auth=(username, password))
        payloadustaskstatus = '{EntityState:{ID:901}}'  # Active
        #update the task status
        urlposttasks = urlposttasks+'/'+taskid
        #print(urlposttasks)
        #print(payloadustaskstatus)
        r = requests.post(urlposttasks, data=payloadustaskstatus, headers=headers, auth=(username, password))
 

if __name__ == "__main__":
   main(sys.argv[1:])
