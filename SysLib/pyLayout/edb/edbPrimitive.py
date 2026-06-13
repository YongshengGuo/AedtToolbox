
#--- coding:utf-8
#--- @Author: Yongsheng.Guo@ansys.com
#--- @Time: 2025-05-15

'''
pingroup for edb function
'''
import os,sys,re
from ..common.common import *
from ..common.complexDict import ComplexDict
from ..primitive.geometry import Point,Polygen
from .edbDefinition import EdbDefinition,EdbDefinitions

try:
    _clr = initClr()
    from System import String
except:
    log.warning("CLR initialization failed in child process (likely duplicate init). Ignoring if not needed.")  
# from System import String

appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)


def getPrimitiveName(obj,edbApp):
    
    
    name = ""
    if isIronpython:
        val = _clr.StrongBox[str]()
        rst = obj.GetProductProperty(edbApp.Edb.ProductId.Designer, 1, val)
        if rst:
            name = val.Value
    else:
        val = String("")
        #edbApp.Edb.ProductId.Designer  0 Deprecated. use Hfss3DLayout instead.  
        _, name = obj.GetProductProperty(edbApp.Edb.ProductId.Designer, 1, val)
        
    name = str(name).strip("'")
    PrimitiveType = str(obj.GetPrimitiveType()).lower()
    if name == "":
        if PrimitiveType == "path":
            ptype = "line"
        elif PrimitiveType == "rectangle":
            ptype = "rect"
        elif PrimitiveType == "polygon":
            ptype = "poly"
        elif PrimitiveType == "bondwire":
            ptype = "bwr"
        else:
            ptype = PrimitiveType
            
        name = "{}__{}".format(ptype, obj.GetId())
#             self.edbApp.SetProductProperty(self._pedb._edb.ProductId.Designer, 1, name)
    return name


class EdbPrimitive(EdbDefinition):
    def __init__(self,obj,edbApp=None):
        super(self.__class__,self).__init__(obj,type="EdbPrimitive",edbApp=edbApp)

    def parse(self,force = False):
        '''
        mapping key must not have same value with maped key.
        '''
        
        if self.parsed and not force:
            return

        maps = {
            "Name":{"Key":"self","Get":lambda s:s.GetName()},
            "ID":{"Key":"self","Get":lambda s:s.obj.GetId()},
            "Net":{"Key":"self","Get":lambda s:s.obj.GetNet(),"Set":lambda s,x:s.SetNet(x)},
            "NetName":{"Key":"self","Get":lambda s:s.obj.GetNet().GetName()},
            "Group":{"Key":"self","Get":lambda s:s.obj.GetGroup()},
            "GroupName":{"Key":"self","Get":lambda s:s.obj.GetGroup().GetName()},
            "Component":{"Key":"self","Get":lambda s:s.obj.GetComponent()},
            "ComponentName":{"Key":"self","Get":lambda s:s.obj.GetComponent().GetName()},
            "ObjType":{"Key":"self","Get":lambda s:s.obj.GetObjType().ToString()},
            "PrimitiveType":{"Key":"self","Get":lambda s:s.obj.GetPrimitiveType()},
            "Layer":{"Key":"self","Get":lambda s:s.obj.GetLayer()},
            "LayerName":{"Key":"self","Get":lambda s:s.obj.GetLayer().GetName()},
        }

        self.maps.update(maps)
        self._info.update("self", self)
        self._info.setMaps(self.maps)
        self.parsed = True

    def GetName(self):
        return getPrimitiveName(self.obj, self.edbApp)


#     def getPhysicallyConnected(self):
#         layoutInst = self.edbApp.layout.GetLayoutInstance()
#         layoutObjInst = layoutInst.GetLayoutObjInstance(self.obj, None)
#         objs = [EdbDefinition(obj.GetLayoutObj(),type="Connectable") for obj in layoutInst.GetConnectedObjects(layoutObjInst).Items]
# #         for each in layoutInst.GetConnectedObjects(layoutObjInst).Items:
# #             obj = each.GetLayoutObj()
# #             if obj.GetObjType() == self.edbApp.Edb.Cell.LayoutObjType.Primitive:
# #                 objs.append(EdbPrimitive(obj,self.edbApp))
# #             elif obj.GetObjType() == self.edbApp.Edb.Cell.LayoutObjType.PadstackInstance:
# #                 objs.append(EdbVia(obj,self.edbApp))
# #             else:
# #                 pass
#         return objs + [self]
    

class EdbPrimitives(EdbDefinitions):

    def __init__(self,edbApp=None):
        '''
        from ansys.aedt.core import Edb
        edbApp = Edb(edbpath=".aedb")
        '''
        super(EdbPrimitives,self).__init__(edbApp,type="Primitives",definitionClass=EdbPrimitive)

#

    @property
    def DefinitionDict(self):
        if self._definitionDict == None:
            if hasattr(self.edbApp.layout,self.type):
                objs = getattr(self.edbApp.layout,self.type)
                self._definitionDict = {}
                self._definitionDict  = ComplexDict(dict([(getPrimitiveName(p,self.edbApp),self.definitionClass(p,self.edbApp)) for p in objs]))
            else:
                self._definitionDict = {}
        return self._definitionDict
    
    
    
