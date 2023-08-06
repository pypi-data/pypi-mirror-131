import subprocess,os
import imp
import multiprocessing

def TTSnorm(text, punc = False, unknown = True, lower = True, rule = False ):
    pid = multiprocessing.current_process().pid
    
    A=imp.find_module('vinorm')[1]

    #print(A)
    I=A+"/{}_input.txt".format(pid)
    with open(I,"w+") as fw:
        fw.write(text)

    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = A+'/lib'

    E=A+"/main"
    Command = [E]
    if punc:
        Command.append("-punc")
    if unknown:
        Command.append("-unknown")
    if lower:
        Command.append("-lower")
    if rule:
        Command.append("-rule")
    O=A+"/{}_output.txt".format(pid)
    Command.extend(["-i", I, "-o", O])
        
    subprocess.check_call(Command, env=myenv, cwd=A)
    
    
    with open(O,"r") as fr:
        text=fr.read()
    TEXT=""
    S=text.split("#line#")
    for s in S:
        if s=="":
            continue
        TEXT+=s+". "


    return TEXT