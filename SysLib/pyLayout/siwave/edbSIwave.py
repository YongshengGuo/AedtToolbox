#--- coding=utf-8
#--- @Author: Yongsheng.Guo@ansys.com, Henry.he@ansys.com,Yang.zhao@ansys.com
#--- @Time: 20250403

import os,sys
from ..common.common import readCfgFile,log
from ..common.config import Config

appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)

class EdbSIwaveOptions(object):

    def __init__(self,edbapp=None):
        '''
        from ansys.aedt.core import Edb
        edbapp = Edb(edbpath=".aedb")
        '''
        self._config = None
        self.edbapp = edbapp
        self.loadOptions()

    def __getitem__(self, key):
        """
        key: str
        """
        return self.get(key)


    def __setitem__(self,key,value):
        self.set(key,value)

    def __getattr__(self,key):

        if key in ["edbapp","_config","maps"]:
            return object.__getattr__(self,key)
        else:
            log.debug("__getattr__ from _dict: %s"%key)
            return self[key]
        

    def __setattr__(self, key, value):
        if key in ["edbapp","_config","maps"]:
            object.__setattr__(self,key,value)
        else:
            log.debug("get property '%s' from dict."%key)
            self[key] = value

    def __repr__(self):
        return "%s Object: %s"%(self.__class__.__name__,self.Name)
    
    def __contains__(self,key):
        return key in self.Config
    
    def __dir__(self):
        return list(dir(self.__class__)) + list(self.__dict__.keys()) + list(self.Props)

    @property
    def Config(self):
        if not self._config:
            self.loadOptions()
            
        return self._config

    @property
    def Props(self):
        propKeys = list(self.Config.Keys)
        if self.Config.maps:
            propKeys += list(self.Config.maps.keys())
        
        return propKeys
    

    def get(self,key):
        '''
        mapping key must not have same value with maped key.
        '''
        
        if not self._config:
            self.loadOptions()
  
        
        if key in self._config and self._config[key] != None: # Map value or already have value
            siwave_id = self.edbapp.edb_api.ProductId.SIWave
            cell = self.edbapp.active_cell._active_cell
            val= cell.GetProductProperty(siwave_id, int(self._config[key]))
            if val[0]:
                return val[1]
            else:
                log.error("Get Property error: %s"%(self.key))
#             cell.SetProductProperty(siwave_id, 515, '1')
        
        if not isinstance(key, str): #key must string
            log.exception("Property error: %s"%(self.key))
        
        
    
    def set(self,key,value):
        '''
        mapping key must not have same value with maped key.
        '''
        
        if not self._config:
            self.loadOptions()
  
        
        if key in self._config and self._config[key] != None: # Map value or already have value
            siwave_id = self.edbapp.edb_api.ProductId.SIWave
            cell = self.edbapp.active_cell._active_cell
            rst = cell.SetProductProperty(siwave_id,int(self._config[key]), str(value))
            if not rst:
                log.error("Get Property error: %s"%(self.key))

        if not isinstance(key, str): #key must string
            log.exception("Property error: %s"%(str(key)))



    def loadOptions(self):
        cfgPath = os.path.join(appDir,"SIwaveProductProperties.cfg")
        cfgDict = readCfgFile(cfgPath)
        maps = {}
        for key,value in cfgDict.items():
            key2 = key.replace("_","") ##remove -  
            if key2 != key:
                key3 = key.title().replace("_","")
                maps[key3] = key
        self._config = Config(cfgDict)
        self._config.setMaps(maps)


    def exportSiwave(self,path=None):
        
        if not path:
            path = os.path.splitext(self.edbapp.edbpath)[0]+".siw"
        
        
        execPath = os.path.join(os.path.dirname(path), "SaveSiw.exec")
        with open(execPath,"w+") as f:
            f.write("SaveSiw")
            f.close()
        cmd = '"{0}" {1} {2} -formatOutput'.format(os.path.join(self.edbapp.base_path,"siwave_ng"),self.edbapp.edbpath,execPath)
        log.info("Save project to Siwave: %s"%path)
        with os.popen(cmd,"r") as output:
            for line in output:
                log.info(line)
            output.close()
        
        return path



if __name__ == "__main__":
    from ansys.aedt.core import Edb
    edbapp = Edb(edbpath=r"C:\work\Project\AE\Script\PSI\PSI_automation_testCase\edb\SIWAVE_PDN_TEST_0716_group1.aedb", edbversion="2024.2")
    siwave_id = edbapp.edb_api.ProductId.SIWave
    cell = edbapp.active_cell._active_cell
    cell.SetProductProperty(siwave_id, 515, '1')
    edbapp.save_edb()
    
    
#     self.cell.SetProductProperty(edb.ProductId.SIWave, kSIwaveProperties.PSI_SIMULATION_PREFERENCE, self.m_simConfig.m_simulationPreference)