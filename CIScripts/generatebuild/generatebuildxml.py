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
# (base) bherudek-ltm1:testpythonbuildxml bherudek$  python generatebuildxml.py -d . -e intPR -a realdeployandtest -p FSM 33306
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

##PurePath

def main(argv):
    correct_usage = 'test.py -e <[intPR|intINCRDeploy|releasePR]> -a <[checkdeploy|checkdeployandtest|realdeployandtest]> -p <optional:[FSM|XYZ|ABX]> -n <optional:[12756]>';
    inputfile = 'choosetests.xlsx'
    templatebuild = 'build_template.xml'
    outputfile = 'build.xml'
    projectteam = 'SHARED'
    change_no = '0'
    try:
        opts, args = getopt.getopt(argv,"d:e:a:p:n:",["deploypackagedirectory", "event=","action=","project","numberchange"])
    except getopt.GetoptError:
        print (correct_usage )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (correct_usage )
            sys.exit()
        elif opt in ("-d", "--deploypackagedirectory"):
            deploypackagepath = arg
        elif opt in ("-n", "--numberchange"):
            change_no = arg   
        elif opt in ("-e", "--event"):
            event = arg
            if event not in {"intPR","intINCRDeploy", "releasePR", "PRODINCRDeploy"}:
                print ('event: ' + str(action))
                print ('Pls set correct event.\n') 
                print (correct_usage )
                sys.exit()
        elif opt in ("-p", "--project"):
            projectteam = arg 
        elif opt in ("-a", "--action"):
            action = arg
            if action not in {"checkdeployonly","checkdeployandtest", "realdeployandtest"}:
                print ('action: ' + str(action))
                print ('Pls set correct action.\n') 
                print (correct_usage )
                sys.exit()

    print ('event environment is ' +str(event))
    print ('action requested is ' + str(action))
    excel_sheet = pd.read_excel(inputfile)
    #print (excel_sheet)

    ## instead of relying on a file, we could also go to the PR on git: https://developer.github.com/v3/pulls/#list-pull-requests-files
    print(deploypackagepath)
    p = Path(deploypackagepath)
    #print(p.glob('**/*.cls'))
    # Note, test classes in the repo get added automatically for test (self reference in excel sheet)
    list_files = list(p.glob('**/*.cls'))
    #print(list_files)
    files_as_keys = list()
    for onefile in list_files:
        files_as_keys.append(PurePosixPath(onefile).stem)
    #print(list(p.glob('**/*.cls')))
    #print(list(PurePosixPath(list(p.glob('*.cls'))).stem))
    ## PurePosixPath('my/library.tar.gz').stem
    #print(files_as_keys)

    list_tests_torun = list()
    for file_key in files_as_keys:
        onetest = excel_sheet.loc[excel_sheet['Class'] == file_key, 'TestsToRun1':'TestsToRun10']

        list_onetest = onetest.values.tolist() 
        flat_onetest = [item for sublist in list_onetest for item in sublist]


        for onetest in list(enumerate(flat_onetest)):
            if str(onetest[1]) not in {'0', '?', 'nan'}:
            #print('enum_allproj[0]: ' + str(enum_allproj[0]))
            #print('enum_allproj[1]: ' + str(enum_allproj[1]))
            #print('enum_allproj[2]: ' + str(enum_allproj[2]))
                list_tests_torun.append(str(onetest[1]))

        #print('onetest: ' + str(onetest))
        #if flat_onetest.empty == False:
        #    list_enum = list(enumerate(flat_onetest))
            #print(list_enum)
            #print(list_enum[0][1])
            #if onetest != 'NaN': 
        #    if str(list_enum[0][1]) not in {'0', '?', 'nan'}:
        #        list_tests_torun.append(str(list_enum[0][1]))
            #print('list_tests_torun: ' + str(list_tests_torun))
            #onetest = None

    print("\n\n list_tests_torun after package directory files_as_keys: " + str(files_as_keys))
    print(list_tests_torun)

    ## we always run all tests that need to work whatever is deployed 
    #allprojecttests = excel_sheet.loc[(excel_sheet['TestKoneWide'] == 'yes' ) | ((excel_sheet['Project'] == 'FSM' | excel_sheet['Project'] == 'SHARED') & excel_sheet['TestProjectWide'] == 'yes'), 'TestsToRun1']
    allprojecttests = excel_sheet.loc[((excel_sheet['TestKoneWide'] == 'yes' ) |  ((excel_sheet['TestProjectWide'] == 'yes') & ((excel_sheet['Project'] == projectteam)) | (excel_sheet['Project'] == 'SHARED'))), 'TestsToRun1':'TestsToRun10']
   
    list_enum_allprojecttests = allprojecttests.values.tolist() #enumerate(plus_test_lists) #list(enumerate(plus_test_lists))
    flat_list_enum_allprojecttests = [item for sublist in list_enum_allprojecttests for item in sublist]

    #print('flat_list_enum_allprojecttests: ' + str(flat_list_enum_allprojecttests))
    for enum_allproj in list(enumerate(flat_list_enum_allprojecttests)):
        if str(enum_allproj[1]) not in {'0', '?', 'nan'}:
            #print('enum_allproj[0]: ' + str(enum_allproj[0]))
            #print('enum_allproj[1]: ' + str(enum_allproj[1]))
            #print('enum_allproj[2]: ' + str(enum_allproj[2]))
            list_tests_torun.append(str(enum_allproj[1]))

    print("\n\n list_tests_torun after Project logic")
    print(list_tests_torun)

    ## now we add tests that the develper requested per targy with a REST CALL
    
    ## TO DO: set better user
    username = 'bherudek@salesforce.com'
    password = 'Tanzen03'
    top_level_url = 'https://kone.tpondemand.com'
    url = 'https://kone.tpondemand.com/api/v1/UserStories/' + change_no + '/tasks/'
    r = requests.get(url, auth=(username, password), stream=True)  
    page = r.content
    soup = BeautifulSoup(str(page),  'html.parser') #'lxml')
    #print(soup.prettify())
    #print(soup.getText())
    developer_tests_list =[]
    for subsoup in soup.tasks.find_all('task'):
        if subsoup['name'] == 'APEXTESTS':
            #print(subsoup.getText())
            #print(subsoup['name'])
            #print(subsoup.find_all('description')):
            for desc in subsoup.find_all('description'):
                
                #print(desc)
                dev_tests_list = desc.getText().replace('</div>','').replace('\\r','').replace('\\n','').split("<div>")
                developer_tests_list = [x for x in dev_tests_list if x]
                #print(developer_tests_list)

    list_tests_torun = list_tests_torun + developer_tests_list
    #print(list_tests_torun)

    print("\n\n list_tests_torun after targy addition")
    print(list_tests_torun)
  

   
    ## now we add tests, if action chosen accordingly
    plus_test_lists =[]
    minus_test_lists = []

    if event == "intPR":
        #plus_test_lists = excel_sheet.loc[excel_sheet['TestOn_IntPullRequest_Overwrite'] == 'yes' , 'TestsToRun1']
        plus_test_lists = excel_sheet.loc[excel_sheet['TestOn_IntPullRequest_Overwrite'] == 'yes' , 'TestsToRun1':'TestsToRun10']
        #print(plus_test_lists)
        minus_test_lists = excel_sheet.loc[excel_sheet['TestOn_IntPullRequest_Overwrite'] == 'no' , 'TestsToRun1':'TestsToRun10']
    elif event == "intINCRDeploy":
        plus_test_lists = excel_sheet.loc[excel_sheet['TestOn_IntIncrDeploy_Overwrite'] == 'yes' , 'TestsToRun1':'TestsToRun10']
        minus_test_lists = excel_sheet.loc[excel_sheet['TestOn_IntIncrDeploy_Overwrite'] == 'no' , 'TestsToRun1':'TestsToRun10']
    elif event == "releasePR":
        plus_test_lists = excel_sheet.loc[excel_sheet['TestOn_ReleasePullRequest_Overwrite'] == 'yes' , 'TestsToRun1':'TestsToRun10']
        minus_test_lists = excel_sheet.loc[excel_sheet['TestOn_ReleasePullRequest_Overwrite'] == 'no' , 'TestsToRun1':'TestsToRun10']
    elif event == "PRODINCRDeploy":
        plus_test_lists = excel_sheet.loc[excel_sheet['TestOn_PRODIncrDeploy_Overwrite'] == 'yes' , 'TestsToRun1':'TestsToRun10']
        minus_test_lists = excel_sheet.loc[excel_sheet['TestOn_PRODIncrDeploy_Overwrite'] == 'no' , 'TestsToRun1':'TestsToRun10']
    print('start')
    #print(plus_test_lists)
    #print(plus_test_lists[0])
    #print(plus_test_lists[1])
    #test = excel_sheet.loc[plus_test_lists, 'TestsToRun1']
    #print(test)
    list_enum_plustests = plus_test_lists.values.tolist() #enumerate(plus_test_lists) #list(enumerate(plus_test_lists))
    flat_list_enum_plustests = [item for sublist in list_enum_plustests for item in sublist]
    #try:
    #    flat_list_enum_plustests = flat_list_enum_plustests.remove('0')
    #    flat_list_enum_plustests = flat_list_enum_plustests.remove('nan')
    #except ValueError:     
    #    None
    #print('list_enum_allproj: ' + str(list_enum_allproj))
    #print(flat_list_enum_plustests)
    for enum_plustest in list(enumerate(flat_list_enum_plustests)):
        #print('enum_plustest[0]: ' + str(enum_plustest[0]))
        #print('enum_plustest[1]: ' + str(enum_plustest[1]))
        if str(enum_plustest[1]) not in {'0', '?', 'nan'}:
            #print('enum_plustest[0]: ' + str(enum_plustest[0]))
            print('enum_plustest[1]: ' + str(enum_plustest[1]))
            #print('enum_plustest[2]: ' + str(enum_plustest[2]))
            list_tests_torun.append(str(enum_plustest[1]))
    
    list_enum_minustests = minus_test_lists.values.tolist() #enumerate(plus_test_lists) #list(enumerate(plus_test_lists))
    flat_list_enum_minustests = [item for sublist in list_enum_minustests for item in sublist]
    for enum_minustest in list(enumerate(flat_list_enum_minustests)):
        if str(enum_minustest[1]) not in {'0', '?', 'nan'}:
            #print('list_enum_allproj: ' + str(enum_allproj[1]))
            try:
                list_tests_torun.remove(str(enum_minustest[1]))
            except ValueError:     
                None
    print("\n\n list_tests_torun after event logic addition")
    print(list_tests_torun)
    
    #print(excel_sheet.loc[excel_sheet['A'] == 'foo'])
    list_tests_torun_nodup = list(set(list_tests_torun))
    #print('list_tests_torun_nodup: ' + str(list_tests_torun_nodup))

    print("\n\n list_tests_torun after dedup")
    print(list_tests_torun_nodup)

   
    f = open('./' + templatebuild, 'r')
    linelist = f.readlines()
    f.close
    deploycodetest_replace = 'DEPLOYCODEREPLACETHIS'
    #deploycodecheckonlytest_replace   '<!-- DEPLOYCODECHECKONLY: REPLACE THIS-->' 
    deploycodetest_test = ''
    for test in list_tests_torun_nodup:   
    	 deploycodetest_test = deploycodetest_test + '\t\t\t\t<runTest>' + test + '</runTest>\n'
    f2 = open('./build.xml', 'w')
    for line in linelist:
        if deploycodetest_replace in line:
            if action == 'realdeployandtest': 
                line = deploycodetest_test
            else:
                line =''
        f2.write(line)
    f2.close

    ## now we make a note into the Pull Request, that this PR was tested and deployed.
    ## Note: after the run, there should be a python script running too giving back the results
    ## This is useful for bookkeeping but also for the developer and reviewers
    ## https://developer.github.com/v3/pulls/comments/
    ## POST /repos/:owner/:repo/pulls/:number/comments
        ## {
            ##"body": "Nice change",
            ##"commit_id": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
            ##"path": "file1.txt",
            ##"position": 4
        ## }
    ## comments on PRs go via the ISSUE API: 
        # https://developer.github.com/v3/guides/working-with-comments/#pull-request-comments
        # https://developer.github.com/v3/issues/comments/#create-a-comment
    ## example:
        # https://github.com/octocat/Spoon-Knife/pull/1176
        # https://github.com/github/platform-samples/blob/master/api/ruby/working-with-comments/pull_request_comment.rb    

    ## Note,  PR and merges can be done from the command line
    ## https://hackernoon.com/how-to-git-pr-from-the-command-line-a5b204a57ab1
    ## for branches, where we do not require a review from an Architect, we could automatically merge them 
    ## after all tests passed

if __name__ == "__main__":
   main(sys.argv[1:])
