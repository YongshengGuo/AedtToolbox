
#coding:utf-8
#--- coding=utf-8
#--- @author: yongsheng.guo@ansys.com
#--- @Time: ver 6.0 20230721

import sys,os,re
from .common import log,loadJson,writeJson,readCfgFile
from .complexDict import ComplexDict


class Config(ComplexDict):
    
    
    def __init__(self,dictData=None):
        super(Config,self).__init__(dictData=dictData,path=None,maps=None)
        FormatDict = {
            "list":[],
            "dict":[],
            "str":[],
            "float":[],
            "int":[],
            "bool":[],
            "func":[]
            }
        self.update("FormatDict", FormatDict)
        self.format()
        
    
    def readJson(self,path):
        if os.path.exists(path):
            config = loadJson(path)
            self.updateOptions(config)
        else:
            log.exception("Not found config file: %s"%path)
    
    def readCfgFile(self,path):
        """
        read ini format file
        """
        cfg_dict = readCfgFile(path)
        self.updateOptions(cfg_dict)

        
    def updateEnvOption(self):
        for key in os.environ:
            if key in self:
                self[key] = os.environ[key]
        self.format()
        
    def updateArgsOption(self):
        #for arguments
        args = sys.argv[1:]
    #         print(args)
        optionList = []
        args2 = args[:]
        l = len(args)
        for i in range(l):
            if args[i].startswith("-"):
                if i > l-2:
                    continue
                
                if not args[i+1].startswith("-"):
                    self._dict.update(args[i][1:],args[i+1])
                    i += 1
                else:
                    self._dict.update(args[i][1:],None)
        self.format()

    def format(self):
        options = self._dict
        #---int
        for k in self.FormatDict["int"]:
            if isinstance(options[k], str):
                options[k] = int(options[k])
                
        #---float
        for k in self.FormatDict["float"]:
            if isinstance(options[k], str):
                options[k] = float(options[k])

        #---str
        for k in self.FormatDict["str"]:
            if not isinstance(options[k], str):
                options[k] = float(options[k])

        #---bool
        for k in self.FormatDict["bool"]:
            if isinstance(options[k], str):
                if options[k].lower() in ["true","1"]:
                    options[k] = True
                elif options[k].lower() in ["false","0"]:
                    options[k] = False
    
        #---list
        for k in self.FormatDict["list"]:
            if isinstance(options[k], str):
                options[k] = re.split("[\s,]*",re.sub(r"[\[\]\'\"]","",options[k]))
    
        #---dict
        for k in self.FormatDict["dict"]:
            if isinstance(options[k], str):
                options[k] = dict([x.split(':', 1) for x in re.split("[\s,]*",re.sub(r"[\[\]\'\"]","",options[k]))])
                
        #---func
        for k in self.FormatDict["func"]:
            if isinstance(options[k], str):
                options[k] = eval(options[k])
            
                
#         return ComplexDict(options)

