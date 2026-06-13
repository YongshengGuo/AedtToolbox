#--- coding=utf-8
#--- @Author: Yongsheng.Guo@ansys.com
#--- @Time: 20230410


import os,sys,re
import importlib
import shutil
import time

# import clr
from .common.common import log


# from .options import options

#log is a globle variable
from .common import common
from .common.common import *



'''初始化oDesktop对象

- 如果已经存在oDesktop对象，则直接返回oDesktop对象，比如已经初始化过oDesktop或者从AEDT启动脚本
- 当不存在oDesktop对象时，根据version 或者 installDir 返回oDesktop对象，同时打开AEDT窗口
- version和installDir都不指定时，会尝试启动最新版本的AEDT
- version和installDir都指定时， version优先级 高于 installDir

Examples:
    >>> oDesktop = initializeDesktop()
    打开最新版本AEDT,返回oDesktop对象
    >>> oDesktop = initializeDesktop(version = "Ansoft.ElectronicsDesktop.2013.1")
    打开版本 AEDT 2013R1

'''



# from .common.common import *

isIronpython = "IronPython" in sys.version
isPython = not isIronpython
is_linux = "posix" in os.name

def initializeDesktop(version=None, installDir=None, nonGraphical = False,newDesktop=False):
    '''
    initializeDesktop'''
    #"2021.1"
    Module = sys.modules['__main__']
    if hasattr(Module, "oDesktop"):
        oDesktop = getattr(Module, "oDesktop")
        return oDesktop
    else:
        oDesktop = None
    
    aedtInstallDir = None
    #set installDir
    # if oDesktop:
    #     aedtInstallDir = oDesktop.GetExeDir()
    if installDir:
        aedtInstallDir = os.path.abspath(installDir) #installDir.strip("/").strip("\\")
        if not os.path.exists(aedtInstallDir):
            log.exception("AEDT Install Path not found: %s"%aedtInstallDir)
        
#         print("AEDT InstallDir: %s"%aedtInstallDir)
    else:
        #environ ANSYSEM_ROOTxxx, set installDir from version
        
        verEnv = None
        if version:
            ver = version.replace(".", "")[-3:]
            verEnv = "ANSYSEM_ROOT%s" % ver
            
            if verEnv in os.environ:
                aedtInstallDir = os.environ[verEnv] 
        
        if aedtInstallDir:
            os.environ["ANSYSEM_ROOT"] = aedtInstallDir
        elif "ANSYSEM_ROOT" in os.environ and os.environ["ANSYSEM_ROOT"].strip():
            aedtInstallDir = os.environ["ANSYSEM_ROOT"]
        else:
            ANSYSEM_ROOTs = list(
                filter(lambda x: "ANSYSEM_ROOT" in x, os.environ))
            if ANSYSEM_ROOTs:
                log.debug("Try to initialize Desktop in latest version")
                ANSYSEM_ROOTs.sort(key=lambda x: x[-3:])
                aedtInstallDir = os.environ[ANSYSEM_ROOTs[-1]]
         
    if aedtInstallDir: 
        print("AEDT InstallDir: %s"%aedtInstallDir)
    else:
        log.exception("please set environ ANSYSEM_ROOT=Ansys EM install path...")
    
    
    sys.path.insert(0,aedtInstallDir)
    sys.path.insert(0,os.path.join(aedtInstallDir, 'PythonFiles', 'DesktopPlugin'))
    
