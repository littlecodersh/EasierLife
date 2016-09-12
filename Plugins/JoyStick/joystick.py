import time, threading

import pygame

SCAN_TIME = 1.0 / 50

class joystick(object):
    __functionDict = {'button':{}, 'axis':{}, 'hat':{}, }
    __statusDict   = {'axis':{}, 'hat':{}, }
    __joyStick     = None
    __alive        = False
    def __init__(self):
        for i in range(5): self.__statusDict['axis'][i] = 0
        for i in range(2): self.__statusDict['hat'][i] = 0
        self.mainThread = threading.Thread(target=self.__main_thread_fn)
        self.mainThread.setDaemon(True)
    def __main_thread_fn(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    self.__functionDict['button'][event.button]('down')
                elif event.type == pygame.JOYBUTTONUP:
                    self.__functionDict['button'][event.button]('up')
            for i in range(self.__joyStick.get_numaxes()):
                self.__switch_determine('axis', i,
                    self.__get_axis_status(self.__joyStick.get_axis(i)))
            hatValue = self.__joyStick.get_hat(0)
            for i in range(2): self.__switch_determine('hat', i, hatValue[i])
    def __get_axis_status(self, axisValue):
        if abs(axisValue) < .5:
            return 0
        elif axisValue < 0:
            return -1
        else:
            return 1
    def __switch_determine(self, part, number, status):
        if status != self.__statusDict[part][number]:
            if self.__statusDict[part][number] != 0:
                self.__functionDict[part].get(
                    number, lambda x: None)(0)
            if status != 0:
                self.__functionDict[part].get(
                    number, lambda x: None)(status)
            self.__statusDict[part][number] = status
    def available(self):
        return __joyStick is not None
    def init(self, stickNumber=0):
        try:
            pygame.init()
            pygame.joystick.init()
            self.__joyStick = pygame.joystick.Joystick(0)
            self.__joyStick.init()
            return True
        except pygame.error:
            return False
    def button_register(self, number):
        if not 0 <= number <= 9:
            raise Exception('No button %s.' % number)
        def _button_register(fn):
            self.__functionDict['button'][number] = fn
            return fn
        return _button_register
    def axis_register(self, number):
        if not 0 <= number <= 4:
            raise Exception('No axis %s.' % number)
        def _axis_register(fn):
            self.__functionDict['axis'][number] = fn
            return fn
        return _axis_register
    def hat_register(self, number):
        if not 0 <= number <= 1:
            raise Exception('No hat %s.' % number)
        def _hat_register(fn):
            self.__functionDict['hat'][number] = fn
            return fn
        return _hat_register
    def start(self):
        self.__alive = True
        self.mainThread.start()
    def stop(self):
        self.__alive = False
        pygame.quit()
