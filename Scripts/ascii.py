#coding=utf8
import thread, time, sys, os, platform

try:
    import termios, tty
    termios.tcgetattr, termios.tcsetattr
    import threading
    OS = 'Linux'
except (ImportError, AttributeError):
    try:
        import msvcrt
        OS = 'Windows'
    except ImportError:
        raise Exception('Mac is currently not supported')
        OS = 'Mac'
    else:
        getch = msvcrt.getch
else:
    def fn():
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        except:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            raise Exception
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    getch = fn

print 'Press any key and I will return ascii (^C to exit)'
c = getch()
while c != chr(3):
    print 'The ascii of you key: %s'%ord(c)
    c = getch()
