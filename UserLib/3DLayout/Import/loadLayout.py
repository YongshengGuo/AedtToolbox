#--- coding:utf-8
#--- @Author: Yongsheng.Guo@ansys.com
#--- @Time: 2025-09-23


import sys,os
appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)
sys.path.append(r"C:\work\Study\Script\Ansys\quickAnalyze\FastSim")
# MessageBox.Show(appDir)
try:
    import pyLayout
except:
    import clr
    layoutlib = os.path.join(appDir,'pyLayout.dll')
    if os.path.exists(layoutlib):
        print("import pyLayout.dll")
        clr.AddReferenceToFileAndPath(layoutlib)
        import pyLayout
        
from pyLayout import Layout

import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import OpenFileDialog,SaveFileDialog,DialogResult,MessageBox

def openFile(fileFilter = "All files(*.*)|*.*"):
    fd = OpenFileDialog()
    fd.Filter = fileFilter 
    fd.RestoreDirectory = True
    if fd.ShowDialog() == DialogResult.OK:
        return str(fd.FileName)
    else:
        return ""


def main():
    path = openFile("All files(*.*)|*.*")
    if path:
        layout = Layout()
        layout.loadLayout(path)

        

if __name__ == '__main__':
#     test1()
    main()
    print("finished.")