#!/usr/bin/python

'''
install python e.g. conda

https://pandas.pydata.org/pandas-docs/stable/install.html

Pip install pandas
pip install xlutils
pip install xlwt
pip install xlrd
pip install openpyxl

'''

# (base) bherudek-ltm1:testpythonbuildxml bherudek$ chmod ugo=rwx *
# (base) bherudek-ltm1:testpythonbuildxml bherudek$  python generatebuildxml.py -d . -t int -a realdeployandtest -p FSM
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

##PurePath

def main(argv):
    correct_usage = 'test.py -t <targetenv> -a <[checkdeploy|checkdeployandtest|realdeployandtest]> -p <optional:[FSM|XYZ|ABX]> -n <optional:[12756]>';
    inputfile = 'choosetests.xlsx'
    templatebuild = 'build_template.xml'
    outputfile = 'build.xml'
    projectteam = 'SHARED'
    try:
        opts, args = getopt.getopt(argv,"d:t:a:p:n:",["deploypackage", "target=","action=","project","number"])
    except getopt.GetoptError:
        print (correct_usage )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print (correct_usage )
            sys.exit()
        elif opt in ("-d", "--deploypackage"):
            deploypackagepath = arg
        elif opt in ("-t", "--targetenv"):
            targetenv = arg
        elif opt in ("-p", "--project"):
            projectteam = arg 
        elif opt in ("-a", "--action"):
            action = arg
            if action not in {"checkdeploy","realdeployandtest"}:
                print ('action: ' + str(action))
                print ('Pls set correct action.\n') 
                print (correct_usage )
                sys.exit()

    print ('target environment is ' +str(targetenv))
    print ('action requested is ' + str(action))
    excel_sheet = pd.read_excel(inputfile)
    #print (excel_sheet)

    print(deploypackagepath)
    p = Path(deploypackagepath)
    #print(p.glob('**/*.cls'))
    list_files = list(p.glob('**/*.cls'))
    #print(list_files)
    files_as_keys = list()
    for onefile in list_files:
        files_as_keys.append(PurePosixPath(onefile).stem)
    #print(list(p.glob('**/*.cls')))
    #print(list(PurePosixPath(list(p.glob('*.cls'))).stem))
    ## PurePosixPath('my/library.tar.gz').stem
    #print(files_as_keys)

## TO DO: REPEAT FOR TestsToRun1 other columns        

    list_tests_torun = list()
    for file_key in files_as_keys:
        onetest = excel_sheet.loc[excel_sheet['Class'] == file_key, 'TestsToRun1']

        #print('onetest: ' + str(onetest))
        if onetest.empty == False:
            list_enum = list(enumerate(onetest))
            #print(list_enum)
            #print(list_enum[0][1])
            #if onetest != 'NaN': 
            if str(list_enum[0][1]) not in {'0', '?', 'nan'}:
                list_tests_torun.append(str(list_enum[0][1]))
            #print('list_tests_torun: ' + str(list_tests_torun))
            onetest = None

    ## we always run all tests that need to work whatever is deployed 
    #allprojecttests = excel_sheet.loc[(excel_sheet['TestKoneWide'] == 'yes' ) | ((excel_sheet['Project'] == 'FSM' | excel_sheet['Project'] == 'SHARED') & excel_sheet['TestProjectWide'] == 'yes'), 'TestsToRun1']
    allprojecttests = excel_sheet.loc[(excel_sheet['TestKoneWide'] == 'yes' ) |  ((excel_sheet['TestProjectWide'] == 'yes') & ((excel_sheet['Project'] == projectteam)) | (excel_sheet['Project'] == 'SHARED')), 'TestsToRun1']
    list_enum_allproj = list(enumerate(allprojecttests))
    #print('list_enum_allproj: ' + str(list_enum_allproj))
    for enum_allproj in list_enum_allproj:
        if str(enum_allproj[1]) not in {'0', '?', 'nan'}:
            #print('list_enum_allproj: ' + str(enum_allproj[1]))
            list_tests_torun.append(str(enum_allproj[1]))
        

    ## per team we rerun certain tests always
    
    #projectteam
    
    #print(excel_sheet.loc[excel_sheet['A'] == 'foo'])
    list_tests_torun_nodup = list(set(list_tests_torun))
    #print('list_tests_torun_nodup: ' + str(list_tests_torun_nodup))

    ## now we add tests, if action chosen accordingly
   
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
            
if __name__ == "__main__":
   main(sys.argv[1:])
