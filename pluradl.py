import sys, os, re
from subprocess import Popen, PIPE, STDOUT


def fail_print():
        print("usage: python pluradl.py [username] [password]")
        print("")
        print("You need to pass your Pluralsight username and password as argument")
        print("")
        print("Example:")
        print("$ python pluradl.py myUsername myPassword")
        print("")
        print("Example of download request command execution invoked internally:")
        print('$ youtube-dl --verbose --username "myUsername" --password "myPassword" \\ ')
        print('             --sleep-interval 150 -o "%(playlist_index)s-%(chapter_number)s-%(title)s-%(resolution)s.%(ext)s" \\')
        print('             "https://app.pluralsight.com/library/courses/linux-server-skills-windows-administrators"')


def _cmd_request(command, logpath, bufflen=512):
    """Create and OS command line request
    
    Arguments:
        command {str} -- Full command string
        logpath {str} -- Path to stdout/stderror log file
    
    Keyword Arguments:
        bufflen {int} -- [description] (default: {512})
    """
    os.chdir(os.path.dirname(logpath))
    print(os.path.dirname(logpath))

    from subprocess import Popen, PIPE, STDOUT
    with Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, bufsize=bufflen) as process, \
        open(logpath, 'ab', bufflen) as file:
            for line in process.stdout:
                sys.stdout.buffer.write(line)
                file.flush()
                file.write(line)
                file.flush()


def _pluradl(COURSE,DLPATH,USERNAME,PASSWORD):
    """Handling the video downloading requests for a single course
    
    Arguments:
        COURSE {str} -- Course identifier
        DLPATH {str} -- Course path
        USERNAME {str} -- Pluralsight username
        PASSWORD {str} -- Pluralsight password
    """
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
    sleep = 150 # <- Change this at your own risk.
    # # # # # # #
    
    # CMD Tool parameters - useful settings when invoking download request
    cmdtool = "youtube-dl"
    verbc = sp + "--verbose"
    usrc = sp + "--username"
    passc = sp + "--password"
    sleepc = sp + "--sleep-interval" + sp + str(sleep)
    template = qu + "%(playlist_index)s-%(chapter_number)s-%(title)s-%(resolution)s.%(ext)s" + qu
    filenamec = sp + "-o" + sp + template
    courseurlc = sp + qu + pluraurl + COURSE + qu
    
    # Command string
    dlstr1 = cmdtool + verbc
    dlstr2 = usrc + usr + passc + usrpass
    dlstr3 = sleepc + filenamec + courseurlc
    command = dlstr1 + dlstr2 + dlstr3
    
    # Command execution and logging
    logile = COURSE + ".log"
    logpath = os.path.join(coursepath,logile)
    _cmd_request(command, logpath, bufflen=512)


def _get_courses(scriptpath):
    """Parsing courselist.txt in pluradl.py script directory path
    
    Arguments:
        scriptpath {str} -- Absolute path to pluradl.py directory
    
    Returns:
        [str] -- List of course identifiers exposed by courselist.txt
    """
    # courses textfile prelocated in the same directory as this script
    filelist = "courselist.txt"
    
    # Loops the list's lines and stores it as a python list
    filepath = os.path.join(scriptpath,filelist)
    courses = []
    try:
        with open(filepath, 'r+') as file:
            for line in file.readlines():
                if re.search(r'\S', line):
                    courses.append(line.strip())
        return courses
    except FileNotFoundError:
        print("There is no courselist.txt in script path. Terminating script ...")


def main():
    """Main execution
    Using command line arguments to pass username and password.
    """

    # Script's absolute directory path
    scriptpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    # Download directory path
    dldirname = "Courses"
    DLPATH = os.path.join(scriptpath,dldirname)
    if not os.path.exists(DLPATH):
        os.mkdir(DLPATH)
    
    # Script's call arguments for username and password
    USERNAME = sys.argv[1]
    PASSWORD = sys.argv[2]
    
    # Looping through the courses determined by _get_courses() and invoke
    # download requests via youtube-dl
    courses = _get_courses(scriptpath)
    if courses:
        for COURSE in courses:
            _pluradl(COURSE,DLPATH,USERNAME,PASSWORD)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        main()
    else:
        fail_print()

