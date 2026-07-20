#--- coding=utf-8
#--- @Author: Yongsheng.Guo@ansys.com
#--- @Time: 20260702

import sys,os
sys.path.append(r"C:\work\Study\Script\Ansys\quickAnalyze\FastSim")
from pyLayout import AedtToolBase,log


def main():
    tool = AedtToolBase()
    tool = tool.initDesign()
    tool.Materials.removeUnusedMaterials()
    tool.save()
    tool.Variables.removeUnusedVariables()
    log.info("Clean Variables and Materials Done!")
    
if __name__ == "__main__":
    main()