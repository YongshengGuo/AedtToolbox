#--- coding=utf-8
#--- @Author: Yongsheng.Guo@ansys.com, Henry.he@ansys.com,Yang.zhao@ansys.com
#--- @Time: 20250401



import os,sys
import time
import shutil
import re

import clr
import System
from System import Activator, Type, Array

class SIwave(object):
    
    """Base class for SIwave"""
    SIwaveVerision = "SIwave.Application"
    oApp = None  
       
    def __init__(self,path=""):
        self.path = ""
        self.dir = ""
        self._oDoc = None
        self.simList = []
        self.optionList = []
        self.siw_info_list = []
        self.netList = []
        self.comps_dict = {}
        
        #option
        self.coreNums = 40
        self.clip = True
        self.clipdistance = "5mm"
        self.netRegular = True
        self.delRLCPort = True
        self.enableHFSSRegions = False
        self.keepSxP = ''
        
        self.setPath(path)
             
    @property
    def oDoc(self):
        if self._oDoc is None:
            Module = sys.modules['__main__']
            if hasattr(Module, "oDoc"):
                self._oDoc = getattr(Module, "oDoc")
        else:
            self._oDoc = self.getoApp().GetActiveProject()
        return  self._oDoc
        
    def __del__(self):
        self._oDoc =None
        self.oApp =None
    
    def refresh(self):
        self.siw_info_list = []
        self.netList = []
        self.comps_dict = {}
    
    def open(self,path = ""):
        self._oDoc = self.getoApp().OpenProject(path) if path != "" else self.getoApp().OpenProject(self.path)
        self.getoApp().RestoreWindow()
        self.refresh()
        print("SIwave Version:{0}".format(self.getoApp().GetVersion()))
         
    def importEDB(self,edbPath):
#         self.getoApp().ScrImportEDB(edbPath)
        self._oDoc = self.getoApp().GetActiveProject()
        self.oDoc.ScrImportEDB(edbPath)
        self._oDoc = self.getoApp().GetActiveProject()
        self.getoApp().RestoreWindow()
         
    def setPath(self,path):
        if path != "":
            self.path = os.path.abspath(path)
            self.projectName = (os.path.basename(self.path)).replace(".siw","") 
            self.dir = os.path.dirname(self.path)
    
    def setOption(self,strEval):
        """ option SIwave API as string """
        eval(strEval)
        
    def addOption(self, option):
        """Add SIwave API as string:  ScrSetNumCpusToUse (4)"""
        self.optionList.append("self.oDoc."+option)
    
    def addSimList(self,simDsp):
        """ 
        PI: simName;PowerNet1 PowerNet2 ... , RefNet, Sink1 current1, [sink2 current]...  ,VRM1 Voltage1, [VRM1 Voltage1]...; PowerNet1 PowerNet2 ... 
        SI: "simName PCIE_TX2P PCIE_TX2N"   "simName net1 net2 ..... "
        """
        if type(simDsp) == str :
            self.simList+= [simDsp]
        else:
            self.simList+=simDsp
    
    def addSweep(self,startFreq,stopFreq,step_Pts,step_numPts_log):
        """ 0,10e9,10e6,"Step", 0,10e9,2000,"numPts", 0,10e9,2000,"log" """
        option = ""
        if step_numPts_log.upper() == "STEP":
            option = "ScrAppendSteppedSweep('syz',{0},{1},{2})"
        elif step_numPts_log.upper() == "NUMPTS":
            option = "ScrAppendSweep('syz',{0},{1},{2},False)"
        elif step_numPts_log.upper() == "LOG":  
            option = "ScrAppendSweep('syz',{0},{1},{2},True)"
        else:
            print("bad sweep description.... ")         
            
        self.addOption(option.format(startFreq,stopFreq,step_Pts))    

    def setCoreNums(self,coreNums):
        self.addOption("ScrSetNumCpusToUse({0})".format(coreNums))

    def setNamingConvention(self, nameConv="$NETNAME_$REFDES_$POSTERMINAL"):
        """$NETNAME_$REFDES_$POSTERMINAL"""
        self.addOption("ScrSetPortNamingConvention('{0}')".format(nameConv))
        
    def setSIwaveVerision(self,ver):
        SIwave.SIwaveVerision = ver    

    def getoApp(self):
        Module = sys.modules['__main__']
        if hasattr(Module, "oApp"):
            SIwave.oApp = getattr(Module, "oApp")
        else:
            SIwave.oApp = SIwave.oApp if SIwave.oApp else Activator.CreateInstance(Type.GetTypeFromProgID(self.SIwaveVerision))
        return SIwave.oApp
    
    def setoApp(self,oApp):
        SIwave.oApp = oApp
        self._oDoc = oApp.GetActiveProject()
    
    def getPart(self,refdes):
        if not self.comps_dict:
            self.comps_dict = dict([c.split()[::-1] for c in self.oDoc.ScrGetComponentList("rlc,integrated circuits,input/output,discrete devices")])
        return self.comps_dict[refdes]
    
    def getRegularNets(self,regNets):
        if not self.netRegular: 
            print("Not use regular")
            return regNets
        
        if len(self.netList) == 0: 
            self.netList = self.oDoc.ScrGetNetNameList()
        
        nets = []
        if type(regNets) == str:
            nets += filter(lambda x: re.match(regNets+"$",x),self.netList) 
        else:    
            for regNet in regNets:
                nets += filter(lambda x: re.match(regNet+"$",x),self.netList)  
        return nets
    

    def GetOutputArray(self):
        return clr.Reference[Array[System.Object]]()
    
    def GetOutputObject(self):
        return clr.Reference[System.Object]()
    
    def GetStringArray(self,arr):
        return Array[str](arr)    
    
    def getPinsFromComponent(self,refdes,net = '.*'):
        return self.queryInfo(refdes = refdes,net = net, out = "pin")
        
    
    #return [[part,refdes,pins,net]....]
    def queryInfo(self, part='.*',refdes='.*',pin='.*',net='.*', out = None):
        info = ('part','refdes','pin','net')
        if not self.siw_info_list:
            for each_net in self.oDoc.ScrGetNetNameList():
