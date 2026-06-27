#--- coding=utf-8
#--- @Time: 20230410
#--- Fixed tracespacing issue 20260622, yongsheng.guo@synopsys.com


import sys
import logging
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import Application

import sys,os
appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)
sys.path.append(os.path.join(appDir,"TLine"))
sys.path.append(r"C:\work\Study\Script\Ansys\quickAnalyze\FastSim")

# isIronpython = "IronPython" in sys.version
# if not isIronpython:
#     from pyLayout import Layout
#     layout = Layout()
#     layout.initDesign()
#     oDesktop = layout.oDesktop

oDesktop = None
Module = sys.modules['__main__']
if hasattr(Module, "oDesktop"):
    oDesktop = getattr(Module, "oDesktop")
else:
    from pyLayout import Layout
    layout = Layout()
    layout.initDesign()
    oDesktop = layout.oDesktop


tempPath = oDesktop.GetTempDirectory()
sysPath = oDesktop.GetSysLibDirectory()

import MainForm
import anstDebug


#oLog = anstDebug.anstDebug('TLine', logging.DEBUG, oDesktop)
oLog = anstDebug.anstDebug('TLine', logging.INFO, oDesktop)

logger = oLog.getLogger()
#logger.debug('TempDir: ' + tempPath)
#logger.debug('SysPath: ' + sysPath)

def main():
    Application.EnableVisualStyles()
    form = MainForm.MainForm(oDesktop, sysPath)
    #form.SetSysPath(sysPath)
    form.SetDefaults()
    Application.Run(form)
    oLog.Finish()


if __name__ == "__main__":
    main()