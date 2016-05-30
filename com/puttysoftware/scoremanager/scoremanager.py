from Tkinter import *
from tkMessageBox import *
from tkSimpleDialog import *
import pickle

class Score(object):

    # Constructor
    def __init__(self, newScore=0, newName="Nobody"):
        self.score = newScore
        self.name = newName

    # Methods
    def getScore(self):
        return self.score

    def getName(self):
        return self.name

    def setScore(self, newScore):
        self.score = newScore

    def setName(self, newName):
        self.name = newName

class ScoreTable(object):

    # Constructor
    def __init__(self, length=10, customUnit=""):
        self.table = list()
        for x in range(0, length - 1):
            self.table.append(Score())
        if customUnit == None:
            self.unit = ""
        else:
            self.unit = " " + customUnit

    # Methods
    def getEntryScore(self, pos):
        return self.table[pos].getScore()

    def getEntryName(self, pos):
        return self.table[pos].getName()

    def getLength(self):
        return len(self.table)

    def getUnit(self):
        return self.unit

    def setEntryScore(self, pos, newScore):
        self.table[pos].setScore(newScore)

    def setEntryName(self, pos, newName):
        self.table[pos].setName(newName);

class SortedScoreTable(ScoreTable):

    # Constructor
    def __init__(self, length=10, ascending=True, startingScore=0, customUnit=""):
        ScoreTable.__init__(self, length, customUnit)
        self.sortOrder = ascending
        for x in range(0, len(self.table) - 1):
            self.table[x].setScore(startingScore)

    def setEntryScore(self, pos, newScore):
        pass

    def setEntryName(self, pos, newName):
        pass

    def addScore(self, newScore, newName):
        newEntry = Score(newScore, newName)
        self.table.append(newEntry)
        self.table.sort()
        if not self.sortOrder:
            self.table.reverse()
        del self.table[-1]

    def checkScore(self, newScore):
        if self.sortOrder:
            for x in range(0, len(self.table) - 1):
                if newScore > self.table[x].getScore():
                    break
            if x == len(self.table):
                return False
        else:
            for x in range(0, len(self.table) - 1):
                if newScore < self.table[x].getScore():
                    break
            if x == len(self.table):
                return False
        return True

class ScoreTableViewer(object):

    # Constants
    ENTRIES_PER_PAGE = 10
    VIEWER_STRING = "Score Table Viewer"

    # Methods
    def view(table, customTitle, unit):
        msg = ""
        title = None
        if customTitle == None or customTitle == "":
            title = ScoreTableViewer.VIEWER_STRING
        else:
            title = customTitle
        for x in range(0, table.getLength(), ScoreTableViewer.ENTRIES_PER_PAGE):
            msg = ""
            for y in range(1, ScoreTableViewer.ENTRIES_PER_PAGE):
                try:
                    msg = msg + table.getEntryName(x + y - 1) + " - " + table.getEntryScore(x + y - 1) + unit + "\n"
                except IndexError:
                    pass
            # Strip final newline character
            msg = msg.rstrip(1)
            showinfo(title, msg)

    view = staticmethod(view)

class ScoreManager(object):

    # Constants
    DID_NOT_MAKE_LIST = "You did not make the score list."
    NAME_PROMPT = "Enter a name for the score list:"

    # Constructor
    def __init__(self, length=10, sortOrder=True, startingScore=0, showFailedMessage=True, customTitle="Score Manager", customUnit=""):
        self.table = SortedScoreTable(length, sortOrder, startingScore, customUnit)
        self.name = ""
        self.displayFailMsg = showFailedMessage
        if customTitle == None or customTitle == "":
            self.title = ScoreManager.DIALOG_TITLE
        else:
            self.title = customTitle
        self.viewerTitle = customTitle

    # Methods
    def addScore(self, newScore, newName="Nobody", promptForName=True):
        success = self.table.checkScore(newScore)
        if not success:
            if self.displayFailMsg:
                showinfo(self.title, ScoreManager.DID_NOT_MAKE_LIST)
        else:
            if promptForName:
                self.name = None
                self.name = askstring(self.title, ScoreManager.NAME_PROMPT)
                if self.name != None:
                    self.table.addScore(newScore, self.name)
                else:
                    success = False
            else:
                self.table.addScore(newScore, newName)
        return success

    def checkScore(self, newScore):
        return self.table.checkScore(newScore)

    def viewTable(self):
        ScoreTableViewer.view(self.table, self.viewerTitle, self.table.getUnit())

class SavedScoreManager(ScoreManager):
    
    # Constructor
    def __init__(self, scoresFile, length=10, sortOrder=True, startingScore=0, showFailedMessage=True, customTitle="High Scores", customUnit=""):
        ScoreManager.__init__(self, length, sortOrder, startingScore, showFailedMessage, customTitle, customUnit)
        self.scoresFilename = scoresFile
        self.readScoresFile()

    # Methods
    def addScore(self, newScore, newName="Nobody", promptForName=True):
        success = ScoreManager.addScore(self, newScore, newName, promptForName)
        self.writeScoresFile()
        return success

    def readScoresFile(self):
        try:
            f = open(self.scoresFilename)
            self.table = pickle.load(f)
            f.close()
        except IOError:
            pass

    def writeScoresFile(self):
        try:
            f = open(self.scoresFilename)
            pickle.dump(self.table, f)
            f.close()
        except IOError:
            pass