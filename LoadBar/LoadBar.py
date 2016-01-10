#coding=utf8

import getpass
import thread
import time
import sys

class LoadBar(object):
    progress = (">  ", ">> ", ">>>", " >>", "  >", "   ")
    clearLine = "\r" + " " * 40 + "\r"
    message = None
    isLaunch = False
    counter = 0

    @staticmethod
    def set_message(message, needLaunch=False):
        LoadBar.message = message
        if not LoadBar.isLaunch and needLaunch:
            LoadBar.launch()

    @staticmethod
    def launch():
        LoadBar.counter = 0
        LoadBar.isLaunch = True
        thread.start_new_thread(LoadBar.draw, ())

    @staticmethod
    def stop():
        LoadBar.counter = -1
        print_line(LoadBar.clearLine, "")
        LoadBar.isLaunch = False

    @staticmethod
    def exit(code=0):
        LoadBar.stop()

    @staticmethod
    def draw():
        try:
            if not LoadBar.isLaunch:
                return

            while LoadBar.counter >= 0:
                print_line(LoadBar.clearLine, "")
                LoadBar.counter += 1
                print_line("%s : %s" % (LoadBar.progress[LoadBar.counter % len(LoadBar.progress)], LoadBar.message), "")
                time.sleep(0.3)
        except:
            pass

def LoadBarPause(fn, *args, **kwargs):
    def wrapped(*args, **kwargs):

        if not LoadBar.isLaunch:
            return fn(*args, **kwargs)

        LoadBar.stop()
        result = fn(*args, **kwargs)
        LoadBar.launch()
        return result

    return wrapped

def LoadBarStop(fn, *args, **kwargs):
    def wrapped(*args, **kwargs):

        if not LoadBar.isLaunch:
            return fn(*args, **kwargs)

        LoadBar.stop()
        result = fn(*args, **kwargs)
        return result

    return wrapped

@LoadBarPause
def get_user_credentials():
    username = raw_input("Login: ")
    password = getpass.getpass("Password: ")
    return (username, password)

@LoadBarPause
def confirm(message):
    print_line(message)
    while True:
        answer = raw_input("Yes/No: ")
        if answer.lower() in ["yes", "ye", "y"]:
            return True
        if answer.lower() in ["no", "n"]:
            return False
        print('Incorrect answer "%s", '
                       'please try again:\n' % answer)

@LoadBarPause
def log_print(message):
    print message

@LoadBarStop
def exit_message(message):
    print_line(message, "\n")

def print_line(line, endLine="\n", out=sys.stdout):
    message = line + endLine
    out.write(message)
    out.flush()

if __name__ == '__main__':
    # Equals to LoadBar.set_message('..',True) >>
    LoadBar.set_message('Demonstrate of LoadBar')
    LoadBar.launch()
    # Equals to LoadBar.set_message('..',True) <<
    time.sleep(3)

    msg = 'You have entered: ' + str(get_user_credentials())
    log_print(msg)
    # Change LoadBar message
    LoadBar.set_message('You have entered the credentials')
    time.sleep(3)

    if confirm('CONTINUE?'):
        LoadBar.set_message('You have confirmed to continue')
        time.sleep(3)
        exit_message('Process Succeed')
    else:
        exit_message('You interrupted the process')
