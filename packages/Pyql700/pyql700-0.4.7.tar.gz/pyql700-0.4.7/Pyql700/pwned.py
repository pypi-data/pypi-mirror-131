#!/usr/bin/env python3

import subprocess
import sys
import subprocess as sp
import os
import pathlib

#================= import packages hard way=====================
import hashlib
import random
import unicodedata  #names

import glob

import_list=['fire', 'alive_progress','time']

#==========================================install check_call======
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#==========================================install import======
def install_and_import(packagelist):
    import importlib
    for i in packagelist:
        try:
            importlib.import_module(i)
        except ImportError:
            install(i)
        finally:
            globals()[i] = importlib.import_module(i)

install_and_import( import_list )

#
#====================================== imports after install
#
from fire import Fire
from alive_progress import alive_bar,config_handler



#====================================================== RUN CODE
def launch(CMD, fake=False):
    #print("D... launchng", CMD)
    ok=False
    if not fake:
        try:
            res=sp.check_output( CMD.split() ).decode("utf8").rstrip()
            ok=True
        except:
            #print("D... CMD call ended !=0....")
            ok=False
        if not ok:
            return None
        #print("D...",res)
        return res



#======================================================main
def chkpass(passw="123456", sha_path="./"):
    if sha_path[-1]!="/":
        sha_path += "/"
    LIST=sha_path+'pwned-passwords-sha1-ordered-by-hash-v5.txt'
    if not os.path.exists(LIST):
        #print("D... LIST EXISTS")
    #else:
        print("D... LIST NOT EXIST !!!!!!!!!",LIST)
        quit()
    print("D... looking for password:", passw.strip() , end="")

    # encode the string
    encoded_str = passw.encode()

    # create a sha1 hash object initialized with the encoded string
    hash_obj = hashlib.sha1(encoded_str)

    # convert the hash object to a hexadecimal value
    hexa_value = hash_obj.hexdigest().upper()
    #print("HEX:",hexa_value)
    res=launch("sgrep "+hexa_value+" "+LIST)
    if not res is None:
        #print(res)
        count=res.split(":")[1]
        print("                    used {:5d}x: PAWNED!!". format(int(count)) ,end="")
        return count
    else:
        print("                                   ... ok", end="")
        return 0


#========================================== support to generatre keys
def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)


#==================================================== replace things =========
def generate_keys(s):
    """
    I want to replace keys I want
    """
    names=["Jiří	  ","Jan	  ","Petr	  ",
           "Josef	  ","Pavel	  ","Jaroslav ",
           "Martin	  ","Miroslav ","Tomáš	  ",
           "František","Zdeněk	  ","Václav	  ",
           "Karel	  ","Milan	  ","Michal	  ",
           "Vladimír ","Lukáš	  ","David	  ",
           "Ladislav ","Jakub	  ","Stanislav",
           "Roman	  ","Ondřej	  ","Antonín  ",
           "Radek	  ","Marek	  ","Daniel	  ",
           "Miloslav ","Vojtěch  ",  "Jaromír  ",
           "Filip	  ","Ivan	  ","Aleš	  ",
           "Libor	  ","Oldřich  ",  "Rudolf	  ",
           "Vlastimil","Jindřich ","Miloš	  ",
           "Adam	  ","Lubomír  "]
    names=[ strip_accents(i.strip()) for i in names]
    for i in names:
        print(i, end=",")
    print()


#=================================== SUPPORT FUNC
def get_pass_codes():
    files=glob.glob("*.subst")
    for fil in files:
        print("D... opening",fil)
        with open(fil) as f:
            res=f.readlines()
        #print(res)
        passrepl={}
        for i in res:
            #print(i)
            key=i.split()[0]
            value=i.split()[1].split(",")
            passrepl[key]=value
        #print(passrepl)
        return passrepl
    print("!... no .subst file")
    quit()

#============================================ ONE FUNC
def subst_pass(*page_file, sha_path="./", printit=False):  #checkonly=True
    """
    I can check the passwords in .page file; or print it
    """
    if isinstance(page_file, list) and  len(page_file) != 0:
        res=[]
        for i in page_file:
            print("D...subst_pass: PAGE--------------------",i)
            res.append(subst_pass(i, sha_path=sha_path, printit=printit))
        print("D... returning:", res, len(res))
        return res
    print("D... on track subst_pass:", page_file)
    fname=page_file[0]
    passrepl=get_pass_codes()
    with open(fname) as f:
        page = f.readlines()
    outtxt=""
    # ==================== replace on each line
    for line in page:
        #print("D... checking line:", line.rstrip() )
        newline = ""
        #================ check p:
        if line.find("p:") >= 0:
            pwd=line.split("p:")[-1]
            pwd=pwd.split(" ")[0]
            chkpass(pwd.rstrip(), sha_path) # I need to strip
        for k in passrepl.keys():
            #print("KEY...",k)

            #================ look for key presence:
            line2=line.lower()
            if line2.find(k) >= 0:
                pos = line2.find(k)
                lent = len(k)
                true_key = line[pos:pos+lent]
                true_map = [ c.isupper() for c in  true_key]
                i = random.randrange(len(passrepl[k]))
                false_key = passrepl[k][i]
                false_key2 = ""
                if len(false_key) != len(true_map):
                    print("D...  PROBLEM !!!!!!!!!!!!!!!!!!!", true_map, false_key)
                    quit()
                for i in range(len(false_key)):
                    if true_map[i]:
                        false_key2 += false_key[i].upper()
                    else:
                        false_key2 += false_key[i].lower()
                #print("D...   KEY FOUND at",pos," :", line.strip())
                line2 = line2[:pos] + false_key2 + line2[pos+lent:]
                if printit:
                    print("\nD...   newline     ",pos," :", line2.strip())
                #outtxt += line2
                if newline == "":
                    newline = line2
        print()
        if newline == "":
            newline = line
        outtxt += newline
    #print("D... output:______________________________________________\n")
    #print(outtxt)
    if not printit:
        return ""
    return outtxt



#========================================================MAIN======
#========================================================MAIN======
#========================================================MAIN======
if __name__ == "__main__":
    #Fire(replace_keys )
    Fire( subst_pass )
