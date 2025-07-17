#--- coding=utf-8
#--- @author: yongsheng.guo@ansys.com
#--- @Time: 20240621


import os,sys
import activeDesktop
oDesktop = activeDesktop.getActiveDesktop()
# print("after ActiveDesktop")

appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)

designTypeList = ("CircuitDesign", "CircuitNetlist","EMIT", "HFSS3DLayoutDesign", "HFSS","HFSS-IE", 
                  "Icepak", "Maxwell2D", "Maxwell3D", "Q2DExtractor", "Q3DExtractor", "RMxprt", "TwinBuilder")

def main():
    
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
            
        
    #String indicating the design type of the active design 
    #("Circuit Design", "Circuit Netlist","EMIT", "HFSS 3D Layout Design", "HFSS",
    # "HFSS-IE", "Icepak", "Maxwell 2D", "Maxwell 3D", "Q2D Extractor", "Q3D Extractor", "RMxprt", or "Twin Builder").

    designType = designType.replace(" ","").replace("-","")
    menuPath = "Menu/Default.xml"
    if designType in designTypeList:
        menuPath = "Menu/%s.xml"%designType
    else:
        menuPath = "Menu/Default.xml"
        
    if not os.path.exists(os.path.join(appDir,"../",menuPath)):
        print("%s Menu not exist, use default menu."%designType)
        menuPath = r"Menu/Default.xml"
        
    print(menuPath)
    activeDesktop.release()

if __name__ == '__main__':
    main()