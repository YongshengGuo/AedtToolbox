#--- coding=utf-8
#--- @author: yongsheng.guo@ansys.com
#--- @Time: 20250621

import os,sys
import re
import time
isIronpython = "IronPython" in sys.version
if not isIronpython:
    print("Note: for Python environment Pyaedt must install, use command: pip install pyadedt.")
    
import clr
try:
    sys.path.append(r'C:\work\Study\Script\cols\VSRepos\simpleWinAPI\simpleWinAPI2\bin\Release')
    clr.AddReference("tidyWinAPI")
    import tidyWinAPI
    from tidyWinAPI import winAPI
except:
    print("import tidyWinAPI error.")
sys.path.insert(0,r"C:\work\Study\Script\Ansys\quickAnalyze\FastSim") #for debug    

clr.AddReference("System.Diagnostics.Process")
from System.Diagnostics import Process
from System import IntPtr

from pyLayout import ComplexDict

class MenuCommand(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.hwnd = None
        self.hMenu = None
        self.menuInfo = {}
    
    
    def GetProcessesByTitle(self, regName):
        return filter(lambda p:re.match(regName, p.MainWindowTitle),Process.GetProcesses())

    def GetProcessesByName(self,name):
        return Process.GetProcessesByName(name)

    def GetHwndFromProcessID(self,processId):
        self.hwnd = winAPI.GetMainWindowHandleFromProcessID(processId)
        return self.hwnd
    
    def findWindowEx(self,hwndParent,hwndChildAfter,lpszClass=None,lpszWindow=None):   
        return winAPI.FindWindowEx(hwndParent,hwndChildAfter,lpszClass,lpszWindow)

    def setWindowText(self, hWnd, text):
        #return winAPI.SendMessage(hWnd,winAPI.WM_SETTEXT,0,text)
        return winAPI.SetWindowText(hwnd, text)

    def getWidowText(self, hWnd):
        return winAPI.GetWidowText(hWnd) 

    def getCompText(self,hWnd, text):
        return winAPI.SendMessage(hWnd,winAPI.WM_SETTEXT,0,text)

    def setCompText(self,hComp, text):
        return winAPI.SendMessage(hComp,winAPI.WM_SETTEXT,0,text)        
        
    def getMenu(self,hwnd = None):
        hwnd = hwnd or self.hwnd  
        print(hwnd)
        if hwnd:      
            self.hMenu = winAPI.GetMenu(hwnd)            
            return self.hMenu
        else:
            print("Bad hwnd handle")
    

        
    def _getMenuIter(self,hmenu,menuDict = None):
        if not menuDict:
            menuDict = {}

        count = winAPI.GetMenuItemCount(hmenu)
        if count == -1:
            return

        for i in range(count):
            menuStr1 = winAPI.GetMenuString(hmenu,i)
            menuStr2 = menuStr1.replace("&","")
            menuStr3 = re.sub(r'\t.*','',menuStr2)
            menuID = winAPI.GetMenuItemID(hmenu,i) #弹出式菜单，就返回-1, 分隔符则返回0

            if menuID == -1:
                hSubmenu = winAPI.GetSubMenu(hmenu,i)
                menuDict[menuStr3] = self._getMenuIter(hSubmenu)
            else:
                menuDict[menuStr3] = {
                    "MenuString": menuStr1,
                    "Name": menuStr3,
                    "ID": menuID
                }
        return menuDict
    
    def getMenuInfo(self,hmenu = None):
        hmenu = hmenu or self.hMenu or self.getMenu()
        if not hmenu:
            print("Bad hmenu handle")
            return
        menuDict = self._getMenuIter(hmenu)
        self.menuInfo = ComplexDict(menuDict)
    
    def updateMenu(self):
        self.menuInfo = {}
        self.getMenuInfo()

    def invokedMenuByID(self,menuID):
        winAPI.MenuClick(self.hwnd,menuID) 
        
    def invokedMenuByName(self,name):
        if not self.menuInfo: return

        try:
            menuItem = self.menuInfo[name]
            if menuItem and "MenuString" in menuItem and "ID" in menuItem:
                self.invokedMenuByID(menuItem["ID"])
                return True
            else:
                raise Exception()
        except:
            pass

        try:
            menuItem = self.menuInfo.findNode(name)
            if menuItem and "MenuString" in menuItem and "ID" in menuItem:
                self.invokedMenuByID(menuItem["ID"])
                return True
            else:
                raise Exception()
        except:
            print("not fond menu item: " + name)
    
    def hasMenuName(self,name):
        if not self.menuInfo: return

        try:
            menuItem = self.menuInfo[name]
            if menuItem:
                return True
            else:
                raise Exception()
        except:
            pass

        try:
            menuItem = self.menuInfo.findNode(name)
            if menuItem:
                return True
            else:
                raise Exception()
        except:
            return False

        return False
    
    def invokedButtom(self,hWnd,ID):
        winAPI.SendMessage(hWnd,winAPI.WM_COMMAND,ID,None)
                
    @classmethod
    def getMenuFromProcessID(cls,processID):
        menuCmd = cls()
        hwnd = menuCmd.GetHwndFromProcessID(processID)
        hMenu = menuCmd.getMenu(hwnd)
        menuCmd.getMenuInfo(hMenu)
        return menuCmd

    @classmethod
    def getMenuFromActiveAEDT(cls):

        Module = sys.modules['__main__']
        if hasattr(Module, "oDesktop"):
            oDesktop = getattr(Module, "oDesktop")
        else:
            from activeDesktop import getActiveDesktop
            oDesktop = getActiveDesktop()

        if not oDesktop: 
            print("No active AEDT")
            return

        processID = oDesktop.GetProcessID()
        return cls.getMenuFromProcessID(processID)


if __name__ == "__main__":
    # menucmd = MenuCommand.getMenuFromActiveAEDT()
    # menucmd.menuInfo.findNode("Toolkit")
    # from activeDesktop import getActiveDesktop
    # oDesktop = getActiveDesktop()
    # print(oDesktop.GetExeDir())
    
    # menuCmd = menuCommand()
    # hwnd = menuCmd.GetHwndFromProcessID(oDesktop.GetProcessID())
    # hMenu = menuCmd.getMenu(hwnd)
    # menuInfo = menuCmd.getMenuInfo(hMenu)

    menuCmd = menuCommand()
    hwnd = menuCmd.GetHwndFromProcessID(oDesktop.GetProcessID())
    hMenu = menuCmd.getMenu(hwnd)
    menuList = menuCmd.getMenuIdList(hMenu)
    print(menuCmd.menuIdList)
    menuCmd.invokedMenuByName("EndCap")
    pass


        