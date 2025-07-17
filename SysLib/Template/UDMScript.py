#--- coding=utf-8
#--- @author: yongsheng.guo@ansys.com
#--- @Time: 20250716

''''
This program serves as an interface for initiating external UDM/UDP connections. 
Please refrain from modifying the code content as much as possible.
'''

import os,sys
UDScriptDir = os.path.join(os.environ["Temp"],"UDScript")
UDScriptFile = os.path.join(os.environ["Temp"],"UDScript","UDMScript.py")

if not os.path.exists(UDScriptFile):
    raise SystemExit("Please reset the UDM or UDP settings")


sys.path.insert(0,UDScriptDir)
from UDMScript import *