#     #path for UDM,UDP
#     sys.path.insert(0,os.path.join(aedtInstallDir,r"syslib\UserDefinedModels\Lib"))
#     sys.path.insert(0,os.path.join(aedtInstallDir,r"PythonFiles\Geometry3DPlugin"))
#     sys.path.insert(0,os.path.join(aedtInstallDir,r"syslib\ACT\ATKDesign\Lib\UDMScript"))
#     #clr.AddReference("Ansys.Ansoft.Geometry3DPluginDotNet")
# 
    os.environ["ANSYS_OADIR"] = os.path.join(aedtInstallDir,'common','oa')
    os.environ["DesktopPluginPyAEDT"] = os.path.join(aedtInstallDir,'PythonFiles','DesktopPlugin')
    if aedtInstallDir not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] = aedtInstallDir + os.pathsep + os.environ["PATH"] 
    
    #for linux edpapp
    if is_linux:
        ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
        os.environ["LD_LIBRARY_PATH"] = os.pathsep.join([
            os.path.join(aedtInstallDir,r"common/mono/Linux64/lib64"),
            os.path.join(aedtInstallDir,r"Delcross"),ld_library_path])
    
    # set version from aedtInstallDir
    if not version:
        ver1 = re.split(r"[\\/]+", aedtInstallDir)[-2]
        ver2 = ver1.replace(".", "")[-3:]
        version = "Ansoft.ElectronicsDesktop.20%s.%s" % (ver2[0:2],ver2[2])
    else:
        if "Ansoft.ElectronicsDesktop" not in version:
            version = "Ansoft.ElectronicsDesktop." + version
    
    #for python
    if not isIronpython:
        #only for nonGraphical or newDesktop = true
        if nonGraphical or newDesktop or is_linux:
            desktop_plugin = None
            try:
                #only for version last then 2024R1
                log.info("load PyDesktopPlugin:%s"%(os.path.join(aedtInstallDir, 'PythonFiles', 'DesktopPlugin')))
                desktop_plugin = importlib.import_module("PyDesktopPlugin")
            except Exception:
                log.info("Not load PyDesktopPlugin in path:%s"%os.path.join(aedtInstallDir, 'PythonFiles', 'DesktopPlugin'))

            
            try:
                if desktop_plugin is None:
                    raise ImportError("PyDesktopPlugin unavailable")
                oAnsoftApp = desktop_plugin.CreateAedtApplication(NGmode=nonGraphical,alwaysNew = newDesktop)
                oDesktop = oAnsoftApp.GetAppDesktop()
            except Exception:
                log.info("PyDesktopPlugin not load, it's only for version last then 2024R1")
                oDesktop = None
        else: 
            try:
                #for python
                log.info("Intial AEDT from python win32com, AEDT Version: %s"%version)
                
                #Aedt Version: Ansoft.ElectronicsDesktop.2025.1.0, remove .0  #20250605
                splits = version.split(".")
                if len(splits)>4:
                    version = ".".join(splits[:4])
                
                import win32com.client  # @UnresolvedImport
                oAnsoftApp = win32com.client.Dispatch(version)
                oDesktop = oAnsoftApp.GetAppDesktop()
            except Exception:
                    log.info("Intial AEDT from python win32com fail, AEDT Version: %s"%version)
                    oDesktop = None
 
    if oDesktop is not None:
        #do not set oDesktop to main modules, AEDT has a chance of crashing under certain circumstances.  
        Module._oDesktop = oDesktop
        return oDesktop
    
    
    if isIronpython:
        #try to initial by clr (.net)
        try:
            #only work for ironpython
            log.info("Intial aedt desktop %s by Ironpython"%version)
    
            if is_linux:
                try:
                    clr_module = importlib.import_module("ansys.aedt.core.generic.clr_module")
                    _clr = clr_module._clr
                except Exception:
                    log.info("Make sure pyaedt have installed on linux: pip install pyaedt")
                    clr_module = importlib.import_module("ansys.aedt.core.internal.clr_module")
                    _clr = clr_module._clr
            else:
                #for windows
                import clr as _clr # @UnresolvedImport
                
            _clr.AddReference("Ansys.Ansoft.DesktopPlugin")
            _clr.AddReference("Ansys.Ansoft.CoreCOMScripting")
            _clr.AddReference("Ansys.Ansoft.PluginCoreDotNet")
    
            AnsoftCOMUtil = __import__("Ansys.Ansoft.CoreCOMScripting")
            #COMUtil = AnsoftCOMUtil.Ansoft.CoreCOMScripting.Util.COMUtil
            StandalonePyScriptWrapper = AnsoftCOMUtil.Ansoft.CoreCOMScripting.COM.StandalonePyScriptWrapper
            if "Ansoft.ElectronicsDesktop" not in version:
                version = "Ansoft.ElectronicsDesktop." + version
            log.debug(version)
            #only work for ironpython
            if nonGraphical or newDesktop:
                oAnsoftApp = StandalonePyScriptWrapper.CreateObjectNew(nonGraphical)
            else:
                oAnsoftApp = StandalonePyScriptWrapper.CreateObject(version)
                  
            oDesktop = oAnsoftApp.GetAppDesktop()
            
        except Exception:
            log.debug("Intial AEDT from clr fail.")
            oDesktop = None
        
        
    if oDesktop is not None:
        Module.oDesktop = oDesktop
        return oDesktop
        
            
    if oDesktop is None:
        raise ValueError("initialize Desktop fail")
    
    Module.oDesktop = oDesktop
    return oDesktop


def _delete_objects():
    module = sys.modules["__main__"]
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
    except Exception:
        pass
    
    import gc
    gc.collect()


def releaseDesktop():
    '''
    releaseDesktop'''
#     release_desktop(close_projects=False, close_desktop=False)
    
    try:
        _delete_objects()
        return True
    except Exception:
        return False
