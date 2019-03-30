import sys, os
from subprocess import Popen, PIPE, STDOUT

def pluradl(COURSE,DLPATH,USERNAME,PASSWORD):

    # OS parameters - Creates course path and sets current download directory
    coursepath = os.path.join(DLPATH,COURSE)
    if not os.path.exists(coursepath):
        os.mkdir(coursepath)
    os.chdir(coursepath)
    
    # Download parameters - important parameters for the Pluralsight webservice
    pluraurl = "https://app.pluralsight.com/library/courses/"
    qu = '"'
    usr = " " + qu + USERNAME + qu
    usrpass = " " + qu + PASSWORD + qu
    # IMPORTANT SETTING TO PREVENT SPAM BLOCKING OF YOUR ACCOUNT/IP AT PLURALSIGHT
    sleep = 120 # <- Change this on your own risk.
    # # # # # # #
    
    # CMD Tool parameters - useful settings for the download process (youtube-dl)
    cmdtool = "youtube-dl"
    verbc = " --verbose"
    usrc = " --username"
    passc = " --password"
    sleepc = " --sleep-interval " + str(sleep)
    tmplc = qu + "%(playlist_index)s-%(chapter_number)s-%(title)s-%(resolution)s.%(ext)s" + qu
    filename = " -o " + tmplc
    courseurl = " " + pluraurl + COURSE
    
    # Command string
    dlstr1 = cmdtool + verbc
    dlstr2 = usrc + usr + passc + usrpass
    dlstr3 = sleepc + filename + courseurl
    dlstr = dlstr1 + dlstr2 + dlstr3
    cmd = dlstr
    
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

    # Courselist textfile prelocated in the directory of the python script
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

    # Script's absolute path
    sysfile = sys.argv[0]
    scriptabspath = os.path.abspath(sysfile)
    scriptpath = os.path.dirname(scriptabspath)
    
    # Download path
    DLPATH = os.path.join(scriptpath,"Courses")
    if not os.path.exists(DLPATH):
        os.mkdir(DLPATH)
    # Script's call arguments for username and password
    USERNAME = sys.argv[1]
    PASSWORD = sys.argv[2]
    
    # Looping through the courselist determined by courselist()
    courseList = courselist(scriptpath)
    for COURSE in courseList:
        pluradl(COURSE,DLPATH,USERNAME,PASSWORD)
