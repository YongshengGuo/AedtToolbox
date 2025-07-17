#--- coding=utf-8
#--- @author: yongsheng.guo@ansys.com
#--- @Time: 20240621


import os,sys
import activeDesktop
activeDesktop.getActiveDesktop()
# print("after ActiveDesktop")
from menuCommand import MenuCommand

appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)
sys.path.insert(0,r"C:\work\Study\Script\Ansys\quickAnalyze\FastSim") #for development



def createUDM(pyPath):
    appDirPy = os.path.dirname(pyPath)
    fileName = os.path.basename(pyPath)
    moduleName= os.path.splitext(fileName)[0]

    UDScriptDir = os.path.join(os.environ["Temp"],"UDScript")
    UDScriptFile = os.path.join(os.environ["Temp"],"UDScript","UDMScript.py")

    if not os.path.exists(UDScriptDir):
        os.makedirs(UDScriptDir, exist_ok=True)

    UDScript =(
    "import os,sys" +"\n"
    "sys.path.insert(0,'%s')"%appDirPy  +"\n"
    "from %s import *"%moduleName
    )

    with open(UDScriptFile,"w") as f:
        f.write(UDScript)
        f.close()

    menuCMD = MenuCommand.getMenuFromActiveAEDT()
    if not menuCMD.hasMenuName("UDMScript"):
        Module = sys.modules['__main__']
        if hasattr(Module, "oDesktop"):
            oDesktop = getattr(Module, "oDesktop")
        else:
            print("Error in getting Active desktop.")
            return
        designType = "NoDesign"

        if oDesktop:
            try:
                oProject = oDesktop.GetActiveProject()
                if oProject:
                    oDesign = oProject.GetActiveDesign()
                    if oDesign:
                        designType = oDesign.GetDesignType()
            except:
                print("No Active Design detected.")
                return


        designTypeList = ("CircuitDesign", "CircuitNetlist","EMIT", "HFSS3DLayoutDesign", "HFSS","HFSSIE", 
                        "Icepak", "Maxwell2D", "Maxwell3D", "Q2DExtractor", "Q3DExtractor", "RMxprt", "TwinBuilder")
        UDDesignTypeList = ("HFSS","HFSSIE","Icepak", "Maxwell3D", "Q3DExtractor")
        designType = designType.replace(" ","").replace("-","")
        if designType not in designTypeList:
            print("Design type %s not supported UDM."%designType)
            return
        UDPath = os.path.join(oDesktop.GetExeDir() ,"syslib","UserDefinedModels",designType)
        import shutil
        shutil.copy(os.path.join(appDir,"Template","UDMScript.py"), UDPath)
        menuCMD.invokedMenuByName("Draw/User Defined Model/Update Menu")
        menuCMD.updateMenu()

    menuCMD.invokedMenuByName("UDMScript")


def createUDM2(pyPath):

    Module = sys.modules['__main__']
    if hasattr(Module, "oDesktop"):
        oDesktop = getattr(Module, "oDesktop")
    else:
        print("Error in getting Active desktop.")
        return
    try:
        oProject = oDesktop.GetActiveProject()
        oDesign = oProject.GetActiveDesign()
        oEditor = oDesign.SetActiveEditor("3D Modeler")
    except:
        print("No Active Design detected.")
    
    oEditor.CreateUserDefinedModel(
        [
            "NAME:UserDefinedModelParameters",
            [
                "NAME:Definition"
            ],
            [
                "NAME:Options"
            ],
            
            "DllName:="		, os.path.basename(pyPath),
            "Library:="		, os.path.dirname(pyPath),
            "Version:="		, "2.0",
            "ConnectionID:="	, ""
        ])

def createUDP(pyPath):
    appDirPy = os.path.dirname(pyPath)
    fileName = os.path.basename(pyPath)
    moduleName= os.path.splitext(fileName)[0]

    UDScriptDir = os.path.join(os.environ["Temp"],"UDScript")
    UDScriptFile = os.path.join(os.environ["Temp"],"UDScript","UDPScript.py")

    if not os.path.exists(UDScriptDir):
        os.makedirs(UDScriptDir, exist_ok=True)

    UDScript =(
    "import os,sys" +"\n"
    "sys.path.insert(0,'%s')"%appDirPy  +"\n"
    "from %s import *"%moduleName
    )

    with open(UDScriptFile,"w") as f:
        f.write(UDScript)
        f.close()

    menuCMD = MenuCommand.getMenuFromActiveAEDT()
    if not menuCMD.hasMenuName("UDPScript"):
        Module = sys.modules['__main__']
        if hasattr(Module, "oDesktop"):
            oDesktop = getattr(Module, "oDesktop")
        else:
            print("Error in getting Active desktop.")
            return
        designType = "NoDesign"

        if oDesktop:
            try:
                oProject = oDesktop.GetActiveProject()
                if oProject:
                    oDesign = oProject.GetActiveDesign()
                    if oDesign:
                        designType = oDesign.GetDesignType()
            except:
                print("No Active Design detected.")
                return


        designTypeList = ("CircuitDesign", "CircuitNetlist","EMIT", "HFSS3DLayoutDesign", "HFSS","HFSSIE", 
                        "Icepak", "Maxwell2D", "Maxwell3D", "Q2DExtractor", "Q3DExtractor", "RMxprt", "TwinBuilder")
        UDDesignTypeList = ("HFSS","HFSSIE","Icepak", "Maxwell3D", "Q3DExtractor")
        designType = designType.replace(" ","").replace("-","")
        if designType not in designTypeList:
            print("Design type %s not supported UDM."%designType)
            return
        UDPath = os.path.join(oDesktop.GetExeDir() ,"syslib","UserDefinedPrimitives")
        import shutil
        shutil.copy(os.path.join(appDir,"Template","UDPScript.py"), UDPath)
        menuCMD.invokedMenuByName("Draw/User Defined Primitive/Update Menu")
        menuCMD.updateMenu()
        
    menuCMD.invokedMenuByName("UDMScript")

def createUDO(pyPath):
    pass

def main():
    '''sys.argv format: argvlist, exePyPath, entryFunc
    '''
    # print("sys.argv: %s"%sys.argv)
    entryFunc = sys.argv[-1]
    pyPath = sys.argv[-2]
    # argvlist = sys.argv[1:-2]

    if entryFunc:
        if entryFunc.upper() == "$UDM":
            createUDM(pyPath)
            return
        elif entryFunc.upper() == "$UDP":
            createUDP(pyPath)
            return
        elif entryFunc.upper() == "$UDO":
            createUDO(pyPath)
            return
        else:
            pass

    sys.argv = sys.argv[:-2]
    sys.argv[0] = pyPath #change to user python file
    appDirPy = os.path.dirname(pyPath)
    fileName = os.path.basename(pyPath)
    moduleName= os.path.splitext(fileName)[0]
#     print(pyPath,moduleName,entryFunc)
    print("Run script: %s"%pyPath)
    sys.path.insert(0,appDirPy)
    module = __import__(moduleName, globals(), locals())
    mainFunc = getattr(module, entryFunc)
    mainFunc()
    activeDesktop.release()

if __name__ == '__main__':
    main()
    
