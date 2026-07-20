'''
Created on 8 May 2021

@author: yguo
'''

import sys,os


class vector(object):
    
    def __init__(self,xyz = None):
        '''
        Constructor
        '''
        self.x = 0
        self.y = 0
        self.z = 0
        
        self.setPoint(xyz)
    
    def setPoint(self,xyz):
        if xyz == None or len(xyz)!=3:
            return
        self.xyz = xyz
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]
        
    def plus(self,V):
        x = "%s + %s"%(self.x,V.x) if V.x!=0 else self.x
        y = "%s + %s"%(self.y,V.y) if V.y!=0 else self.y
        z = "%s + %s"%(self.z,V.z) if V.z!=0 else self.z
        return vector([x,y,z])
        
#     def subtract(self,xyz):
#         x = "%s - %s"%(self.x,xyz[0]) if xyz[0]!=0 else self.x
#         y = "%s - %s"%(self.y,xyz[1]) if xyz[1]!=0 else self.y
#         z = "%s - %s"%(self.z,xyz[2]) if xyz[2]!=0 else self.z
#         return vector([x,y,z])


class polyline(object):
    '''
    classdocs
    '''
    def __init__(self,points = None):
        '''
        Constructor
        '''
        self.points = points
    
    def createPolyline(self,oEditor,points,name,material = "copper",color = "(143 175 143)",Transparency = 0):
        PLPoints =   [["NAME:PLPoint","X:=", "%s"%p[0],"Y:=", "%s"%p[1],"Z:=", "%s"%p[2]] for p in points]
        # Each segment connects point i to i+1, so segment count must be len(points)-1.
        PLSegments = [["NAME:PLSegment","SegmentType:=", "Line","StartIndex:=", i,"NoOfPoints:=", 2] for i in range(len(points)-1)]
        oEditor.CreatePolyline(
            [
                "NAME:PolylineParameters",
                "IsPolylineCovered:="    , True,
                "IsPolylineClosed:="    , True,
                [
                    "NAME:PolylinePoints"
                    
                ] + PLPoints,
                [
                    "NAME:PolylineSegments"
                ] + PLSegments,
                [
                    "NAME:PolylineXSection",
                    "XSectionType:="    , "None",
                    "XSectionOrient:="    , "Auto",
                    "XSectionWidth:="    , "0mm",
                    "XSectionTopWidth:="    , "0mm",
                    "XSectionHeight:="    , "0mm",
                    "XSectionNumSegments:="    , "0",
                    "XSectionBendType:="    , "Corner"
                ]
            ], 
            [
                "NAME:Attributes",
                "Name:="        , name,
                "Flags:="        , "",
                "Color:="        , color,
                "Transparency:="    , Transparency,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="        , "",
                "MaterialValue:="    , "\"%s\""%material,
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="        , False,
                "ShellElement:="    , False,
                "ShellElementThickness:=", "0mm",
                "IsMaterialEditable:="    , True,
                "UseMaterialAppearance:=", False,
                "IsLightweight:="    , False
            ])

              

class RectShape(object):      
    '''
    classdocs
    '''
    def __init__(self,width = 0, height = 0, width2 = None):
        '''
        Constructor
        '''
        self.width = width
        self.width2 = width2 if width2 is not None else width
        self.height = height
        
        self.leftX = 0
        self.leftY = 0
        self.name = "line1"
        self.material = "copper"
        
    def setWidth(self,width, width2 = None):
        self.width = width
        if width2 is not None:
            self.width2 = width2
        else:
            self.width2 = width
            
    def setHeight(self,height):
        self.height = height
    
    def setLeft(self,X,Y):
        self.leftX,self.leftY = X,Y
        
    def creatRectangle(self,oEditor = None,name = None, material = None,color = "(143 175 143)",transparency = 0):

        dx = "(%s-%s)/2"%(self.width,self.width2)
        p0 = vector((self.leftX,self.leftY,0))
        p1 = p0.plus(vector((dx,self.height,0)))
        p2 = p1.plus(vector((self.width2,0,0)))
        p3 = p0.plus(vector((self.width,0,0)))
        
        points = [p.xyz for p in (p0,p1,p2,p3,p0)]
        poly = polyline()
        poly.createPolyline(oEditor, points, name , material,color,transparency)
        
        
            
