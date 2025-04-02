
import os,sys
import ActiveDesktop
ActiveDesktop.getActiveDesktop()
# print("after ActiveDesktop")


appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)
sys.path.insert(0,r"C:\work\Study\Script\Ansys\quickAnalyze\FastSim") #for development


if __name__ == '__main__':

    '''sys.argv format: argvlist, exePyPath, entryFunc
    '''
    
    # print("sys.argv: %s"%sys.argv)
    entryFunc = sys.argv[-1]
    pyPath = sys.argv[-2]

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
    ActiveDesktop.release()