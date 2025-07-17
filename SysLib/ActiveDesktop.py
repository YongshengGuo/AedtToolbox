#--- coding=utf-8
#--- @author: yongsheng.guo@ansys.com
#--- @Time: 20240215



import os,sys
import re
import time
isIronpython = "IronPython" in sys.version

appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)
sys.path.append(os.path.join(appDir,r"..\site-packages"))


try:
    import clr
except:
    if not isIronpython:
        print("Note: for Python environment Pyaedt must install, use command: pip install pyaedt")
    exit()

try:
    sys.path.append(r'C:\work\Study\Script\cols\VSRepos\simpleWinAPI\simpleWinAPI2\bin\Release')
    clr.AddReference("tidyWinAPI")
    import tidyWinAPI
    from tidyWinAPI import winAPI
except:
    print("import tidyWinAPI error.")
    
from System import IntPtr

'''
    BOOL CALLBACK EnumWindowsProc(
      _In_ HWND   hwnd,
      _In_ LPARAM lParam
    );
'''



def getAllInstances(progID):
    #ironpython environment
    if isIronpython:
        print("Running in Ironpython environment")
        # import System.Collections.ICollection
        apps = winAPI.GetRunningInstances(progID)
        return [apps[i] for i in range(apps.Count)]
    else:
        #python environment
        print("Running in Python environment")
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        context = pythoncom.CreateBindCtx(0)
        RunningObjectTable = pythoncom.GetRunningObjectTable()
        monikiers = RunningObjectTable.EnumRunning()
        apps = []
        print("Get Runing Aedt instance ....")
        for monikier in monikiers:
            name = monikier.GetDisplayName(context, monikier)
#             print(name)
            if progID in name:
                print(name)
                obj = RunningObjectTable.GetObject(monikier)
                app = win32com.client.Dispatch(obj.QueryInterface(pythoncom.IID_IDispatch))
                apps.append(app)
            else:
                continue
        
        return apps
    
    
def GetTopWindow(hWnd=IntPtr(0)):
    '''
    要检查其子窗口的父窗口的句柄。 如果此参数为 NULL，则该函数将返回 Z 顺序顶部窗口的句柄。
    '''
    return winAPI.GetTopWindow(hWnd)


def GetWidowText(hWnd):
    return winAPI.GetWidowText(hWnd) 

def FindWindowEx(hwndParent=IntPtr(0),hwndChildAfter=None,lpszClass=None,lpszWindow=None):   
    return winAPI.FindWindowEx(hwndParent,hwndChildAfter,lpszClass,lpszWindow)

def GetWindowThreadProcessId(hWnd):
    return winAPI.GetWindowThreadProcessId(hWnd)

def getoDesktopByProcessID(processID):
    apps = getAllInstances("ElectronicsDesktop")
    if not apps:
        print("No Aedt application running ...")
        return None
    
    for app in apps:
        if app.GetProcessID() == processID:
            return app
    
    print("not found Aedt with process_id:%s"%processID)
    return None

def getSiwaveoAppByTitle(title):
    apps = getAllInstances("SIwave.Application")
    if not apps:
        print("No SIwave application running ...")
        return None
    
    for app in apps:
        if app.GetProcessID() == processID:
            return app
    
    print("not found SIwave with process_id:%s"%processID)
    return None

def getActiveDesktop():
    
    apps = getAllInstances("ElectronicsDesktop")
    if not apps:
        print("No Aedt application running ...")
        return None
    
    try:
        current_window = GetTopWindow(IntPtr(0))
        while current_window:
            window_title = GetWidowText(current_window)
            
            if window_title and "Electronics Desktop" in window_title:
                process_id = GetWindowThreadProcessId(current_window)
                for app in apps:
                    if process_id == app.GetProcessID():
                        print("Get current actived AEDT: %s"%window_title)
                        print("Aedt install Dir:%s"%app.GetExeDir())
                        
                        # 将活动桌面实例保存到主模块
                        main_module = sys.modules['__main__']
                        main_module.oDesktop = app
                        return app
            
            current_window = FindWindowEx(hwndChildAfter=current_window)
            
        return None

    except Exception as e:
        print("Error in get_active_desktop:%s"%str(e))
        return None


def release():
    module = sys.modules["__main__"]
    
    # try:
    #     pid = module.oDesktop.GetProcessID()
    #     os.kill(pid, 9)
    # except AttributeError:
    #     pass

    try:
        del module.COMUtil
    except AttributeError:
        pass

    try:
        del module.oDesktop
    except AttributeError:
        pass
    try:
        del module.pyaedt_initialized
    except AttributeError:
        pass
    try:
        del module.oAnsoftApplication
    except AttributeError:
        pass
    try:
        del module.desktop
    except AttributeError:
        pass
    try:
        del module.sDesktopinstallDirectory
    except AttributeError:
        pass
    try:
        del module.isoutsideDesktop
    except AttributeError:
        pass
    try:
        del module.AEDTVersion
    except AttributeError:
        pass
    try:
        del sys.modules["glob"]
    except:
        pass
    
    import gc
    gc.collect()

if __name__ == "__main__":
    oDesktop = getActiveDesktop()
    print(oDesktop.GetExeDir())
    pass