class tLines(object):
    '''
    classdocs
    '''
    def __init__(self,oProject = None, oDesign = None):
        '''
        Constructor
        '''
        self.lineCount = 20
        
        self.oProject = oProject
        self.oDesign = oDesign
        
    def initProject(self,oProject,oDesign):
        self.oProject = oProject
        self.oDesign = oDesign
    
    def creatVariables(self):
        varList = []
        varList += ["w_line%s_top"%i for i in range(1,self.lineCount+1)]
        varList += ["w_line%s_bot"%i for i in range(1,self.lineCount+1)]
        varList += ["s_line%s_line%s"%(i, i+1) for i in range(1,self.lineCount)]
        
#         varList += ["w_line%s_leftX"%i for i in range(1,self.lineCount+1)]
#         varList += ["w_line%s_lefty"%i for i in range(1,self.lineCount+1)]
        for var in varList:
            self.addVariable(var, "5mil")
        
        self.addVariable("s_left","40mil")
        self.addVariable("s_right","40mil")
        
        self.addVariable("T_gnd_top","1.2mil")
        self.addVariable("T_gnd_bot","1.2mil")
        self.addVariable("T_line","1.2mil")
        
        self.addVariable("H_core","5mil")
        self.addVariable("H_pp","4mil")
        
        self.addVariable("line1_left","s_left")
        self.addVariable("line1_right","s_left+w_line1_bot")
        for i in range(2,self.lineCount+1):
            self.addVariable("line%s_left"%i,"line%s_right+s_line%s_line%s"%(i-1, i-1, i))
            self.addVariable("line%s_right"%i,"line%s_left+w_line%s_bot"%(i,i))
        self.addVariable("max_right","line%s_right+s_right"%(self.lineCount))
     
        #huray
        self.addVariable("huray_radius_line_left","0.5um")
        self.addVariable("huray_radius_line_top","0.5um")
        self.addVariable("huray_radius_line_right","0.5um")
        self.addVariable("huray_radius_line_bot","0.5um")
        self.addVariable("huray_radius_gnd_top","0.5um")
        self.addVariable("huray_radius_gnd_bot","0.5um")
        
        self.addVariable("huray_ratio_line_left","2.9")
        self.addVariable("huray_ratio_line_top","2.9")
        self.addVariable("huray_ratio_line_right","2.9")
        self.addVariable("huray_ratio_line_bot","2.9")
        self.addVariable("huray_ratio_gnd_top","2.9")
        self.addVariable("huray_ratio_gnd_bot","2.9")
        
        #material
        self.addVariable("$pp_dk","3.6")
        self.addVariable("$core_dk","3.6")
        self.addVariable("$fill_dk","3.6")
        
        self.addVariable("$pp_df","0.008")
        self.addVariable("$core_df","0.008")
        self.addVariable("$fill_df","0.008")
        
        self.addVariable("$cond_line","5.8e7")
        self.addVariable("$cond_top_gnd","5.8e7")
        self.addVariable("$cond_bot_gnd","5.8e7")
        
    
    def creatMaterial(self):
        self.addMaterial("pp", "$pp_dk", "$pp_df") 
        self.addMaterial("core", "$core_dk", "$core_df") 
        self.addMaterial("fill", "$fill_dk", "$fill_df") 
        
        self.addMaterial("cond_line", cond="$cond_line") 
        self.addMaterial("cond_top_gnd", cond="$cond_top_gnd") 
        self.addMaterial("cond_bot_gnd", cond="$cond_bot_gnd") 
     
        
    def creatTlines(self):
        oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        for i in range(1,self.lineCount+1):
            rect = RectShape("w_line%s_bot"%i,"T_line","w_line%s_top"%i)
            rect.setLeft("line%s_left"%i,"T_gnd_bot+H_core")
            rect.creatRectangle(oEditor, "tline%s"%i, "cond_line",color = "(255 255 0)")


    def creatGNDCond(self):
        oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        #bot GND
        rect = RectShape("max_right","T_gnd_bot")
        rect.setLeft(0,0)
        rect.creatRectangle(oEditor, "gnd_bot", "cond_bot_gnd",color = "(255 128 64)")
        #top gnd
        rect = RectShape("max_right","T_gnd_top")
        rect.setLeft(0,"T_gnd_bot+H_core+T_line+H_pp")
        rect.creatRectangle(oEditor, "gnd_top", "cond_top_gnd",color = "(255 128 64)")
        
    def creatDielectric(self):
        oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        #core
        rect = RectShape("max_right","H_core")
        rect.setLeft(0,"T_gnd_bot")
        rect.creatRectangle(oEditor, "core", "core",transparency = 0.6)
        
        #fill
        rect = RectShape("max_right","T_line")
        rect.setLeft(0,"T_gnd_bot+H_core")
        rect.creatRectangle(oEditor, "fill", "fill",transparency = 0.9)
        
        #pp
        rect = RectShape("max_right","H_pp")
        rect.setLeft(0,"T_gnd_bot+H_core+T_line")
        rect.creatRectangle(oEditor, "pp", "pp",transparency = 0.6)


    def setHurayModel(self):
        oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        edges = [oEditor.GetEdgeIDsFromObject("tline%s"%i) for i in range(1,self.lineCount+1)]
        edges_left,edges_top,edges_right,edges_bot = zip(*edges)
        self.addFiniteCond("huray_line_left",edges_left, "huray_radius_line_left", "huray_ratio_line_left")
        self.addFiniteCond("huray_line_top",edges_top, "huray_radius_line_top", "huray_ratio_line_top")
        self.addFiniteCond("huray_line_right",edges_right, "huray_radius_line_right", "huray_ratio_line_right")
        self.addFiniteCond("huray_line_bot",edges_bot, "huray_radius_line_bot", "huray_ratio_line_bot")
        
        edges = oEditor.GetEdgeIDsFromObject("gnd_top")
        self.addFiniteCond("huray_gnd_top",edges, "huray_radius_gnd_top", "huray_ratio_gnd_top")
        edges = oEditor.GetEdgeIDsFromObject("gnd_bot")
        self.addFiniteCond("huray_gnd_bot",edges, "huray_radius_gnd_bot", "huray_ratio_gnd_bot")
        
    def setSolverOption(self):
        oModule = self.oDesign.GetModule("BoundarySetup")
        oModule.AssignSingleReferenceGround(
            [
                "NAME:gnd",
                "Objects:="        , ["gnd_bot","gnd_top"],
                "SolveOption:="        , "Automatic",
            ])
        
        for i in range(1,self.lineCount+1):
            oModule.AssignSingleSignalLine(
                [
                    "NAME:tline%s"%i,
                    "Objects:="        , ["tline%s"%i],
                    "SolveOption:="        , "Automatic"
                ])

    def addVariable(self,var,val):
        obj = self.oProject if var.startswith("$") else self.oDesign

        # Check variable existence in the correct scope.
        if var in obj.GetVariables():
            return

        obj.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:%s"%("ProjectVariableTab" if var.startswith("$") else "LocalVariableTab"),
                    [
                        "NAME:PropServers", 
                        "%s"%("ProjectVariables" if var.startswith("$") else "LocalVariables")
                    ],
                    [
                        "NAME:NewProps",
                        [
                            "NAME:%s"%var,
                            "PropType:=", "VariableProp",
                            "UserDef:=", True,
                            "Value:=", "%s"%val
                        ]
                    ]
                ]
            ])
        
    def addMaterial(self,name=None,dk=1,df=0,cond=0):
        oProject = self.oProject
        
        
        oDefinitionManager = oProject.GetDefinitionManager()
        oMaterialManager = oDefinitionManager.GetManager("Material")
        if name in oMaterialManager.GetNames():
            return
        
        oDefinitionManager.AddMaterial(
            [
                "NAME:%s"%name,
                "CoordinateSystemType:=", "Cartesian",
                "BulkOrSurfaceType:="    , 1,
                [
                    "NAME:PhysicsTypes",
                    "set:="            , ["Electromagnetic"]
                ],
                "permittivity:="    , "%s"%dk,
                "dielectric_loss_tangent:=", "%s"%df,
                "conductivity:="    , "%s"%cond,
            ])
     
    def addFiniteCond(self,name,edges,radius,ratio):
        oModule = self.oDesign.GetModule("BoundarySetup")
        edgeList = [int(e) for e in edges]
        oModule.AssignFiniteCond(
            [
                "NAME:%s"%name,
                "Edges:="        , edgeList,
                "UseCoating:="        , False,
                "Radius:="        , "%s"%radius,
                "Ratio:="        , "%s"%ratio
            ]) 
        
        
    def autoSolveOption(self,objs):
        boundarySetups = ["BoundarySetup:%s"%o for o in objs]
        self.oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:2DExtractor",
                    [
                        "NAME:PropServers", 
                    ] + boundarySetups,
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Solve Option",
                            "Value:="        , "SolveOnBoundary"
                        ],
                        [
                            "NAME:Solve Option",
                            "Value:="        , "Automatic"
                        ]
                    ]
                ]
            ])


    def addSolution(self):
        oModule = self.oDesign.GetModule("AnalysisSetup")
        oModule.InsertSetup("2DMatrix", 
            [
                "NAME:Setup1",
                "AdaptiveFreq:="    , "10GHz",
                "SaveFields:="        , True,
                "Enabled:="        , True,
                [
                    "NAME:MeshLink",
                    "ImportMesh:="        , False
                ],
                [
                    "NAME:CGDataBlock",
                    "MaxPass:="        , 50,
                    "MinPass:="        , 1,
                    "MinConvPass:="        , 1,
                    "PerError:="        , 0.1,
                    "PerRefine:="        , 30,
                    "DataType:="        , "CG",
                    "Included:="        , True,
                    "UseParamConv:="    , False,
                    "UseLossyParamConv:="    , False,
                    "PerErrorParamConv:="    , 1,
                    "UseLossConv:="        , False
                ],
                [
                    "NAME:RLDataBlock",
                    "MaxPass:="        , 50,
                    "MinPass:="        , 1,
                    "MinConvPass:="        , 1,
                    "PerError:="        , 0.1,
                    "PerRefine:="        , 30,
                    "DataType:="        , "RL",
                    "Included:="        , True,
                    "UseParamConv:="    , False,
                    "UseLossyParamConv:="    , False,
                    "PerErrorParamConv:="    , 1,
                    "UseLossConv:="        , False
                ]
            ])
        oModule.InsertSweep("Setup1", 
            [
                "NAME:Sweep1",
                "IsEnabled:="        , True,
                "RangeType:="        , "LinearCount",
                "RangeStart:="        , "0Hz",
                "RangeEnd:="        , "0Hz",
                "RangeCount:="        , 1,
                [
                    "NAME:SweepRanges",
                    [
                        "NAME:Subrange",
                        "RangeType:="        , "LogScale",
                        "RangeStart:="        , "1Hz",
                        "RangeEnd:="        , "1GHz",
                        "RangeCount:="        , 1,
                        "RangeSamples:="    , 10
                    ],
                    [
                        "NAME:Subrange",
                        "RangeType:="        , "LogScale",
                        "RangeStart:="        , "1GHz",
                        "RangeEnd:="        , "100GHz",
                        "RangeCount:="        , 1,
                        "RangeSamples:="    , 10
                    ]
                ],
                "Type:="        , "Interpolating",
                "SaveFields:="        , False,
                "SaveRadFields:="    , False,
                "InterpTolerance:="    , 0.5,
                "InterpMaxSolns:="    , 50,
                "InterpMinSolns:="    , 0,
                "InterpMinSubranges:="    , 1,
                "MinSolvedFreq:="    , "100000"
            ])

