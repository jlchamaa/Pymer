import Tkinter as tk
import tkMessageBox
import ttk
import tkFont
from pymer.digits import bigDigits,bigDigitsIndexes

class windowManager(ttk.Frame):
    def __init__(self,session,parent):
        ttk.Frame.__init__(self, parent)
        self.session = session
        self.mono10 = tkFont.Font(family="Consolas", size=10)
        self.mono20 = tkFont.Font(family="Consolas", size=20)
        self.blinking = False
        self.sessionsButtonsList = []
        self.root = parent
        self.currentTime = str(27)
        self.initializeWindows()

    def initializeWindows(self):
        self.root.title("PyMer")
        self.root.resizable(False,False)
        self.grid()
        ttk.Style().configure("TFrame", background="#111")
        self.timeLabel = tk.Label(self, font = self.mono10, background='#111', foreground='#82b1ff')
        self.timeLabel.grid(row=0,column=1,columnspan=2)
        self.scrambleLabel = tk.Label(self, font = self.mono10, background='#111', foreground='#82b1ff',relief='raised')
        self.scrambleLabel.grid(row=1,column=1,columnspan=2,sticky=tk.N+tk.E+tk.W)
        self.questionLabel = tk.Label(self, font = self.mono10, background='#111', foreground='#82b1ff',relief='raised',text="Press Spacebar to start")
        self.questionLabel.grid(row=2,column=2,sticky=tk.N)
        self.logFrame = ttk.Frame(self,relief='flat')
        self.logFrame.grid(row=0,column=0,rowspan=3,sticky=tk.E)
        self.sessionFrame = ttk.Frame(self,relief='flat')
        self.sessionFrame.grid(row=2, column=1, sticky=tk.N)
        self.drawTime(0,True)
        self.createToolbox()

    def showScramble(self, scramble):
        self.scrambleLabel['text'] = scramble

    def showLog(self, dataObj):
        rowNum=20
        for i in dataObj:
            stringToWrite = "   "
            numToWrite = str(i[1]) + "."
            stringToWrite += numToWrite.ljust(5)
            time = i[0]
            if time == None:
                stringToWrite += "DNF ".rjust(8)
            else:
                mins = int(time / 60)
                sex = time % 60
                timeToWrite = ""
                if mins > 0:
                    timeToWrite += str(mins) + ":"
                    timeToWrite += "{:0>5.2f}".format(sex)
                else:
                    timeToWrite += "{0:.2f}".format(sex)
                if i[2]:
                    timeToWrite += "+"
                else:
                    timeToWrite += " "
                stringToWrite += timeToWrite.rjust(8)
            if i[3] is not None:
                stringToWrite += "   " + "{0:.2f}".format(i[3])
            labelToMake = tk.Label(self.logFrame,name=str(i[1]), font=self.mono10, background='#82b1ff', foreground='#111',bd='0')
            labelToMake['text']=stringToWrite
            labelToMake.grid(row=rowNum, column=0, sticky=tk.NE+tk.S,ipady='2.5')
            rowNum -= 1
        while rowNum > 0:
            labelToMake = tk.Label(self.logFrame, font=self.mono10, background='#82b1ff',foreground='#111', bd='0')
            labelToMake['text'] = "  "
            labelToMake.grid(row=rowNum, column=0, sticky=tk.NE + tk.SW , ipady='2.5')
            rowNum -= 1

    def createToolbox(self):
        self.toolboxFrame = ttk.Frame(self,relief='flat')
        p2 = tk.Button(self.toolboxFrame,name='p2',text='+2',relief='flat',font=self.mono10, bg='#82b1ff',bd='0',command=lambda: self.dbWrapper('p2'))
        p2.grid(row=0,column=0,padx=(1,0))
        dnf = tk.Button(self.toolboxFrame, name='dnf', text='DNF', relief='flat', font=self.mono10, bg='#82b1ff', bd='0',command = lambda: self.dbWrapper('dnf'))
        dnf.grid(row=0, column=1)
        remove = tk.Button(self.toolboxFrame, name='remove', text='X', relief='flat', font=self.mono10, bg='#82b1ff', bd='0',command=lambda: self.dbWrapper('remove'))
        remove.grid(row=0, column=2)
        self.toolboxFrame.grid(row='3',column='0',sticky=tk.N)



    def dbWrapper(self,buttonType):
        if buttonType == 'dnf':
            self.session.DNF()
        elif buttonType == 'p2':
            self.session.plusTwo()
        elif buttonType == 'remove':
            self.session.bindKeys('deleteRecord')
            self.questionLabel['text'] = "Press Enter To Confirm Record Delete"
        self.session.showSessionsAndLogs()

    def showSessions(self, names, current):
        oldWidgets = self.sessionFrame.winfo_children()
        i=1
        for num,name in sorted(names.items()):
            bg='#111'
            fg = '#82b1ff'
            if num == current:
                fg= '#111'
                bg= '#82b1ff'
            sessionNumber = tk.Label(self.sessionFrame, font=self.mono10, background=bg, foreground=fg,text="    " + str(num )+'.')
            sessionNumber.bind('<Button-1>', lambda event, num=str(num): self.session.changeSessionNumber(event,num))
            sessionNumber.grid(row=i,column=0,sticky=tk.NW)
            sessionNameEntry = tk.Entry(self.sessionFrame, font=self.mono10, background=bg, foreground=fg)
            sessionNameEntry.grid(row=i,column=1,sticky=tk.NW)
            sessionNameEntry.bind('<Button-1>', lambda event, num=str(num): self.session.changeSessionNumber(event,num))
            sessionNameEntry.bind('<FocusIn>',lambda event, widget=sessionNameEntry: self.enterEntry(event,widget))
            sessionNameEntry.bind('<Return>', lambda event, widget=sessionNameEntry, num=str(num): self.leaveEntryWithEdit(event,widget,num))
            sessionNameEntry.bind('<Escape>', lambda event, widget=sessionNameEntry: self.leaveEntryWithoutEdit(event,widget))
            sessionNameEntry.insert(0,name)
            i+=1
        for widget in oldWidgets:
            widget.destroy()

    def enterEntry(self,event,widget):
        self.session.editting = True

    def leaveEntryWithEdit(self,event,widget,num):
        widgetName = widget.get()
        self.session.dbObject.renameSession(num,widgetName)
        self.session.editting = False

    def leaveEntryWithoutEdit(self, event,widget):
        self.session.editting = False

    def drawTime(self, time, positive):
        if not positive:
            if int(time) == 3 or int(time) == 2 or int(time) == 4:
                if not self.blinking:
                    if (int(time * 10) % 10) == 2:
                        ttk.Style().configure("TFrame", background="#82b1ff")
                        self.blinking = not self.blinking
                if self.blinking:
                    if (int(time * 10) % 10) == 0:
                        ttk.Style().configure("TFrame", background="#111")
                        self.blinking = not self.blinking
            if int(time) == 1 or int(time) == 0:
                if not self.blinking:
                    if (int(time * 10) % 2) == 1:
                        ttk.Style().configure("TFrame", background="#82b1ff")
                        self.blinking = not self.blinking
                if self.blinking:
                    if (int(time * 10) % 2) == 0:
                        ttk.Style().configure("TFrame", background="#111")
                        self.blinking = not self.blinking
        if positive and self.blinking:
            ttk.Style().configure("TFrame", background="#111")
            self.blinking = not self.blinking
        digits = self.secondsToDigits(time)
        i = 0
        finalString = ""
        for digitsLine in bigDigits:
            lineToWrite = ""
            lineToWrite += self.fetchDigitChunk(digitsLine, digits['tenmins'], time > 600)  # tens place of mins
            lineToWrite += self.fetchDigitChunk(digitsLine, digits['minutes'], time > 60)  # singles of mins
            lineToWrite += self.fetchDigitChunk(digitsLine, 11, time > 60)  # add colon
            lineToWrite += self.fetchDigitChunk(digitsLine, digits['tensPlace'], time > 10)  # add tensPlace
            lineToWrite += self.fetchDigitChunk(digitsLine, digits['onesPlace'], True)  # add onesPlace
            lineToWrite += self.fetchDigitChunk(digitsLine, 10, True)  # add decimal
            lineToWrite += self.fetchDigitChunk(digitsLine, digits['tenths'], time<600)  # add tenths
            lineToWrite += self.fetchDigitChunk(digitsLine, digits['hundredths'], positive and time<60)  # add hundredths
            finalString += lineToWrite +"\n"
        self.timeLabel['text'] = finalString
        self.root.update()

    def secondsToDigits(self, time):
        timeDigits = {}
        timeDigits['tenmins'] = int(time/600)
        timeDigits['minutes'] = int(time/60) % 10
        seconds = time%60
        timeDigits['tensPlace'] = int(seconds/10)
        timeDigits['onesPlace'] = int(seconds%10)
        jiffies = round(seconds % 1,2)
        timeDigits['tenths'] = int(jiffies*10)
        timeDigits['hundredths'] = int(jiffies*100 % 10)
        return timeDigits

    def fetchDigitChunk(self, line, number, show):
        # 10 gets .   11 get :
        if show:
            return  line[bigDigitsIndexes[number]:bigDigitsIndexes[number+1]]
        else:
            return ""
