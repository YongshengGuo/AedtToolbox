
import os,sys
import activeDesktop
print("ActiveDesktop")
activeDesktop.getActiveDesktop()
print("after ActiveDesktop")

if __name__ == '__main__':

    '''sys.argv format: argvlist, exePyPath, entryFunc
    '''
    
    print("sys.argv: %s"%sys.argv)
    entryFunc = "main"
    pyPath = r"C:\work\Study\Script\Ansys\quickAnalyze\Yguo\BrtFrt.py"

    appDir = os.path.dirname(pyPath)
    sys.path.insert(0,appDir)
    
    fileName = os.path.basename(pyPath)
    moduleName= os.path.splitext(fileName)[0]
#     print(pyPath,moduleName,entryFunc)
    module = __import__(moduleName, globals(), locals())
    mainFunc = getattr(module, entryFunc)
    mainFunc()