def test():
    aedtInstallDir = r"C:\Program Files\AnsysEM\AnsysEM22.2\Win64"
    sys.path.append(aedtInstallDir)
    sys.path.append(os.path.join(aedtInstallDir, 'PythonFiles','DesktopPlugin'))
    import ScriptEnv
    ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
    module = sys.modules['__main__']
    oDesktop = module.oDesktop
    oDesktop.RestoreWindow()
    oProject = oDesktop.GetActiveProject()
    oProject.InsertDesign("2D Extractor", "", "", "")
    oDesign = oProject.GetActiveDesign()
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    s = RectShape("5mil","1.2mil")
    s.setLeft("10mil", "10mil")
    s.creatRectangle(oEditor)
    
def test2():
    import sys,os
    aedtInstallDir = r"C:\Program Files\AnsysEM\v242\Win64"
    sys.path.append(aedtInstallDir)
    sys.path.append(os.path.join(aedtInstallDir, 'PythonFiles','DesktopPlugin'))
    import ScriptEnv
    ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
    module = sys.modules['__main__']
    oDesktop = module.oDesktop
    oDesktop.RestoreWindow()
    
    
    oProject = oDesktop.GetActiveProject()
    oProject.InsertDesign("2D Extractor", "", "", "")
    oDesign = oProject.GetActiveDesign()
    oEditor = oDesign.SetActiveEditor('3D Modeler')
    t = tLines(oProject,oDesign)
    t.lineCount = 4
    t.creatVariables()
    t.creatMaterial()
    t.creatTlines()
    t.creatGNDCond()
    t.creatDielectric()
    t.setSolverOption()
    t.setHurayModel()
    t.addSolution()

