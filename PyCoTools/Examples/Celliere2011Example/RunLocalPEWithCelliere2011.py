# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 15:19:52 2017

@author: b3053674
"""

import PyCoTools
import os
import FilePaths
import shutil
import sys




def runHJ(copasi_file,parameters,report_name,mode):
    '''
    copasi_file:
        file to run hook and jeeves from 
    parameters:
        dictionary of parameters. Keys must match model names, values are input parameters
    report_name:
        name of the report to output PE data.
    mode:
        either 'SGE' for SGE cluster or 'true' to run on current machine
    
    Take parameters from global parameter estimation and perform local parameter
    estimation around these parameters.
    
    Need to instantiate ParameterEstimation class before inserting parameters
    '''
    if 'RSS' in parameters.keys():
        del parameters['RSS']
    for i in parameters:
        print i,':\t',parameters[i]
    PyCoTools.pycopi.InsertParameters(copasi_file,ParameterDict=parameters)
    
    PE=PyCoTools.pycopi.ParameterEstimation(copasi_file,C.noisy_timecourse_report,
                                         Method='HookeJeeves',
                                         IterationLimit=20000,
                                         Tolerance=1e-30,
                                         RandomizeStartValues='false',
                                         Plot='true',
                                         SaveFig='true',
                                         UseTemplateStartValues='false',
                                         )

        
    PE.set_up()
    ## Run via scan task because this gives only best values in function
    ## evaluations, rather than the periodic function evaluations as well
    print '\n\n'
    print report_name
    print '\n'
    PyCoTools.pycopi.Scan(copasi_file,ScanType='repeat',Run=mode,
                          NumberOfSteps=1,
                          ReportName=report,
                          ReportType='parameter_estimation')

#data.shape[0]*0.01)
if __name__=='__main__':
    C=FilePaths.Celliere2011Example()
    
    if os.path.isdir(C.PEData_dir):
        PEData_path=C.PEData_dir
    elif os.path.isdir(C.PEData_dir) !=True:
        if os.path.isfile(C.PEData_file):
            PEData_path=C.PEData_file
            
    if os.path.isdir(PEData_path)!=True:
        raise TypeError
            
            
    data= PyCoTools.PEAnalysis.ParsePEData(PEData_path).data
    print data
                                      
#    if sys.platform=='win32':
#        '''
#        Run hook and jeeves from the top 1 percent
#        best estimated parameter from the genetic algorithm
#        Run on windows machine
#        '''
#        mode='true'
#        for i in range(int(data.shape[0]*0.1)):
#            print 'running secondary PE on index {} with starting RSS of {}'.format(i,data.iloc[i]['RSS'])
#            if os.path.isdir(C.local_PEData_dir)!=True:
#                os.mkdir(C.local_PEData_dir)
#            report=os.path.join(C.local_PEData_dir,'{}.txt'.format(i))
#            print runHJ(C.celliere2011_model,data.iloc[i].to_dict(),report,mode)
#
#    elif sys.platform=='linux2':
#        '''
#        A few differences required when running on a clutser. 
#        Generally there is a time delay between submitting job and 
#        running the job. This time delay is longer than the time between an iteration
#        of the below loop meaning that by the time the job gets submitted, all
#        jobs get the same report name. Solution - copy and enumerate copasi file. 
#        
#        '''
#        mode='SGE'
#        print mode
##        for i in range(int(data.shape[0]*0.01)):
##            print 'running secondary PE on index {} with starting RSS of {}'.format(i,data.iloc[i]['RSS'])
##            if os.path.isdir(C.local_PEData_dir)!=True:
##                os.mkdir(C.local_PEData_dir)
##            report=os.path.join(C.local_PEData_dir,'{}.txt'.format(i))
##            enum_cps=os.path.splitext(C.celliere2011_model)[0]+'temp{}.cps'.format(str(i))
##            shutil.copyfile(C.celliere2011_model,enum_cps)
##            print runHJ(enum_cps,data.iloc[i].to_dict(),report,mode)        
#        































