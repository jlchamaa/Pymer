from pymer.dbO import dbO
from pymer.windowManager import windowManager
import Tkinter as tk
import datetime
import time
import random


class session(tk.Frame):
    def __init__(self,parent):
        self.winMan = windowManager(self,parent)
        self.dbObject = dbO()
        self.inspection = 15
        self.penalty = 2
        self.session = '1'
        self.solve = {}
        self.timeStruct = {}
        self.createScramble()
        self.bindKeys('main')
        self.allSessions = self.dbObject.getAllSessionNames()
        self.showSessionsAndLogs()
        self.editting = False

    def processMainInput(self, event):
        if self.editting:
            return "break"
        inputKey = event.keysym.lower()
        if inputKey == 'space':
            self.timeStruct['phase'] = 0
            self.timer()
        elif inputKey.isdigit():
            self.changeSessionNumber(None,str(inputKey))
        elif inputKey == 'q':
            self.winMan.root.quit()
        elif inputKey == 'r':
            self.bindKeys('deleteRecord')
            self.winMan.questionLabel['text'] = "Press Enter To Confirm Record Delete"
        elif inputKey == 'd':
            self.DNF()
        elif inputKey == 'p':
            self.plusTwo()
        elif inputKey == 'e':
            self.bindKeys('deleteSession')
            self.winMan.questionLabel['text'] = "Press Enter To Confirm Session Delete"
        self.showSessionsAndLogs()

    def removeSession(self,event,num):
        if num == None:
            self.dbObject.deleteSession(self.session)
        self.session = '1'
        self.showSessionsAndLogs()

    def removeRecord(self):
        self.dbObject.removeRecord(self.session)
        self.showSessionsAndLogs()

    def DNF(self):
        self.dbObject.DNF(self.session)
        self.showSessionsAndLogs()

    def plusTwo(self):
        self.dbObject.plusTwo(self.session)
        self.showSessionsAndLogs()

    def changeSessionNumber(self,event,strNumber):
        if self.session is not strNumber:
            self.session = strNumber
            self.showSessionsAndLogs()

    def timer(self):
        self.bindKeys('timer')
        phase = self.timeStruct['phase']
        if phase == 0: #setup
            self.timeStruct['start'] = time.time()
            self.timeStruct['epoch'] = self.timeStruct['start'] + self.inspection
            self.timeStruct['quit'] = False
            self.timeStruct['DNF'] = False
            self.timeStruct['phase'] = 1
            self.solve['plusTwo'] = False
            self.winMan.root.after(1,self.timer)
        elif phase == 1: #countdown
            currentTime = round(time.time() - self.timeStruct['epoch'], 2)
            self.winMan.drawTime(abs(currentTime), False)
            if currentTime > 0 :
                self.timeStruct['phase'] = 2
                self.winMan.drawTime(abs(2), False)
                self.solve['plusTwo'] = True
            self.winMan.root.after(1,self.timer)
        elif phase == 2: #plus2
            currentTime = round(time.time() - self.timeStruct['epoch'], 2)
            if currentTime >= 2:
                self.timeStruct['DNF'] = True
                self.timeStruct['phase'] = 4
            self.winMan.root.after(1,self.timer)
        elif phase == 3: #stopwatch
            currentTime = round(time.time() - self.timeStruct['epoch'], 2)
            self.winMan.drawTime(abs(currentTime), True)
            self.winMan.root.after(1,self.timer)
        elif phase  == 4: #cleanup
            currentTime = round(time.time() - self.timeStruct['epoch'], 2)
            self.winMan.drawTime(abs(currentTime), True)
            self.bindKeys('main')
            if self.timeStruct['quit']:
                self.winMan.drawTime(0, True)
                pass
            else:
                if self.solve['plusTwo']:
                    currentTime += 2
                if self.timeStruct['DNF'] :
                    currentTime = None
                    self.winMan.drawTime(0, True)
                    self.solve['plusTwo'] = False
                self.solve['time'] = currentTime
                self.solve['session'] = self.session
                self.solve['date'] = datetime.datetime.now()
                self.dbObject.writeDb(self.solve)
                self.showSessionsAndLogs()

    def processTimerInput(self,event):
        inputKey = (event.keysym).lower()
        if (inputKey == 'space'):
            phase = self.timeStruct['phase']
            if phase == 1 or phase == 2:
                self.timeStruct['epoch'] = time.time()
                self.timeStruct['phase'] = 3
            if phase == 3:
                self.timeStruct['phase'] = 4
        elif inputKey == 'escape':
            phase = self.timeStruct['phase']
            if phase == 1 or phase == 2:
                self.timeStruct['phase'] = 4
                self.timeStruct['quit'] = True


    def createScramble(self):
        scramble = ""
        directions = ["F", "U", "R", "B", "D", "L"]
        lastDir = -1
        cases = [" ", "' ", "2 "]
        i = 0
        while (i < 25):
            i += 1
            if lastDir >= 0:
                while lastDir % 3 == newDir % 3: newDir = random.randint(0, 5)
            else:
                newDir = random.randint(0, 5)
            lastDir = newDir
            scramble += directions[newDir]
            scramble += cases[random.randint(0, 2)]
        self.solve['scramble'] = scramble
        self.winMan.showScramble(scramble)

    def showSessionsAndLogs(self):
        # return code (0,carry on) (1, restart loop) (2, abort)
        try:
            self.allSessions = self.dbObject.getAllSessionNames()
            self.allSessions[self.session]  # will raise exception if invalid
            self.winMan.showSessions(self.allSessions, self.session)
            self.winMan.showLog(self.dbObject.deliverDb(self.session, 20))
            return 0
        except KeyError:
            self.dbObject.addSession(self.session, 'Session' + self.session)

    def processDelete(self,event,type):
        inputKey = (event.keysym).lower()
        if inputKey == 'return':
            if type == 'record':
                self.removeRecord()
            if type == 'session':
                self.removeSession(None,None)
        self.winMan.questionLabel['text']="Press Space to start"
        self.bindKeys('main')


    def bindKeys(self,case):
        if case == 'main':
            self.winMan.root.bind('<Key>', self.processMainInput)
        elif case == 'timer':
            self.winMan.root.bind('<Key>', self.processTimerInput)
        elif case == 'deleteRecord':
            self.winMan.root.bind('<Key>', lambda event, type='record': self.processDelete(event,type))
        elif case == 'deleteSession':
            self.winMan.root.bind('<Key>', lambda event, type='session': self.processDelete(event, type))
        else:
            x =1/0 #bind Key Case Not Handled
