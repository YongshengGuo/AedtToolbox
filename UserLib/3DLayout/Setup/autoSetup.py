#coding:utf-8
#--- coding=utf-8
#--- @author: yongsheng.guo@ansys.com
#--- @Time: 20260304




import sys,os,re
appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)
sys.path.append(os.path.join(appDir,"..","site-packages"))

sys.path.append(r"C:\work\Study\Script\Ansys\quickAnalyze\FastSim")
sys.path.append(r"G:\Work\Script\Repository\quickAnalyze\FastSim")

from pyLayout import Layout,log,ExtractBase,SimConfig


log.info("HFSS Autosetup, this progrom powered by Ansys AE.")


class HfssAutoSetup(ExtractBase):
    '''
    classdocs
    '''
    def __init__(self, configDict=None, oDesktop = None):
        '''
        Constructor
        
        '''
        configPath = os.path.join(appDir,r"default.json")
        if not os.path.exists(configPath):
            log.error("Not found default.json in script dir, use global default.json")
            configPath = None
        
        super(HfssAutoSetup, self).__init__(configPath,oDesktop)
        if configDict: 
            self.setConfig(configDict)


    def setConfig(self, configDict):

        for k,v in configDict.items():
            
            #v can be dict, list, str, int, float, bool
            #v="TRUE" or "FALSE" will be converted to bool
            if isinstance(v, str):
                if v.upper() == "TRUE":
                    v = True
                elif v.upper() == "FALSE":
                    v = False
                    
            try:
                val = self._config[k]
            except:
                count = self._config.updateByKey(k,v) #update by key
                if not count:
                    log.warning("key %s not found."%k)
                else:
                    self._config.update(k,v)
            else:
                self._config[k] = v

    def run(self):
        '''
        workflow:
        
        laod PCB -> load stackup -> configComponents -> ConfigNets -> Cutout -> Port -> solveSetup -> Solve -> datas -> Post
        '''
        self.layout = Layout()
        self.layout.initDesign()

        # #---cutout pcb to reduced simulaiton time
        # self.cutoutDesign()
        # #---clear layout befor analysis
        # self.clearLayout()
        
        # #--- Config Nets
        # self.configNets()

        # #---Component models
        # self.configComponents()
    
        # #---backdrill
        # self.backdrill()
    
        # #---pin group
        # self.createPinGroup()

        # #---Create solderball
        # self.createSolderall()
        
        # #---setPadstack
        # self.setPadstack()
        
        # #---create ports
        # self.setPorts()
        
        # #---create createSource
        # self.createSource()

        # #---create ports
        # self.geometryCheckAndAutofix()
        
        #---solve frequency, sweep scope
        self.solveSetup()

        #---set airbox
        self.setAirbox()

        # #---run the simution
        # self.analyze()



#for test
if __name__ == '__main__':
    config = {
    'Setup/Name': 'HFSSAutoSetup',
    'SolutionType': 'HFSS',
    'AdaptiveFrequency': '5Ghz',
    'Order': 'Mixed',
    'DeltaS': '0.02',
    'Setup/Sweep/Name': 'sweep1',
    'SweepType': 'Interpolating',
    'InterpolatingTolerance': '0.002',
    'SweepData': 'LIN 0GHz 20GHz 0.01GHz',
    'Airbox/Options/ExtentType': 'BboxExtent',
    'Airbox/Options/AirHorExt/Ext': '1.5mm',
    'Airbox/Options/AirPosZExt/Ext': '1.5mm',
    'Airbox/Options/AirNegZExt/Ext': '1.5mm',
}
    hfssSetup = HfssAutoSetup(config)
    hfssSetup.run()
    print("Finish setup.")

    

