import sys, os
from subprocess import Popen, PIPE, STDOUT

def pluradl(COURSE,DLPATH,USERNAME,PASSWORD):

    # OS parameters - Creates course path and sets current course directory
    coursepath = os.path.join(DLPATH,COURSE)
    if not os.path.exists(coursepath):
        os.mkdir(coursepath)
    os.chdir(coursepath)

    # Quote and space char
    # # # # # # # # # # # #
    qu = '"';  sp = " "   # 
    # Download parameters - important parameters for the Pluralsight webservice
    pluraurl = "https://app.pluralsight.com/library/courses/"
    usr = sp + qu + USERNAME + qu
    usrpass = sp + qu + PASSWORD + qu
    # IMPORTANT SETTING TO PREVENT SPAM BLOCKING OF YOUR ACCOUNT/IP AT PLURALSIGHT
    sleep = 120 # <- Change this at your own risk.
    # # # # # # #
    
    # CMD Tool parameters - useful settings for the download process (youtube-dl)
    cmdtool = "youtube-dl"
    verbc = sp + "--verbose"
    usrc = sp + "--username"
    passc = sp + "--password"
    sleepc = sp + "--sleep-interval" + sp + str(sleep)
    template = qu + "%(playlist_index)s-%(chapter_number)s-%(title)s-%(resolution)s.%(ext)s" + qu
    filenamec = " -o " + template
    courseurlc = sp + qu + pluraurl + COURSE + qu
    
    # Command string
    dlstr1 = cmdtool + verbc
    dlstr2 = usrc + usr + passc + usrpass
    dlstr3 = sleepc + filenamec + courseurlc
    cmd = dlstr1 + dlstr2 + dlstr3
    
    # Command execution and logging
    bufflen = 512
    logile = COURSE + ".log"
    logpath = os.path.join(coursepath,logile)
    with Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=bufflen) as process, \
        open(logpath, 'ab',bufflen) as file:
        for line in process.stdout:
            sys.stdout.buffer.write(line)
            file.flush()
            file.write(line)
            file.flush()

def courselist(scriptpath):

    # Courselist textfile prelocated in the same directory as this script
    filelist = "courselist.txt"
    
    # Loops the list's lines and stores it as a python list
    filepath = os.path.join(scriptpath,filelist)
    lines = "notNull"
    courseList = []
    with open(filepath, 'r+') as file:
        while lines != "":
            lines = file.readline()
            if lines != "":
                course = lines.split("\n")[0]
                courseList.append(course)
    return courseList

if __name__ == "__main__":

    # Script's absolute directory path
    sysfile = sys.argv[0]
    scriptabspath = os.path.abspath(sysfile)
    scriptpath = os.path.dirname(scriptabspath)
    
    # Download directory path
    dldirname = "Courses"
    DLPATH = os.path.join(scriptpath,dldirname)
    if not os.path.exists(DLPATH):
        os.mkdir(DLPATH)
    # Script's call arguments for username and password
    USERNAME = sys.argv[1]
    PASSWORD = sys.argv[2]
    
    # Looping through the courselist determined by courselist()
    courseList = courselist(scriptpath)
    for COURSE in courseList:
        pluradl(COURSE,DLPATH,USERNAME,PASSWORD)
