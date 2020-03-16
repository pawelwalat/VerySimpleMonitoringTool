import os
import subprocess
import shlex
shlex.split("/bin/prog -i data.txt -o \"more data.txt\"")

def run(command, timeout=2.0):
    f = subprocess.Popen(shlex.split(command),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)   
    f.wait()     
    output, errors = f.communicate()    
    return str(output)+'\\n'+str(errors)
    