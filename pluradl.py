import sys, os, re
from subprocess import Popen, PIPE, STDOUT

# IMPORTANT SETTINGS TO PREVENT SPAM BLOCKING OF YOUR ACCOUNT/IP AT PLURALSIGHT #
SLEEP_INTERVAL = 150 #                                                          #
SLEEP_OFFSET = 50    #               Change this at your own risk.              #
RATE_LIMIT = "1M"    #                                                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

DLPATH, USERNAME, PASSWORD = "", "", ""

PLURAURL = "https://app.pluralsight.com/library/courses/"


def fail_print():
    """Prints out a default message to user when there is not enough arguments
    passed to pluradl.py.
    """
    print("usage: python pluradl.py [username] [password]")
    print("")
    print("You need to pass your Pluralsight username and password as argument")
    print("")
    print("Example:")
    print('$ python pluradl.py "youremail@example.com" "yourPassword"')
    print("")
    print("Example of download request command execution string:")
    print('$ youtube-dl --verbose --username "user@mymail.com" --password "myPassword" \\ ')
    print('             --sleep-interval 150 -o "%(playlist_index)s-%(chapter_number)s-%(title)s-%(resolution)s.%(ext)s" \\')
    print('             "https://app.pluralsight.com/library/courses/linux-server-skills-windows-administrators"')


def _get_courses(scriptpath):
    """Parsing courselist.txt
    
    Arguments:
        scriptpath {str} -- Absolute path to script directory
    
    Returns:
        [str] -- List of course identifiers exposed by courselist.txt
    """
    # courses textfile prelocated inside script directory
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


def _cmd_request(command, logpath):
    """Invokes an OS command line request
    
    Arguments:
        command {str} -- Full command string
        logpath {str} -- Path to stdout/stderror log file
    
    """
    os.chdir(os.path.dirname(logpath))
    print("Logging stdout/stderror to:\n" + logpath + "\n")

    with Popen(command, shell=True, stdout=PIPE, stderr=STDOUT, encoding="utf8") as process, \
        open(file=logpath, mode='wt', buffering=1) as file:
            for line in process.stdout:
                file.write(line)
                sys.stdout.write(line)


def _get_youtube_dl_cli_command(course, sleep_interval=150, sleep_offset=50, rate_limit="1M"):
    """Putting together youtube-dl CLI command used to invoke the download requests.
    
    Arguments:
        course {str} -- Course identifier
    
    Keyword Arguments:
        sleep_interval {int} -- Minimum sleep time between video downloads (default: {150})
        sleep_offset {int} -- Randomize sleep time up to minimum sleep time plus this value (default: {50})
        rate_limit {str} -- Download speed limit (use "K" or "M" ) (default: {"1M"})
    
    Returns:
        str -- youtue-dl CLI command
    """
    # Quote and space char
    # # # # # # # # # # # #
    qu = '"';  sp = ' '   # 
    # Download parameters #
    pluraurl = PLURAURL
    username = qu + USERNAME + qu
    password = qu + PASSWORD + qu
    filename_template = qu + "%(playlist_index)s-%(chapter_number)s-%(title)s-%(resolution)s.%(ext)s" + qu
    minsleep = sleep_interval
    
    # CMD Tool # # # # # #
    tool = "youtube-dl"  #
    # Flags - useful settings when invoking download request
    usr =  "--username" + sp + username
    pw =  "--password" + sp + password
    minsl =  "--sleep-interval" + sp + str(minsleep)
    maxsl =  "--max-sleep-interval" + sp + str(minsleep + sleep_offset)
    lrate = "--limit-rate" + sp + rate_limit
    fn =  "-o" + sp + filename_template
    vrb =   "--verbose"
    curl = qu + pluraurl + course + qu

    # Join command
    cmdline = [tool, usr, pw, minsl, maxsl, lrate, fn, vrb, curl]
    command = sp.join(cmdline)

    return command


def _pluradl(course, sleep_interval=150, sleep_offset=50, rate_limit="1M"):
    """Handling the video downloading requests for a single course
    
    Arguments:
        course {str} -- Course identifier
    
    Keyword Arguments:
        sleep_interval {int} -- Minimum sleep time between video downloads (default: {150})
        sleep_offset {int} -- Randomize sleep time up to minimum sleep time plus this value (default: {50})
        rate_limit {str} -- Download speed limit (use "K" or "M" ) (default: {"1M"})
    
    Returns:
        str -- youtue-dl CLI command
    """
    # OS parameters - Creates course path and sets current course directory
    coursepath = os.path.join(DLPATH,course)
    if not os.path.exists(coursepath):
        os.mkdir(coursepath)
    os.chdir(coursepath)

    command = _get_youtube_dl_cli_command(course,
                                          sleep_interval=sleep_interval,
                                          sleep_offset=sleep_offset,
                                          rate_limit=rate_limit)
    
    # Execute command and log stdout/stderror
    logile = course + ".log"
    logpath = os.path.join(coursepath,logile)
    _cmd_request(command, logpath)


def download_courses(courses, sleep_interval=150, sleep_offset=50, rate_limit="1M"):
    """Dowloading all courses listed in courselist.txt
    
    Arguments:
        courses {[type]} -- List of course ID
    
    Keyword Arguments:
        sleep_interval {int} -- Minimum sleep time between video downloads (default: {150})
        sleep_offset {int} -- Randomize sleep time up to minimum sleep time plus this value (default: {50})
        rate_limit {str} -- Download speed limit (use "K" or "M" ) (default: {"1M"})
    """
    for course in courses:
        _pluradl(course, sleep_interval=sleep_interval, sleep_offset=sleep_offset, rate_limit=rate_limit)


def main():
    """Main execution
    Using command line arguments to store username and password,
    loops through the course IDs and invoking download requests.
    """
    global DLPATH
    global USERNAME
    global PASSWORD

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

    # Looping through the courses determined by _get_courses() invoking download requests
    courses = _get_courses(scriptpath)
    if courses:
        download_courses(courses,
                         sleep_interval=SLEEP_INTERVAL,
                         sleep_offset=SLEEP_OFFSET,
                         rate_limit=RATE_LIMIT)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        main()
    else:
        fail_print()