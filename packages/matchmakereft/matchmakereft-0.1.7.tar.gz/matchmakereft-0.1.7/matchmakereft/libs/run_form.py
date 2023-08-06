import subprocess
import glob
import sys
import os
import re
import math
from colorama import Fore
from colorama import Style
from tqdm.auto import tqdm, trange
from time import sleep
from . import file as jsf

def better_log(file,indexlist):
    if not os.path.isfile(file+".mat"):
        with open(file) as f:
            lines = f.read().splitlines()
            i0=0
            i1=0
            for i,li in enumerate(lines):
                if "ampl" in li:
                    i0=i;
                if ";" in li:
                    i1=i;
        lin=''.join([x.strip() for x in  lines[i0:i1+1]])
        for i in range(20):
            lin=lin.replace("f"+str(i+1),"fl"+str(i+1))
        lin=lin.replace("e_","ee")
        lin=lin.replace("[MM.epsi]","epsilonbar")
        lin=re.sub(r'd_\(([0-9a-zA-Z]*),([0-9a-zA-Z]*)\)', r'dd[\1,\2]', lin)
        lin=re.sub(r'esfull\(([0-9]*)\)', r'esfull[\1]', lin)
        lin=re.sub(r'eseft\(([0-9]*)\)', r'eseft[\1]', lin)
        lin=lin.replace("=","->")
        lin=lin.replace(";",",")
        lin="{"+lin+"}"
        lin=lin.replace(",}","}")
        with open(file+".mat","w") as ff:
            ff.write(lin)

def read_new_indices(dirname):
    # define new parameters
    with open(dirname+'QGRAF/model_data/newindices','r') as f:
        all_lines = f.readlines()
    return ', '.join([x.split("=")[0] for x in all_lines])

def run_form(dirname0,isEFT):
    if os.path.isdir(dirname0):
        filesdonealready=[]
        dirname=jsf.proper_dir_path(dirname0)
        newindices=read_new_indices(dirname)
        currentdir=os.getcwd()
        if os.path.isdir(dirname+"FORM/proc_0loop/"):
            os.chdir(dirname+"FORM/proc_0loop/")
            aux = glob.glob("*frm")
            nam = str(math.ceil(math.log10(len(aux))))
            frm = "{n_fmt:"+nam+"}/{total_fmt:"+nam+"} amplitudes | {percentage:3.0f}% |{bar:20}| {desc}" 
            filelist=tqdm(aux, bar_format=frm)
            filelist.write("Computing the tree-level amplitudes for model "+dirname[:-1])
            for fil in filelist:

                filelist.set_description_str("(amplitude %s)" % fil[:-4].replace("_"," "))
                # filelist.set_description("Computing the tree-level amplitude %s" % fil[:-4].replace("_"," "))
                # we check for the .out file because the .log is created even if form doesnt run smoothly
                if os.path.isfile(fil[:-4]+".out"):
                    filesdonealready.append(fil[:-4]+".out")
                else:

                    try:
                        p=subprocess.run(("form -F "+fil).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    except subprocess.CalledProcessError as E:
                        # there was a problem, go back to the original directory and raise an exception
                        os.chdir(currentdir)
                        raise Exception("\n"+ Fore.RED + "There was an error when running "+' '.join(E.args[1])+" in "+dirname+"FORM/proc_0loop/, please check!"+Style.RESET_ALL+"\n")
                if os.path.isfile(fil[:-4]+".log"):
                    better_log(fil[:-4]+".log",newindices)
                if os.path.isfile(fil[:-4]+".out"):
                    better_log(fil[:-4]+".out",newindices)
            os.chdir(currentdir)
        if os.path.isdir(dirname+"FORM/proc_1loop/") and not isEFT:
            os.chdir(dirname+"FORM/proc_1loop/")
            aux = glob.glob("*frm")
            nam = str(math.ceil(math.log10(len(aux))))
            frm = "{n_fmt:"+nam+"}/{total_fmt:"+nam+"} amplitudes | {percentage:3.0f}% |{bar:20}| {desc}" 
            filelist=tqdm(aux, bar_format=frm)
            filelist.write("Computing the one-loop amplitudes for model "+dirname[:-1])
            for fil in filelist:
                filelist.set_description_str("(amplitude %s)" % fil[:-4].replace("_"," "))
                # we check for the .out file because the .log is created even if form doesnt run smoothly
                if os.path.isfile(fil[:-4]+".out"):
                    filesdonealready.append(fil[:-4]+".out")
                else:
                    try:
                        p=subprocess.run(("form -F "+fil).split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    except subprocess.CalledProcessError as E:
                        # there was a problem, go back to the original directory and raise an exception
                        os.chdir(currentdir)
                        raise Exception("\n"+ Fore.RED + "There was an error when running "+' '.join(E.args[1])+" in "+dirname+"FORM/proc_1loop/, please check!"+Style.RESET_ALL+"\n")
                if os.path.isfile(fil[:-4]+".log"):
                    better_log(fil[:-4]+".log",newindices)
                if os.path.isfile(fil[:-4]+".out"):
                    better_log(fil[:-4]+".out",newindices)
            os.chdir(currentdir)

    else:
        print("not a valid directory")

