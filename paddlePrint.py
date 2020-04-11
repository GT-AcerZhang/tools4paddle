"""
!wget https://raw.githubusercontent.com/nemon-/tools4paddle/master/paddlePrint.py
from paddlePrint import print,showlog
# or
import paddlePrint as pt
print=pt.pprint

print(1,2,3,log='0.txt')
print(9,8,'l',{'k':0},(6,),range(9))
# or
showlog()
showlog('all')
showlog(2)
showlog(-2)
"""
import sys

class setting:
    _old_print_=print
    _old_stdout_=sys.stdout
    _log_file_name_=None
    _log_file_hadl_=None
    
    def __init__():
        pass

def pprint(*args,nolog=False,**kwargs):
    if 'log'in kwargs.keys() :
        setting._log_file_name_=kwargs['log']
        kwargs.pop('log')
    setting._old_print_(*args,**kwargs)
    if (not nolog) and setting._log_file_name_!=None and ('log' not in kwargs.keys() or kwargs['file']==sys.stdout):
        new_kwargs = {k:v for k,v in kwargs.items()}
        _log_file_hadl_ = open(setting._log_file_name_,'a+')
        new_kwargs['file'] =  _log_file_hadl_
        setting._old_print_(*args,**new_kwargs)

def print(*args,**kwargs):
    pprint(*args,**kwargs)

def showlog(lines=0,log=None):
    if log==None:
        _log=setting._log_file_name_
    else:
        _log=log
    if _log!=None :
        setting._old_print_('log file name : '+_log)
    if lines!=0:
        with open(_log,'r') as h_log_file:
            ls = h_log_file.readlines()
            if type(lines)!=int :
                pass
            elif lines<0:
                ls = ls[lines:]
            elif lines>0:
                ls = ls[:lines]
            for l in ls:
                setting._old_print_( l ,end='')