def createTlines(lineCount):
    
    
    module = sys.modules['__main__']
    if hasattr(module, "oDesktop"):
        oDesktop = module.oDesktop
    else:
        from pyLayout import Layout
        layout = Layout()
        layout.initDesign()
        oDesktop = layout.oDesktop

    oProject = oDesktop.GetActiveProject()
    oProject.InsertDesign("2D Extractor", "", "", "")
    oDesign = oProject.GetActiveDesign()
    oEditor = oDesign.SetActiveEditor('3D Modeler')
    t = tLines(oProject,oDesign)
    t.lineCount = lineCount
    t.creatVariables()
    t.creatMaterial()
    t.creatTlines()
    t.creatGNDCond()
    t.creatDielectric()
    t.setSolverOption()
    t.setHurayModel()
    t.addSolution()


def launch_gui(default_line_count=4):
    import tkinter as tk
    from tkinter import messagebox

    def on_ok():
        raw_value = line_count_var.get().strip()
        try:
            count = int(raw_value)
            if count <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for Line Count.")
            return

        try:
            createTlines(count)
            messagebox.showinfo("Completed", "Parameterized Tline model has been generated successfully.")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Execution Failed", "Failed to generate model:\n%s" % e)

    def on_cancel():
        root.destroy()

    root = tk.Tk()
    root.title("Parameterized Tline Generator")
    root.resizable(False, False)

    container = tk.Frame(root, padx=16, pady=14)
    container.pack(fill="both", expand=True)

    title_label = tk.Label(container, text="Parameterized Tlines Generator", font=("Segoe UI", 11, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, sticky="w")

    desc = (
        "This tool generates parameterized Tlines.\n"
        "Enter line count to automatically build a parameterized model\n"
        "for subsequent analysis."
    )
    desc_label = tk.Label(container, text=desc, justify="left")
    desc_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 12))

    tk.Label(container, text="Line Count:").grid(row=2, column=0, sticky="w")
    line_count_var = tk.StringVar(value=str(default_line_count))
    line_count_entry = tk.Entry(container, textvariable=line_count_var, width=12)
    line_count_entry.grid(row=2, column=1, sticky="w")
    line_count_entry.focus_set()

    button_bar = tk.Frame(container)
    button_bar.grid(row=3, column=0, columnspan=2, sticky="e", pady=(14, 0))

    ok_btn = tk.Button(button_bar, text="OK", width=10, command=on_ok)
    ok_btn.pack(side="left", padx=(0, 8))
    cancel_btn = tk.Button(button_bar, text="Cancel", width=10, command=on_cancel)
    cancel_btn.pack(side="left")

    root.bind("<Return>", lambda _event: on_ok())
    root.bind("<Escape>", lambda _event: on_cancel())
    root.mainloop()

def main():
    launch_gui(4)
      
if __name__ == '__main__':
    launch_gui(4)
    