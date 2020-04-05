"""
!wget https://raw.githubusercontent.com/nemon-/tools4paddle/master/paddlePrint.py
from paddlePrint import pprint
pprint('abc')

pprint('log begin',file_name='/home/aistudio/_log.txt')
pprint('123')
pprint('def',end='-----')
pprint('ghi')
pprint('x=%f'%.123456,nolog=True)
pprint(read_lines=2)
pprint(read_lines=-2)
pprint('='*5,nolog=True)
pprint(read_lines=True)
"""

class pprint():
    _fname =None
    _f_handle = None
    def __init__(self,content='',out=True,file_name=None,read_lines=0,end='\n',nolog=False):
        if file_name!=None:
            pprint._fname=file_name
        if pprint._fname!=None:
            import io
            if not nolog:
                if type(pprint._f_handle)!=io.TextIOWrapper or pprint._f_handle.closed:
                    pprint._f_handle=open(pprint._fname,'a+')
                pprint._f_handle.write( content if type(content)==str else repr(content))
                pprint._f_handle.write(end)
                pprint._f_handle.close()
            if read_lines!=0:
                pprint._f_handle=open(pprint._fname,'r')
                lines = pprint._f_handle.readlines()
                if int==type(read_lines):
                    lines = lines[:read_lines]
                pprint._f_handle.close()
                for line in lines:
                    print( line,end='')
        if out:
            print(content)
        return None