#                 pins=clr.Reference[Array[System.Object]]()
#                 parts=clr.Reference[Array[System.Object]]()
#                 refDesList=clr.Reference[Array[System.Object]]()
                pins,parts,refDesList=[],[],[]
                self.oDoc.ScrGetPinsOnNet(each_net, 'ANY', '', pins, parts, refDesList)
                if len(pins)>0:
                    self.siw_info_list += [[parts[i],refDesList[i],pins[i],each_net] for i in range(len(pins))]
                    
#                     self.siw_info_list += [[parts.GetValue(i),refDesList.GetValue(i),pins.GetValue(i),each_net] for i in range(pins.Length)]
        
        #match all the string ($ end of string)
        part += '$'
        refdes += '$'
        pin += '$'
        net += '$'       
        filterFun = lambda(x): re.match(part, x[0]) and re.match(refdes, x[1]) and re.match(pin, x[2]) and  re.match(net, x[3])           
        result = filter(filterFun,self.siw_info_list) 
        
        if not result: return []
        
        if out:
            #filter out
            if type(out) == str: out = [out]
            out = [x.lower() for x in out]
            result = zip(*result)
            outResult = map(lambda x:result[info.index(x)], out)
            return outResult if len(outResult)>1 else outResult[0]
        else:  
            #return [part,refdes,pins,net]
            return result
    
    
    #---PinGroup
    
    def creatPinGroupbyPins(self,refdes,pinList,pinGroupName):
        pinArray = self.GetStringArray(pinList)
        self.oDoc.ScrCreatePinGroups (self.getPart(refdes), refdes, pinArray, pinGroupName, False)
    
    def placePinGroupVoltageSource(self,voltage,netName,refNet,component):
        """ '1V',netName,refNet,U1 """
        voltageSources = [s.split()[-1] for s in self.oDoc.ScrGetComponentList("voltage sources")]
        print("V_"+netName+"_"+component,voltageSources)
        print("V_"+netName+"_"+component in voltageSources)
        if "V_"+netName+"_"+component in voltageSources:
            print("VoltageSource exist, return.: "+ "V_"+netName+"_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
            return
        
        pinGroupList = self.oDoc.ScrGetPinGroupNameList(self.getPart(component),component)
        if netName+"_group_"+component not in pinGroupList:             
            #self.oDoc.ScrCreatePinGroupByNet(self.getPart(component), component, netName, netName+"_group_"+component, False)          
            pins = Array[str](self.queryInfo(refdes=component,net= netName,out = 'pin'))
            if not pins: return   
            print("Creat PinGroup: "+ netName+"_group_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
            self.oDoc.ScrCreatePinGroups (self.getPart(component), component, pins,  netName+"_group_"+component, False)
        if refNet+"_group_"+component not in pinGroupList:             
            #self.oDoc.ScrCreatePinGroupByNet(self.getPart(component), component, refNet, refNet+"_group_"+component, False)
            pins = Array[str](self.queryInfo(refdes=component,net= refNet,out = 'pin'))
            if not pins: return 
            print("Creat PinGroup: "+ refNet+"_group_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
            self.oDoc.ScrCreatePinGroups (self.getPart(component), component, pins, refNet+"_group_"+component, False)

        print("Creat VoltageSource: "+ "V_"+netName+"_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
        self.oDoc.ScrPlaceCircuitElement("V_"+netName+"_"+component, "V_"+netName+"_"+component, 5, 1, 
           self.getPart(component), component, netName+"_group_"+component, 1, self.getPart(component), 
           component, refNet+"_group_"+component, 0, 0, 1e-6, 0, voltage.upper().replace('V', ''), 0)

    def placePinGroupCurrentSource(self,current,netName,refNet,component):
        """ '1A',netName,refNet,U1 """
        currentSources = [s.split()[-1] for s in self.oDoc.ScrGetComponentList("current sources")]
        if "I_"+netName+"_"+component in currentSources:
            print("CurrentSource exist, return.: "+ "I_"+netName+"_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
            return
        
        pinGroupList = self.oDoc.ScrGetPinGroupNameList(self.getPart(component),component)
        if netName+"_group_"+component not in pinGroupList: 
            #self.oDoc.ScrCreatePinGroupByNet(self.getPart(component), component, netName, netName+"_group_"+component, False)
            pins = Array[str](self.queryInfo(refdes=component,net= netName,out = 'pin'))
            if not pins: return  
            print("Creat PinGroup: "+ netName+"_group_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
            self.oDoc.ScrCreatePinGroups (self.getPart(component), component, pins,  netName+"_group_"+component, False)
            
        
        if refNet+"_group_"+component not in pinGroupList:             
            #self.oDoc.ScrCreatePinGroupByNet(self.getPart(component), component, refNet, refNet+"_group_"+component, False)
            pins = Array[str](self.queryInfo(refdes=component,net= refNet,out = 'pin'))
            if not pins: return 
            print("Creat PinGroup: "+ refNet+"_group_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
            self.oDoc.ScrCreatePinGroups (self.getPart(component), component, pins, refNet+"_group_"+component, False)
            
        
        print("Creat CurrentSource: "+ "I_"+netName+"_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
        self.oDoc.ScrPlaceCircuitElement("I_"+netName+"_"+component, "I_"+netName+"_"+component, 4, 1, 
           self.getPart(component), component, netName+"_group_"+component, 1, self.getPart(component), component, refNet+"_group_"+component, 0, 0, 5e7, 0, current.upper().replace('A', ''), 0)
 
    def createCurrentOnComponent(self,component,net,totalCurrent,refNet = "GND"):
        
        pins = self.queryInfo(refdes=component,net= net,out = 'pin')
        val = totalCurrent/len(pins)
        newElemList = []
        #INT circuitElementType (3 = port; 4 = current source; 5 = voltage source)
        self.oDoc.ScrPlaceCircuitElementsToNearestRefPin (4, val, self.getPart(component),component, net, self.getPart(component),component, refNet, newElemList)
        return newElemList
       
    def creatPortOnNets(self,Nets):
        #self.oDoc.ScrUnselectAll()
        self.UnselectAll()
        for net in Nets : self.oDoc.ScrNetSetSelected(net,1)
        ports,posPins,refPins = None,None,None
        self.oDoc.ScrPlacePortsAtPinsOnSelectedNetsPinNamesOut(50,"GND",False,ports,posPins,refPins)
        if self.delRLCPort:
            self.deleteRLCPorts()

    def placePinGroupPort2(self,refz,netName,refNet,component):
        pinGroupList = self.oDoc.ScrGetPinGroupNameList(self.getPart(component),component)
        if netName+"_group_"+component not in pinGroupList:             
            #self.oDoc.ScrCreatePinGroupByNet(self.getPart(component), component, netName, netName+"_group_"+component, False)
            pins = Array[str](self.queryInfo(refdes=component,net= netName,out = 'pin'))
            if not pins: return   
            print("Creat PinGroup: "+ netName+"_group_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
            self.oDoc.ScrCreatePinGroups (self.getPart(component), component, pins,  netName+"_group_"+component, False)
        if refNet+"_group_"+component not in pinGroupList:             
            #self.oDoc.ScrCreatePinGroupByNet(self.getPart(component), component, refNet, refNet+"_group_"+component, False) 
            pins = Array[str](self.queryInfo(refdes=component,net= refNet,out = 'pin'))
            if not pins: return   
            print("Creat PinGroup: "+ refNet+"_group_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
            self.oDoc.ScrCreatePinGroups (self.getPart(component), component, pins,  refNet+"_group_"+component, False)  
        print("placePinGroupPort: "+ "P_"+netName+"_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
        rst = self.oDoc.ScrPlaceCircuitElement("P_"+netName+"_"+component, "P_"+netName+"_"+component, 3, 1, 
            self.getPart(component), component, netName+"_group_"+component, 1, self.getPart(component), component, refNet+"_group_"+component, 0, 0, 0, refz, 0, 0)

        if not rst:
            print("Error in creat PinGroupPort: "+ "P_"+netName+"_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))

    def placePinGroupPort(self,refz,netName,refNet,component):
        pinGroupList = self.oDoc.ScrGetPinGroupNameList(self.getPart(component),component)
        posGroup = netName+"_group_"+component
        refGroup = refNet +"_group_"+component
        if posGroup not in pinGroupList: 
            self.oDoc.ScrCreatePinGroupByNet(self.getPart(component), component, netName, posGroup, False)
            print("Creat PinGroup: "+ posGroup + time.strftime("  %Y-%m-%d %H:%M:%S"))
        if refGroup not in pinGroupList: 
            self.oDoc.ScrCreatePinGroupByNet(self.getPart(component), component, refNet, refGroup, False)
            print("Creat PinGroup: "+ refGroup + time.strftime("  %Y-%m-%d %H:%M:%S"))
        
        print("Creat PinGroupPort: "+ "P_"+netName+"_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))
        rst = self.oDoc.ScrPlaceCircuitElement("P_"+netName+"_"+component, "P_"+netName+"_"+component, 3, 1, 
           self.getPart(component), component, posGroup, 1, self.getPart(component), component, refGroup, 0, 0, 0, refz, 0, 0)
        
        if not rst:
            print("Error in creat PinGroupPort: "+ "P_"+netName+"_"+component + time.strftime("  %Y-%m-%d %H:%M:%S"))


    def placePinGroupVoltageSourcebyPinList(self,refdes,posList,neglist,voltage = 1,portName = None):
        """posList"""
        if not portName:
            portName = posList[0]
        else:
            posGroupName = "pos_" + portName
            negGroupName = "neg_" + portName    
                        
        self.creatPinGroupbyPins(refdes, posList, posGroupName)
        self.creatPinGroupbyPins(refdes, neglist, negGroupName)
        print("Creat VoltageSource: "+ portName + time.strftime("  %Y-%m-%d %H:%M:%S"))
        self.oDoc.ScrPlaceCircuitElement(portName, portName, 5, 1, 
        self.getPart(refdes), refdes, posGroupName, 1, self.getPart(refdes), refdes, negGroupName, 0, 0, 1e-6, 0, voltage.upper().replace('V', ''), 0)

    def placePinGroupCurrentSourcebyPinList(self,refdes,posList,neglist,current = 1,portName = None):
        """posList"""
        if not portName:
            portName = posList[0]
        else:
            posGroupName = "pos_" + portName
            negGroupName = "neg_" + portName    
                        
        self.creatPinGroupbyPins(refdes, posList, posGroupName)
        self.creatPinGroupbyPins(refdes, neglist, negGroupName)
        print("Creat CurrentSource: "+ portName + time.strftime("  %Y-%m-%d %H:%M:%S"))
        self.oDoc.ScrPlaceCircuitElement(portName, portName, 4, 1, 
        self.getPart(refdes), refdes, posGroupName, 1, self.getPart(refdes), refdes, negGroupName, 0, 0, 5e7, 0, current.upper().replace('A', ''), 0)


    def placePinGroupPortbyPinList(self,refdes,posList,neglist,refz = 50,portName = None):
        """posList"""
        if not portName:
            portName = posList[0]
        else:
            posGroupName = "pos_" + portName
            negGroupName = "neg_" + portName    
                        
        self.creatPinGroupbyPins(refdes, posList, posGroupName)
        self.creatPinGroupbyPins(refdes, neglist, negGroupName)
        self.oDoc.ScrPlaceCircuitElement("P_"+refdes+"_"+portName, "P_"+refdes+"_"+portName, 3, 1, 
        self.getPart(refdes), refdes, posGroupName, 1, self.getPart(refdes), refdes, negGroupName, 0, 0, 0, refz, 0, 0)
           
           
           
    #---Via
    
    def setAllViasPlatingRatio(self,ratio=0.2):
        oDoc = self.oDoc
        padstacks = oDoc.ScrGetPadstackNameList()
        for pad in padstacks:
            oDoc.ScrSetPadstackViaPlatingRatio(pad, 0.2)
    
    #---Source       
    def disableAllSource(self):
        for ckt in self.oDoc.ScrGetComponentList("current sources"): self.oDoc.ScrActivateCktElem(ckt.split()[-1],"csource",0)
        for ckt in self.oDoc.ScrGetComponentList("voltage sources"): self.oDoc.ScrActivateCktElem(ckt.split()[-1],"vsource",0)
        
    def deleteAllSource(self):
        for ckt in self.oDoc.ScrGetComponentList("current sources"): self.oDoc.ScrDeleteCktElem(ckt.split()[-1])
        for ckt in self.oDoc.ScrGetComponentList("voltage sources"): self.oDoc.ScrDeleteCktElem(ckt.split()[-1])

    def disableAllPorts(self):
        for ckt in self.oDoc.ScrGetComponentList("ports"): self.oDoc.ScrActivateCktElem(ckt.split()[-1],"port",0)

    def deleteAllPorts(self):
        for ckt in self.oDoc.ScrGetComponentList("ports"): self.oDoc.ScrDeleteCktElem(ckt.split()[-1])

    def deleteRLCPorts(self):
        ports = self.oDoc.ScrGetComponentList("ports")
        for port in ports:
            if re.match(r'^[RLC][0-9]+$',port.split('_')[-2]):
                self.oDoc.ScrDeleteCktElem(port.split()[-1])   
                print("delete rlc port:" + port)
    
    def UnselectAll(self):
        try:
            self.oDoc.ScrUnselectAll()
        except:
            for net in self.oDoc.ScrGetNetNameList() : 
                self.oDoc.ScrNetSetSelected(net,0)
    
    def deleteNets(self,netList):
        if len(netList)>0:
            #netList = System.Collections.Generic.List[str](netList)
            print("del netlist:",netList)
            netList = System.Array[str](netList)
            self.oDoc.ScrDeleteNets(netList)
#             for net in netList:
#                 self.oDoc.ScrDeleteNet(net)
    def deleteCompoment(self,refdes):
        try:
            self.oDoc.ScrDeleteCktElem(refdes)
        except:
            print("Componet could not delete: %s"%refdes)
    
    def clearSimNets(self,keepNetList,keepPwr = True):
        netList = self.oDoc.ScrGetNetNameList()
        delNetList = filter(lambda x:x not in keepNetList, netList)
        if keepPwr:
            pwrNetList = self.oDoc.ScrGetPwrGndNetNameList()
            delNetList = filter(lambda x:x not in pwrNetList, delNetList)
        self.deleteNets(delNetList)
    
    def testGetNets(self):
        self.open(self.path)
        for sim in self.simList:
            simDsp = sim.split()
            simName = "SYZ_"+ simDsp[0]
            Nets = self.getRegularNets(simDsp[1:])
            if len(Nets) == 0:
                print("Error get nets " + simName)
            else:
                print(simName,Nets)
                
        self.oDoc.ScrCloseProject()    
    
    def clipDesign(self,Nets,cutType = 0):
        #for net in self.oDoc.ScrGetNetNameList() : self.oDoc.ScrNetSetSelected(net,0)
        #self.oDoc.ScrUnselectAll()
        self.UnselectAll()
        for net in Nets : self.oDoc.ScrNetSetSelected(net,1)
        self.oDoc.ScrClipDesignAroundNets(Array[str](Nets),self.clipdistance,True,cutType,True,False) 
        # 0 : Cut traces which cross the boundary
        # 1 : Include all traces that overlap the extent
        # 2 : Include only traces which are completely inside the extent
            
    def configSim(self):
        #default setting
        self.oDoc.ScrSetSyzInterpSweep(True)     
        self.oDoc.ScrSetNumCpusToUse(self.coreNums)       
        self.deleteAllPorts()
        #self.oDoc.ScrSetPortNamingConvention("$NETNAME_$REFDES_$POSTERMINAL")
        #self.oDoc.ScrSetPortNamingConvention("$NETNAME_$REFDES")
        #self.oDoc.ScrAppendSteppedSweep('syz', 0, 20e9, 20e6) #sweep form 0 to 20Ghz, step 20Mhz     
        self.oDoc.ScrClearAllSweeps("syz")
        map(self.setOption,self.optionList)    
     
    #solution
    def existSolution(self,solutionNane):
        rstDir = self.path[:-4]+".siwaveresults"
        if not os.path.exists(rstDir):
            return False
        
        solutionFile = os.path.join(rstDir,os.path.basename(self.path)[:-4]+".asol")
        if not os.path.exists(solutionFile):
            return False
        
        with open(solutionFile,"r") as f:
            txt = f.read()
            f.close()
        
        regx = re.compile(r"\$begin '(.*?)'[^\$]+DiskName=[^\$]+TimeStamp=[^\$]+\$end")
        solutions = regx.findall(txt,re.DOTALL)
        if solutionNane in solutions:
            return True
        else:
            return False
     
     
    def exportConnection(self,path): 
        #return [part,refdes,pins,net]
        with open(path,'w+') as f:
            f.write("\n".join(self.queryInfo()))        
            f.close()
        
    def run(self,simNets):
        pass    
    
    def runAllNoBreak(self):
        for sim in self.simList:
            try:
                self.run(sim)
            except:
                print("some error in doing analysis: " +sim)
          
    def runAll(self):
        map(self.run,self.simList)
        
    def runBatchMode(self, run = True, execstr = ""):
        """if run = False, only generate files"""
        batch_list = map(lambda simNets:self.run(simNets, batch=True), self.simList)
        batch_str = r'SET siwave_path= "C:\Program Files\AnsysEM\AnsysEM19.2\Win64"' + "\n" + "".join(batch_list) + "pause"        
        batName = self.__class__.__name__ + ".bat"
        execName = self.__class__.__name__ + ".exec"
        open(os.path.join(self.dir,batName),'w+').write(batch_str)
        open(os.path.join(self.dir,execName),'w+').write(execstr)
        if run:
            os.system(os.path.join(self.dir,batName)+ " " + os.path.join(self.dir,execName))
            
    def exportDCReport(self,powerNets,simName):
        netxml =  "\n".join(map(lambda s:"<net><net_name>{0}</net_name><visible>1</visible></net>".format(s),powerNets))    
        xmlContent = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?><dc_plot_filters><nets>\n{0}</nets></dc_plot_filters>""".format(netxml)
        fo = open(simName+".xml","w+")
        fo.write(xmlContent)
        fo.close()
        self.oDoc.ScrExportDcSimReportOptions(True,simName+".xml")
        self.oDoc.ScrExportDcSimReport(simName,"white",simName+".htm")
        self.oDoc.ScrExportElementData(simName,"via_"+simName+".csv","Vias")
        self.oDoc.ScrExportElementData(simName,"CurrentSources_"+simName+".csv","Current Sources")  
        self.oDoc.ScrExportElementData(simName,"VoltageSources_"+simName+".csv","Voltage Sources")
            
    def runDCsim(self,simDsp,distributed = False,clip = None,deleteSource=True,clearNets = True):
        #'V1P5_S3, V1P5_S3 GND U2A5 10A, V1P5_S3 GND U1B5 1V'
        #self.setPath(self.oDoc.GetFilePath())
        simconfigs= simDsp.split(',')
        simName = "DC_"+ simconfigs[0]
        
        if self.existSolution(simName):
            print("%s exist, return."%simName)
            self.oDoc.ScrCloseProject()
            return
        
        if deleteSource:
            self.deleteAllSource() 
        self.configSim()
        #self.setAllViasPlatingRatio(0.2)

        powerNets = []
        refNets = []
        for config in simconfigs[1:]:
            VS_comp= config.split()
            if len(VS_comp) == 4:
                powerNet = VS_comp[0]
                refNet = VS_comp[1]
                comp = VS_comp[2]
                source = VS_comp[3]
                powerNets.append(powerNet)
                refNets.append(refNet)
            elif len(VS_comp) == 2:
                comp = VS_comp[0]
                source = VS_comp[1] 
            elif len(VS_comp) == 1:
                powerNets.append(VS_comp[0])
                continue
            else:
                print("skip config : " + config) 
                continue
                
            if "V" in source.upper():
                self.placePinGroupVoltageSource(source,powerNet,refNet,comp)
            elif "A" in source.upper():
                totalCurrent = float(source.upper().replace('A', ''))
                if distributed:
                    print("place Distributed Currents: %s %s %s"%(comp, powerNet, source))
                    self.placeDistributedCurrents(comp, powerNet, totalCurrent, refNet)
                else:
                    print("place pinGroup Currents: %s %s %s"%(comp, powerNet, source))
                    self.placePinGroupCurrentSource(source,powerNet,refNet,comp)
            else:
                print("source error: " + simDsp)
        powerNets = list(set(powerNets))
        refNets = list(set(refNets))
        if clip is not None:
            print("Clip project: "+ simName + time.strftime("  %Y-%m-%d %H:%M:%S"))
            self.clipdistance = clip
            self.clipDesign(powerNets)
                    
        if clearNets:
            self.clearSimNets(powerNets+ refNets, keepPwr=False)
            for item in self.oDoc.ScrGetComponentList("rlc,integrated circuits,input/output,discrete devices"):
                part,refdes = item.split()
                comp = Component(refdes,siwBase=self)
                if len(comp.pins)<2:
                    print("delete invalid components: %s"%refdes)
                    self.deleteCompoment(refdes)

        self.UnselectAll()
        print("Select net for simulation: "+ ",".join(powerNets+ refNets) + time.strftime("  %Y-%m-%d %H:%M:%S"))
        for net in powerNets+ refNets: 
            self.oDoc.ScrNetSetSelected(net,1)
        
        #export power data
        self.oDoc.ScrExportDcPowerDataToIcepak(True)
        print("Save project: "+ simName + time.strftime("  %Y-%m-%d %H:%M:%S"))
        self.oDoc.Save()      
        print("Start simulation: " + simName + time.strftime("  %Y-%m-%d %H:%M:%S"))
        runsim = self.oDoc.ScrRunSimulation("dc", simName)
        if runsim:
            print(simName + ": Some error in simulation...... ")

        else:        
            print("Export Report: " + simName + time.strftime("  %Y-%m-%d %H:%M:%S"))
            try:
                self.exportDCReport(powerNets,simName) 
            except:
                print(simName + ": Export Report error...... ")
        self.oDoc.Save()
        self.oDoc.ScrCloseProject()
        print("Close simulation: "  + simName+ time.strftime("  %Y-%m-%d %H:%M:%S"))
    
    def runIcepak_back(self,DCSim):
        convection = True
        forcedAir = False
        topOrAmbientTempC = 25
        topOrOverallFlowDir = "+Y"
        topOrOverallFlowSpeed = 0
        bottomTempC = 25
        bottomFlowDir  = "+Y"
        bottomFlowSpeed = 0
        gravVecX = 0
        gravVecY = 0
        gravVecZ = -10
        self.oDoc.ScrSetIcepakThermalEnv(convection,forcedAir,topOrAmbientTempC,topOrOverallFlowDir,topOrOverallFlowSpeed,
                                         bottomTempC,bottomFlowDir,bottomFlowSpeed,gravVecX,gravVecY,gravVecZ)
        
        #basic, detailed, exhaustive
        #oDoc.ScrSetIcepakMeshingDetail('basic')
        print("Run simulation:" + 'Icepak_'+DCSim)
        runsim = self.oDoc.ScrRunIcepakSimulation('Icepak_'+DCSim, DCSim)
        
        if runsim:
            print('Icepak_'+DCSim + ": Some error in simulation...... ")

        else:        
            print("Export Icapak Report: " + 'Icepak_'+DCSim + time.strftime("  %Y-%m-%d %H:%M:%S"))
            try:
                htmPah = self.oDoc.GetFilePath()[:-4]+"_Temperature.htm"
                self.oDoc.ScrExportIcepakSimReport('Icepak_'+DCSim, htmPah)
            except:
                print('Icepak_'+DCSim + ": Export Report error...... ")
                
    def runIcepak(self,DCSim):
        """
        Natural convertion PCB only 
        """
        print("Running Icepak from SIwave ...")
        options = {
            "ICEPAK_SETUP_NAME":'"%s"'%"IcepakSim",
            "ICEPAK_DC_SIM_NAME":'"%s"'%"DCSim",
            "ICEPAK_USE_DC_CONV_LOOP":"0",
            "ICEPAK_MESH_FIDELITY":"1",
            "ICEPAK_FLOW_STYLE":"1",  #1: convertion PCB +component(optional), 3: Natural conduction PCB only 
            "ICEPAK_GRAV_X":"0.0",
            "ICEPAK_GRAV_Y":"0.0",
            "ICEPAK_GRAV_Z":"-9.8",
            "ICEPAK_AMBIENT_TEMP":"20"
            }
        
        DCName = DCSim
        IcepakName = DCName + "_icepak"
        if self.existSolution(IcepakName):
            print("%s exist, return."%IcepakName)
            self.oDoc.ScrCloseProject()
            return
        
        options["ICEPAK_DC_SIM_NAME"] = '"%s"'%DCName
        options["ICEPAK_SETUP_NAME"] = '"%s"'%IcepakName
        siwPath = self.path
        with open(siwPath,"r") as f:
            txt = f.read()
            f.close()
            
        lines = txt.split("\n")
        for i in range(len(lines)):
            if not lines[i].strip():
                #space line
                continue
            x = lines[i].split()
            if x[0] in options:
                print(x[0],options[x[0]])
                lines[i] = " ".join([x[0],options[x[0]]])
                
        #Icepak set Component power to 0
        B_POWER_DISSIPATION = 0
        pwrd = []
        for i in range(len(lines)):
            if not lines[i].strip():
                #space line
                continue
            x = lines[i].split()
            if "B_POWER_DISSIPATION" in x[0]:
                B_POWER_DISSIPATION = 1
                continue
            elif "E_POWER_DISSIPATION" in x[0]:
                B_POWER_DISSIPATION = 0
                continue
                break
            else:
                pass
            
            if B_POWER_DISSIPATION == 0:
                continue
            print("not include %s power:"%x[1])
            x[3] = "0"
            lines[i] = " ".join(x)
            pwrd.append(x)
                
        txt = "\n".join(lines)
        with open(siwPath,"w+") as f:
            txt = f.write(txt)
            f.close()
            
            
        temp = r'<Part GenHeatSink="0" HeightInMM="{7}" IncludeInModel="0" LengthInMM="{5}" PartName={0} PowerDissipation="0" RefDes={1} WidthInMM="{6}"/>'
        #DR50017-P086CC_1_SCONN288_DDR5" "JE2" 0 0 0 5.598668 127.169926 2.250000
        xml = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>' + "\n"
        xml += '<Parts>' + "\n"
        xml += "\n".join([temp.format(*p) for p in pwrd])
        xml += r'</Parts>'
        #<Part GenHeatSink="0" HeightInMM="2.25" IncludeInModel="0" LengthInMM="54.7324" PartName="13903877-00" PowerDissipation="0" RefDes="U1" WidthInMM="75.4344"/>
                
        
        pwrdPath = siwPath[:-4]+".pwrd"
        with open(pwrdPath,"w+") as f:
            txt = f.write(xml)
            f.close()
            
        #run Icepak
        print("Run simulation:" + IcepakName)
        self.open(siwPath)
        pwrdPath = siwPath[:-4]+".pwrd"
        self.oDoc.ScrSetNumCpusToUse(self.coreNums)
        self.oDoc.ScrSetIcepakComponentConfig(pwrdPath)
        runsim = self.oDoc.ScrRunIcepakSimulation(IcepakName, DCName)
        if runsim:
            print('Icepak_'+IcepakName + ": Some error in simulation...... ")

        else:        
            print("Export Icapak Report: " + IcepakName + time.strftime("  %Y-%m-%d %H:%M:%S"))
            try:
                htmPah = siwPath[:-4]+"_Temperature.htm"
                self.oDoc.ScrExportIcepakSimReport(IcepakName, htmPah)
            except:
                print(IcepakName + ": Export Report error...... ")
    
        self.oDoc.Save()
        self.oDoc.ScrCloseProject()
        print("Close simulation: "  + IcepakName+ time.strftime("  %Y-%m-%d %H:%M:%S"))
    
    def runPDN(self, simDsp,clip = None,distributed = False,clearNets = True):
        #'V1P5_S3, V1P5_S3 GND U2A5 10A, V1P5_S3 GND U1B5 1V'
        simconfigs= simDsp.split(',')
        simName = "PDN_"+ simconfigs[0]

        if self.existSolution(simName):
            print("%s exist, return."%simName)
            self.oDoc.ScrCloseProject()
            return
        
        #configSim, will delete ports
        self.configSim()    

        powerNets = []
        refNets = []
        
        for config in simconfigs[1:]:
            VS_comp= config.split()
            if len(VS_comp) > 2:
                powerNet = VS_comp[0]
                refNet = VS_comp[1]
                comp = VS_comp[2]
                source = VS_comp[3]
                powerNets.append(powerNet)
                refNets.append(refNet)
            elif len(VS_comp) == 2:
                comp = VS_comp[0]
                source = VS_comp[1] 
                
            elif len(VS_comp) == 1:
                powerNets.append(VS_comp[0])
                continue
            else:
                print("skip config : " + config) 
                continue
            
            #short VRM
            self.oDoc.ScrSIwaveSyzComputeExactDcPoint(True)
            if "V" in source.upper():
                self.placePinGroupPort(0.1,powerNet,refNet,comp)
#                 self.placePinGroupRes(1e-9,powerNet,refNet,comp)
#                 self.placePinGroupVoltageSource(source,powerNet,refNet,comp)
            elif "A" in source.upper():
                if distributed:
                    print("place Distributed Ports: %s %s %s"%(comp, powerNet, source))
                    self.placeDistributedPorts(comp,powerNet,0.1,refNet)
                else:
                    print("place pinGroup Ports: %s %s %s"%(comp, powerNet, source))
                    self.placePinGroupPort(0.1,powerNet,refNet,comp)
            else:
                print("source error: " + simDsp)
            
            #self.placePinGroupPort(0.1,powerNet,refNet,comp)
            
        powerNets = list(set(powerNets))
        refNets = list(set(refNets))
        if clip is not None:
            print("Clip project: "+ simName + time.strftime("  %Y-%m-%d %H:%M:%S"))
            self.clipdistance = clip 
            self.clipDesign(powerNets)
        
        if clearNets:
            self.clearSimNets(powerNets+ refNets, keepPwr=False)
            for item in self.oDoc.ScrGetComponentList("rlc,integrated circuits,input/output,discrete devices"):
                part,refdes = item.split()
                comp = Component(refdes,siwBase=self)
                if len(comp.pins)<2:
                    print("delete invalid components: %s"%refdes)
                    self.deleteCompoment(refdes)
        
        self.UnselectAll()

        print("Select net for simulation: "+ ",".join(powerNets+ refNets) + time.strftime("  %Y-%m-%d %H:%M:%S"))
        for net in powerNets+ refNets: 
            self.oDoc.ScrNetSetSelected(net,1)

        print("Save project: "+ simName + time.strftime("  %Y-%m-%d %H:%M:%S"))
        self.oDoc.Save()   
             
        print("Start simulation: " + simName + time.strftime("  %Y-%m-%d %H:%M:%S"))
        runsim = self.oDoc.ScrRunSimulation("syz", simName)
        if runsim:
            print("Some error in simulation...... ")
        else:        
            siwPath = self.oDoc.GetFilePath()
            self.oDoc.ScrExportSyzSimToTouchstone(simName,siwPath[:-4])
            print("output SNP for: "+ siwPath + time.strftime("  %Y-%m-%d %H:%M:%S"))
            
        #Save and Close
        self.oDoc.Save()
        self.oDoc.ScrCloseProject()
        print("Close simulation: "  + simName+ time.strftime("  %Y-%m-%d %H:%M:%S"))               
    