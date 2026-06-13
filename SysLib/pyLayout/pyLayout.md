# pyLayout API Documentation for Agent Indexing

## Overview

`pyLayout` is a Python library for automating Ansys Electronics Desktop (AEDT) 3D Layout design operations. It provides a high-level, Pythonic interface to interact with PCB layouts, including components, nets, primitives, layers, materials, setups, and simulation results.

**Core Class**: [`Layout`](pyLayout\pyLayout.py#L91-L1980)

---

## Table of Contents

1. [Layout Initialization](#layout-initialization)
2. [Core Collections](#core-collections)
3. [Primitive Objects](#primitive-objects)
4. [Definition Objects](#definition-objects)
5. [IO Operations](#io-operations)
6. [Simulation & Analysis](#simulation--analysis)
7. [Utility Methods](#utility-methods)

---

## Layout Initialization

### Constructor

```python
from pyLayout import Layout

# Initialize with default settings (latest AEDT version)
layout = Layout()

# Initialize with specific version
layout = Layout(version="2023.2")

# Initialize with custom parameters
layout = Layout(
    version="2023.2",
    installDir=None,
    nonGraphical=False,
    newDesktop=False,
    usePyAedt=False,
    oDesktop=None
)
```

**Parameters:**
- `version` (str): AEDT version (e.g., "2023.2", "2024.1")
- `installDir` (str): Custom AEDT installation directory
- `nonGraphical` (bool): Run in non-graphical mode
- `newDesktop` (bool): Create new desktop instance
- `usePyAedt` (bool): Use PyAEDT gRPC API
- `oDesktop`: Pre-existing oDesktop COM object

### Connection Methods

#### Initialize Design
```python
# Initialize first available project and design
layout.initDesign()

# Initialize specific project
layout.initDesign(projectName="MyProject")

# Initialize specific project and design
layout.initDesign(projectName="MyProject", designName="Layout1")

# Initialize without loading objects (faster)
layout.initDesign(initLayout=False)
```

#### Connect via gRPC
```python
# Connect to running AEDT instance via gRPC
layout.getDesktopByGrpc(port=50051, machine="localhost", process_id=None)
```

#### Load Existing Layout
```python
# Load from various formats
layout.loadLayout("design.brd", layoutType="Cadence")
layout.loadLayout("design.aedb", layoutType="EDB")
layout.loadLayout("design.aedt", layoutType="AEDT")
layout.loadLayout("design.siw", layoutType="SIwave")
layout.loadLayout("design.tgz", layoutType="ODB++")
layout.loadLayout("design.xml", layoutType="IPC")
layout.loadLayout("design.gds", layoutType="GDS")
```

#### Open AEDT Project
```python
layout.openAedt("path/to/project.aedt", unlock=False)
layout.openArchive("path/to/project.aedtz", newPath=None)
```

### Properties

```python
# Information properties
layout.Info              # ComplexDict with all layout info
layout.ProjectName       # Current project name
layout.DesignName        # Current design name
layout.ProjectPath       # Full path to .aedt file
layout.ProjectDir        # Project directory
layout.EdbPath           # Path to .aedb database
layout.ResultsPath       # Results directory
layout.Version           # AEDT version string
layout.InstallDir        # AEDT installation directory
layout.ProcessID         # AEDT process ID

# Unit system
layout.unit              # Current unit (e.g., "mm", "mil")
```

---

## Core Collections

All collections support dictionary-style access with regex pattern matching:

```python
# Direct access by name
comp = layout.Components["U1"]
net = layout.Nets["DDR3_A1"]

# Regex pattern matching (returns list)
comps = layout.Components["U.*"]      # All components starting with U
nets = layout.Nets["DDR3_A.*"]        # All nets matching DDR3_A.*

# Index-based access
port = layout.Ports[0]
via = layout.Vias[5]

# Slice access
pins = layout.Pins[0:10]
```

### Collection Overview

| Collection | Access Path | Description | Object Type |
|-----------|-------------|-------------|-------------|
| **Objects** | `layout.Objects` | All primitive objects | [`Objects3DL`](pyLayout\primitive\primitive.py#L567-L611) |
| **Components** | `layout.Components` | PCB components | [`Components`](pyLayout\primitive\component.py#L624-L874) |
| **Nets** | `layout.Nets` | Electrical nets | [`Nets`](pyLayout\definition\net.py#L361-L654) |
| **Pins** | `layout.Pins` | Component pins | [`Pins`](pyLayout\primitive\pin.py#L237-L240) |
| **Vias** | `layout.Vias` | Vias | [`Vias`](pyLayout\primitive\via.py#L138-L141) |
| **Traces** | `layout.Traces` | Lines and arcs | [`Objects3DL`](pyLayout\primitive\primitive.py#L567-L611) |
| **Shapes** | `layout.Shapes` | Rectangles, polygons, circles | [`Objects3DL`](pyLayout\primitive\primitive.py#L567-L611) |
| **Lines** | `layout.Lines` | Line primitives | [`Lines`](pyLayout\primitive\line.py#L45-L90) |
| **Arcs** | `layout.Arcs` | Arc primitives | Primitives |
| **Rects** | `layout.Rects` | Rectangle primitives | Primitives |
| **Polys** | `layout.Polys` | Polygon primitives | Primitives |
| **Circles** | `layout.Circles` | Circle primitives | Primitives |
| **Voids** | `layout.Voids` | Void objects | [`Objects3DL`](pyLayout\primitive\primitive.py#L567-L611) |
| **Ports** | `layout.Ports` | Simulation ports | [`Ports`](pyLayout\primitive\port.py#L218-L411) |
| **Sources** | `layout.Sources` | Voltage/current sources | [`Sources`](pyLayout\primitive\source.py#L144-L518) |
| **Layers** | `layout.Layers` | Stackup layers | [`Layers`](pyLayout\definition\layer.py#L618-L1172) |
| **Materials** | `layout.Materials` | Material definitions | [`Materials`](pyLayout\definition\material.py#L141-L374) |
| **Variables** | `layout.Variables` | Design variables | [`Variables`](pyLayout\definition\variable.py#L154-L249) |
| **Setups** | `layout.Setups` | Simulation setups | [`Setups`](pyLayout\definition\setup.py#L599-L650) |
| **Solutions** | `layout.Solutions` | Simulation results | [`Solutions`](pyLayout\postData\solution.py#L105-L191) |
| **PadStacks** | `layout.PadStacks` | Padstack definitions | [`PadStacks`](pyLayout\definition\padStack.py#L90-L101) |
| **ComponentDefs** | `layout.ComponentDefs` | Component definitions | [`ComponentDefs`](pyLayout\definition\componentLib.py#L35-L157) |
| **ModelDefs** | `layout.ModelDefs` | Model definitions (S-parameter, SPICE) | [`ModelDefs`](pyLayout\definition\modelDef.py#L30-L96) |
| **PinGroups** | `layout.PinGroups` | Pin group definitions | [`PinGroups`](pyLayout\definition\pinGroup.py#L88-L399) |
| **AirBox** | `layout.AirBox` | HFSS airbox settings | [`Airbox`](pyLayout\definition\airbox.py#L11-L41) |

---

## Primitive Objects

### Components ([`Components`](pyLayout\primitive\component.py#L624-L874))

```python
# Access component
comp = layout.Components["U1"]

# Get components by part name (supports regex)
comps = layout.Components.getComponentsByPart("CAP.*")

# Find component by pin
comp = layout.Components.findComponentByPin("U1-1")

# Export BOM
layout.Components.exportBom("bom.csv")

# Delete invalid RLC components
layout.Components.deleteInvalidRLC()

# Delete components with insufficient connections
layout.Components.deleteInvalidComponents(ConnectedNetsLessThen=2, PinsLessThen=2)

# Create component from pins
comp_name = layout.Components.createByPins(
    pinList=["U1-1", "U1-2"],
    layerName="Top",
    compName="MyComp"
)

# Update component models from dictionary
models = [
    {
        "RefDes": "U1",
        "Part": "cap1",
        "PartType": "Capacitor",
        "FileName": "model.s2p",
        "R": None,
        "L": None,
        "C": None,
        "Library": None
    }
]
layout.Components.updateModels(models)
```

**Component Object Properties:**
```python
comp.Name              # Reference designator
comp.Part              # Part name
comp.PartType          # Component type (Resistor, Capacitor, etc.)
comp.Pins              # Pin collection
comp.PinNames          # List of pin names
comp.NetNames          # List of connected net names
comp.Location          # Component location
comp.Rotation          # Rotation angle
```

### Nets ([`Nets`](pyLayout\definition\net.py#L361-L654))

```python
# Access net
net = layout.Nets["DDR3_A1"]

# Get signal nets
sig_nets = layout.Nets.SignalNetNames

# Get power/ground nets
pwr_nets = layout.Nets.PowerNetNames

# Get components connected to nets
comps = layout.Nets.getComponentsOnNets(["VCC", "GND"], ignorRLC=True)

# Create ports on nets
layout.Nets.createPortsOnNets(["SIG1", "SIG2"], comps=None, ignorRLC=True)

# Get nets by regex pattern
nets = layout.Nets.getRegularNets("DDR3_A[0-7]")

# Rename X-net (for differential pairs)
layout.Nets.reNameXnetForce("DP.*", tail="_C")

# Auto-rename RLC nets
layout.Nets.autoRLCnet(on="R")  # or "C", "L", "RC", "RLC"

# Merge physically connected nets
layout.Nets.mergePhysicallyConnectedNets()

# Disjoint nets
layout.Nets.disjointNets()

# Add nets to Power/Ground class
layout.Nets.addPwrGndNets(["VCC1", "VCC2"])

# Remove nets from Power/Ground class
layout.Nets.removePwrGndNets(["VCC1"])

# Delete nets
layout.Nets.deleteNets(["NET1", "NET2"])
```

**Net Object Properties:**
```python
net.Name               # Net name
net.Objects            # Objects on this net
net.getConnectedComponnets()  # Connected components
net.getNetConnected()  # Electrically connected objects
net.getPhysicallyConnected()  # Physically connected objects
net.rename(new_name)   # Rename net
net.disjoint()         # Disjoint net into separate nets
```

### Pins ([`Pins`](pyLayout\primitive\pin.py#L237-L240))

```python
# Access pin
pin = layout.Pins["U1-1"]
pin = layout.Pins["U1_1"]  # Alternative naming

# Pin properties
pin.Location           # Pin location (Point object)
pin.X, pin.Y          # Coordinates
pin.Net                # Connected net name
pin.StartLayer         # Start layer name
pin.EndLayer           # End layer name
pin.HoleDiameter       # Hole diameter
pin.PadDiameter        # Pad diameter
```

### Vias ([`Vias`](pyLayout\primitive\via.py#L138-L141))

```python
# Access via
via = layout.Vias["Via1"]

# Via properties
via.Location           # Via location
via.HoleDiameter       # Hole diameter
via.PadStack           # Padstack name
via.StartLayer         # Start layer
via.EndLayer           # End layer
```

### Ports ([`Ports`](pyLayout\primitive\port.py#L218-L411))

```python
# Access port
port = layout.Ports["Port1"]

# Reorder ports
layout.Ports.reorder(
    compOrder=["U1", "U2"],
    netOrder=["SIG1", "SIG2"],
    portOrder=["U1.1.SIG1", "U2.1.SIG2"]
)

# Add ports on nets
layout.Ports.add(netNames=["SIG1", "SIG2"], compNames=None)

# Add pin group port
port = layout.Ports.addPinGroupPort(
    posPins=["U1-1", "U1-2"],
    refPins=["U1-3", "U1-4"],
    compName="U1",
    posNet="SIG_P",
    negNet="SIG_N",
    name="DiffPort1",
    portZ0=50.0
)
```

**Port Object Properties:**
```python
port.Name              # Port name
port.Impedance         # Port impedance
port.Type              # Port type
port.setPortImpedance(z0)  # Set impedance
port.delete()          # Delete port
```

### Sources ([`Sources`](pyLayout\primitive\source.py#L144-L518))

```python
# Add voltage source between two points
source = layout.Sources.addVoltageSource(
    pt0=[0, 0],
    layer0="Top",
    pt1=[1, 1],
    layer1="Bottom",
    name="VSource1",
    magnitude="1V",
    resistance=1e-6
)

# Add current source
source = layout.Sources.addCurrentSource(
    pt0=[0, 0],
    layer0="Top",
    pt1=[1, 1],
    layer1="Bottom",
    name="ISource1",
    magnitude="1A",
    resistance=50e6
)

# Add pin group voltage source
source = layout.Sources.addPinGroupVoltageSource(
    posPins=["U1-1", "U1-2"],
    negPins=["U1-3", "U1-4"],
    magnitude="1V",
    resistance=1e-6,
    name="VSrc1"
)

# Add pin group current source
source = layout.Sources.addPinGroupCurrentSource(
    posPins=["U1-1"],
    negPins=["U1-2"],
    magnitude="1A",
    resistance=1e6,
    name="ISrc1"
)

# Add source by pin
source = layout.Sources.addSourceByPin(
    type="Voltage",  # or "Current"
    posPin="U1-1",
    negPin="U1-2",
    name="Source1",
    magnitude="1V",
    resistance=1e-6
)

# Add source from dictionary
source_dict = {
    "Type": "Voltage",
    "PosPins": ["U1-1"],
    "RefPins": ["U1-2"],
    "CompName": "U1",
    "Magnitude": "1V",
    "Resistance": 1e-6,
    "Name": "VSrc1"
}
layout.Sources.addSourceByDict(source_dict)

# Delete sources
layout.Sources.deleteSource("VSource1")
layout.Sources.deleteAllSources()
```

### Primitives Creation

```python
# Add circle
circle = layout.addCircle(
    layerName="Top",
    location=[0, 0],
    r="1mm",
    net="NET1",
    name="Circle1"
)

# Add line
line = layout.addLine(
    layerName="Top",
    points=[[0, 0], [1, 1], [2, 2]],
    width="0.1mm",
    net="NET1",
    name="Line1"
)

# Add rectangle
rect = layout.addRectangle(
    layerName="Top",
    ptA=[0, 0],
    ptB=[1, 1],
    net="NET1",
    name="Rect1"
)

# Add polygon
poly = layout.addpolygon(
    layerName="Top",
    points=[[0, 0], [1, 0], [1, 1], [0, 1]],
    net="NET1",
    name="Poly1"
)

# Add via
via = layout.addVia(
    position=[0, 0],
    padStack="via1",
    hole="0.2mm",
    upperLayer="Top",
    lowerLayer="Bottom",
    isPin=False,
    net="NET1",
    name="Via1"
)
```

---

## Definition Objects

### Layers ([`Layers`](pyLayout\definition\layer.py#L618-L1172))

```python
# Access layer by name
layer = layout.Layers["Top"]
layer = layout.Layers["C1"]     # First conductor layer
layer = layout.Layers["D1"]     # First dielectric layer
layer = layout.Layers["S1"]     # First stackup layer

# Access by index
layer = layout.Layers[0]        # First layer
layers = layout.Layers[0:5]     # First 5 layers

# Layer lists
cond_layers = layout.Layers.ConductorLayerNames
dielec_layers = layout.Layers.DielectricLayerNames
all_layers = layout.Layers.LayerNames

# Get visible conductor layers
visible = layout.Layers.getVisibleConductorLayers()

# Add layer
layout.Layers.addLayer(
    name="NewLayer",
    type="signal",  # or "dielectric"
    height=None,
    refLayer="S1",
    direction="above"  # or "below"
)

# Remove layer
layout.Layers.removeLayer("LayerName")

# Reverse stackup
layout.Layers.reversedStakup()

# Get layer by height
layer_name = layout.Layers.getLayerByHeight(
    height="0.5mm",
    type="Conductor",  # or "Dielectric"
    adjust="Near"      # or "above", "below", "Inner", "Outer"
)

# Load stackup from CSV
layout.Layers.loadFromCSV("stackup.csv")

# Export stackup to CSV
layout.Layers.exportCsv("stackup.csv")

# Export/import XML
layout.Layers.exportXml("stackup.xml")
layout.Layers.importXml("stackup.xml")

# Update layers from dictionary
layers_info = [
    {
        "Name": "Top",
        "Type": "signal",
        "Material": "copper",
        "Thickness": "35um",
        "DK": None,
        "DF": None,
        "Cond": "5.8e7",
        "Roughness": "0.5um"
    },
    {
        "Name": "Dielectric1",
        "Type": "dielectric",
        "Material": "FR4_epoxy",
        "Thickness": "0.2mm",
        "DK": 4.4,
        "DF": 0.02
    }
]
layout.Layers.loadFromDict(layers_info)

# Set layer data with different modes
layout.Layers.setLayerDatas(layers_info, mode=0)
# mode: 0=Auto, 1=byIndex, 2=byName, 3=force
```

**Layer Object Properties:**
```python
layer.Name             # Layer name
layer.Type             # Layer type (signal, dielectric)
layer.Material         # Material name
layer.Thickness        # Layer thickness
layer.Upper            # Upper elevation
layer.Lower            # Lower elevation
layer.DK               # Dielectric constant
layer.DF               # Dissipation factor
layer.Roughness        # Surface roughness
layer.isVisible()      # Check if layer is visible
layer.setData(data_dict)  # Update layer properties
layer.update()         # Apply changes to layout
```

### Materials ([`Materials`](pyLayout\definition\material.py#L141-L374))

```python
# Access material
mat = layout.Materials["copper"]
mat = layout.Materials["FR4_epoxy"]

# Create material
mat = layout.Materials.create(
    name="MyMaterial",
    DK=4.4,
    DF=0.02,
    Cond=5.8e7
)

# Add material
mat = layout.Materials.add(
    name="MyMaterial",
    DK=4.4,
    DF=0.02
)

# Add Djordjevic-Sarkar model (causal material)
mat = layout.Materials.addHFSSDSModle(
    name="FR4_DS",
    dk=4.4,
    df=0.02,
    f1=1e9,
    cond_dc=1e-12,
    fB=10**12/(2*math.pi)
)

# Add standard DS model
mat = layout.Materials.addStdDSModel(
    name="FR4_StdDS",
    e_infi=4.0,
    e_delta=0.4,
    fA=1e6,
    fB=1e12,
    cond_dc=1e-12
)

# Get material by name (case-insensitive)
mat = layout.Materials.getByName("COPPER")
```

**Material Object Properties:**
```python
mat.Name               # Material name
mat.DK                 # Dielectric constant
mat.DF                 # Dissipation factor
mat.Cond               # Conductivity
mat.Mu                 # Permeability
mat.TanDelta           # Loss tangent
mat.update()           # Apply changes
```

### Variables ([`Variables`](pyLayout\definition\variable.py#L154-L249))

```python
# Access variable
var = layout.Variables["width"]
var = layout.Variables["$global_var"]  # Project variable

# Set variable value
layout.Variables["width"] = "0.1mm"
layout.Variables.width = "0.1mm"

# Add variable
var = layout.Variables.add("myVar", "10mil")

# Evaluate expression
value = layout.Variables.evalExpression("width*2")

# Set variables from dictionary
var_dict = {"width": "0.1mm", "length": "10mm"}
layout.Variables.setByDict(var_dict)
```

**Variable Object Properties:**
```python
var.Name               # Variable name
var.Value              # Variable value (string)
var.SIValue            # Value in SI units (float)
var.Expression         # Expression string
```

### Setups ([`Setups`](pyLayout\definition\setup.py#L599-L650))

```python
# Access setup
setup = layout.Setups["Setup1"]

# Add setup
setup = layout.Setups.add(name="Setup1", solutionType="HFSS")
# solutionType: "HFSS", "SIwaveDCIR", "SIwave"

# Get all setup names
names = layout.Setups.getAllSetupNames()

# Analyze all setups
layout.Setups.analyzeAll()
```

**Setup Object Properties:**
```python
setup.Name             # Setup name
setup.SolveSetupType   # Solution type
setup.Sweeps           # Frequency sweeps
setup.Analyze()        # Run analysis
```

### Solutions ([`Solutions`](pyLayout\postData\solution.py#L105-L191))

```python
# Access solution
sol = layout.Solutions["Setup1:Sweep1"]
sol = layout.Solutions[0]  # First solution

# Get all solutions
solutions = layout.Solutions.All

# Export S-parameters
sol.exportSNP("output.s2p")

# Get solution data
data = sol.getData()
```

### PadStacks ([`PadStacks`](pyLayout\definition\padStack.py#L90-L101))

```python
# Access padstack
ps = layout.PadStacks["via1"]

# Add padstack
layout.PadStacks.add(name="myVia", padSize="16mil", drill="8mil")
```

### ComponentDefs ([`ComponentDefs`](pyLayout\definition\componentLib.py#L35-L157))

```python
# Access component definition
comp_def = layout.ComponentDefs["CAP0402"]

# Add component definition
layout.ComponentDefs.add(name="MyCompDef")

# Add S-parameter model definition
layout.ComponentDefs.addSNPDef(
    part="CAP0402",
    modelName="CAP_Model",
    pinMap=(["Port1", "Port2"], ["1", "2"])
)

# Add SPICE model definition
layout.ComponentDefs.addSpiceDef(name="SPICE_Model")
```

### ModelDefs ([`ModelDefs`](pyLayout\definition\modelDef.py#L30-L96))

```python
# Add S-parameter model
model = layout.ModelDefs.addSnpModel(
    path="model.s2p",
    name="MyModel",
    pinMap=(["Port1", "Port2"], ["1", "2"])
)

# Add SPICE model
model = layout.ModelDefs.addSpiceModel(
    path="model.cir",
    name="SpiceModel"
)
```

### PinGroups ([`PinGroups`](pyLayout\definition\pinGroup.py#L88-L399))

```python
# Access pin group
pg = layout.PinGroups["PinGroup1"]

# Create pin group from pins
layout.PinGroups.createByPins(
    pinList=["U1-1", "U1-2"],
    compName="U1",
    groupName="MyPinGroup"
)

# Create pin groups by grid
layout.PinGroups.createByGrid(
    pinList=["U1-1", "U1-2", "U1-3"],
    compName="U1",
    nets=["VCC", "GND"],
    groupName="GridGroup",
    rows=2,
    cols=2
)

# Create from dictionary
group_dict = {
    "Name": "MyGroup",
    "Refdes": "U1",
    "Pins": ["1", "2"],  # Short pin names
    "Nets": ["VCC"],
    "Rows": 1,
    "Cols": 1
}
layout.PinGroups.createByDict(group_dict)

# Create from list of dictionaries
layout.PinGroups.createByDictList([group_dict1, group_dict2])

# Find pin group by pin
pg = layout.PinGroups.findPinGroupByPin("U1-1")

# Delete pin group
layout.PinGroups.deletePinGroup("PinGroup1")
layout.PinGroups.deleteAllPinGroups()
```

### AirBox ([`Airbox`](pyLayout\definition\airbox.py#L11-L41))

```python
# Access airbox settings
airbox = layout.AirBox

# Update airbox
airbox.update()
```

---

## IO Operations

### Import Layouts

```python
# Import EDB
layout.importEBD("design.aedb")

# Import Cadence BRD
layout.importBrd(
    path="design.brd",
    edbPath="output.aedb",
    controlFile=""
)

# Import ODB++
layout.importODB(
    path="design.tgz",
    edbPath="output.aedb",
    controlFile=""
)

# Import IPC-2581
layout.importIPC2581(
    path="design.xml",
    edbPath="output.aedb",
    controlFile=""
)

# Import SIwave
layout.importSIwave(
    path="design.siw",
    edbPath="output.aedb"
)

# Translate layout (generic)
edb_path = layout.translateLayout(
    layoutPath="design.brd",
    edbOutPath="output.aedb",
    controlFile="",
    extractExePath=None,
    layoutType=None
)
```

### Export Layouts

```python
# Export to GDSII
layout.exportGDS(
    path="output.gds",
    outLayerMapPath="layermap.txt"
)

# Export to SIwave
layout.exportSiwave(path="output.siw")
```

### Project Management

```python
# New project
layout.newProject(projectName="MyProject")

# New design
layout.newDesign(newDesignName="Layout1", projectName="MyProject")

# Save project
layout.save()

# Save as
layout.saveAs("new_project.aedt", OverWrite=True)

# Close project
layout.close(save=True)

# Delete project
layout.deleteProject()
layout.deleteDesign()

# Delete from disk
layout.deleteFromDisk()

# Reload project
layout.reload()
layout.reloadEdb()

# Copy AEDT project
Layout.copyAEDT(source="src.aedt", target="dst.aedt")
```

---

## Simulation & Analysis

### Analysis Control

```python
# Analyze all setups
layout.analyze()

# Set number of cores
layout.setCores(cores=20, hpcType="Pack")
# hpcType: "Pack" or "Workgroup"

# Set HPC license type
layout.setHPCType("Pack")

# Submit distributed job
layout.submitJob(host="localhost", cores=20)

# Batch analysis
layout.batchAnalysis(host="localhost", cores=20)

# Wait for license
layout.waitForlicense(
    featureList=[{"module": "HFSSSolver"}],
    timeout=6000
)
```

### Geometry Operations

```python
# Cutout subdesign
layout.clip(
    newDesignName="Cutout",
    includeNetList=["SIG1", "SIG2"],
    clipNetList=["GND", "VCC"],
    expansion="2mm",
    InPlace=False
)

# Generate HFSS regions
layout.autoHFSSRegions()

# Geometry check and autofix
messages = layout.geometryCheckAndAutofix(
    checkList=["minimum_area", "self_intersection"]
)

# Sanitize layout
layout.sanitize(nets=["NET1", "NET2"])

# Heal small voids
layout.healingVoid(smallArea="0.5mm2")
```

### IC Mode

```python
# Enable/disable IC mode
layout.enableICMode(flag=True)
```

---

## Utility Methods

### Object Query

```python
# Get objects by type
objs = layout.getObjects(type="*")
# Types: 'pin', 'via', 'rect', 'arc', 'line', 'poly', 'plg', 
#        'circle void', 'line void', 'rect void', 'poly void', 
#        'plg void', 'text', 'cell', 'Measurement', 'Port', 
#        'Port Instance', 'Edge Port', 'component', 'CS', 'S3D', 'ViaGroup'

# Get objects by net
objs = layout.getObjectsbyNet(net="NET1", type="*")

# Get objects by layer
objs = layout.getObjectsbyLayer(layer="Top", type="*")

# Get objects by point
objs = layout.getObjectByPoint(
    point=[0, 0],
    layer="*",
    radius=0
)

# Get primitive objects
prims = layout.getPrimitiveObjects(types=["pin", "via"])
```

### Selection & Modification

```python
# Select objects
layout.select(objs=["Obj1", "Obj2"])

# Delete objects
layout.delete(objs=["Obj1", "Obj2"])
```

### Unit System

```python
# Get current unit
unit = layout.getUnit()
unit = layout.getUnit2()  # More reliable

# Set unit
old_unit = layout.setUnit("um")
```

### Messages

```python
# Get AEDT messages
messages = layout.getAedtMessage(level=0)
# level: 0=all, 1=warning and above, 2=error only

# Add message
layout.addAedtmessage("Custom message", level=0)
```

### EDB App

```python
# Get EDB app
edb_app = layout.getEdbApp()

# Refresh EDB app
layout.refreshEdbApp()
```

### Logging

```python
# Set log path
layout.setLogPath("custom.log")
```

### Process Control

```python
# Kill AEDT process
layout.killProcess()

# Quit AEDT
layout.quitAedt(force=False)

# Release resources
layout.release()
```

### Design Operations

```python
# Copy design
layout.copyDesign()

# Paste design
new_name = layout.pasteDesign()

# Assembly layout (3D stacking)
layout.AssemblyLayout(
    layout2=layout2,
    layout1_pin1="U1-1",
    layout1_pin2="U1-2",
    layout2_pin1="U2-1",
    layout2_pin2="U2-2",
    SourceComp=None,
    SolerBall=None,
    flip=False
)

# Place design
layout.placeDesign(
    layout2=layout2,
    layout1_pin1="U1-1",
    layout1_pin2="U1-2",
    layout2_pin1="U2-1",
    layout2_pin2="U2-2",
    flip=False
)

# Merge layouts
layout._merge(
    layout2=layout2,
    solderOnComponents={"U1": ("14mil", "14mil")},
    align=None,
    solderBallSize="14mil,14mil",
    stackupReversed=False,
    prefix=""
)
```

### Script Arguments (Batch Mode)

```python
# Check if running in batch mode
is_batch = Layout.isBatchMode()

# Get script arguments
args = Layout.getScriptArgument()
```

### Relative Path

```python
# Get relative path from project directory
rel_path = layout.getRelPath("/absolute/path/to/file")
```

### License Management

```python
# Enable/disable autosave
enabled = layout.enableAutosave(flag=True)
```

---

## Common Patterns

### Iterating Over Collections

```python
# Iterate over components
for comp in layout.Components:
    print(comp.Name, comp.Part)

# Iterate over nets
for net in layout.Nets:
    print(net.Name)

# Iterate over layers
for layer in layout.Layers:
    print(layer.Name, layer.Thickness)
```

### Filtering Collections

```python
# Filter components by part type
caps = [c for c in layout.Components if c.PartType == "Capacitor"]

# Filter nets by name pattern
import re
sig_nets = [n for n in layout.Nets if re.match(r"SIG\d+", n.Name)]

# Filter by layer
top_objs = layout.Shapes.filterByLayer("Top")
```

### Working with Units

```python
from pyLayout.common.unit import Unit

# Convert units
length = Unit("10mil")
print(length["mm"])    # Convert to mm
print(length["um"])    # Convert to um
print(length.V)        # Get value in meters
```

### Error Handling

```python
try:
    comp = layout.Components["U1"]
except Exception as e:
    print(f"Component not found: {e}")

# Check if object exists
if "U1" in layout.Components:
    comp = layout.Components["U1"]
```

---

## Best Practices

1. **Always initialize design before accessing objects:**
   ```python
   layout.initDesign()
   ```

2. **Use context managers for resource cleanup:**
   ```python
   try:
       # Your code here
       pass
   finally:
       layout.release()
   ```

3. **Refresh collections after modifications:**
   ```python
   layout.Components.push("NewComp")
   layout.Components.refresh()
   ```

4. **Use regex patterns for bulk operations:**
   ```python
   comps = layout.Components["U.*"]
   for comp in comps:
       # Process each component
       pass
   ```

5. **Cache frequently accessed objects:**
   ```python
   # Instead of repeated lookups
   u1 = layout.Components["U1"]
   pins = u1.Pins
   ```

---

## Notes

- All collection objects support lazy loading for performance
- Regex patterns are case-insensitive
- Most methods return `None` on failure and log errors
- Use `layout.Info` to access all layout metadata
- COM objects are automatically managed, but call `release()` when done
- For batch processing, use `Layout.isBatchMode()` to detect execution context

---

## Related Modules

- [`pyLayout.common`](pyLayout\common): Utility modules (logging, units, progress bars)
- [`pyLayout.primitive`](pyLayout\primitive): Primitive object classes
- [`pyLayout.definition`](pyLayout\definition): Definition classes (layers, materials, etc.)
- [`pyLayout.postData`](pyLayout\postData): Solution data handling
- [`pyLayout.edb`](pyLayout\edb): EDB database interface

---

*Generated for agent indexing - Last updated: 2026-05-15*
