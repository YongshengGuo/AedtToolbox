# Notes:  



import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import Application
import math
import decimal
import string
import re
import System.Drawing
import System.Windows.Forms
import System.Drawing.Drawing2D
import logging
import datetime


#from System.Diagnostics import Process
from System import Array
from System.Drawing import *
from System.Windows.Forms import *
from System.Drawing.Drawing2D import *
from System.Windows.Forms import MessageBox

import sys,os
appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)


class MainForm(Form):

	def __init__(self, oDesktop, szPath = None):

#** -- Note!!--  Figure out variables and see which should be strings or ints/floats 
		self.oDesktop = oDesktop
		self.simulate = 0  		  #flag to see if simulate button has been selected
		self.designcounter = 1    #increments Q2D designs so user so allow adding multiple designs in one session
		self.microstrip = 0
		self.SLMS = int(0)
		self.broadside = 0
		self.GCPW = 0
		self.differential = 0
		self.m_sysPath = ''
		self.m_libPath = appDir + "/"
		self.units = 'mil'
		
		self.tracespacing = float()
		self.tracewidth = float()
		self.toptracewidth = float()
		self.bottomtracewidth = float()
		self.maxtracewidth = float()
		self.numberoftraces = int()
		self.diffspacing = float()
		self.tracethickness = float()
		self.planethickness = float()
		self.topdielectricthickness = float()
		self.bottomdielectricthickness = float()
		self.D5thickness = float()
		self.gndwidth = float()

		self.SMdielectricfreq = float(1)
		self.SMdielectricfrequnits = ''
		self.SMEr = float(4)
		self.SMTand = float(0.02)
		
		self.Bdielfreq = float(1)
		self.Bdielectricfrequnits = ''
		self.BdielEr = float(4)
		self.BdielTand = float(0.02)

		self.Tdielfreq = float(1)
		self.Tdielfrequnits = ''
		self.TdielEr = float(4)
		self.TdielTand = float(0.02)

		self.D4dielfreq = float(1)
		self.D4dielfrequnits = ''
		self.D4dielEr = float(4)
		self.D4dielTand = float(0.02)

		self.D5dielfreq = float(1)
		self.D5dielfrequnits = ''
		self.D5dielEr = float(4)
		self.D5dielTand = float(0.02)

		self.etching = 'none'
		self.etchpercent = float(0.0)
		self.etchvalue = 1
		self.roughnesstype = int()
		self.surfaceroughnesstop = float(2.5)
		self.surfaceroughnessSides = float(2.5)
		self.surfaceroughnessbottom = float(2.5)
		self.surfaceroughnessunits = 'um'		
		self.HHsurfaceratiotop = float(2.5)
		self.noduleradiustop = float(0.5)
		self.HHsurfaceratiosides = float(2.5)
		self.noduleradiussides = float(0.5)
		self.HHsurfaceratiobottom = float(2.5)		
		self.noduleradiusbottom = float(0.5)	
		self.plating = False
		self.useplatingmaterial = False
		self.platingmaterial = 'copper'
		self.platingthickness = 0	
		self.platingthicknessunits = 'mil'
		self.soldermaskmaterial = "\"polyimide\""
		self.soldermaskthickness = float()
		self.soldermaskunits = 'mil'
		self.simulate = 0
	
		self.solutionfreq = float(10)
		self.solutionstartfreq = float(0)
		self.solutionstopfreq = float(100)
		self.solutionstepfreq = float(100)
		self.Solutionfrequnits = 'GHz'
		self.StartFrequnits = 'GHz'
		self.StopFrequnits = 'GHz'
		self.FreqStepunits = 'MHz'
		self.freqsweeptype = 'none'	


		self.InitializeComponent()
		
	
		
	def SetDefaults(self):
		self._ANSYSLogoPictureBox.Image = Image.FromFile(self.m_libPath+"Images/ANSYSlogo.png")
		self._etchpictureBox.Image = Image.FromFile(self.m_libPath+"Images/etch1.png")
		self._pictureBox2.Image = Image.FromFile(self.m_libPath+"Images/WelcomeScreen.png")
	
	def InitializeComponent(self):
		self._components = System.ComponentModel.Container()
		self._ToopMenuStrip = System.Windows.Forms.MenuStrip()
		self._fileToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._helpToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._exitToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._aboutToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._TopPanel = System.Windows.Forms.Panel()
		self._pictureBox1 = System.Windows.Forms.PictureBox()
		self._DesignSelectComboBox = System.Windows.Forms.ComboBox()
		self._MainPanel = System.Windows.Forms.Panel()
		self._UnitsGroupBox = System.Windows.Forms.GroupBox()
		self._MillsRadioButton = System.Windows.Forms.RadioButton()
		self._InchesRadioButton = System.Windows.Forms.RadioButton()
		self._MicronsRadioButton = System.Windows.Forms.RadioButton()
		self._MillimetersRadioButton = System.Windows.Forms.RadioButton()
		self._DesignParametersgroupBox = System.Windows.Forms.GroupBox()
		self._PlaneThicknessTextBox = System.Windows.Forms.TextBox()
		self._PlaneThicknesslabel = System.Windows.Forms.Label()
		self._TraceThicknesslabel = System.Windows.Forms.Label()
		self._TraceThicknessTextBox = System.Windows.Forms.TextBox()
		self._TraceSpaceTextBox = System.Windows.Forms.TextBox()
		self._TraceSpacinglabel = System.Windows.Forms.Label()
		self._TraceWidthlabel = System.Windows.Forms.Label()
		self._TraceWidthTextBox = System.Windows.Forms.TextBox()
		self._TopDielectricTextBox = System.Windows.Forms.TextBox()
		self._TopDielectriclabel = System.Windows.Forms.Label()
		self._BottomDielectriclabel = System.Windows.Forms.Label()
		self._BottomDielectricTextBox = System.Windows.Forms.TextBox()
		self._DifferentialSpacingTextBox = System.Windows.Forms.TextBox()
		self._DifferentialSpacinglabel = System.Windows.Forms.Label()
		self._label8 = System.Windows.Forms.Label()
		self._label9 = System.Windows.Forms.Label()
		self._label10 = System.Windows.Forms.Label()
		self._label11 = System.Windows.Forms.Label()
		self._label12 = System.Windows.Forms.Label()
		self._label13 = System.Windows.Forms.Label()
		self._label14 = System.Windows.Forms.Label()
		self._groupBox2 = System.Windows.Forms.GroupBox()
		self._DielPropGroupBox = System.Windows.Forms.GroupBox()
		self._ActionGroupBox = System.Windows.Forms.GroupBox()
		self._SolverUsageGroupBox = System.Windows.Forms.GroupBox()
		self._ZoLabel = System.Windows.Forms.Label()
		self._CalculateButton = System.Windows.Forms.Button()
		self._SimulateButton = System.Windows.Forms.Button()
		self._ModelExportGroupBox = System.Windows.Forms.GroupBox()
		self._TabularRadioButton = System.Windows.Forms.RadioButton()
		self._LumpedElementRadioButton = System.Windows.Forms.RadioButton()
		self._ModelLocationButton = System.Windows.Forms.Button()
		self._ANSYSLogoPictureBox = System.Windows.Forms.PictureBox()
		self._pictureBox2 = System.Windows.Forms.PictureBox()
		self._GUIshow = System.Windows.Forms.RadioButton()
		self._GUIhide = System.Windows.Forms.RadioButton()
		self._tabControl2 = System.Windows.Forms.TabControl()
		self._Simulation_Parameters_Tab = System.Windows.Forms.TabPage()
		self._numberoftraceslabel = System.Windows.Forms.Label()
		self._NumberofTracesTextbox = System.Windows.Forms.TextBox()
		self._label15 = System.Windows.Forms.Label()
		self._SolderMaskThicknessTextBox = System.Windows.Forms.TextBox()
		self._SolderMaskThicknessLabel = System.Windows.Forms.Label()
		self._Zotextbox = System.Windows.Forms.TextBox()
		self._label1 = System.Windows.Forms.Label()
		self._label2 = System.Windows.Forms.Label()
		self._label3 = System.Windows.Forms.Label()
		self._label4 = System.Windows.Forms.Label()
		self._SolutionFreqTextBox = System.Windows.Forms.TextBox()
		self._SolutionFreqLabel = System.Windows.Forms.Label()
		self._FrequencySweepLabel = System.Windows.Forms.Label()
		self._DiscreteRadioButton = System.Windows.Forms.RadioButton()
		self._InterpolatingRadioButton = System.Windows.Forms.RadioButton()
		self._NoneRadioButton = System.Windows.Forms.RadioButton()
		self._StartFreqLabel = System.Windows.Forms.Label()
		self._FreqStopLabel = System.Windows.Forms.Label()
		self._FreqStopTextBox = System.Windows.Forms.TextBox()
		self._FreqStepLabel = System.Windows.Forms.Label()
		self._FreqStepTextBox = System.Windows.Forms.TextBox()
		self._solutionfrequnitscomboBox = System.Windows.Forms.ComboBox()
		self._StartFrequnitscomboBox = System.Windows.Forms.ComboBox()
		self._StopFrequnitscomboBox = System.Windows.Forms.ComboBox()
		self._FreqStepunitscomboBox = System.Windows.Forms.ComboBox()
		self._FreqStartTextBox = System.Windows.Forms.TextBox()
		self._SolutionSetupGroupBox = System.Windows.Forms.GroupBox()
		self._tabPage5 = System.Windows.Forms.TabPage()
		self._trackBar1 = System.Windows.Forms.TrackBar()
		self._etchpictureBox = System.Windows.Forms.PictureBox()
		self._etchfacterlabel = System.Windows.Forms.Label()
		self._toppercentetchlabel = System.Windows.Forms.Label()
		self._overetchradioButton = System.Windows.Forms.RadioButton()
		self._underetchradioButton = System.Windows.Forms.RadioButton()
		self._noetchradioButton = System.Windows.Forms.RadioButton()
		self._tabPage4 = System.Windows.Forms.TabPage()
		self._HurayRadioButton = System.Windows.Forms.RadioButton()
		self._HammerstadRadioButton = System.Windows.Forms.RadioButton()
		self._NoRoughnessRadioButton = System.Windows.Forms.RadioButton()
		self._TopTraceGroupBox = System.Windows.Forms.GroupBox()
		self._HallHurayLabelTop = System.Windows.Forms.Label()
		self._HallHuraytTextBoxTop = System.Windows.Forms.TextBox()
		self._SurfaceRoughTextBoxTop = System.Windows.Forms.TextBox()
		self._SurfaceRoughLabelTop = System.Windows.Forms.Label()
		self._RoughnessUnitsComboBox = System.Windows.Forms.ComboBox()
		self._SidesTraceGroupBox = System.Windows.Forms.GroupBox()
		self._HallHuraytTextBoxSides = System.Windows.Forms.TextBox()
		self._HallHurayLabelSides = System.Windows.Forms.Label()
		self._SurfaceRoughTextBoxSides = System.Windows.Forms.TextBox()
		self._SurfaceRoughLabelSides = System.Windows.Forms.Label()
		self._BottomTraceGroupBox = System.Windows.Forms.GroupBox()
		self._HallHuraytTextBoxBottom = System.Windows.Forms.TextBox()
		self._HallHurayLabelBottom = System.Windows.Forms.Label()
		self._SurfaceRoughTextBoxBottom = System.Windows.Forms.TextBox()
		self._SurfaceRoughLabelBottom = System.Windows.Forms.Label()
		self._RoughnessUnitslabel = System.Windows.Forms.Label()
		self._tabControl3 = System.Windows.Forms.TabControl()
		self._SMgroupbox = System.Windows.Forms.GroupBox()
		self._SMtextBox = System.Windows.Forms.TextBox()
		self._SMunitscomboBox = System.Windows.Forms.ComboBox()
		self._SMErtextBox = System.Windows.Forms.TextBox()
		self._SMTandtextBox = System.Windows.Forms.TextBox()
		self._BottomDielgroupBox = System.Windows.Forms.GroupBox()
		self._BottomDielTandtextBox = System.Windows.Forms.TextBox()
		self._BottomDielErtextBox = System.Windows.Forms.TextBox()
		self._BottomDielcomboBox = System.Windows.Forms.ComboBox()
		self._BottomDieltextBox = System.Windows.Forms.TextBox()
		self._TopDielgroupBox = System.Windows.Forms.GroupBox()
		self._TopDielTandtextBox = System.Windows.Forms.TextBox()
		self._TopDielErtextBox = System.Windows.Forms.TextBox()
		self._TopDielcomboBox = System.Windows.Forms.ComboBox()
		self._TopDieltextBox = System.Windows.Forms.TextBox()
		self._ConductorExampleinputlabel = System.Windows.Forms.Label()
		self._ZoLabelDiff = System.Windows.Forms.Label()
		self._ZotextboxDiff = System.Windows.Forms.TextBox()
		self._IPCeqnsLabel = System.Windows.Forms.Label()
		self._D5textbox = System.Windows.Forms.TextBox()
		self._labelD5 = System.Windows.Forms.Label()
		self._D5thicknesslabel = System.Windows.Forms.Label()
		self._D4groupBox = System.Windows.Forms.GroupBox()
		self._D5groupBox = System.Windows.Forms.GroupBox()
		self._D4textBox = System.Windows.Forms.TextBox()
		self._D4ErtextBox = System.Windows.Forms.TextBox()
		self._D4TandtextBox = System.Windows.Forms.TextBox()
		self._D5dieltextBox = System.Windows.Forms.TextBox()
		self._D5ErtextBox = System.Windows.Forms.TextBox()
		self._D5TandtextBox = System.Windows.Forms.TextBox()
		self._D4comboBox = System.Windows.Forms.ComboBox()
		self._D5comboBox = System.Windows.Forms.ComboBox()
		self._errorProvider1 = System.Windows.Forms.ErrorProvider(self._components)
		self._ToopMenuStrip.SuspendLayout()
		self._TopPanel.SuspendLayout()
		self._pictureBox1.BeginInit()
		self._MainPanel.SuspendLayout()
		self._UnitsGroupBox.SuspendLayout()
		self._DesignParametersgroupBox.SuspendLayout()
		self._DielPropGroupBox.SuspendLayout()
		self._ActionGroupBox.SuspendLayout()
		self._SolverUsageGroupBox.SuspendLayout()
		self._ModelExportGroupBox.SuspendLayout()
		self._ANSYSLogoPictureBox.BeginInit()
		self._pictureBox2.BeginInit()
		self._tabControl2.SuspendLayout()
		self._Simulation_Parameters_Tab.SuspendLayout()
		self._SolutionSetupGroupBox.SuspendLayout()
		self._tabPage5.SuspendLayout()
		self._trackBar1.BeginInit()
		self._etchpictureBox.BeginInit()
		self._tabPage4.SuspendLayout()
		self._TopTraceGroupBox.SuspendLayout()
		self._SidesTraceGroupBox.SuspendLayout()
		self._BottomTraceGroupBox.SuspendLayout()
		self._tabControl3.SuspendLayout()
		self._SMgroupbox.SuspendLayout()
		self._BottomDielgroupBox.SuspendLayout()
		self._TopDielgroupBox.SuspendLayout()
		self._D4groupBox.SuspendLayout()
		self._D5groupBox.SuspendLayout()
		self._errorProvider1.BeginInit()
		self.SuspendLayout()
		# 
		# ToopMenuStrip
		# 
		self._ToopMenuStrip.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._fileToolStripMenuItem,
			self._helpToolStripMenuItem]))
		self._ToopMenuStrip.Location = System.Drawing.Point(0, 0)
		self._ToopMenuStrip.Name = "ToopMenuStrip"
		self._ToopMenuStrip.Size = System.Drawing.Size(1296, 24)
		self._ToopMenuStrip.TabIndex = 0
		self._ToopMenuStrip.Text = "menuStrip1"
		# 
		# fileToolStripMenuItem
		# 
		self._fileToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._exitToolStripMenuItem]))
		self._fileToolStripMenuItem.Name = "fileToolStripMenuItem"
		self._fileToolStripMenuItem.Size = System.Drawing.Size(37, 20)
		self._fileToolStripMenuItem.Text = "File"
		# 
		# helpToolStripMenuItem
		# 
		self._helpToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._aboutToolStripMenuItem]))
		self._helpToolStripMenuItem.Name = "helpToolStripMenuItem"
		self._helpToolStripMenuItem.Size = System.Drawing.Size(44, 20)
		self._helpToolStripMenuItem.Text = "Help"
		# 
		# exitToolStripMenuItem
		# 
		self._exitToolStripMenuItem.Name = "exitToolStripMenuItem"
		self._exitToolStripMenuItem.Size = System.Drawing.Size(92, 22)
		self._exitToolStripMenuItem.Text = "Exit"
		self._exitToolStripMenuItem.Click += self.ExitToolStripMenuItemClick
		# 
		# aboutToolStripMenuItem
		# 
		self._aboutToolStripMenuItem.Name = "aboutToolStripMenuItem"
		self._aboutToolStripMenuItem.Size = System.Drawing.Size(107, 22)
		self._aboutToolStripMenuItem.Text = "About"
		self._aboutToolStripMenuItem.Click += self.AboutToolStripMenuItemClick
		# 
		# TopPanel
		# 
		self._TopPanel.BackColor = System.Drawing.SystemColors.ScrollBar
		self._TopPanel.Controls.Add(self._ANSYSLogoPictureBox)
		self._TopPanel.Controls.Add(self._ModelExportGroupBox)
		self._TopPanel.Controls.Add(self._SolverUsageGroupBox)
		self._TopPanel.Controls.Add(self._UnitsGroupBox)
		self._TopPanel.Dock = System.Windows.Forms.DockStyle.Top
		self._TopPanel.Location = System.Drawing.Point(0, 24)
		self._TopPanel.Name = "TopPanel"
		self._TopPanel.Size = System.Drawing.Size(1296, 74)
		self._TopPanel.TabIndex = 1
		# 
		# pictureBox1
		# 
		self._pictureBox1.Location = System.Drawing.Point(0, 0)
		self._pictureBox1.Name = "pictureBox1"
		self._pictureBox1.Size = System.Drawing.Size(100, 50)
		self._pictureBox1.TabIndex = 0
		self._pictureBox1.TabStop = False
		# 
		# DesignSelectComboBox
		# 
		self._DesignSelectComboBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._DesignSelectComboBox.FormattingEnabled = True
		self._DesignSelectComboBox.Items.AddRange(System.Array[System.Object](
			["Microstrip - Single Ended",
			"Microstrip - Differential",
			"Stripline - Single Ended",
			"Stripline - Differential",
			"Stripline - Broadside Coupled",
			"Grounded Coplanar Waveguide"]))
		self._DesignSelectComboBox.Location = System.Drawing.Point(13, 6)
		self._DesignSelectComboBox.Name = "DesignSelectComboBox"
		self._DesignSelectComboBox.Size = System.Drawing.Size(231, 23)
		self._DesignSelectComboBox.TabIndex = 0
		self._DesignSelectComboBox.Text = "Select Design Type"
		self._DesignSelectComboBox.SelectedIndexChanged += self.DesignSelectComboBoxSelectedIndexChanged
		# 
		# MainPanel
		# 
		self._MainPanel.BackColor = System.Drawing.SystemColors.AppWorkspace
		self._MainPanel.Controls.Add(self._tabControl2)
		self._MainPanel.Controls.Add(self._pictureBox2)
		self._MainPanel.Controls.Add(self._DesignSelectComboBox)
		self._MainPanel.Controls.Add(self._DesignParametersgroupBox)
		self._MainPanel.Controls.Add(self._ActionGroupBox)
		self._MainPanel.Dock = System.Windows.Forms.DockStyle.Top
		self._MainPanel.Location = System.Drawing.Point(0, 98)
		self._MainPanel.Name = "MainPanel"
		self._MainPanel.Size = System.Drawing.Size(1296, 797)
		self._MainPanel.TabIndex = 2
		# 
		# UnitsGroupBox
		# 
		self._UnitsGroupBox.Controls.Add(self._MillimetersRadioButton)
		self._UnitsGroupBox.Controls.Add(self._MicronsRadioButton)
		self._UnitsGroupBox.Controls.Add(self._InchesRadioButton)
		self._UnitsGroupBox.Controls.Add(self._MillsRadioButton)
		self._UnitsGroupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._UnitsGroupBox.Location = System.Drawing.Point(221, 5)
		self._UnitsGroupBox.Name = "UnitsGroupBox"
		self._UnitsGroupBox.Size = System.Drawing.Size(434, 62)
		self._UnitsGroupBox.TabIndex = 0
		self._UnitsGroupBox.TabStop = False
		self._UnitsGroupBox.Text = "Units"
		# 
		# MillsRadioButton
		# 
		self._MillsRadioButton.Checked = True
		self._MillsRadioButton.Location = System.Drawing.Point(33, 22)
		self._MillsRadioButton.Name = "MillsRadioButton"
		self._MillsRadioButton.Size = System.Drawing.Size(104, 24)
		self._MillsRadioButton.TabIndex = 0
		self._MillsRadioButton.TabStop = True
		self._MillsRadioButton.Text = "Mills"
		self._MillsRadioButton.UseVisualStyleBackColor = True
		self._MillsRadioButton.CheckedChanged += self.MillsRadioButtonCheckedChanged
		# 
		# InchesRadioButton
		# 
		self._InchesRadioButton.Location = System.Drawing.Point(118, 16)
		self._InchesRadioButton.Name = "InchesRadioButton"
		self._InchesRadioButton.Size = System.Drawing.Size(104, 36)
		self._InchesRadioButton.TabIndex = 0
		self._InchesRadioButton.Text = "Inches"
		self._InchesRadioButton.UseVisualStyleBackColor = True
		self._InchesRadioButton.CheckedChanged += self.InchesRadioButtonCheckedChanged
		# 
		# MicronsRadioButton
		# 
		self._MicronsRadioButton.Location = System.Drawing.Point(213, 23)
		self._MicronsRadioButton.Name = "MicronsRadioButton"
		self._MicronsRadioButton.Size = System.Drawing.Size(104, 23)
		self._MicronsRadioButton.TabIndex = 0
		self._MicronsRadioButton.Text = "Microns"
		self._MicronsRadioButton.UseVisualStyleBackColor = True
		self._MicronsRadioButton.CheckedChanged += self.MicronsRadioButtonCheckedChanged
		# 
		# MillimetersRadioButton
		# 
		self._MillimetersRadioButton.Location = System.Drawing.Point(312, 22)
		self._MillimetersRadioButton.Name = "MillimetersRadioButton"
		self._MillimetersRadioButton.Size = System.Drawing.Size(104, 24)
		self._MillimetersRadioButton.TabIndex = 0
		self._MillimetersRadioButton.Text = "Millimeters"
		self._MillimetersRadioButton.UseVisualStyleBackColor = True
		self._MillimetersRadioButton.CheckedChanged += self.MillimetersRadioButtonCheckedChanged
		# 
		# DesignParametersgroupBox
		# 
		self._DesignParametersgroupBox.Anchor = System.Windows.Forms.AnchorStyles.Right
		self._DesignParametersgroupBox.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
		self._DesignParametersgroupBox.Controls.Add(self._D5thicknesslabel)
		self._DesignParametersgroupBox.Controls.Add(self._labelD5)
		self._DesignParametersgroupBox.Controls.Add(self._D5textbox)
		self._DesignParametersgroupBox.Controls.Add(self._label15)
		self._DesignParametersgroupBox.Controls.Add(self._SolderMaskThicknessTextBox)
		self._DesignParametersgroupBox.Controls.Add(self._SolderMaskThicknessLabel)
		self._DesignParametersgroupBox.Controls.Add(self._numberoftraceslabel)
		self._DesignParametersgroupBox.Controls.Add(self._NumberofTracesTextbox)
		self._DesignParametersgroupBox.Controls.Add(self._label14)
		self._DesignParametersgroupBox.Controls.Add(self._label13)
		self._DesignParametersgroupBox.Controls.Add(self._label12)
		self._DesignParametersgroupBox.Controls.Add(self._label11)
		self._DesignParametersgroupBox.Controls.Add(self._label10)
		self._DesignParametersgroupBox.Controls.Add(self._label9)
		self._DesignParametersgroupBox.Controls.Add(self._label8)
		self._DesignParametersgroupBox.Controls.Add(self._DifferentialSpacingTextBox)
		self._DesignParametersgroupBox.Controls.Add(self._DifferentialSpacinglabel)
		self._DesignParametersgroupBox.Controls.Add(self._TopDielectricTextBox)
		self._DesignParametersgroupBox.Controls.Add(self._TopDielectriclabel)
		self._DesignParametersgroupBox.Controls.Add(self._BottomDielectriclabel)
		self._DesignParametersgroupBox.Controls.Add(self._BottomDielectricTextBox)
		self._DesignParametersgroupBox.Controls.Add(self._TraceSpaceTextBox)
		self._DesignParametersgroupBox.Controls.Add(self._TraceSpacinglabel)
		self._DesignParametersgroupBox.Controls.Add(self._TraceWidthlabel)
		self._DesignParametersgroupBox.Controls.Add(self._TraceWidthTextBox)
		self._DesignParametersgroupBox.Controls.Add(self._TraceThicknessTextBox)
		self._DesignParametersgroupBox.Controls.Add(self._TraceThicknesslabel)
		self._DesignParametersgroupBox.Controls.Add(self._PlaneThicknesslabel)
		self._DesignParametersgroupBox.Controls.Add(self._PlaneThicknessTextBox)
		self._DesignParametersgroupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._DesignParametersgroupBox.Location = System.Drawing.Point(1006, 18)
		self._DesignParametersgroupBox.Name = "DesignParametersgroupBox"
		self._DesignParametersgroupBox.Size = System.Drawing.Size(278, 317)
		self._DesignParametersgroupBox.TabIndex = 1
		self._DesignParametersgroupBox.TabStop = False
		self._DesignParametersgroupBox.Text = "Design Parameters"
		# 
		# PlaneThicknessTextBox
		# 
		self._PlaneThicknessTextBox.Location = System.Drawing.Point(172, 61)
		self._PlaneThicknessTextBox.Name = "PlaneThicknessTextBox"
		self._PlaneThicknessTextBox.Size = System.Drawing.Size(50, 21)
		self._PlaneThicknessTextBox.TabIndex = 2
		self._PlaneThicknessTextBox.Text = "0.85"
		self._PlaneThicknessTextBox.Visible = False
		self._PlaneThicknessTextBox.TextChanged += self.PlaneThicknessTextBoxTextChanged
		# 
		# PlaneThicknesslabel
		# 
		self._PlaneThicknesslabel.AutoSize = True
		self._PlaneThicknesslabel.Location = System.Drawing.Point(9, 66)
		self._PlaneThicknesslabel.Name = "PlaneThicknesslabel"
		self._PlaneThicknesslabel.Size = System.Drawing.Size(97, 15)
		self._PlaneThicknesslabel.TabIndex = 1
		self._PlaneThicknesslabel.Text = "Plane Thickness"
		self._PlaneThicknesslabel.Visible = False
		# 
		# TraceThicknesslabel
		# 
		self._TraceThicknesslabel.AutoSize = True
		self._TraceThicknesslabel.Location = System.Drawing.Point(9, 97)
		self._TraceThicknesslabel.Name = "TraceThicknesslabel"
		self._TraceThicknesslabel.Size = System.Drawing.Size(96, 15)
		self._TraceThicknesslabel.TabIndex = 2
		self._TraceThicknesslabel.Text = "Trace Thickness"
		self._TraceThicknesslabel.Visible = False
		# 
		# TraceThicknessTextBox
		# 
		self._TraceThicknessTextBox.Location = System.Drawing.Point(172, 91)
		self._TraceThicknessTextBox.Name = "TraceThicknessTextBox"
		self._TraceThicknessTextBox.Size = System.Drawing.Size(50, 21)
		self._TraceThicknessTextBox.TabIndex = 3
		self._TraceThicknessTextBox.Text = "0.85"
		self._TraceThicknessTextBox.Visible = False
		self._TraceThicknessTextBox.TextChanged += self.TraceThicknessTextBoxTextChanged
		# 
		# TraceSpaceTextBox
		# 
		self._TraceSpaceTextBox.Location = System.Drawing.Point(172, 151)
		self._TraceSpaceTextBox.Name = "TraceSpaceTextBox"
		self._TraceSpaceTextBox.Size = System.Drawing.Size(50, 21)
		self._TraceSpaceTextBox.TabIndex = 5
		self._TraceSpaceTextBox.Text = " 8"
		self._TraceSpaceTextBox.Visible = False
		self._TraceSpaceTextBox.TextChanged += self.TraceSpaceTextBoxTextChanged
		# 
		# TraceSpacinglabel
		# 
		self._TraceSpacinglabel.AutoSize = True
		self._TraceSpacinglabel.Location = System.Drawing.Point(9, 157)
		self._TraceSpacinglabel.Name = "TraceSpacinglabel"
		self._TraceSpacinglabel.Size = System.Drawing.Size(86, 15)
		self._TraceSpacinglabel.TabIndex = 6
		self._TraceSpacinglabel.Text = "Trace Spacing"
		self._TraceSpacinglabel.Visible = False
		# 
		# TraceWidthlabel
		# 
		self._TraceWidthlabel.AutoSize = True
		self._TraceWidthlabel.Location = System.Drawing.Point(9, 126)
		self._TraceWidthlabel.Name = "TraceWidthlabel"
		self._TraceWidthlabel.Size = System.Drawing.Size(72, 15)
		self._TraceWidthlabel.TabIndex = 5
		self._TraceWidthlabel.Text = "Trace Width"
		self._TraceWidthlabel.Visible = False
		# 
		# TraceWidthTextBox
		# 
		self._TraceWidthTextBox.Location = System.Drawing.Point(172, 121)
		self._TraceWidthTextBox.Name = "TraceWidthTextBox"
		self._TraceWidthTextBox.Size = System.Drawing.Size(50, 21)
		self._TraceWidthTextBox.TabIndex = 4
		self._TraceWidthTextBox.Text = " 6"
		self._TraceWidthTextBox.Visible = False
		self._TraceWidthTextBox.TextChanged += self.TraceWidthTextBoxTextChanged
		# 
		# TopDielectricTextBox
		# 
		self._TopDielectricTextBox.Location = System.Drawing.Point(172, 211)
		self._TopDielectricTextBox.Name = "TopDielectricTextBox"
		self._TopDielectricTextBox.Size = System.Drawing.Size(50, 21)
		self._TopDielectricTextBox.TabIndex = 7
		self._TopDielectricTextBox.Text = " 6"
		self._TopDielectricTextBox.Visible = False
		self._TopDielectricTextBox.TextChanged += self.TopDielectricTextBoxTextChanged
		# 
		# TopDielectriclabel
		# 
		self._TopDielectriclabel.AutoSize = True
		self._TopDielectriclabel.Location = System.Drawing.Point(9, 217)
		self._TopDielectriclabel.Name = "TopDielectriclabel"
		self._TopDielectriclabel.Size = System.Drawing.Size(82, 15)
		self._TopDielectriclabel.TabIndex = 10
		self._TopDielectriclabel.Text = "Top Dielectric"
		self._TopDielectriclabel.Visible = False
		# 
		# BottomDielectriclabel
		# 
		self._BottomDielectriclabel.AutoSize = True
		self._BottomDielectriclabel.Location = System.Drawing.Point(9, 186)
		self._BottomDielectriclabel.Name = "BottomDielectriclabel"
		self._BottomDielectriclabel.Size = System.Drawing.Size(100, 15)
		self._BottomDielectriclabel.TabIndex = 9
		self._BottomDielectriclabel.Text = "Bottom Dielectric"
		self._BottomDielectriclabel.Visible = False
		# 
		# BottomDielectricTextBox
		# 
		self._BottomDielectricTextBox.Location = System.Drawing.Point(172, 181)
		self._BottomDielectricTextBox.Name = "BottomDielectricTextBox"
		self._BottomDielectricTextBox.Size = System.Drawing.Size(50, 21)
		self._BottomDielectricTextBox.TabIndex = 6
		self._BottomDielectricTextBox.Text = " 3.55"
		self._BottomDielectricTextBox.Visible = False
		self._BottomDielectricTextBox.TextChanged += self.BottomDielectricTextBoxTextChanged
		# 
		# DifferentialSpacingTextBox
		# 
		self._DifferentialSpacingTextBox.Location = System.Drawing.Point(172, 241)
		self._DifferentialSpacingTextBox.Name = "DifferentialSpacingTextBox"
		self._DifferentialSpacingTextBox.Size = System.Drawing.Size(50, 21)
		self._DifferentialSpacingTextBox.TabIndex = 8
		self._DifferentialSpacingTextBox.Text = " 16"
		self._DifferentialSpacingTextBox.Visible = False
		self._DifferentialSpacingTextBox.TextChanged += self.DifferentialSpacingTextBoxTextChanged
		# 
		# DifferentialSpacinglabel
		# 
		self._DifferentialSpacinglabel.AutoSize = True
		self._DifferentialSpacinglabel.Location = System.Drawing.Point(10, 247)
		self._DifferentialSpacinglabel.Name = "DifferentialSpacinglabel"
		self._DifferentialSpacinglabel.Size = System.Drawing.Size(114, 15)
		self._DifferentialSpacinglabel.TabIndex = 12
		self._DifferentialSpacinglabel.Text = "Differential Spacing"
		self._DifferentialSpacinglabel.Visible = False
		# 
		# label8
		# 
		self._label8.Location = System.Drawing.Point(230, 61)
		self._label8.Name = "label8"
		self._label8.Size = System.Drawing.Size(32, 18)
		self._label8.TabIndex = 14
		self._label8.Visible = False
		# 
		# label9
		# 
		self._label9.Location = System.Drawing.Point(230, 91)
		self._label9.Name = "label9"
		self._label9.Size = System.Drawing.Size(32, 18)
		self._label9.TabIndex = 15
		self._label9.Visible = False
		# 
		# label10
		# 
		self._label10.Location = System.Drawing.Point(230, 121)
		self._label10.Name = "label10"
		self._label10.Size = System.Drawing.Size(32, 18)
		self._label10.TabIndex = 16
		self._label10.Visible = False
		# 
		# label11
		# 
		self._label11.Location = System.Drawing.Point(230, 151)
		self._label11.Name = "label11"
		self._label11.Size = System.Drawing.Size(32, 18)
		self._label11.TabIndex = 17
		self._label11.Visible = False
		# 
		# label12
		# 
		self._label12.Location = System.Drawing.Point(230, 181)
		self._label12.Name = "label12"
		self._label12.Size = System.Drawing.Size(32, 18)
		self._label12.TabIndex = 18
		self._label12.Visible = False
		# 
		# label13
		# 
		self._label13.Location = System.Drawing.Point(230, 211)
		self._label13.Name = "label13"
		self._label13.Size = System.Drawing.Size(32, 18)
		self._label13.TabIndex = 19
		self._label13.Visible = False
		# 
		# label14
		# 
		self._label14.Location = System.Drawing.Point(230, 241)
		self._label14.Name = "label14"
		self._label14.Size = System.Drawing.Size(32, 18)
		self._label14.TabIndex = 20
		self._label14.Visible = False
		# 
		# groupBox2
		# 
		self._groupBox2.Anchor = System.Windows.Forms.AnchorStyles.None
		self._groupBox2.AutoSize = True
		self._groupBox2.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._groupBox2.Location = System.Drawing.Point(323, 6)
		self._groupBox2.Name = "groupBox2"
		self._groupBox2.Size = System.Drawing.Size(414, 298)
		self._groupBox2.TabIndex = 16
		self._groupBox2.TabStop = False
		self._groupBox2.Text = "Advanced Conductor Options"
		self._groupBox2.Visible = False
		# 
		# DielPropGroupBox
		# 
		self._DielPropGroupBox.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right
		self._DielPropGroupBox.Controls.Add(self._D4groupBox)
		self._DielPropGroupBox.Controls.Add(self._D5groupBox)
		self._DielPropGroupBox.Controls.Add(self._TopDielgroupBox)
		self._DielPropGroupBox.Controls.Add(self._label1)
		self._DielPropGroupBox.Controls.Add(self._BottomDielgroupBox)
		self._DielPropGroupBox.Controls.Add(self._label3)
		self._DielPropGroupBox.Controls.Add(self._SMgroupbox)
		self._DielPropGroupBox.Controls.Add(self._label4)
		self._DielPropGroupBox.Controls.Add(self._label2)
		self._DielPropGroupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._DielPropGroupBox.Location = System.Drawing.Point(743, 6)
		self._DielPropGroupBox.Name = "DielPropGroupBox"
		self._DielPropGroupBox.Size = System.Drawing.Size(538, 298)
		self._DielPropGroupBox.TabIndex = 17
		self._DielPropGroupBox.TabStop = False
		self._DielPropGroupBox.Text = "Dielectric Properties"
		self._DielPropGroupBox.Visible = False
		# 
		# ActionGroupBox
		# 
		self._ActionGroupBox.Anchor = System.Windows.Forms.AnchorStyles.Right
		self._ActionGroupBox.Controls.Add(self._IPCeqnsLabel)
		self._ActionGroupBox.Controls.Add(self._ZotextboxDiff)
		self._ActionGroupBox.Controls.Add(self._ZoLabelDiff)
		self._ActionGroupBox.Controls.Add(self._Zotextbox)
		self._ActionGroupBox.Controls.Add(self._SimulateButton)
		self._ActionGroupBox.Controls.Add(self._CalculateButton)
		self._ActionGroupBox.Controls.Add(self._ZoLabel)
		self._ActionGroupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ActionGroupBox.Location = System.Drawing.Point(1006, 339)
		self._ActionGroupBox.Margin = System.Windows.Forms.Padding(1)
		self._ActionGroupBox.Name = "ActionGroupBox"
		self._ActionGroupBox.Size = System.Drawing.Size(278, 101)
		self._ActionGroupBox.TabIndex = 18
		self._ActionGroupBox.TabStop = False
		self._ActionGroupBox.Text = "Action"
		# 
		# SolverUsageGroupBox
		# 
		self._SolverUsageGroupBox.Controls.Add(self._GUIhide)
		self._SolverUsageGroupBox.Controls.Add(self._GUIshow)
		self._SolverUsageGroupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._SolverUsageGroupBox.Location = System.Drawing.Point(661, 6)
		self._SolverUsageGroupBox.Name = "SolverUsageGroupBox"
		self._SolverUsageGroupBox.Size = System.Drawing.Size(190, 62)
		self._SolverUsageGroupBox.TabIndex = 0
		self._SolverUsageGroupBox.TabStop = False
		self._SolverUsageGroupBox.Text = "Solver Visability"
		self._SolverUsageGroupBox.Visible = False
		# 
		# ZoLabel
		# 
		self._ZoLabel.AutoSize = True
		self._ZoLabel.Location = System.Drawing.Point(159, 26)
		self._ZoLabel.Name = "ZoLabel"
		self._ZoLabel.Size = System.Drawing.Size(30, 15)
		self._ZoLabel.TabIndex = 0
		self._ZoLabel.Text = "Zo:  "
		self._ZoLabel.Visible = False
		# 
		# CalculateButton
		# 
		self._CalculateButton.Anchor = System.Windows.Forms.AnchorStyles.Left
		self._CalculateButton.AutoSize = True
		self._CalculateButton.Location = System.Drawing.Point(23, 22)
		self._CalculateButton.Name = "CalculateButton"
		self._CalculateButton.Size = System.Drawing.Size(79, 28)
		self._CalculateButton.TabIndex = 37
		self._CalculateButton.TabStop = False
		self._CalculateButton.Text = "Calculate"
		self._CalculateButton.UseVisualStyleBackColor = True
		self._CalculateButton.Visible = False
		self._CalculateButton.Click += self.CalculatebButtonClick
		# 
		# SimulateButton
		# 
		self._SimulateButton.Anchor = System.Windows.Forms.AnchorStyles.Left
		self._SimulateButton.Location = System.Drawing.Point(23, 61)
		self._SimulateButton.Name = "SimulateButton"
		self._SimulateButton.Size = System.Drawing.Size(79, 28)
		self._SimulateButton.TabIndex = 38
		self._SimulateButton.TabStop = False
		self._SimulateButton.Text = "Create"
		self._SimulateButton.UseVisualStyleBackColor = True
		self._SimulateButton.Visible = False
		self._SimulateButton.Click += self.SimulateButtonClick
		# 
		# ModelExportGroupBox
		# 
		self._ModelExportGroupBox.Controls.Add(self._ModelLocationButton)
		self._ModelExportGroupBox.Controls.Add(self._LumpedElementRadioButton)
		self._ModelExportGroupBox.Controls.Add(self._TabularRadioButton)
		self._ModelExportGroupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ModelExportGroupBox.Location = System.Drawing.Point(857, 5)
		self._ModelExportGroupBox.Name = "ModelExportGroupBox"
		self._ModelExportGroupBox.Size = System.Drawing.Size(415, 62)
		self._ModelExportGroupBox.TabIndex = 0
		self._ModelExportGroupBox.TabStop = False
		self._ModelExportGroupBox.Text = "Model Export"
		self._ModelExportGroupBox.Visible = False
		# 
		# TabularRadioButton
		# 
		self._TabularRadioButton.AutoSize = True
		self._TabularRadioButton.Location = System.Drawing.Point(10, 25)
		self._TabularRadioButton.Name = "TabularRadioButton"
		self._TabularRadioButton.Size = System.Drawing.Size(130, 19)
		self._TabularRadioButton.TabIndex = 0
		self._TabularRadioButton.Text = "Tabular W-element"
		self._TabularRadioButton.UseVisualStyleBackColor = True
		self._TabularRadioButton.CheckedChanged += self.TabularRadioButtonCheckedChanged
		# 
		# LumpedElementRadioButton
		# 
		self._LumpedElementRadioButton.AutoSize = True
		self._LumpedElementRadioButton.Location = System.Drawing.Point(168, 25)
		self._LumpedElementRadioButton.Name = "LumpedElementRadioButton"
		self._LumpedElementRadioButton.Size = System.Drawing.Size(120, 19)
		self._LumpedElementRadioButton.TabIndex = 0
		self._LumpedElementRadioButton.Text = "Lumped Element"
		self._LumpedElementRadioButton.UseVisualStyleBackColor = True
		self._LumpedElementRadioButton.CheckedChanged += self.LumpedElementRadioButtonCheckedChanged
		# 
		# ModelLocationButton
		# 
		self._ModelLocationButton.AutoSize = True
		self._ModelLocationButton.BackColor = System.Drawing.SystemColors.ControlDarkDark
		self._ModelLocationButton.Cursor = System.Windows.Forms.Cursors.Default
		self._ModelLocationButton.Location = System.Drawing.Point(317, 22)
		self._ModelLocationButton.Name = "ModelLocationButton"
		self._ModelLocationButton.Size = System.Drawing.Size(83, 30)
		self._ModelLocationButton.TabIndex = 0
		self._ModelLocationButton.Text = "Location.."
		self._ModelLocationButton.UseVisualStyleBackColor = True
		self._ModelLocationButton.Click += self.ModelLocationButtonClick
		# 
		# ANSYSLogoPictureBox
		# 
		self._ANSYSLogoPictureBox.Location = System.Drawing.Point(4, 6)
		self._ANSYSLogoPictureBox.Name = "ANSYSLogoPictureBox"
		self._ANSYSLogoPictureBox.Size = System.Drawing.Size(202, 62)
		self._ANSYSLogoPictureBox.TabIndex = 4
		self._ANSYSLogoPictureBox.TabStop = False
		# 
		# pictureBox2
		# 
		self._pictureBox2.Location = System.Drawing.Point(13, 34)
		self._pictureBox2.Name = "pictureBox2"
		self._pictureBox2.Size = System.Drawing.Size(978, 406)
		self._pictureBox2.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._pictureBox2.TabIndex = 19
		self._pictureBox2.TabStop = False
		# 
		# GUIshow
		# 
		self._GUIshow.AutoSize = True
		self._GUIshow.Location = System.Drawing.Point(15, 25)
		self._GUIshow.Name = "GUIshow"
		self._GUIshow.Size = System.Drawing.Size(56, 19)
		self._GUIshow.TabIndex = 0
		self._GUIshow.Text = "Show"
		self._GUIshow.UseVisualStyleBackColor = True
		self._GUIshow.CheckedChanged += self.GUIshowCheckedChanged
		# 
		# GUIhide
		# 
		self._GUIhide.AutoSize = True
		self._GUIhide.Location = System.Drawing.Point(115, 25)
		self._GUIhide.Name = "GUIhide"
		self._GUIhide.Size = System.Drawing.Size(51, 19)
		self._GUIhide.TabIndex = 1
		self._GUIhide.Text = "Hide"
		self._GUIhide.UseVisualStyleBackColor = True
		self._GUIhide.CheckedChanged += self.GUIhideCheckedChanged
		# 
		# tabControl2
		# 
		self._tabControl2.Controls.Add(self._Simulation_Parameters_Tab)
		self._tabControl2.Location = System.Drawing.Point(0, 441)
		self._tabControl2.Name = "tabControl2"
		self._tabControl2.SelectedIndex = 0
		self._tabControl2.Size = System.Drawing.Size(1295, 339)
		self._tabControl2.TabIndex = 20
		# 
		# Simulation_Parameters_Tab
		# 
		self._Simulation_Parameters_Tab.BackColor = System.Drawing.Color.LightGray
		self._Simulation_Parameters_Tab.Controls.Add(self._tabControl3)
		self._Simulation_Parameters_Tab.Controls.Add(self._SolutionSetupGroupBox)
		self._Simulation_Parameters_Tab.Controls.Add(self._groupBox2)
		self._Simulation_Parameters_Tab.Controls.Add(self._DielPropGroupBox)
		self._Simulation_Parameters_Tab.Location = System.Drawing.Point(4, 22)
		self._Simulation_Parameters_Tab.Name = "Simulation_Parameters_Tab"
		self._Simulation_Parameters_Tab.Padding = System.Windows.Forms.Padding(3)
		self._Simulation_Parameters_Tab.Size = System.Drawing.Size(1287, 313)
		self._Simulation_Parameters_Tab.TabIndex = 0
		self._Simulation_Parameters_Tab.Text = "Simulation Parameters"
		# 
		# numberoftraceslabel
		# 
		self._numberoftraceslabel.AutoSize = True
		self._numberoftraceslabel.Location = System.Drawing.Point(9, 35)
		self._numberoftraceslabel.Name = "numberoftraceslabel"
		self._numberoftraceslabel.Size = System.Drawing.Size(105, 15)
		self._numberoftraceslabel.TabIndex = 22
		self._numberoftraceslabel.Text = "Number of Traces"
		self._numberoftraceslabel.Visible = False
		# 
		# NumberofTracesTextbox
		# 
		self._NumberofTracesTextbox.Location = System.Drawing.Point(172, 30)
		self._NumberofTracesTextbox.Name = "NumberofTracesTextbox"
		self._NumberofTracesTextbox.Size = System.Drawing.Size(50, 21)
		self._NumberofTracesTextbox.TabIndex = 1
		self._NumberofTracesTextbox.Text = "4"
		self._NumberofTracesTextbox.Visible = False
		self._NumberofTracesTextbox.TextChanged += self.NumberofTracesTextboxTextChanged
		# 
		# label15
		# 
		self._label15.Location = System.Drawing.Point(230, 271)
		self._label15.Name = "label15"
		self._label15.Size = System.Drawing.Size(32, 18)
		self._label15.TabIndex = 25
		self._label15.Visible = False
		# 
		# SolderMaskThicknessTextBox
		# 
		self._SolderMaskThicknessTextBox.Location = System.Drawing.Point(172, 273)
		self._SolderMaskThicknessTextBox.Name = "SolderMaskThicknessTextBox"
		self._SolderMaskThicknessTextBox.Size = System.Drawing.Size(50, 21)
		self._SolderMaskThicknessTextBox.TabIndex = 9
		self._SolderMaskThicknessTextBox.Text = " 0.5"
		self._SolderMaskThicknessTextBox.Visible = False
		self._SolderMaskThicknessTextBox.TextChanged += self.SolderMaskThicknessTextBoxTextChanged
		# 
		# SolderMaskThicknessLabel
		# 
		self._SolderMaskThicknessLabel.AutoSize = True
		self._SolderMaskThicknessLabel.Location = System.Drawing.Point(10, 276)
		self._SolderMaskThicknessLabel.Name = "SolderMaskThicknessLabel"
		self._SolderMaskThicknessLabel.Size = System.Drawing.Size(131, 15)
		self._SolderMaskThicknessLabel.TabIndex = 23
		self._SolderMaskThicknessLabel.Text = "Soldermask Thickness"
		self._SolderMaskThicknessLabel.Visible = False
		# 
		# Zotextbox
		# 
		self._Zotextbox.Location = System.Drawing.Point(198, 23)
		self._Zotextbox.Name = "Zotextbox"
		self._Zotextbox.Size = System.Drawing.Size(55, 21)
		self._Zotextbox.TabIndex = 0
		self._Zotextbox.TabStop = False
		self._Zotextbox.Visible = False
		# 
		# label1
		# 
		self._label1.Font = System.Drawing.Font("Microsoft Sans Serif", 10.2, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._label1.Location = System.Drawing.Point(12, 26)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(508, 44)
		self._label1.TabIndex = 1
		self._label1.Text = "Fill in material characteristics, example values preloaded.  Values will automatically be fit with Djordjevic-Sarker Model"
		self._label1.TextAlign = System.Drawing.ContentAlignment.TopCenter
		# 
		# label2
		# 
		self._label2.Location = System.Drawing.Point(13, 135)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(102, 23)
		self._label2.TabIndex = 2
		self._label2.Text = "Frequency:"
		# 
		# label3
		# 
		self._label3.Location = System.Drawing.Point(12, 174)
		self._label3.Name = "label3"
		self._label3.Size = System.Drawing.Size(102, 44)
		self._label3.TabIndex = 3
		self._label3.Text = "Relative Permittivity:"
		# 
		# label4
		# 
		self._label4.Location = System.Drawing.Point(13, 235)
		self._label4.Name = "label4"
		self._label4.Size = System.Drawing.Size(104, 23)
		self._label4.TabIndex = 4
		self._label4.Text = "Loss Tangent:"
		# 
		# SolutionFreqTextBox
		# 
		self._SolutionFreqTextBox.Location = System.Drawing.Point(147, 24)
		self._SolutionFreqTextBox.Name = "SolutionFreqTextBox"
		self._SolutionFreqTextBox.Size = System.Drawing.Size(62, 21)
		self._SolutionFreqTextBox.TabIndex = 10
		self._SolutionFreqTextBox.Text = "10"
		self._SolutionFreqTextBox.TextChanged += self.SolutionFreqTextBoxTextChanged
		# 
		# SolutionFreqLabel
		# 
		self._SolutionFreqLabel.AutoSize = True
		self._SolutionFreqLabel.Location = System.Drawing.Point(6, 27)
		self._SolutionFreqLabel.Name = "SolutionFreqLabel"
		self._SolutionFreqLabel.Size = System.Drawing.Size(112, 15)
		self._SolutionFreqLabel.TabIndex = 1
		self._SolutionFreqLabel.Text = "Solution Frequency"
		# 
		# FrequencySweepLabel
		# 
		self._FrequencySweepLabel.AutoSize = True
		self._FrequencySweepLabel.Location = System.Drawing.Point(6, 57)
		self._FrequencySweepLabel.Name = "FrequencySweepLabel"
		self._FrequencySweepLabel.Size = System.Drawing.Size(105, 15)
		self._FrequencySweepLabel.TabIndex = 3
		self._FrequencySweepLabel.Text = "Frequency Sweep"
		# 
		# DiscreteRadioButton
		# 
		self._DiscreteRadioButton.AutoSize = True
		self._DiscreteRadioButton.Location = System.Drawing.Point(95, 84)
		self._DiscreteRadioButton.Name = "DiscreteRadioButton"
		self._DiscreteRadioButton.Size = System.Drawing.Size(70, 19)
		self._DiscreteRadioButton.TabIndex = 0
		self._DiscreteRadioButton.Text = "Discrete"
		self._DiscreteRadioButton.UseVisualStyleBackColor = True
		self._DiscreteRadioButton.CheckedChanged += self.DiscreteRadioButtonCheckedChanged
		# 
		# InterpolatingRadioButton
		# 
		self._InterpolatingRadioButton.AutoSize = True
		self._InterpolatingRadioButton.Location = System.Drawing.Point(190, 84)
		self._InterpolatingRadioButton.Name = "InterpolatingRadioButton"
		self._InterpolatingRadioButton.Size = System.Drawing.Size(93, 19)
		self._InterpolatingRadioButton.TabIndex = 0
		self._InterpolatingRadioButton.Text = "Interpolating"
		self._InterpolatingRadioButton.UseVisualStyleBackColor = True
		self._InterpolatingRadioButton.CheckedChanged += self.InterpolatingRadioButtonCheckedChanged
		# 
		# NoneRadioButton
		# 
		self._NoneRadioButton.AutoSize = True
		self._NoneRadioButton.Checked = True
		self._NoneRadioButton.Location = System.Drawing.Point(20, 84)
		self._NoneRadioButton.Name = "NoneRadioButton"
		self._NoneRadioButton.Size = System.Drawing.Size(55, 19)
		self._NoneRadioButton.TabIndex = 0
		self._NoneRadioButton.TabStop = True
		self._NoneRadioButton.Text = "None"
		self._NoneRadioButton.UseVisualStyleBackColor = True
		self._NoneRadioButton.CheckedChanged += self.NoneRadioButtonCheckedChanged
		# 
		# StartFreqLabel
		# 
		self._StartFreqLabel.AutoSize = True
		self._StartFreqLabel.Location = System.Drawing.Point(20, 123)
		self._StartFreqLabel.Name = "StartFreqLabel"
		self._StartFreqLabel.Size = System.Drawing.Size(92, 15)
		self._StartFreqLabel.TabIndex = 7
		self._StartFreqLabel.Text = "Frequency Start"
		self._StartFreqLabel.Visible = False
		# 
		# FreqStopLabel
		# 
		self._FreqStopLabel.AutoSize = True
		self._FreqStopLabel.Location = System.Drawing.Point(20, 160)
		self._FreqStopLabel.Name = "FreqStopLabel"
		self._FreqStopLabel.Size = System.Drawing.Size(92, 15)
		self._FreqStopLabel.TabIndex = 10
		self._FreqStopLabel.Text = "Frequency Stop"
		self._FreqStopLabel.Visible = False
		# 
		# FreqStopTextBox
		# 
		self._FreqStopTextBox.Location = System.Drawing.Point(139, 157)
		self._FreqStopTextBox.Name = "FreqStopTextBox"
		self._FreqStopTextBox.Size = System.Drawing.Size(62, 21)
		self._FreqStopTextBox.TabIndex = 14
		self._FreqStopTextBox.Text = "100"
		self._FreqStopTextBox.Visible = False
		self._FreqStopTextBox.TextChanged += self.FreqStopTextBoxTextChanged
		# 
		# FreqStepLabel
		# 
		self._FreqStepLabel.AutoSize = True
		self._FreqStepLabel.Location = System.Drawing.Point(20, 197)
		self._FreqStepLabel.Name = "FreqStepLabel"
		self._FreqStepLabel.Size = System.Drawing.Size(92, 15)
		self._FreqStepLabel.TabIndex = 13
		self._FreqStepLabel.Text = "Frequency Step"
		self._FreqStepLabel.Visible = False
		# 
		# FreqStepTextBox
		# 
		self._FreqStepTextBox.Location = System.Drawing.Point(139, 194)
		self._FreqStepTextBox.Name = "FreqStepTextBox"
		self._FreqStepTextBox.Size = System.Drawing.Size(62, 21)
		self._FreqStepTextBox.TabIndex = 16
		self._FreqStepTextBox.Text = "100"
		self._FreqStepTextBox.Visible = False
		self._FreqStepTextBox.TextChanged += self.FreqStepTextBoxTextChanged
		# 
		# solutionfrequnitscomboBox
		# 
		self._solutionfrequnitscomboBox.FormattingEnabled = True
		self._solutionfrequnitscomboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._solutionfrequnitscomboBox.Location = System.Drawing.Point(215, 24)
		self._solutionfrequnitscomboBox.Name = "solutionfrequnitscomboBox"
		self._solutionfrequnitscomboBox.Size = System.Drawing.Size(60, 23)
		self._solutionfrequnitscomboBox.TabIndex = 11
		self._solutionfrequnitscomboBox.Text = "GHz"
		self._solutionfrequnitscomboBox.SelectedIndexChanged += self.SolutionfrequnitscomboBoxSelectedIndexChanged
		# 
		# StartFrequnitscomboBox
		# 
		self._StartFrequnitscomboBox.FormattingEnabled = True
		self._StartFrequnitscomboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._StartFrequnitscomboBox.Location = System.Drawing.Point(207, 118)
		self._StartFrequnitscomboBox.Name = "StartFrequnitscomboBox"
		self._StartFrequnitscomboBox.Size = System.Drawing.Size(61, 23)
		self._StartFrequnitscomboBox.TabIndex = 13
		self._StartFrequnitscomboBox.Text = "GHz"
		self._StartFrequnitscomboBox.Visible = False
		self._StartFrequnitscomboBox.SelectedIndexChanged += self.StartFrequnitscomboBoxSelectedIndexChanged
		# 
		# StopFrequnitscomboBox
		# 
		self._StopFrequnitscomboBox.FormattingEnabled = True
		self._StopFrequnitscomboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._StopFrequnitscomboBox.Location = System.Drawing.Point(207, 157)
		self._StopFrequnitscomboBox.Name = "StopFrequnitscomboBox"
		self._StopFrequnitscomboBox.Size = System.Drawing.Size(61, 23)
		self._StopFrequnitscomboBox.TabIndex = 15
		self._StopFrequnitscomboBox.Text = "GHz"
		self._StopFrequnitscomboBox.Visible = False
		self._StopFrequnitscomboBox.SelectedIndexChanged += self.StopFrequnitscomboBoxSelectedIndexChanged
		# 
		# FreqStepunitscomboBox
		# 
		self._FreqStepunitscomboBox.FormattingEnabled = True
		self._FreqStepunitscomboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._FreqStepunitscomboBox.Location = System.Drawing.Point(207, 194)
		self._FreqStepunitscomboBox.Name = "FreqStepunitscomboBox"
		self._FreqStepunitscomboBox.Size = System.Drawing.Size(61, 23)
		self._FreqStepunitscomboBox.TabIndex = 17
		self._FreqStepunitscomboBox.Text = "MHz"
		self._FreqStepunitscomboBox.Visible = False
		self._FreqStepunitscomboBox.SelectedIndexChanged += self.FreqStepunitscomboBoxSelectedIndexChanged
		# 
		# FreqStartTextBox
		# 
		self._FreqStartTextBox.Location = System.Drawing.Point(140, 118)
		self._FreqStartTextBox.Name = "FreqStartTextBox"
		self._FreqStartTextBox.Size = System.Drawing.Size(62, 21)
		self._FreqStartTextBox.TabIndex = 12
		self._FreqStartTextBox.Text = "0"
		self._FreqStartTextBox.Visible = False
		self._FreqStartTextBox.TextChanged += self.FreqStartTextBoxTextChanged
		# 
		# SolutionSetupGroupBox
		# 
		self._SolutionSetupGroupBox.Anchor = System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left
		self._SolutionSetupGroupBox.AutoSize = True
		self._SolutionSetupGroupBox.Controls.Add(self._FreqStartTextBox)
		self._SolutionSetupGroupBox.Controls.Add(self._FreqStepunitscomboBox)
		self._SolutionSetupGroupBox.Controls.Add(self._StopFrequnitscomboBox)
		self._SolutionSetupGroupBox.Controls.Add(self._StartFrequnitscomboBox)
		self._SolutionSetupGroupBox.Controls.Add(self._solutionfrequnitscomboBox)
		self._SolutionSetupGroupBox.Controls.Add(self._FreqStepTextBox)
		self._SolutionSetupGroupBox.Controls.Add(self._FreqStepLabel)
		self._SolutionSetupGroupBox.Controls.Add(self._FreqStopTextBox)
		self._SolutionSetupGroupBox.Controls.Add(self._FreqStopLabel)
		self._SolutionSetupGroupBox.Controls.Add(self._StartFreqLabel)
		self._SolutionSetupGroupBox.Controls.Add(self._NoneRadioButton)
		self._SolutionSetupGroupBox.Controls.Add(self._InterpolatingRadioButton)
		self._SolutionSetupGroupBox.Controls.Add(self._DiscreteRadioButton)
		self._SolutionSetupGroupBox.Controls.Add(self._FrequencySweepLabel)
		self._SolutionSetupGroupBox.Controls.Add(self._SolutionFreqLabel)
		self._SolutionSetupGroupBox.Controls.Add(self._SolutionFreqTextBox)
		self._SolutionSetupGroupBox.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._SolutionSetupGroupBox.Location = System.Drawing.Point(9, 6)
		self._SolutionSetupGroupBox.Name = "SolutionSetupGroupBox"
		self._SolutionSetupGroupBox.Size = System.Drawing.Size(308, 298)
		self._SolutionSetupGroupBox.TabIndex = 0
		self._SolutionSetupGroupBox.TabStop = False
		self._SolutionSetupGroupBox.Text = "Solution Setup "
		self._SolutionSetupGroupBox.Visible = False
		# 
		# tabPage5
		# 
		self._tabPage5.Controls.Add(self._noetchradioButton)
		self._tabPage5.Controls.Add(self._underetchradioButton)
		self._tabPage5.Controls.Add(self._overetchradioButton)
		self._tabPage5.Controls.Add(self._toppercentetchlabel)
		self._tabPage5.Controls.Add(self._etchfacterlabel)
		self._tabPage5.Controls.Add(self._etchpictureBox)
		self._tabPage5.Controls.Add(self._trackBar1)
		self._tabPage5.Location = System.Drawing.Point(4, 22)
		self._tabPage5.Name = "tabPage5"
		self._tabPage5.Padding = System.Windows.Forms.Padding(3)
		self._tabPage5.Size = System.Drawing.Size(383, 242)
		self._tabPage5.TabIndex = 1
		self._tabPage5.Text = "Trace Etching"
		self._tabPage5.UseVisualStyleBackColor = True
		# 
		# trackBar1
		# 
		self._trackBar1.Location = System.Drawing.Point(7, 149)
		self._trackBar1.Maximum = 51
		self._trackBar1.Minimum = 1
		self._trackBar1.Name = "trackBar1"
		self._trackBar1.Size = System.Drawing.Size(370, 45)
		self._trackBar1.TabIndex = 1
		self._trackBar1.Value = 1
		self._trackBar1.Visible = False
		self._trackBar1.Scroll += self.TrackBar1Scroll
		# 
		# etchpictureBox
		# 
		self._etchpictureBox.Location = System.Drawing.Point(7, 0)
		self._etchpictureBox.Name = "etchpictureBox"
		self._etchpictureBox.Size = System.Drawing.Size(370, 142)
		self._etchpictureBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._etchpictureBox.TabIndex = 2
		self._etchpictureBox.TabStop = False
		# 
		# etchfacterlabel
		# 
		self._etchfacterlabel.AutoSize = True
		self._etchfacterlabel.Location = System.Drawing.Point(15, 119)
		self._etchfacterlabel.Name = "etchfacterlabel"
		self._etchfacterlabel.Size = System.Drawing.Size(71, 13)
		self._etchfacterlabel.TabIndex = 3
		self._etchfacterlabel.Text = "Etch Factor:  "
		self._etchfacterlabel.Visible = False
		# 
		# toppercentetchlabel
		# 
		self._toppercentetchlabel.AutoSize = True
		self._toppercentetchlabel.Location = System.Drawing.Point(143, 119)
		self._toppercentetchlabel.Name = "toppercentetchlabel"
		self._toppercentetchlabel.Size = System.Drawing.Size(108, 13)
		self._toppercentetchlabel.TabIndex = 4
		self._toppercentetchlabel.Text = "Top as % of Bottom:  "
		self._toppercentetchlabel.Visible = False
		# 
		# overetchradioButton
		# 
		self._overetchradioButton.Location = System.Drawing.Point(94, 5)
		self._overetchradioButton.Name = "overetchradioButton"
		self._overetchradioButton.Size = System.Drawing.Size(103, 29)
		self._overetchradioButton.TabIndex = 5
		self._overetchradioButton.Text = "Over Etch"
		self._overetchradioButton.UseVisualStyleBackColor = True
		self._overetchradioButton.CheckedChanged += self.OveretchradioButtonCheckedChanged
		# 
		# underetchradioButton
		# 
		self._underetchradioButton.Location = System.Drawing.Point(206, 5)
		self._underetchradioButton.Name = "underetchradioButton"
		self._underetchradioButton.Size = System.Drawing.Size(112, 29)
		self._underetchradioButton.TabIndex = 6
		self._underetchradioButton.Text = "Under Etch"
		self._underetchradioButton.UseVisualStyleBackColor = True
		self._underetchradioButton.CheckedChanged += self.UnderetchradioButtonCheckedChanged
		# 
		# noetchradioButton
		# 
		self._noetchradioButton.Checked = True
		self._noetchradioButton.Location = System.Drawing.Point(15, 5)
		self._noetchradioButton.Name = "noetchradioButton"
		self._noetchradioButton.Size = System.Drawing.Size(67, 29)
		self._noetchradioButton.TabIndex = 7
		self._noetchradioButton.TabStop = True
		self._noetchradioButton.Text = "None"
		self._noetchradioButton.UseVisualStyleBackColor = True
		self._noetchradioButton.CheckedChanged += self.NoetchradioButtonCheckedChanged
		# 
		# tabPage4
		# 
		self._tabPage4.BackColor = System.Drawing.Color.LightGray
		self._tabPage4.Controls.Add(self._ConductorExampleinputlabel)
		self._tabPage4.Controls.Add(self._RoughnessUnitslabel)
		self._tabPage4.Controls.Add(self._BottomTraceGroupBox)
		self._tabPage4.Controls.Add(self._SidesTraceGroupBox)
		self._tabPage4.Controls.Add(self._RoughnessUnitsComboBox)
		self._tabPage4.Controls.Add(self._TopTraceGroupBox)
		self._tabPage4.Controls.Add(self._NoRoughnessRadioButton)
		self._tabPage4.Controls.Add(self._HammerstadRadioButton)
		self._tabPage4.Controls.Add(self._HurayRadioButton)
		self._tabPage4.Location = System.Drawing.Point(4, 22)
		self._tabPage4.Name = "tabPage4"
		self._tabPage4.Padding = System.Windows.Forms.Padding(3)
		self._tabPage4.Size = System.Drawing.Size(383, 242)
		self._tabPage4.TabIndex = 0
		self._tabPage4.Text = "Surface Roughness Modeling"
		# 
		# HurayRadioButton
		# 
		self._HurayRadioButton.AutoSize = True
		self._HurayRadioButton.Location = System.Drawing.Point(252, 4)
		self._HurayRadioButton.Name = "HurayRadioButton"
		self._HurayRadioButton.Size = System.Drawing.Size(53, 17)
		self._HurayRadioButton.TabIndex = 0
		self._HurayRadioButton.Text = "Huray"
		self._HurayRadioButton.UseVisualStyleBackColor = True
		self._HurayRadioButton.CheckedChanged += self.HurayRadioButtonCheckedChanged
		# 
		# HammerstadRadioButton
		# 
		self._HammerstadRadioButton.AutoSize = True
		self._HammerstadRadioButton.Location = System.Drawing.Point(83, 4)
		self._HammerstadRadioButton.Name = "HammerstadRadioButton"
		self._HammerstadRadioButton.Size = System.Drawing.Size(121, 17)
		self._HammerstadRadioButton.TabIndex = 0
		self._HammerstadRadioButton.Text = "Hammerstad-Jensen"
		self._HammerstadRadioButton.UseVisualStyleBackColor = True
		self._HammerstadRadioButton.CheckedChanged += self.HammerstadRadioButtonCheckedChanged
		# 
		# NoRoughnessRadioButton
		# 
		self._NoRoughnessRadioButton.AutoSize = True
		self._NoRoughnessRadioButton.Checked = True
		self._NoRoughnessRadioButton.Location = System.Drawing.Point(8, 4)
		self._NoRoughnessRadioButton.Name = "NoRoughnessRadioButton"
		self._NoRoughnessRadioButton.Size = System.Drawing.Size(51, 17)
		self._NoRoughnessRadioButton.TabIndex = 0
		self._NoRoughnessRadioButton.TabStop = True
		self._NoRoughnessRadioButton.Text = "None"
		self._NoRoughnessRadioButton.UseVisualStyleBackColor = True
		self._NoRoughnessRadioButton.CheckedChanged += self.NoRoughnessRadioButtonCheckedChanged
		# 
		# TopTraceGroupBox
		# 
		self._TopTraceGroupBox.BackColor = System.Drawing.Color.Transparent
		self._TopTraceGroupBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center
		self._TopTraceGroupBox.Controls.Add(self._SurfaceRoughLabelTop)
		self._TopTraceGroupBox.Controls.Add(self._SurfaceRoughTextBoxTop)
		self._TopTraceGroupBox.Controls.Add(self._HallHuraytTextBoxTop)
		self._TopTraceGroupBox.Controls.Add(self._HallHurayLabelTop)
		self._TopTraceGroupBox.Location = System.Drawing.Point(10, 35)
		self._TopTraceGroupBox.Name = "TopTraceGroupBox"
		self._TopTraceGroupBox.Padding = System.Windows.Forms.Padding(1)
		self._TopTraceGroupBox.Size = System.Drawing.Size(253, 65)
		self._TopTraceGroupBox.TabIndex = 14
		self._TopTraceGroupBox.TabStop = False
		self._TopTraceGroupBox.Text = "Top of Trace"
		self._TopTraceGroupBox.Visible = False
		# 
		# HallHurayLabelTop
		# 
		self._HallHurayLabelTop.AutoSize = True
		self._HallHurayLabelTop.Font = System.Drawing.Font("Microsoft Sans Serif", 7.20000029, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._HallHurayLabelTop.Location = System.Drawing.Point(5, 17)
		self._HallHurayLabelTop.Name = "HallHurayLabelTop"
		self._HallHurayLabelTop.Size = System.Drawing.Size(120, 13)
		self._HallHurayLabelTop.TabIndex = 10
		self._HallHurayLabelTop.Text = "Hall-Huray Surface Ratio"
		# 
		# HallHuraytTextBoxTop
		# 
		self._HallHuraytTextBoxTop.Location = System.Drawing.Point(189, 14)
		self._HallHuraytTextBoxTop.Margin = System.Windows.Forms.Padding(1)
		self._HallHuraytTextBoxTop.Name = "HallHuraytTextBoxTop"
		self._HallHuraytTextBoxTop.Size = System.Drawing.Size(54, 20)
		self._HallHuraytTextBoxTop.TabIndex = 18
		self._HallHuraytTextBoxTop.Text = "2.5"
		self._HallHuraytTextBoxTop.TextChanged += self.HallHuraytTextBoxTopTextChanged
		# 
		# SurfaceRoughTextBoxTop
		# 
		self._SurfaceRoughTextBoxTop.Location = System.Drawing.Point(189, 40)
		self._SurfaceRoughTextBoxTop.Name = "SurfaceRoughTextBoxTop"
		self._SurfaceRoughTextBoxTop.Size = System.Drawing.Size(54, 20)
		self._SurfaceRoughTextBoxTop.TabIndex = 19
		self._SurfaceRoughTextBoxTop.Text = "0.5"
		self._SurfaceRoughTextBoxTop.TextChanged += self.SurfaceRoughTextBoxTopTextChanged
		# 
		# SurfaceRoughLabelTop
		# 
		self._SurfaceRoughLabelTop.AutoSize = True
		self._SurfaceRoughLabelTop.Font = System.Drawing.Font("Microsoft Sans Serif", 7.20000029, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._SurfaceRoughLabelTop.Location = System.Drawing.Point(5, 41)
		self._SurfaceRoughLabelTop.Name = "SurfaceRoughLabelTop"
		self._SurfaceRoughLabelTop.Size = System.Drawing.Size(131, 13)
		self._SurfaceRoughLabelTop.TabIndex = 7
		self._SurfaceRoughLabelTop.Text = "Surface Roughness (RMS)"
		# 
		# RoughnessUnitsComboBox
		# 
		self._RoughnessUnitsComboBox.FormattingEnabled = True
		self._RoughnessUnitsComboBox.Items.AddRange(System.Array[System.Object](
			["um",
			"mm",
			"cm"]))
		self._RoughnessUnitsComboBox.Location = System.Drawing.Point(279, 60)
		self._RoughnessUnitsComboBox.Name = "RoughnessUnitsComboBox"
		self._RoughnessUnitsComboBox.Size = System.Drawing.Size(51, 21)
		self._RoughnessUnitsComboBox.TabIndex = 24
		self._RoughnessUnitsComboBox.Text = "um"
		self._RoughnessUnitsComboBox.Visible = False
		self._RoughnessUnitsComboBox.SelectedIndexChanged += self.RoughnessUnitsComboBoxSelectedIndexChanged
		# 
		# SidesTraceGroupBox
		# 
		self._SidesTraceGroupBox.BackColor = System.Drawing.Color.Transparent
		self._SidesTraceGroupBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center
		self._SidesTraceGroupBox.Controls.Add(self._SurfaceRoughLabelSides)
		self._SidesTraceGroupBox.Controls.Add(self._SurfaceRoughTextBoxSides)
		self._SidesTraceGroupBox.Controls.Add(self._HallHurayLabelSides)
		self._SidesTraceGroupBox.Controls.Add(self._HallHuraytTextBoxSides)
		self._SidesTraceGroupBox.Location = System.Drawing.Point(10, 100)
		self._SidesTraceGroupBox.Name = "SidesTraceGroupBox"
		self._SidesTraceGroupBox.Padding = System.Windows.Forms.Padding(1)
		self._SidesTraceGroupBox.Size = System.Drawing.Size(253, 65)
		self._SidesTraceGroupBox.TabIndex = 15
		self._SidesTraceGroupBox.TabStop = False
		self._SidesTraceGroupBox.Text = "Sides of Trace"
		self._SidesTraceGroupBox.Visible = False
		# 
		# HallHuraytTextBoxSides
		# 
		self._HallHuraytTextBoxSides.Location = System.Drawing.Point(187, 15)
		self._HallHuraytTextBoxSides.Margin = System.Windows.Forms.Padding(1)
		self._HallHuraytTextBoxSides.Name = "HallHuraytTextBoxSides"
		self._HallHuraytTextBoxSides.Size = System.Drawing.Size(54, 20)
		self._HallHuraytTextBoxSides.TabIndex = 20
		self._HallHuraytTextBoxSides.Text = "2.5"
		self._HallHuraytTextBoxSides.TextChanged += self.HallHuraytTextBoxSidesTextChanged
		# 
		# HallHurayLabelSides
		# 
		self._HallHurayLabelSides.AutoSize = True
		self._HallHurayLabelSides.Font = System.Drawing.Font("Microsoft Sans Serif", 7.20000029, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._HallHurayLabelSides.Location = System.Drawing.Point(5, 21)
		self._HallHurayLabelSides.Name = "HallHurayLabelSides"
		self._HallHurayLabelSides.Size = System.Drawing.Size(120, 13)
		self._HallHurayLabelSides.TabIndex = 15
		self._HallHurayLabelSides.Text = "Hall-Huray Surface Ratio"
		# 
		# SurfaceRoughTextBoxSides
		# 
		self._SurfaceRoughTextBoxSides.Location = System.Drawing.Point(187, 40)
		self._SurfaceRoughTextBoxSides.Name = "SurfaceRoughTextBoxSides"
		self._SurfaceRoughTextBoxSides.Size = System.Drawing.Size(54, 20)
		self._SurfaceRoughTextBoxSides.TabIndex = 21
		self._SurfaceRoughTextBoxSides.Text = "0.5"
		self._SurfaceRoughTextBoxSides.TextChanged += self.SurfaceRoughTextBoxSidesTextChanged
		# 
		# SurfaceRoughLabelSides
		# 
		self._SurfaceRoughLabelSides.AutoSize = True
		self._SurfaceRoughLabelSides.Font = System.Drawing.Font("Microsoft Sans Serif", 7.20000029, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._SurfaceRoughLabelSides.Location = System.Drawing.Point(5, 43)
		self._SurfaceRoughLabelSides.Name = "SurfaceRoughLabelSides"
		self._SurfaceRoughLabelSides.Size = System.Drawing.Size(131, 13)
		self._SurfaceRoughLabelSides.TabIndex = 13
		self._SurfaceRoughLabelSides.Text = "Surface Roughness (RMS)"
		# 
		# BottomTraceGroupBox
		# 
		self._BottomTraceGroupBox.BackColor = System.Drawing.Color.Transparent
		self._BottomTraceGroupBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center
		self._BottomTraceGroupBox.Controls.Add(self._SurfaceRoughLabelBottom)
		self._BottomTraceGroupBox.Controls.Add(self._SurfaceRoughTextBoxBottom)
		self._BottomTraceGroupBox.Controls.Add(self._HallHurayLabelBottom)
		self._BottomTraceGroupBox.Controls.Add(self._HallHuraytTextBoxBottom)
		self._BottomTraceGroupBox.Location = System.Drawing.Point(10, 165)
		self._BottomTraceGroupBox.Name = "BottomTraceGroupBox"
		self._BottomTraceGroupBox.Padding = System.Windows.Forms.Padding(1)
		self._BottomTraceGroupBox.Size = System.Drawing.Size(253, 65)
		self._BottomTraceGroupBox.TabIndex = 16
		self._BottomTraceGroupBox.TabStop = False
		self._BottomTraceGroupBox.Text = "Bottom of Trace"
		self._BottomTraceGroupBox.Visible = False
		# 
		# HallHuraytTextBoxBottom
		# 
		self._HallHuraytTextBoxBottom.Location = System.Drawing.Point(187, 14)
		self._HallHuraytTextBoxBottom.Margin = System.Windows.Forms.Padding(1)
		self._HallHuraytTextBoxBottom.Name = "HallHuraytTextBoxBottom"
		self._HallHuraytTextBoxBottom.Size = System.Drawing.Size(54, 20)
		self._HallHuraytTextBoxBottom.TabIndex = 22
		self._HallHuraytTextBoxBottom.Text = "2.5"
		self._HallHuraytTextBoxBottom.TextChanged += self.HallHuraytTextBoxBottomTextChanged
		# 
		# HallHurayLabelBottom
		# 
		self._HallHurayLabelBottom.AutoSize = True
		self._HallHurayLabelBottom.Font = System.Drawing.Font("Microsoft Sans Serif", 7.20000029, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._HallHurayLabelBottom.Location = System.Drawing.Point(5, 20)
		self._HallHurayLabelBottom.Name = "HallHurayLabelBottom"
		self._HallHurayLabelBottom.Size = System.Drawing.Size(120, 13)
		self._HallHurayLabelBottom.TabIndex = 23
		self._HallHurayLabelBottom.Text = "Hall-Huray Surface Ratio"
		# 
		# SurfaceRoughTextBoxBottom
		# 
		self._SurfaceRoughTextBoxBottom.Location = System.Drawing.Point(187, 40)
		self._SurfaceRoughTextBoxBottom.Name = "SurfaceRoughTextBoxBottom"
		self._SurfaceRoughTextBoxBottom.Size = System.Drawing.Size(54, 20)
		self._SurfaceRoughTextBoxBottom.TabIndex = 23
		self._SurfaceRoughTextBoxBottom.Text = "0.5"
		self._SurfaceRoughTextBoxBottom.TextChanged += self.SurfaceRoughTextBoxBottomTextChanged
		# 
		# SurfaceRoughLabelBottom
		# 
		self._SurfaceRoughLabelBottom.AutoSize = True
		self._SurfaceRoughLabelBottom.Font = System.Drawing.Font("Microsoft Sans Serif", 7.20000029, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._SurfaceRoughLabelBottom.Location = System.Drawing.Point(5, 43)
		self._SurfaceRoughLabelBottom.Name = "SurfaceRoughLabelBottom"
		self._SurfaceRoughLabelBottom.Size = System.Drawing.Size(131, 13)
		self._SurfaceRoughLabelBottom.TabIndex = 21
		self._SurfaceRoughLabelBottom.Text = "Surface Roughness (RMS)"
		# 
		# RoughnessUnitslabel
		# 
		self._RoughnessUnitslabel.AutoSize = True
		self._RoughnessUnitslabel.Location = System.Drawing.Point(279, 40)
		self._RoughnessUnitslabel.Name = "RoughnessUnitslabel"
		self._RoughnessUnitslabel.Size = System.Drawing.Size(31, 13)
		self._RoughnessUnitslabel.TabIndex = 17
		self._RoughnessUnitslabel.Text = "Units"
		self._RoughnessUnitslabel.Visible = False
		# 
		# tabControl3
		# 
		self._tabControl3.Controls.Add(self._tabPage4)
		self._tabControl3.Controls.Add(self._tabPage5)
		self._tabControl3.Location = System.Drawing.Point(335, 30)
		self._tabControl3.Name = "tabControl3"
		self._tabControl3.SelectedIndex = 0
		self._tabControl3.Size = System.Drawing.Size(391, 268)
		self._tabControl3.TabIndex = 21
		self._tabControl3.Visible = False
		# 
		# SMgroupbox
		# 
		self._SMgroupbox.BackColor = System.Drawing.Color.LightGray
		self._SMgroupbox.Controls.Add(self._SMTandtextBox)
		self._SMgroupbox.Controls.Add(self._SMErtextBox)
		self._SMgroupbox.Controls.Add(self._SMunitscomboBox)
		self._SMgroupbox.Controls.Add(self._SMtextBox)
		self._SMgroupbox.Location = System.Drawing.Point(114, 89)
		self._SMgroupbox.Name = "SMgroupbox"
		self._SMgroupbox.Size = System.Drawing.Size(135, 189)
		self._SMgroupbox.TabIndex = 5
		self._SMgroupbox.TabStop = False
		self._SMgroupbox.Text = "Soldermask"
		self._SMgroupbox.Visible = False
		# 
		# SMtextBox
		# 
		self._SMtextBox.Location = System.Drawing.Point(6, 41)
		self._SMtextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._SMtextBox.Name = "SMtextBox"
		self._SMtextBox.Size = System.Drawing.Size(50, 26)
		self._SMtextBox.TabIndex = 25
		self._SMtextBox.Text = "1"
		self._SMtextBox.TextChanged += self.SMtextBoxTextChanged
		# 
		# SMunitscomboBox
		# 
		self._SMunitscomboBox.FormattingEnabled = True
		self._SMunitscomboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._SMunitscomboBox.Location = System.Drawing.Point(59, 41)
		self._SMunitscomboBox.Name = "SMunitscomboBox"
		self._SMunitscomboBox.Size = System.Drawing.Size(60, 23)
		self._SMunitscomboBox.TabIndex = 26
		self._SMunitscomboBox.Text = "GHz"
		self._SMunitscomboBox.SelectedIndexChanged += self.SMunitscomboBoxSelectedIndexChanged
		# 
		# SMErtextBox
		# 
		self._SMErtextBox.Location = System.Drawing.Point(6, 94)
		self._SMErtextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._SMErtextBox.Name = "SMErtextBox"
		self._SMErtextBox.Size = System.Drawing.Size(50, 26)
		self._SMErtextBox.TabIndex = 27
		self._SMErtextBox.Text = "4"
		self._SMErtextBox.TextChanged += self.SMErtextBoxTextChanged
		# 
		# SMTandtextBox
		# 
		self._SMTandtextBox.Location = System.Drawing.Point(6, 144)
		self._SMTandtextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._SMTandtextBox.Name = "SMTandtextBox"
		self._SMTandtextBox.Size = System.Drawing.Size(50, 26)
		self._SMTandtextBox.TabIndex = 28
		self._SMTandtextBox.Text = "0.02"
		self._SMTandtextBox.TextChanged += self.SMTandtextBoxTextChanged
		# 
		# BottomDielgroupBox
		# 
		self._BottomDielgroupBox.BackColor = System.Drawing.Color.LightGray
		self._BottomDielgroupBox.Controls.Add(self._BottomDielTandtextBox)
		self._BottomDielgroupBox.Controls.Add(self._BottomDielErtextBox)
		self._BottomDielgroupBox.Controls.Add(self._BottomDielcomboBox)
		self._BottomDielgroupBox.Controls.Add(self._BottomDieltextBox)
		self._BottomDielgroupBox.Location = System.Drawing.Point(253, 89)
		self._BottomDielgroupBox.Name = "BottomDielgroupBox"
		self._BottomDielgroupBox.Size = System.Drawing.Size(135, 189)
		self._BottomDielgroupBox.TabIndex = 6
		self._BottomDielgroupBox.TabStop = False
		self._BottomDielgroupBox.Text = "Bottom Dielectric"
		self._BottomDielgroupBox.Visible = False
		# 
		# BottomDielTandtextBox
		# 
		self._BottomDielTandtextBox.Location = System.Drawing.Point(6, 144)
		self._BottomDielTandtextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._BottomDielTandtextBox.Name = "BottomDielTandtextBox"
		self._BottomDielTandtextBox.Size = System.Drawing.Size(50, 26)
		self._BottomDielTandtextBox.TabIndex = 32
		self._BottomDielTandtextBox.Text = "0.02"
		self._BottomDielTandtextBox.TextChanged += self.BottomDielTandtextBoxTextChanged
		# 
		# BottomDielErtextBox
		# 
		self._BottomDielErtextBox.Location = System.Drawing.Point(6, 94)
		self._BottomDielErtextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._BottomDielErtextBox.Name = "BottomDielErtextBox"
		self._BottomDielErtextBox.Size = System.Drawing.Size(50, 26)
		self._BottomDielErtextBox.TabIndex = 31
		self._BottomDielErtextBox.Text = "4"
		self._BottomDielErtextBox.TextChanged += self.BottomDielErtextBoxTextChanged
		# 
		# BottomDielcomboBox
		# 
		self._BottomDielcomboBox.FormattingEnabled = True
		self._BottomDielcomboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._BottomDielcomboBox.Location = System.Drawing.Point(59, 41)
		self._BottomDielcomboBox.Name = "BottomDielcomboBox"
		self._BottomDielcomboBox.Size = System.Drawing.Size(60, 23)
		self._BottomDielcomboBox.TabIndex = 30
		self._BottomDielcomboBox.Text = "GHz"
		self._BottomDielcomboBox.SelectedIndexChanged += self.BottomDielcomboBoxSelectedIndexChanged
		# 
		# BottomDieltextBox
		# 
		self._BottomDieltextBox.Location = System.Drawing.Point(6, 41)
		self._BottomDieltextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._BottomDieltextBox.Name = "BottomDieltextBox"
		self._BottomDieltextBox.Size = System.Drawing.Size(50, 26)
		self._BottomDieltextBox.TabIndex = 29
		self._BottomDieltextBox.Text = "1"
		self._BottomDieltextBox.TextChanged += self.BottomDieltextBoxTextChanged
		# 
		# TopDielgroupBox
		# 
		self._TopDielgroupBox.BackColor = System.Drawing.Color.LightGray
		self._TopDielgroupBox.Controls.Add(self._TopDielTandtextBox)
		self._TopDielgroupBox.Controls.Add(self._TopDielErtextBox)
		self._TopDielgroupBox.Controls.Add(self._TopDielcomboBox)
		self._TopDielgroupBox.Controls.Add(self._TopDieltextBox)
		self._TopDielgroupBox.Location = System.Drawing.Point(394, 89)
		self._TopDielgroupBox.Name = "TopDielgroupBox"
		self._TopDielgroupBox.Size = System.Drawing.Size(135, 189)
		self._TopDielgroupBox.TabIndex = 7
		self._TopDielgroupBox.TabStop = False
		self._TopDielgroupBox.Text = "Top Dielectric"
		self._TopDielgroupBox.Visible = False
		# 
		# TopDielTandtextBox
		# 
		self._TopDielTandtextBox.Location = System.Drawing.Point(6, 144)
		self._TopDielTandtextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._TopDielTandtextBox.Name = "TopDielTandtextBox"
		self._TopDielTandtextBox.Size = System.Drawing.Size(50, 26)
		self._TopDielTandtextBox.TabIndex = 36
		self._TopDielTandtextBox.Text = "0.02"
		self._TopDielTandtextBox.TextChanged += self.TopDielTandtextBoxTextChanged
		# 
		# TopDielErtextBox
		# 
		self._TopDielErtextBox.Location = System.Drawing.Point(6, 94)
		self._TopDielErtextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._TopDielErtextBox.Name = "TopDielErtextBox"
		self._TopDielErtextBox.Size = System.Drawing.Size(50, 26)
		self._TopDielErtextBox.TabIndex = 35
		self._TopDielErtextBox.Text = "4"
		self._TopDielErtextBox.TextChanged += self.TopDielErtextBoxTextChanged
		# 
		# TopDielcomboBox
		# 
		self._TopDielcomboBox.FormattingEnabled = True
		self._TopDielcomboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._TopDielcomboBox.Location = System.Drawing.Point(59, 41)
		self._TopDielcomboBox.Name = "TopDielcomboBox"
		self._TopDielcomboBox.Size = System.Drawing.Size(60, 23)
		self._TopDielcomboBox.TabIndex = 34
		self._TopDielcomboBox.Text = "GHz"
		self._TopDielcomboBox.SelectedIndexChanged += self.TopDielcomboBoxSelectedIndexChanged
		# 
		# TopDieltextBox
		# 
		self._TopDieltextBox.Location = System.Drawing.Point(6, 41)
		self._TopDieltextBox.MinimumSize = System.Drawing.Size(0, 26)
		self._TopDieltextBox.Name = "TopDieltextBox"
		self._TopDieltextBox.Size = System.Drawing.Size(50, 26)
		self._TopDieltextBox.TabIndex = 33
		self._TopDieltextBox.Text = "1"
		self._TopDieltextBox.TextChanged += self.TopDieltextBoxTextChanged
		# 
		# ConductorExampleinputlabel
		# 
		self._ConductorExampleinputlabel.Location = System.Drawing.Point(279, 103)
		self._ConductorExampleinputlabel.Name = "ConductorExampleinputlabel"
		self._ConductorExampleinputlabel.Size = System.Drawing.Size(84, 66)
		self._ConductorExampleinputlabel.TabIndex = 25
		self._ConductorExampleinputlabel.Text = "Example Values Pre-Loaded"
		self._ConductorExampleinputlabel.Visible = False
		# 
		# ZoLabelDiff
		# 
		self._ZoLabelDiff.AutoSize = True
		self._ZoLabelDiff.Location = System.Drawing.Point(140, 62)
		self._ZoLabelDiff.Name = "ZoLabelDiff"
		self._ZoLabelDiff.Size = System.Drawing.Size(46, 15)
		self._ZoLabelDiff.TabIndex = 6
		self._ZoLabelDiff.Text = "Zodiff:  "
		self._ZoLabelDiff.Visible = False
		# 
		# ZotextboxDiff
		# 
		self._ZotextboxDiff.Location = System.Drawing.Point(198, 56)
		self._ZotextboxDiff.Name = "ZotextboxDiff"
		self._ZotextboxDiff.Size = System.Drawing.Size(55, 21)
		self._ZotextboxDiff.TabIndex = 0
		self._ZotextboxDiff.TabStop = False
		self._ZotextboxDiff.Visible = False
		# 
		# IPCeqnsLabel
		# 
		self._IPCeqnsLabel.Enabled = False
		self._IPCeqnsLabel.Font = System.Drawing.Font("Microsoft Sans Serif", 6, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._IPCeqnsLabel.Location = System.Drawing.Point(107, 77)
		self._IPCeqnsLabel.Name = "IPCeqnsLabel"
		self._IPCeqnsLabel.Size = System.Drawing.Size(167, 21)
		self._IPCeqnsLabel.TabIndex = 8
		self._IPCeqnsLabel.Text = "Zo Calc References: Help -> About"
		self._IPCeqnsLabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		self._IPCeqnsLabel.Visible = False
		# 
		# D5textbox
		# 
		self._D5textbox.Location = System.Drawing.Point(172, 303)
		self._D5textbox.Name = "D5textbox"
		self._D5textbox.Size = System.Drawing.Size(50, 21)
		self._D5textbox.TabIndex = 27
		self._D5textbox.Visible = False
		self._D5textbox.TextChanged += self.D5textboxTextChanged
		# 
		# labelD5
		# 
		self._labelD5.Location = System.Drawing.Point(230, 303)
		self._labelD5.Name = "labelD5"
		self._labelD5.Size = System.Drawing.Size(32, 18)
		self._labelD5.TabIndex = 28
		self._labelD5.Visible = False
		# 
		# D5thicknesslabel
		# 
		self._D5thicknesslabel.Location = System.Drawing.Point(9, 294)
		self._D5thicknesslabel.Name = "D5thicknesslabel"
		self._D5thicknesslabel.Size = System.Drawing.Size(160, 18)
		self._D5thicknesslabel.TabIndex = 29
		self._D5thicknesslabel.Text = "D5 Thickness"
		self._D5thicknesslabel.Visible = False
		# 
		# D4groupBox
		# 
		self._D4groupBox.Controls.Add(self._D4comboBox)
		self._D4groupBox.Controls.Add(self._D4TandtextBox)
		self._D4groupBox.Controls.Add(self._D4ErtextBox)
		self._D4groupBox.Controls.Add(self._D4textBox)
		self._D4groupBox.Location = System.Drawing.Point(363, 89)
		self._D4groupBox.Name = "D4groupBox"
		self._D4groupBox.Size = System.Drawing.Size(80, 190)
		self._D4groupBox.TabIndex = 8
		self._D4groupBox.TabStop = False
		self._D4groupBox.Text = "D4"
		self._D4groupBox.Visible = False
		# 
		# D5groupBox
		# 
		self._D5groupBox.Controls.Add(self._D5comboBox)
		self._D5groupBox.Controls.Add(self._D5TandtextBox)
		self._D5groupBox.Controls.Add(self._D5ErtextBox)
		self._D5groupBox.Controls.Add(self._D5dieltextBox)
		self._D5groupBox.Location = System.Drawing.Point(446, 88)
		self._D5groupBox.Name = "D5groupBox"
		self._D5groupBox.Size = System.Drawing.Size(80, 190)
		self._D5groupBox.TabIndex = 9
		self._D5groupBox.TabStop = False
		self._D5groupBox.Text = "D5"
		self._D5groupBox.Visible = False
		# 
		# D4textBox
		# 
		self._D4textBox.Location = System.Drawing.Point(10, 24)
		self._D4textBox.Name = "D4textBox"
		self._D4textBox.Size = System.Drawing.Size(60, 21)
		self._D4textBox.TabIndex = 0
		self._D4textBox.Text = "1"
		self._D4textBox.Visible = False
		self._D4textBox.TextChanged += self.D4textBoxTextChanged
		# 
		# D4ErtextBox
		# 
		self._D4ErtextBox.Location = System.Drawing.Point(10, 94)
		self._D4ErtextBox.Name = "D4ErtextBox"
		self._D4ErtextBox.Size = System.Drawing.Size(60, 21)
		self._D4ErtextBox.TabIndex = 1
		self._D4ErtextBox.Text = "4"
		self._D4ErtextBox.Visible = False
		self._D4ErtextBox.TextChanged += self.D4ErtextBoxTextChanged
		# 
		# D4TandtextBox
		# 
		self._D4TandtextBox.Location = System.Drawing.Point(10, 144)
		self._D4TandtextBox.Name = "D4TandtextBox"
		self._D4TandtextBox.Size = System.Drawing.Size(60, 21)
		self._D4TandtextBox.TabIndex = 2
		self._D4TandtextBox.Text = "0.02"
		self._D4TandtextBox.Visible = False
		self._D4TandtextBox.TextChanged += self.D4TandtextBoxTextChanged
		# 
		# D5dieltextBox
		# 
		self._D5dieltextBox.Location = System.Drawing.Point(10, 24)
		self._D5dieltextBox.Name = "D5dieltextBox"
		self._D5dieltextBox.Size = System.Drawing.Size(60, 21)
		self._D5dieltextBox.TabIndex = 0
		self._D5dieltextBox.Text = "1"
		self._D5dieltextBox.Visible = False
		self._D5dieltextBox.TextChanged += self.D5dieltextBoxTextChanged
		# 
		# D5ErtextBox
		# 
		self._D5ErtextBox.Location = System.Drawing.Point(10, 94)
		self._D5ErtextBox.Name = "D5ErtextBox"
		self._D5ErtextBox.Size = System.Drawing.Size(60, 21)
		self._D5ErtextBox.TabIndex = 1
		self._D5ErtextBox.Text = "4"
		self._D5ErtextBox.Visible = False
		self._D5ErtextBox.TextChanged += self.D5ErtextBoxTextChanged
		# 
		# D5TandtextBox
		# 
		self._D5TandtextBox.Location = System.Drawing.Point(10, 144)
		self._D5TandtextBox.Name = "D5TandtextBox"
		self._D5TandtextBox.Size = System.Drawing.Size(60, 21)
		self._D5TandtextBox.TabIndex = 2
		self._D5TandtextBox.Text = "0.02"
		self._D5TandtextBox.Visible = False
		self._D5TandtextBox.TextChanged += self.D5TandtextBoxTextChanged
		# 
		# D4comboBox
		# 
		self._D4comboBox.FormattingEnabled = True
		self._D4comboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._D4comboBox.Location = System.Drawing.Point(10, 53)
		self._D4comboBox.Name = "D4comboBox"
		self._D4comboBox.Size = System.Drawing.Size(60, 23)
		self._D4comboBox.TabIndex = 3
		self._D4comboBox.Text = "GHz"
		self._D4comboBox.Visible = False
		self._D4comboBox.SelectedIndexChanged += self.D4comboBoxSelectedIndexChanged
		# 
		# D5comboBox
		# 
		self._D5comboBox.FormattingEnabled = True
		self._D5comboBox.Items.AddRange(System.Array[System.Object](
			["GHz",
			"MHz",
			"KHz",
			"Hz"]))
		self._D5comboBox.Location = System.Drawing.Point(10, 53)
		self._D5comboBox.Name = "D5comboBox"
		self._D5comboBox.Size = System.Drawing.Size(60, 23)
		self._D5comboBox.TabIndex = 3
		self._D5comboBox.Text = "GHz"
		self._D5comboBox.Visible = False
		self._D5comboBox.SelectedIndexChanged += self.D5comboBoxSelectedIndexChanged
		# 
		# errorProvider1
		# 
		self._errorProvider1.BlinkStyle = System.Windows.Forms.ErrorBlinkStyle.AlwaysBlink
		self._errorProvider1.ContainerControl = self
		# 
		# MainForm
		# 
		self.AutoSize = True
		self.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None
		self.ClientSize = System.Drawing.Size(1296, 886)
		self.Controls.Add(self._MainPanel)
		self.Controls.Add(self._TopPanel)
		self.Controls.Add(self._ToopMenuStrip)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.Fixed3D
		self.MainMenuStrip = self._ToopMenuStrip
		self.Name = "MainForm"
		self.Text = "Transmission Line Toolkit 20260622"
		self.TopMost = False
		self._ToopMenuStrip.ResumeLayout(False)
		self._ToopMenuStrip.PerformLayout()
		self._TopPanel.ResumeLayout(False)
		self._pictureBox1.EndInit()
		self._MainPanel.ResumeLayout(False)
		self._UnitsGroupBox.ResumeLayout(False)
		self._DesignParametersgroupBox.ResumeLayout(False)
		self._DesignParametersgroupBox.PerformLayout()
		self._DielPropGroupBox.ResumeLayout(False)
		self._ActionGroupBox.ResumeLayout(False)
		self._ActionGroupBox.PerformLayout()
		self._SolverUsageGroupBox.ResumeLayout(False)
		self._SolverUsageGroupBox.PerformLayout()
		self._ModelExportGroupBox.ResumeLayout(False)
		self._ModelExportGroupBox.PerformLayout()
		self._ANSYSLogoPictureBox.EndInit()
		self._pictureBox2.EndInit()
		self._tabControl2.ResumeLayout(False)
		self._Simulation_Parameters_Tab.ResumeLayout(False)
		self._Simulation_Parameters_Tab.PerformLayout()
		self._SolutionSetupGroupBox.ResumeLayout(False)
		self._SolutionSetupGroupBox.PerformLayout()
		self._tabPage5.ResumeLayout(False)
		self._tabPage5.PerformLayout()
		self._trackBar1.EndInit()
		self._etchpictureBox.EndInit()
		self._tabPage4.ResumeLayout(False)
		self._tabPage4.PerformLayout()
		self._TopTraceGroupBox.ResumeLayout(False)
		self._TopTraceGroupBox.PerformLayout()
		self._SidesTraceGroupBox.ResumeLayout(False)
		self._SidesTraceGroupBox.PerformLayout()
		self._BottomTraceGroupBox.ResumeLayout(False)
		self._BottomTraceGroupBox.PerformLayout()
		self._tabControl3.ResumeLayout(False)
		self._SMgroupbox.ResumeLayout(False)
		self._SMgroupbox.PerformLayout()
		self._BottomDielgroupBox.ResumeLayout(False)
		self._BottomDielgroupBox.PerformLayout()
		self._TopDielgroupBox.ResumeLayout(False)
		self._TopDielgroupBox.PerformLayout()
		self._D4groupBox.ResumeLayout(False)
		self._D4groupBox.PerformLayout()
		self._D5groupBox.ResumeLayout(False)
		self._D5groupBox.PerformLayout()
		self._errorProvider1.EndInit()
		self.ResumeLayout(False)
		self.PerformLayout()

      #################################
      # All the GUI handling commands #
################################################################################################################
	
	
	
	
##########################################################################################
	# Delect Design type from design combobox  and make design parameters visible or not  #	
	#######################################################################################	
	
	def DesignSelectComboBoxSelectedIndexChanged(self, sender, e):
		modeltype = str(sender.Text)
		szPath = self.m_libPath
		
				
		if modeltype == "Microstrip - Single Ended":
			self._pictureBox2.Image = Image.FromFile(szPath+"Images/MS_Single.png")
			self.microstrip = 1
			self.differential = 0	
			self.broadside = 0	
			self.SLMS = 1
			self.GCPW = 0
			
			self._underetchradioButton.Visible = True
			self._overetchradioButton.Text = "Top Etching"
			
			
			self._DesignParametersgroupBox.Location = System.Drawing.Point(1006, 6)
			self._DesignParametersgroupBox.Size = System.Drawing.Size(278, 329)			

			self._numberoftraceslabel.Visible = True
			self._NumberofTracesTextbox.Visible = True
			self._numberoftraceslabel.Location = System.Drawing.Point(9, 25)
			self._NumberofTracesTextbox.Location = System.Drawing.Point(172, 20)		
						
			self._TraceWidthlabel.Visible = True
			self._TraceWidthTextBox.Visible = True				
			self._TraceWidthlabel.Location = System.Drawing.Point(9, 115)
			self._TraceWidthTextBox.Location = System.Drawing.Point(172, 110)			
			self._label10.Visible = True
			self._label10.Text = self.units		
			self._label10.Location = System.Drawing.Point(230, 110)			
			
			self._PlaneThicknessTextBox.Visible = True
			self._PlaneThicknesslabel.Visible = True			
			self._PlaneThicknesslabel.Location = System.Drawing.Point(9, 55)
			self._PlaneThicknessTextBox.Location = System.Drawing.Point(172, 50)
			self._label8.Visible = True
			self._label8.Text = self.units			
			self._label8.Location = System.Drawing.Point(230, 50)
				
			self._TraceThicknesslabel.Visible = True
			self._TraceThicknessTextBox.Visible = True
			self._TraceThicknesslabel.Location = System.Drawing.Point(9, 85)
			self._TraceThicknessTextBox.Location = System.Drawing.Point(172, 80)
			self._label9.Visible = True
			self._label9.Text = self.units			
			self._label9.Location = System.Drawing.Point(230, 80)			

			self._DifferentialSpacinglabel.Location = System.Drawing.Point(9, 145)
			self._DifferentialSpacingTextBox.Location = System.Drawing.Point(172, 140)
			self._label14.Location = System.Drawing.Point(230, 140)
			self._DifferentialSpacinglabel.Visible = False
			self._DifferentialSpacingTextBox.Visible = False
			self._label14.Visible = False
			self._label14.Text = self.units				
						
			self._TopDielectriclabel.Visible = False
			self._TopDielectricTextBox.Visible = False
			self._TopDielectriclabel.Location = System.Drawing.Point(9, 175)
			self._TopDielectricTextBox.Location = System.Drawing.Point(172, 170)
			self._TopDielectriclabel.Text = "Top Dielectric"			
			self._label12.Location = System.Drawing.Point(230, 170)
			self._label12.Visible = False
			self._label12.Text = self.units
			
			self._BottomDielectriclabel.Visible = True
			self._BottomDielectricTextBox.Visible = True
			self._BottomDielectriclabel.Location = System.Drawing.Point(9, 175)
			self._BottomDielectricTextBox.Location = System.Drawing.Point(172, 170)
			self._BottomDielectriclabel.Text = "Bottom Dielectric"		
			self._label13.Location = System.Drawing.Point(230, 170)
			self._label13.Visible = True
			self._label13.Text = self.units

			self._TraceSpaceTextBox.Visible = True
			self._TraceSpacinglabel.Visible = True
			self._TraceSpaceTextBox.Location = System.Drawing.Point(172, 140)
			self._TraceSpacinglabel.Location = System.Drawing.Point(9, 145)	
			self._TraceSpacinglabel.Text = "Trace Spacing"
			self._label11.Location = System.Drawing.Point(230, 140)			
			self._label11.Visible = True
			self._label11.Text = self.units
		
			self._SolderMaskThicknessTextBox.Visible = True
			self._SolderMaskThicknessLabel.Visible = True
			self._SolderMaskThicknessTextBox.Location = System.Drawing.Point(172, 200)
			self._SolderMaskThicknessLabel.Location = System.Drawing.Point(9, 205)
			self._SolderMaskThicknessLabel.Text = "Solder Mask Thickness"
			self._label15.Location = System.Drawing.Point(230, 200)				
			self._label15.Visible = True
			self._label15.Text = self.units	
			
			self._DielPropGroupBox.Visible = True
			self._tabControl3.Visible = True			
			self._SMgroupbox.Visible = True
			self._BottomDielgroupBox.Visible = True
			self._TopDielgroupBox.Visible = False
			
			### Calculate Button  ####	
			self._CalculateButton.Visible = True
			self._SimulateButton.Visible = True
			self._ZoLabel.Visible = True
			self._Zotextbox.Visible = True
			self._ZoLabelDiff.Visible = False
			self._ZotextboxDiff.Visible = False			
			self._IPCeqnsLabel.Visible = True			
			self._SolutionSetupGroupBox.Visible = True
			self._groupBox2.Visible = True
			
			####  Dielectrics handline  #####
			
			####Solder Mask Dielectric ####
			self._SMgroupbox.Size = System.Drawing.Size(135, 189)
			self._SMgroupbox.Location = System.Drawing.Point(114, 89)			
			self._SMgroupbox.Text = "Solder Mask"	
			self._SMtextBox.Location = System.Drawing.Point(6, 41)		
			self._SMtextBox.Size = System.Drawing.Size(50, 26)
			self._SMunitscomboBox.Location = System.Drawing.Point(59, 41)
			self._SMunitscomboBox.Size = System.Drawing.Size(60, 26)
			self._SMErtextBox.Location = System.Drawing.Point(6, 94)
			self._SMErtextBox.Size = System.Drawing.Size(50, 26)
			self._SMTandtextBox.Location = System.Drawing.Point(6, 144)
			self._SMTandtextBox.Size = System.Drawing.Size(50, 26)
			self._SMgroupbox.Visible = True
			self._SMtextBox.Visible = True
			self._SMunitscomboBox.Visible = True
			self._SMErtextBox.Visible = True			
			
			
			####Bottom Dielectric ####	
			self._BottomDielgroupBox.Location = System.Drawing.Point(253, 89)		
			self._BottomDielgroupBox.Size = System.Drawing.Size(135, 189)
			self._BottomDielgroupBox.Text = "Bottom Dielectric"
			self._BottomDieltextBox.Location = System.Drawing.Point(6, 41)		
			self._BottomDieltextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielcomboBox.Location = System.Drawing.Point(59, 41)
			self._BottomDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._BottomDielErtextBox.Location = System.Drawing.Point(6, 94)
			self._BottomDielErtextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielTandtextBox.Location = System.Drawing.Point(6, 144)
			self._BottomDielTandtextBox.Size = System.Drawing.Size(50, 26)				
			
			
			
			#### D4 Dielectric ####		
			self._D4groupBox.Visible = False
			self._D4textBox.Visible = False
			self._D4comboBox.Visible = False
			self._D4ErtextBox.Visible = False
			self._D4TandtextBox.Visible = False	
			#### D5 Dielectric ####
			self._D5groupBox.Visible = False
			self._D5dieltextBox.Visible = False
			self._D5comboBox.Visible = False
			self._D5ErtextBox.Visible = False
			self._D5TandtextBox.Visible = False			
			#### Top Dielectric ####
			self._TopDielgroupBox.Visible = False			
			

			#Set Default Values for 50 ohm line
			self._NumberofTracesTextbox.Text = "4"
			self._PlaneThicknessTextBox.Text = "0.8"
			self._TraceThicknessTextBox.Text = "0.8"
			self._TraceWidthTextBox.Text = "6"
			self._TraceSpaceTextBox.Text = "8"
			self._BottomDielectricTextBox.Text = "3.55"
			self._SolderMaskThicknessTextBox.Text = "0.5"
			self.numberoftraces = 4
			self.planethickness = 0.8
			self.tracethickness = 0.8
			self.tracewidth = 6
			self.tracespacing = 8
			self.bottomdielectricthickness = 3.55
			self.soldermaskthickness = 0.5

			self.SMdielectricfreq = 1	
			self._SMtextBox.Text = "1"
			self.SMdielectricfrequnits = 'GHz'	
			self._SMunitscomboBox.Text = "GHz"	
			self.SMEr = 4
			self._SMErtextBox.Text = "4"
			self.SMTand = 0.02
			self._SMTandtextBox.Text = "0.02"
	
			self.Bdielfreq = 1
			self._BottomDieltextBox.Text = "1"
			self.Bdielectricfrequnits = 'GHz'
			self._BottomDielcomboBox.Text = "GHz"
			self.BdielEr = 4	
			self._BottomDielErtextBox.Text = "4"
			self.BdielTand = 0.02
			self._BottomDielTandtextBox.Text = "0.02"
	
			self.Tdielfreq = 1
			self._TopDieltextBox.Text = "1"
			self.Tdielfrequnits = 'GHz'		
			self._TopDielcomboBox.Text = "GHz"
			self.TdielEr = 4
			self._TopDielErtextBox.Text = "4"
			self.TdielTand = 0.02	
			self._TopDielTandtextBox.Text = "0.02"
	
			self.D4dielfreq = 1	
			self._D4textBox.Text = "1"
			self.D4dielfrequnits = 'GHz'
			self._D4comboBox.Text = "GHz"
			self.D4dielEr = 4
			self._D4ErtextBox.Text = "4"
			self.D4dielTand = 0.02
			self._D4TandtextBox.Text = "0.02"
	
			self.D5dielfreq = 1
			self._D5dieltextBox.Text = "1"
			self.D5dielfrequnits = 'GHz'
			self._D5comboBox.Text = "GHz"
			self.D5dielEr = 4
			self._D5ErtextBox.Text = "4"
			self.D5dielTand = 0.02
			self._D5TandtextBox.Text = "0.02"
						
			self._Zotextbox.Text = " "
			self._ZotextboxDiff.Text = " "

		if modeltype == "Microstrip - Differential":
			self._pictureBox2.Image = Image.FromFile(szPath+"Images/MS_Diff.png")
			self.microstrip = 1
			self.differential = 1
			self.broadside = 0	
			self.SLMS = 1
			self.GCPW = 0
			
			self._underetchradioButton.Visible = True			
									
			self._DesignParametersgroupBox.Location = System.Drawing.Point(1006, 6)
			self._DesignParametersgroupBox.Size = System.Drawing.Size(278, 329)			

			self._numberoftraceslabel.Visible = True
			self._NumberofTracesTextbox.Visible = True
			self._numberoftraceslabel.Location = System.Drawing.Point(9, 25)
			self._NumberofTracesTextbox.Location = System.Drawing.Point(172, 20)		
						
			self._TraceWidthlabel.Visible = True
			self._TraceWidthTextBox.Visible = True				
			self._TraceWidthlabel.Location = System.Drawing.Point(9, 115)
			self._TraceWidthTextBox.Location = System.Drawing.Point(172, 110)			
			self._label10.Visible = True
			self._label10.Text = self.units		
			self._label10.Location = System.Drawing.Point(230, 110)			
			
			self._PlaneThicknessTextBox.Visible = True
			self._PlaneThicknesslabel.Visible = True			
			self._PlaneThicknesslabel.Location = System.Drawing.Point(9, 55)
			self._PlaneThicknessTextBox.Location = System.Drawing.Point(172, 50)
			self._label8.Visible = True
			self._label8.Text = self.units			
			self._label8.Location = System.Drawing.Point(230, 50)
				
			self._TraceThicknesslabel.Visible = True
			self._TraceThicknessTextBox.Visible = True
			self._TraceThicknesslabel.Location = System.Drawing.Point(9, 85)
			self._TraceThicknessTextBox.Location = System.Drawing.Point(172, 80)
			self._label9.Visible = True
			self._label9.Text = self.units			
			self._label9.Location = System.Drawing.Point(230, 80)			

			self._DifferentialSpacinglabel.Location = System.Drawing.Point(9, 235)
			self._DifferentialSpacingTextBox.Location = System.Drawing.Point(172, 230)
			self._label14.Location = System.Drawing.Point(230, 230)
			self._DifferentialSpacinglabel.Visible = True
			self._DifferentialSpacingTextBox.Visible = True
			self._label14.Visible = True
			self._label14.Text = self.units				
						
			self._TopDielectriclabel.Visible = False
			self._TopDielectricTextBox.Visible = False
			self._TopDielectriclabel.Location = System.Drawing.Point(9, 175)
			self._TopDielectricTextBox.Location = System.Drawing.Point(172, 170)
			self._TopDielectriclabel.Text = "Top Dielectric"			
			self._label12.Location = System.Drawing.Point(230, 170)
			self._label12.Visible = False
			self._label12.Text = self.units
			
			self._BottomDielectriclabel.Visible = True
			self._BottomDielectricTextBox.Visible = True
			self._BottomDielectriclabel.Location = System.Drawing.Point(9, 175)
			self._BottomDielectricTextBox.Location = System.Drawing.Point(172, 170)
			self._BottomDielectriclabel.Text = "Bottom Dielectric"		
			self._label13.Location = System.Drawing.Point(230, 170)
			self._label13.Visible = True
			self._label13.Text = self.units

			self._TraceSpaceTextBox.Visible = True
			self._TraceSpacinglabel.Visible = True
			self._TraceSpaceTextBox.Location = System.Drawing.Point(172, 140)
			self._TraceSpacinglabel.Location = System.Drawing.Point(9, 145)	
			self._TraceSpacinglabel.Text = "Trace Spacing"
			self._label11.Location = System.Drawing.Point(230, 140)			
			self._label11.Visible = True
			self._label11.Text = self.units
		
			self._SolderMaskThicknessTextBox.Visible = True
			self._SolderMaskThicknessLabel.Visible = True
			self._SolderMaskThicknessTextBox.Location = System.Drawing.Point(172, 200)
			self._SolderMaskThicknessLabel.Location = System.Drawing.Point(9, 205)
			self._SolderMaskThicknessLabel.Text = "Solder Mask Thickness"
			self._label15.Location = System.Drawing.Point(230, 200)				
			self._label15.Visible = True
			self._label15.Text = self.units	


			self._DielPropGroupBox.Visible = True
			self._tabControl3.Visible = True			
			self._SMgroupbox.Visible = True
			self._BottomDielgroupBox.Visible = True
			self._TopDielgroupBox.Visible = False


			self._D5textbox.Visible = False
			self._D5thicknesslabel.Visible = False
			self._D5textbox.Location = System.Drawing.Point(172, 290)
			self._labelD5.Location = System.Drawing.Point(230, 290)				
			self._labelD5.Visible = False
			self._labelD5.Text = self.units	
			
			self._Zotextbox.Text = " "
			self._ZotextboxDiff.Text = " "			

			####Dielectrics Panel Handling  #####
			
			####Solder Mask Dielectric ####
			self._SMgroupbox.Size = System.Drawing.Size(135, 189)
			self._SMgroupbox.Location = System.Drawing.Point(114, 89)			
			self._SMgroupbox.Text = "Solder Mask"	
			self._SMtextBox.Location = System.Drawing.Point(6, 41)		
			self._SMtextBox.Size = System.Drawing.Size(50, 26)
			self._SMunitscomboBox.Location = System.Drawing.Point(59, 41)
			self._SMunitscomboBox.Size = System.Drawing.Size(60, 26)
			self._SMErtextBox.Location = System.Drawing.Point(6, 94)
			self._SMErtextBox.Size = System.Drawing.Size(50, 26)
			self._SMTandtextBox.Location = System.Drawing.Point(6, 144)
			self._SMTandtextBox.Size = System.Drawing.Size(50, 26)
			self._SMgroupbox.Visible = True
			self._SMtextBox.Visible = True
			self._SMunitscomboBox.Visible = True
			self._SMErtextBox.Visible = True			
						
			####Bottom Dielectric ####	
			self._BottomDielgroupBox.Location = System.Drawing.Point(253, 89)		
			self._BottomDielgroupBox.Size = System.Drawing.Size(135, 189)
			self._BottomDielgroupBox.Text = "Bottom Dielectric"
			self._BottomDieltextBox.Location = System.Drawing.Point(6, 41)		
			self._BottomDieltextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielcomboBox.Location = System.Drawing.Point(59, 41)
			self._BottomDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._BottomDielErtextBox.Location = System.Drawing.Point(6, 94)
			self._BottomDielErtextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielTandtextBox.Location = System.Drawing.Point(6, 144)
			self._BottomDielTandtextBox.Size = System.Drawing.Size(50, 26)				
						
			#### D4 Dielectric ####		
			self._D4groupBox.Visible = False
			self._D4textBox.Visible = False
			self._D4comboBox.Visible = False
			self._D4ErtextBox.Visible = False
			self._D4TandtextBox.Visible = False	
			#### D5 Dielectric ####
			self._D5groupBox.Visible = False
			self._D5dieltextBox.Visible = False
			self._D5comboBox.Visible = False
			self._D5ErtextBox.Visible = False
			self._D5TandtextBox.Visible = False			
			#### Top Dielectric ####
			self._TopDielgroupBox.Visible = False



			#Set Default Values for 100 ohm diff line
			self._ZoLabelDiff.Visible = True
			self._ZotextboxDiff.Visible = True
			self._NumberofTracesTextbox.Text = "4"
			self._PlaneThicknessTextBox.Text = "0.8"
			self._TraceThicknessTextBox.Text = "0.8"
			self._TraceWidthTextBox.Text = "5.5"
			self._TraceSpaceTextBox.Text = "8"
			self._BottomDielectricTextBox.Text = "3.55"						
			self._SolderMaskThicknessTextBox.Text = "0.5"	
			self._DifferentialSpacingTextBox.Text = "16"
			self.numberoftraces = 4
			self.planethickness = 0.8
			self.tracethickness = 0.8
			self.tracewidth = 5.5
			self.tracespacing = 8
			self.bottomdielectricthickness = 3.55
			self.soldermaskthickness = 0.5
			self.diffspacing = 16

			self._CalculateButton.Visible = True
			self._SimulateButton.Visible = True
			self._ZoLabel.Visible = True
			self._Zotextbox.Visible = True
			self._ZoLabelDiff.Visible = True
			self._ZotextboxDiff.Visible = True			
			self._IPCeqnsLabel.Visible = True			
			self._SolutionSetupGroupBox.Visible = True
			self._groupBox2.Visible = True
			self._DielPropGroupBox.Visible = True
			self._tabControl3.Visible = True

			self.SMdielectricfreq = 1	
			self._SMtextBox.Text = "1"
			self.SMdielectricfrequnits = 'GHz'	
			self._SMunitscomboBox.Text = "GHz"	
			self.SMEr = 4
			self._SMErtextBox.Text = "4"
			self.SMTand = 0.02
			self._SMTandtextBox.Text = "0.02"
	
			self.Bdielfreq = 1
			self._BottomDieltextBox.Text = "1"
			self.Bdielectricfrequnits = 'GHz'
			self._BottomDielcomboBox.Text = "GHz"
			self.BdielEr = 4	
			self._BottomDielErtextBox.Text = "4"
			self.BdielTand = 0.02
			self._BottomDielTandtextBox.Text = "0.02"
	
			self.Tdielfreq = 1
			self._TopDieltextBox.Text = "1"
			self.Tdielfrequnits = 'GHz'		
			self._TopDielcomboBox.Text = "GHz"
			self.TdielEr = 4
			self._TopDielErtextBox.Text = "4"
			self.TdielTand = 0.02	
			self._TopDielTandtextBox.Text = "0.02"
	
			self.D4dielfreq = 1	
			self._D4textBox.Text = "1"
			self.D4dielfrequnits = 'GHz'
			self._D4comboBox.Text = "GHz"
			self.D4dielEr = 4
			self._D4ErtextBox.Text = "4"
			self.D4dielTand = 0.02
			self._D4TandtextBox.Text = "0.02"
	
			self.D5dielfreq = 1
			self._D5dieltextBox.Text = "1"
			self.D5dielfrequnits = 'GHz'
			self._D5comboBox.Text = "GHz"
			self.D5dielEr = 4
			self._D5ErtextBox.Text = "4"
			self.D5dielTand = 0.02
			self._D5TandtextBox.Text = "0.02"




		if modeltype == "Stripline - Single Ended":
			self._pictureBox2.Image = Image.FromFile(szPath+"Images/SL_Single.png")
			self.microstrip = 0
			self.differential = 0
			self.broadside = 0	
			self.SLMS = 1
			self.GCPW = 0
			
			self._underetchradioButton.Visible = True			
			
			self._DesignParametersgroupBox.Location = System.Drawing.Point(1006, 6)
			self._DesignParametersgroupBox.Size = System.Drawing.Size(278, 329)			

			self._numberoftraceslabel.Visible = True
			self._NumberofTracesTextbox.Visible = True
			self._numberoftraceslabel.Location = System.Drawing.Point(9, 25)
			self._NumberofTracesTextbox.Location = System.Drawing.Point(172, 20)		
						
			self._TraceWidthlabel.Visible = True
			self._TraceWidthTextBox.Visible = True				
			self._TraceWidthlabel.Location = System.Drawing.Point(9, 115)
			self._TraceWidthTextBox.Location = System.Drawing.Point(172, 110)			
			self._label10.Visible = True
			self._label10.Text = self.units		
			self._label10.Location = System.Drawing.Point(230, 110)			
			
			self._PlaneThicknessTextBox.Visible = True
			self._PlaneThicknesslabel.Visible = True			
			self._PlaneThicknesslabel.Location = System.Drawing.Point(9, 55)
			self._PlaneThicknessTextBox.Location = System.Drawing.Point(172, 50)
			self._label8.Visible = True
			self._label8.Text = self.units			
			self._label8.Location = System.Drawing.Point(230, 50)
				
			self._TraceThicknesslabel.Visible = True
			self._TraceThicknessTextBox.Visible = True
			self._TraceThicknesslabel.Location = System.Drawing.Point(9, 85)
			self._TraceThicknessTextBox.Location = System.Drawing.Point(172, 80)
			self._label9.Visible = True
			self._label9.Text = self.units			
			self._label9.Location = System.Drawing.Point(230, 80)			

			self._DifferentialSpacinglabel.Location = System.Drawing.Point(9, 145)
			self._DifferentialSpacingTextBox.Location = System.Drawing.Point(172, 140)
			self._label14.Location = System.Drawing.Point(230, 140)
			self._DifferentialSpacinglabel.Visible = False
			self._DifferentialSpacingTextBox.Visible = False
			self._label14.Visible = False
			self._label14.Text = self.units				
						
			self._TopDielectriclabel.Visible = True
			self._TopDielectricTextBox.Visible = True
			self._TopDielectriclabel.Location = System.Drawing.Point(9, 205)
			self._TopDielectricTextBox.Location = System.Drawing.Point(172, 200)
			self._TopDielectriclabel.Text = "Top Dielectric"			
			self._label12.Location = System.Drawing.Point(230, 200)
			self._label12.Visible = True
			self._label12.Text = self.units
			
			self._BottomDielectriclabel.Visible = True
			self._BottomDielectricTextBox.Visible = True
			self._BottomDielectriclabel.Location = System.Drawing.Point(9, 175)
			self._BottomDielectricTextBox.Location = System.Drawing.Point(172, 170)
			self._BottomDielectriclabel.Text = "Bottom Dielectric"		
			self._label13.Location = System.Drawing.Point(230, 170)
			self._label13.Visible = True
			self._label13.Text = self.units

			self._TraceSpaceTextBox.Visible = True
			self._TraceSpacinglabel.Visible = True
			self._TraceSpaceTextBox.Location = System.Drawing.Point(172, 140)
			self._TraceSpacinglabel.Location = System.Drawing.Point(9, 145)	
			self._TraceSpacinglabel.Text = "Trace Spacing"
			self._label11.Location = System.Drawing.Point(230, 140)			
			self._label11.Visible = True
			self._label11.Text = self.units
		
			self._SolderMaskThicknessTextBox.Visible = False
			self._SolderMaskThicknessLabel.Visible = False
			self._SolderMaskThicknessTextBox.Location = System.Drawing.Point(172, 200)
			self._SolderMaskThicknessLabel.Location = System.Drawing.Point(9, 205)
			self._SolderMaskThicknessLabel.Text = "Solder Mask Thickness"
			self._label15.Location = System.Drawing.Point(230, 200)				
			self._label15.Visible = False
			self._label15.Text = self.units	


			self._DielPropGroupBox.Visible = True
			self._tabControl3.Visible = True			
			self._SMgroupbox.Visible = True
			self._BottomDielgroupBox.Visible = True
			self._TopDielgroupBox.Visible = False


			self._D5textbox.Visible = False
			self._D5thicknesslabel.Visible = False
			self._D5textbox.Location = System.Drawing.Point(172, 290)
			self._labelD5.Location = System.Drawing.Point(230, 290)				
			self._labelD5.Visible = False
			self._labelD5.Text = self.units	
			
			
			
			####  Dielectrics handline  #####
			self._SMgroupbox.Visible = False

			
			####Top Dielectric ####
			self._TopDielgroupBox.Location = System.Drawing.Point(114, 89)		
			self._TopDielgroupBox.Size = System.Drawing.Size(135, 190)
			self._TopDielgroupBox.Text = "Top Dielectric"
			self._TopDieltextBox.Location = System.Drawing.Point(6, 41)		
			self._TopDieltextBox.Size = System.Drawing.Size(50, 26)
			self._TopDielcomboBox.Location = System.Drawing.Point(59, 41)
			self._TopDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._TopDielErtextBox.Location = System.Drawing.Point(6, 94)
			self._TopDielErtextBox.Size = System.Drawing.Size(50, 26)
			self._TopDielTandtextBox.Location = System.Drawing.Point(6, 144)
			self._TopDielTandtextBox.Size = System.Drawing.Size(50, 26)		
					
			####Bottom Dielectric ####	
			self._BottomDielgroupBox.Location = System.Drawing.Point(253, 89)		
			self._BottomDielgroupBox.Size = System.Drawing.Size(135, 189)
			self._BottomDielgroupBox.Text = "Bottom Dielectric"
			self._BottomDieltextBox.Location = System.Drawing.Point(6, 41)		
			self._BottomDieltextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielcomboBox.Location = System.Drawing.Point(59, 41)
			self._BottomDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._BottomDielErtextBox.Location = System.Drawing.Point(6, 94)
			self._BottomDielErtextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielTandtextBox.Location = System.Drawing.Point(6, 144)
			self._BottomDielTandtextBox.Size = System.Drawing.Size(50, 26)				
						
			#### D4 Dielectric ####		
			self._D4groupBox.Visible = False
			self._D4textBox.Visible = False
			self._D4comboBox.Visible = False
			self._D4ErtextBox.Visible = False
			self._D4TandtextBox.Visible = False	
			#### D5 Dielectric ####
			self._D5groupBox.Visible = False
			self._D5dieltextBox.Visible = False
			self._D5comboBox.Visible = False
			self._D5ErtextBox.Visible = False
			self._D5TandtextBox.Visible = False			
			#### Top Dielectric ####
			self._TopDielgroupBox.Visible = True
				
			
			
			
			####Calculate Button ####			
			self._CalculateButton.Visible = True
			self._SimulateButton.Visible = True
			self._ZoLabel.Visible = True
			self._Zotextbox.Visible = True
			self._ZoLabelDiff.Visible = False
			self._ZotextboxDiff.Visible = False			
			self._IPCeqnsLabel.Visible = True			
			self._SolutionSetupGroupBox.Visible = True
			self._groupBox2.Visible = True

			
			#Set Default Values for 50 ohm line
			self._NumberofTracesTextbox.Text = "4"
			self._PlaneThicknessTextBox.Text = "0.85"
			self._TraceThicknessTextBox.Text = "0.85"
			self._TraceWidthTextBox.Text = "5"
			self._TraceSpaceTextBox.Text = "10"
			self._BottomDielectricTextBox.Text = "7"
			self._TopDielectricTextBox.Text = "6.5"		
			self.numberoftraces = 4
			self.planethickness = 0.85
			self.tracethickness = 0.85
			self.tracewidth = 5
			self.tracespacing = 10
			self.bottomdielectricthickness = 7
			self.topdielectricthickness =6.5

			self.SMdielectricfreq = 1	
			self._SMtextBox.Text = "1"
			self.SMdielectricfrequnits = 'GHz'	
			self._SMunitscomboBox.Text = "GHz"	
			self.SMEr = 4
			self._SMErtextBox.Text = "4"
			self.SMTand = 0.02
			self._SMTandtextBox.Text = "0.02"
	
			self.Bdielfreq = 1
			self._BottomDieltextBox.Text = "1"
			self.Bdielectricfrequnits = 'GHz'
			self._BottomDielcomboBox.Text = "GHz"
			self.BdielEr = 4	
			self._BottomDielErtextBox.Text = "4"
			self.BdielTand = 0.02
			self._BottomDielTandtextBox.Text = "0.02"
	
			self.Tdielfreq = 1
			self._TopDieltextBox.Text = "1"
			self.Tdielfrequnits = 'GHz'		
			self._TopDielcomboBox.Text = "GHz"
			self.TdielEr = 4
			self._TopDielErtextBox.Text = "4"
			self.TdielTand = 0.02	
			self._TopDielTandtextBox.Text = "0.02"
	
			self.D4dielfreq = 1	
			self._D4textBox.Text = "1"
			self.D4dielfrequnits = 'GHz'
			self._D4comboBox.Text = "GHz"
			self.D4dielEr = 4
			self._D4ErtextBox.Text = "4"
			self.D4dielTand = 0.02
			self._D4TandtextBox.Text = "0.02"
	
			self.D5dielfreq = 1
			self._D5dieltextBox.Text = "1"
			self.D5dielfrequnits = 'GHz'
			self._D5comboBox.Text = "GHz"
			self.D5dielEr = 4
			self._D5ErtextBox.Text = "4"
			self.D5dielTand = 0.02
			self._D5TandtextBox.Text = "0.02"


			self._Zotextbox.Text = " "
			self._ZotextboxDiff.Text = " "		
			

		if modeltype == "Stripline - Differential":
			self._pictureBox2.Image = Image.FromFile(szPath+"Images/SL_Diff.png")
			self.microstrip = 0
			self.differential = 1
			self.broadside = 0	
			self.SLMS = 1
			self.GCPW = 0

			self._underetchradioButton.Visible = True

			self._DesignParametersgroupBox.Location = System.Drawing.Point(1006, 6)
			self._DesignParametersgroupBox.Size = System.Drawing.Size(278, 329)			

			self._numberoftraceslabel.Visible = True
			self._NumberofTracesTextbox.Visible = True
			self._numberoftraceslabel.Location = System.Drawing.Point(9, 25)
			self._NumberofTracesTextbox.Location = System.Drawing.Point(172, 20)		
						
			self._TraceWidthlabel.Visible = True
			self._TraceWidthTextBox.Visible = True				
			self._TraceWidthlabel.Location = System.Drawing.Point(9, 115)
			self._TraceWidthTextBox.Location = System.Drawing.Point(172, 110)			
			self._label10.Visible = True
			self._label10.Text = self.units		
			self._label10.Location = System.Drawing.Point(230, 110)			
			
			self._PlaneThicknessTextBox.Visible = True
			self._PlaneThicknesslabel.Visible = True			
			self._PlaneThicknesslabel.Location = System.Drawing.Point(9, 55)
			self._PlaneThicknessTextBox.Location = System.Drawing.Point(172, 50)
			self._label8.Visible = True
			self._label8.Text = self.units			
			self._label8.Location = System.Drawing.Point(230, 50)
				
			self._TraceThicknesslabel.Visible = True
			self._TraceThicknessTextBox.Visible = True
			self._TraceThicknesslabel.Location = System.Drawing.Point(9, 85)
			self._TraceThicknessTextBox.Location = System.Drawing.Point(172, 80)
			self._label9.Visible = True
			self._label9.Text = self.units			
			self._label9.Location = System.Drawing.Point(230, 80)			

			self._DifferentialSpacinglabel.Location = System.Drawing.Point(9, 235)
			self._DifferentialSpacingTextBox.Location = System.Drawing.Point(172, 230)
			self._label14.Location = System.Drawing.Point(230, 230)
			self._DifferentialSpacinglabel.Visible = True
			self._DifferentialSpacingTextBox.Visible = True
			self._label14.Visible = True
			self._label14.Text = self.units				
						
			self._TopDielectriclabel.Visible = True
			self._TopDielectricTextBox.Visible = True
			self._TopDielectriclabel.Location = System.Drawing.Point(9, 205)
			self._TopDielectricTextBox.Location = System.Drawing.Point(172, 200)
			self._TopDielectriclabel.Text = "Top Dielectric"			
			self._label12.Location = System.Drawing.Point(230, 200)
			self._label12.Visible = True
			self._label12.Text = self.units
			
			self._BottomDielectriclabel.Visible = True
			self._BottomDielectricTextBox.Visible = True
			self._BottomDielectriclabel.Location = System.Drawing.Point(9, 175)
			self._BottomDielectricTextBox.Location = System.Drawing.Point(172, 170)
			self._BottomDielectriclabel.Text = "Bottom Dielectric"		
			self._label13.Location = System.Drawing.Point(230, 170)
			self._label13.Visible = True
			self._label13.Text = self.units

			self._TraceSpaceTextBox.Visible = True
			self._TraceSpacinglabel.Visible = True
			self._TraceSpaceTextBox.Location = System.Drawing.Point(172, 140)
			self._TraceSpacinglabel.Location = System.Drawing.Point(9, 145)	
			self._TraceSpacinglabel.Text = "Trace Spacing"
			self._label11.Location = System.Drawing.Point(230, 140)			
			self._label11.Visible = True
			self._label11.Text = self.units
		
			self._SolderMaskThicknessTextBox.Visible = False
			self._SolderMaskThicknessLabel.Visible = False
			self._SolderMaskThicknessTextBox.Location = System.Drawing.Point(172, 200)
			self._SolderMaskThicknessLabel.Location = System.Drawing.Point(9, 205)
			self._SolderMaskThicknessLabel.Text = "Solder Mask Thickness"
			self._label15.Location = System.Drawing.Point(230, 200)				
			self._label15.Visible = False
			self._label15.Text = self.units	


			####  Dielectrics handline  #####
			self._SMgroupbox.Visible = False

			
			####Top Dielectric ####
			self._TopDielgroupBox.Location = System.Drawing.Point(114, 89)		
			self._TopDielgroupBox.Size = System.Drawing.Size(135, 190)
			self._TopDielgroupBox.Text = "Top Dielectric"
			self._TopDieltextBox.Location = System.Drawing.Point(6, 41)		
			self._TopDieltextBox.Size = System.Drawing.Size(50, 26)
			self._TopDielcomboBox.Location = System.Drawing.Point(59, 41)
			self._TopDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._TopDielErtextBox.Location = System.Drawing.Point(6, 94)
			self._TopDielErtextBox.Size = System.Drawing.Size(50, 26)
			self._TopDielTandtextBox.Location = System.Drawing.Point(6, 144)
			self._TopDielTandtextBox.Size = System.Drawing.Size(50, 26)
			self._TopDielgroupBox.Visible = False			
					
			####Bottom Dielectric ####	
			self._BottomDielgroupBox.Location = System.Drawing.Point(253, 89)		
			self._BottomDielgroupBox.Size = System.Drawing.Size(135, 189)
			self._BottomDielgroupBox.Text = "Bottom Dielectric"
			self._BottomDieltextBox.Location = System.Drawing.Point(6, 41)		
			self._BottomDieltextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielcomboBox.Location = System.Drawing.Point(59, 41)
			self._BottomDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._BottomDielErtextBox.Location = System.Drawing.Point(6, 94)
			self._BottomDielErtextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielTandtextBox.Location = System.Drawing.Point(6, 144)
			self._BottomDielTandtextBox.Size = System.Drawing.Size(50, 26)	
			self._BottomDielgroupBox.Visible = True			
						
			#### D4 Dielectric ####		
			self._D4groupBox.Visible = False
			self._D4textBox.Visible = False
			self._D4comboBox.Visible = False
			self._D4ErtextBox.Visible = False
			self._D4TandtextBox.Visible = False	
			#### D5 Dielectric ####
			self._D5groupBox.Visible = False
			self._D5dieltextBox.Visible = False
			self._D5comboBox.Visible = False
			self._D5ErtextBox.Visible = False
			self._D5TandtextBox.Visible = False			
			#### Top Dielectric ####
			self._TopDielgroupBox.Visible = True



			self._D5textbox.Visible = False
			self._D5thicknesslabel.Visible = False
			self._D5textbox.Location = System.Drawing.Point(172, 290)
			self._labelD5.Location = System.Drawing.Point(230, 290)				
			self._labelD5.Visible = False
			self._labelD5.Text = self.units	
								
			self._CalculateButton.Visible = True
			self._SimulateButton.Visible = True
			self._ZoLabel.Visible = True
			self._Zotextbox.Visible = True
			self._ZoLabelDiff.Visible = False
			self._ZotextboxDiff.Visible = False			
			self._IPCeqnsLabel.Visible = True			
			self._SolutionSetupGroupBox.Visible = True
			self._groupBox2.Visible = True
			self._DielPropGroupBox.Visible = True
			self._tabControl3.Visible = True			

			
			#Set Default Values for 100 ohm diff line
			self._ZoLabelDiff.Visible = True
			self._ZotextboxDiff.Visible = True
			self._NumberofTracesTextbox.Text = "4"
			self._PlaneThicknessTextBox.Text = "0.85"
			self._TraceThicknessTextBox.Text = "0.85"
			self._TraceWidthTextBox.Text = "4"
			self._TraceSpaceTextBox.Text = "10"
			self._BottomDielectricTextBox.Text = "6"
			self._TopDielectricTextBox.Text = "6"
			self._DifferentialSpacingTextBox.Text = "16"			
			self.numberoftraces = 4
			self.planethickness = 0.8
			self.tracethickness = 0.8
			self.tracewidth = 4
			self.tracespacing = 8
			self.bottomdielectricthickness = 6
			self.topdielectricthickness = 6
			self.diffspacing = 16

			self.SMdielectricfreq = 1	
			self._SMtextBox.Text = "1"
			self.SMdielectricfrequnits = 'GHz'	
			self._SMunitscomboBox.Text = "GHz"	
			self.SMEr = 4
			self._SMErtextBox.Text = "4"
			self.SMTand = 0.02
			self._SMTandtextBox.Text = "0.02"
	
			self.Bdielfreq = 1
			self._BottomDieltextBox.Text = "1"
			self.Bdielectricfrequnits = 'GHz'
			self._BottomDielcomboBox.Text = "GHz"
			self.BdielEr = 4	
			self._BottomDielErtextBox.Text = "4"
			self.BdielTand = 0.02
			self._BottomDielTandtextBox.Text = "0.02"
	
			self.Tdielfreq = 1
			self._TopDieltextBox.Text = "1"
			self.Tdielfrequnits = 'GHz'		
			self._TopDielcomboBox.Text = "GHz"
			self.TdielEr = 4
			self._TopDielErtextBox.Text = "4"
			self.TdielTand = 0.02	
			self._TopDielTandtextBox.Text = "0.02"
	
			self.D4dielfreq = 1	
			self._D4textBox.Text = "1"
			self.D4dielfrequnits = 'GHz'
			self._D4comboBox.Text = "GHz"
			self.D4dielEr = 4
			self._D4ErtextBox.Text = "4"
			self.D4dielTand = 0.02
			self._D4TandtextBox.Text = "0.02"
	
			self.D5dielfreq = 1
			self._D5dieltextBox.Text = "1"
			self.D5dielfrequnits = 'GHz'
			self._D5comboBox.Text = "GHz"
			self.D5dielEr = 4
			self._D5ErtextBox.Text = "4"
			self.D5dielTand = 0.02
			self._D5TandtextBox.Text = "0.02"
			
			
			self._Zotextbox.Text = " "
			self._ZotextboxDiff.Text = " "			
			
			
			
			

		if modeltype == "Stripline - Broadside Coupled":
			self._pictureBox2.Image = Image.FromFile(szPath+"Images/SL_Broadside.png")		
			self.microstrip = 0
			self.differential = 0
			self.broadside = 1	
			self.SLMS = 0
			self.GCPW = 0

			self._underetchradioButton.Visible = False
			self._overetchradioButton.Text = "Top Etching"			

			self._DesignParametersgroupBox.Location = System.Drawing.Point(1006, 6)
			self._DesignParametersgroupBox.Size = System.Drawing.Size(278, 329)			

			self._numberoftraceslabel.Visible = True
			self._NumberofTracesTextbox.Visible = True
			self._numberoftraceslabel.Location = System.Drawing.Point(9, 25)
			self._NumberofTracesTextbox.Location = System.Drawing.Point(172, 20)				
			
			self._TraceWidthlabel.Visible = True
			self._TraceWidthTextBox.Visible = True				
			self._TraceWidthlabel.Location = System.Drawing.Point(9, 55)
			self._TraceWidthTextBox.Location = System.Drawing.Point(172, 50)			
			self._label10.Visible = True
			self._label10.Text = self.units		
			self._label10.Location = System.Drawing.Point(230, 50)			
			
			self._PlaneThicknessTextBox.Visible = True
			self._PlaneThicknesslabel.Visible = True			
			self._PlaneThicknesslabel.Location = System.Drawing.Point(9, 85)
			self._PlaneThicknessTextBox.Location = System.Drawing.Point(172, 80)
			self._label8.Visible = True
			self._label8.Text = self.units			
			self._label8.Location = System.Drawing.Point(230, 80)
				
			self._TraceThicknesslabel.Visible = True
			self._TraceThicknessTextBox.Visible = True
			self._TraceThicknesslabel.Location = System.Drawing.Point(9, 115)
			self._TraceThicknessTextBox.Location = System.Drawing.Point(172, 110)
			self._label9.Visible = True
			self._label9.Text = self.units			
			self._label9.Location = System.Drawing.Point(230, 110)			

			self._DifferentialSpacinglabel.Location = System.Drawing.Point(9, 145)
			self._DifferentialSpacingTextBox.Location = System.Drawing.Point(172, 140)
			self._label14.Location = System.Drawing.Point(230, 140)
			self._DifferentialSpacinglabel.Visible = True
			self._DifferentialSpacingTextBox.Visible = True
			self._label14.Visible = True
			self._label14.Text = self.units							
			
			self._TopDielectriclabel.Visible = True
			self._TopDielectricTextBox.Visible = True
			self._TopDielectriclabel.Location = System.Drawing.Point(9, 175)
			self._TopDielectricTextBox.Location = System.Drawing.Point(172, 170)
			self._TopDielectriclabel.Text = "D1 Thickness"			
			self._label12.Location = System.Drawing.Point(230, 170)
			self._label12.Visible = True
			self._label12.Text = self.units			

			self._BottomDielectriclabel.Visible = True
			self._BottomDielectricTextBox.Visible = True
			self._BottomDielectriclabel.Location = System.Drawing.Point(9, 205)
			self._BottomDielectricTextBox.Location = System.Drawing.Point(172, 200)
			self._BottomDielectriclabel.Text = "D2 Thickness"		
			self._label13.Location = System.Drawing.Point(230, 200)
			self._label13.Visible = True
			self._label13.Text = self.units

			self._TraceSpaceTextBox.Visible = True
			self._TraceSpacinglabel.Visible = True
			self._TraceSpaceTextBox.Location = System.Drawing.Point(172, 230)
			self._TraceSpacinglabel.Location = System.Drawing.Point(9, 235)	
			self._TraceSpacinglabel.Text = "D3 Thickness"
			self._label11.Location = System.Drawing.Point(230, 230)			
			self._label11.Visible = True
			self._label11.Text = self.units	
	
			self._SolderMaskThicknessTextBox.Visible = True
			self._SolderMaskThicknessLabel.Visible = True
			self._SolderMaskThicknessTextBox.Location = System.Drawing.Point(172, 260)
			self._SolderMaskThicknessLabel.Location = System.Drawing.Point(9, 265)
			self._SolderMaskThicknessLabel.Text = "D4 Thickness"
			self._label15.Location = System.Drawing.Point(230, 260)				
			self._label15.Visible = True
			self._label15.Text = self.units		

			self._D5textbox.Visible = True
			self._D5thicknesslabel.Visible = True
			self._D5thicknesslabel.Location = System.Drawing.Point(9, 295)
			self._D5textbox.Location = System.Drawing.Point(172, 290)
			self._labelD5.Location = System.Drawing.Point(230, 290)	
			self._D5thicknesslabel.Text = "D5 Thickness"			
			self._labelD5.Visible = True
			self._labelD5.Text = self.units	
			
			###Calculate Button  ####
			self._CalculateButton.Visible = True
			self._SimulateButton.Visible = True
			self._ZoLabel.Visible = True
			self._Zotextbox.Visible = True
			self._ZoLabelDiff.Visible = False
			self._ZotextboxDiff.Visible = False		
			self._IPCeqnsLabel.Visible = True			
			self._SolutionSetupGroupBox.Visible = True
			self._groupBox2.Visible = True
			
			self._DielPropGroupBox.Visible = True
			self._tabControl3.Visible = True			
			self._SMgroupbox.Visible = True
		
			
			### set Dielecrics panel to reflect model selected  ###
			self._label2.Location = System.Drawing.Point(13, 118)		
			self._label3.Location = System.Drawing.Point(13, 174)	
			self._label4.Location = System.Drawing.Point(13, 235)

			self._BottomDielgroupBox.Visible = True
			self._TopDielgroupBox.Visible = True
			self._SMgroupbox.Visible = True
			
			#### D4 Dielectric ####	
			self._D4groupBox.Location = System.Drawing.Point(363, 89)	
			self._D4groupBox.Size = System.Drawing.Size(80, 190)
			self._D4groupBox.Visible = True
			self._D4textBox.Visible = True
			self._D4comboBox.Visible = True
			self._D4ErtextBox.Visible = True
			self._D4TandtextBox.Visible = True	
			#### D5 Dielectric ####
			self._D5groupBox.Visible = True
			self._D5dieltextBox.Visible = True
			self._D5comboBox.Visible = True
			self._D5ErtextBox.Visible = True
			self._D5TandtextBox.Visible = True			
					
			####Solder Mask Dielectric ####
			self._SMgroupbox.Size = System.Drawing.Size(80, 190)
			self._SMgroupbox.Text = "D1"	
			self._SMtextBox.Location = System.Drawing.Point(10, 24)		
			self._SMtextBox.Size = System.Drawing.Size(60, 26)
			self._SMunitscomboBox.Location = System.Drawing.Point(10, 53)
			self._SMunitscomboBox.Size = System.Drawing.Size(60, 26)
			self._SMErtextBox.Location = System.Drawing.Point(10, 94)
			self._SMErtextBox.Size = System.Drawing.Size(60, 26)
			self._SMTandtextBox.Location = System.Drawing.Point(10, 144)
			self._SMTandtextBox.Size = System.Drawing.Size(60, 26)
			####Bottom Dielectric ####	
			self._BottomDielgroupBox.Location = System.Drawing.Point(197, 89)		
			self._BottomDielgroupBox.Size = System.Drawing.Size(80, 190)
			self._BottomDielgroupBox.Text = "D2"
			self._BottomDieltextBox.Location = System.Drawing.Point(10, 24)		
			self._BottomDieltextBox.Size = System.Drawing.Size(60, 26)
			self._BottomDielcomboBox.Location = System.Drawing.Point(10, 53)
			self._BottomDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._BottomDielErtextBox.Location = System.Drawing.Point(10, 94)
			self._BottomDielErtextBox.Size = System.Drawing.Size(60, 26)
			self._BottomDielTandtextBox.Location = System.Drawing.Point(10, 144)
			self._BottomDielTandtextBox.Size = System.Drawing.Size(60, 26)			
			####Top Dielectric ####			
			self._TopDielgroupBox.Location = System.Drawing.Point(280, 89)		
			self._TopDielgroupBox.Size = System.Drawing.Size(80, 190)
			self._TopDielgroupBox.Text = "D3"
			self._TopDieltextBox.Location = System.Drawing.Point(10, 24)		
			self._TopDieltextBox.Size = System.Drawing.Size(60, 26)
			self._TopDielcomboBox.Location = System.Drawing.Point(10, 53)
			self._TopDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._TopDielErtextBox.Location = System.Drawing.Point(10, 94)
			self._TopDielErtextBox.Size = System.Drawing.Size(60, 26)
			self._TopDielTandtextBox.Location = System.Drawing.Point(10, 144)
			self._TopDielTandtextBox.Size = System.Drawing.Size(60, 26)			

		
		
			#Set Default Values for 100 ohm diff line

			self._SolderMaskThicknessTextBox.Text = "8"	
			self._NumberofTracesTextbox.Text = "4"
			self._PlaneThicknessTextBox.Text = "1"
			self._TraceThicknessTextBox.Text = "1"
			self._TraceWidthTextBox.Text = "3.5"
			self._TraceSpaceTextBox.Text = "7.25"
			self._BottomDielectricTextBox.Text = "8"
			self._TopDielectricTextBox.Text = "8"
			self._DifferentialSpacingTextBox.Text = "16"			
			self._D5textbox.Text = "8"
			self.numberoftraces = 4
			self.planethickness = 1
			self.tracethickness = 1
			self.tracewidth = 3.5
			self.tracespacing = 7.25
			self.bottomdielectricthickness = 8
			self.topdielectricthickness = 8
			self.diffspacing = 16
			self.D5thickness = 6.12
			self.soldermaskthickness = 8

			self.SMdielectricfreq = 1	
			self._SMtextBox.Text = "1"
			self.SMdielectricfrequnits = 'GHz'	
			self._SMunitscomboBox.Text = "GHz"	
			self.SMEr = 4
			self._SMErtextBox.Text = "4"
			self.SMTand = 0.02
			self._SMTandtextBox.Text = "0.02"
	
			self.Bdielfreq = 1
			self._BottomDieltextBox.Text = "1"
			self.Bdielectricfrequnits = 'GHz'
			self._BottomDielcomboBox.Text = "GHz"
			self.BdielEr = 4	
			self._BottomDielErtextBox.Text = "4"
			self.BdielTand = 0.02
			self._BottomDielTandtextBox.Text = "0.02"
	
			self.Tdielfreq = 1
			self._TopDieltextBox.Text = "1"
			self.Tdielfrequnits = 'GHz'		
			self._TopDielcomboBox.Text = "GHz"
			self.TdielEr = 4
			self._TopDielErtextBox.Text = "4"
			self.TdielTand = 0.02	
			self._TopDielTandtextBox.Text = "0.02"
	
			self.D4dielfreq = 1	
			self._D4textBox.Text = "1"
			self.D4dielfrequnits = 'GHz'
			self._D4comboBox.Text = "GHz"
			self.D4dielEr = 4
			self._D4ErtextBox.Text = "4"
			self.D4dielTand = 0.02
			self._D4TandtextBox.Text = "0.02"
	
			self.D5dielfreq = 1
			self._D5dieltextBox.Text = "1"
			self.D5dielfrequnits = 'GHz'
			self._D5comboBox.Text = "GHz"
			self.D5dielEr = 4
			self._D5ErtextBox.Text = "4"
			self.D5dielTand = 0.02
			self._D5TandtextBox.Text = "0.02"

			self._Zotextbox.Text = " "
			self._ZotextboxDiff.Text = " "


		if modeltype == "Grounded Coplanar Waveguide":
			self._pictureBox2.Image = Image.FromFile(szPath+"Images/GCPW.png")
			self.microstrip = 8
			self.differential = 0
			self.broadside = 0	
			self.GCPW = 1
			self.SLMS = 0

			self._underetchradioButton.Visible = False
			self._overetchradioButton.Text = "Etching"			

			self._DesignParametersgroupBox.Location = System.Drawing.Point(1006, 6)
			self._DesignParametersgroupBox.Size = System.Drawing.Size(278, 329)			

			self._numberoftraceslabel.Visible = True
			self._NumberofTracesTextbox.Visible = True
			self._numberoftraceslabel.Location = System.Drawing.Point(9, 25)
			self._NumberofTracesTextbox.Location = System.Drawing.Point(172, 20)				
			
			self._TraceWidthlabel.Visible = True
			self._TraceWidthTextBox.Visible = True				
			self._TraceWidthlabel.Location = System.Drawing.Point(9, 55)
			self._TraceWidthTextBox.Location = System.Drawing.Point(172, 50)			
			self._label10.Visible = True
			self._label10.Text = self.units		
			self._label10.Location = System.Drawing.Point(230, 50)			
			
			self._PlaneThicknessTextBox.Visible = True
			self._PlaneThicknesslabel.Visible = True			
			self._PlaneThicknesslabel.Location = System.Drawing.Point(9, 175)
			self._PlaneThicknessTextBox.Location = System.Drawing.Point(172, 170)
			self._label8.Visible = True
			self._label8.Text = self.units			
			self._label8.Location = System.Drawing.Point(230, 170)
				
			self._TraceThicknesslabel.Visible = True
			self._TraceThicknessTextBox.Visible = True
			self._TraceThicknesslabel.Location = System.Drawing.Point(9, 145)
			self._TraceThicknessTextBox.Location = System.Drawing.Point(172, 140)
			self._label9.Visible = True
			self._label9.Text = self.units			
			self._label9.Location = System.Drawing.Point(230, 140)			

			self._DifferentialSpacinglabel.Location = System.Drawing.Point(9, 145)
			self._DifferentialSpacingTextBox.Location = System.Drawing.Point(172, 140)
			self._label14.Location = System.Drawing.Point(230, 140)
			self._DifferentialSpacinglabel.Visible = False
			self._DifferentialSpacingTextBox.Visible = False
			self._label14.Visible = False
			self._label14.Text = self.units							
			
			self._TopDielectriclabel.Visible = False
			self._TopDielectricTextBox.Visible = False
			self._TopDielectriclabel.Location = System.Drawing.Point(9, 175)
			self._TopDielectricTextBox.Location = System.Drawing.Point(172, 170)
			self._TopDielectriclabel.Text = "D1 Thickness"			
			self._label12.Location = System.Drawing.Point(230, 170)
			self._label12.Visible = False
			self._label12.Text = self.units			

			self._BottomDielectriclabel.Visible = True
			self._BottomDielectricTextBox.Visible = True
			self._BottomDielectriclabel.Location = System.Drawing.Point(9, 235)
			self._BottomDielectricTextBox.Location = System.Drawing.Point(172, 230)
			self._BottomDielectriclabel.Text = "Dielectric Thickness"		
			self._label13.Location = System.Drawing.Point(230, 230)
			self._label13.Visible = True
			self._label13.Text = self.units

			self._TraceSpaceTextBox.Visible = True
			self._TraceSpacinglabel.Visible = True
			self._TraceSpaceTextBox.Location = System.Drawing.Point(172, 110)
			self._TraceSpacinglabel.Location = System.Drawing.Point(9, 115)	
			self._TraceSpacinglabel.Text = "Trace Spacing"
			self._label11.Location = System.Drawing.Point(230, 110)			
			self._label11.Visible = True
			self._label11.Text = self.units	
	
			self._SolderMaskThicknessTextBox.Visible = True
			self._SolderMaskThicknessLabel.Visible = True
			self._SolderMaskThicknessTextBox.Location = System.Drawing.Point(172, 200)
			self._SolderMaskThicknessLabel.Location = System.Drawing.Point(9, 205)
			self._SolderMaskThicknessLabel.Text = "Soldermask Thickness"
			self._label15.Location = System.Drawing.Point(230, 200)				
			self._label15.Visible = True
			self._label15.Text = self.units		

			self._D5textbox.Visible = True
			self._D5thicknesslabel.Visible = True
			self._D5thicknesslabel.Location = System.Drawing.Point(9, 85)
			self._D5textbox.Location = System.Drawing.Point(172, 80)
			self._labelD5.Location = System.Drawing.Point(230, 80)
			self._D5thicknesslabel.Text = "Gnd Width"			
			self._labelD5.Visible = True
			self._labelD5.Text = self.units	
			
			###Calculate Button  ####
			self._CalculateButton.Visible = True
			self._SimulateButton.Visible = True
			self._ZoLabel.Visible = True
			self._Zotextbox.Visible = True
			self._ZoLabelDiff.Visible = True
			self._ZotextboxDiff.Visible = True	
			self._ZoLabelDiff.Text = "Er(eff):"			
			self._IPCeqnsLabel.Visible = True			
			self._SolutionSetupGroupBox.Visible = True
			self._groupBox2.Visible = True
			
			self._DielPropGroupBox.Visible = True
			self._tabControl3.Visible = True			
			self._SMgroupbox.Visible = True
		
			
			####  Dielectrics handline  #####		
			self._DielPropGroupBox.Visible = True
			self._tabControl3.Visible = True			
			self._SMgroupbox.Visible = True
			self._BottomDielgroupBox.Visible = True
			self._TopDielgroupBox.Visible = False
			
			####Solder Mask Dielectric ####
			self._SMgroupbox.Size = System.Drawing.Size(135, 189)
			self._SMgroupbox.Location = System.Drawing.Point(114, 89)			
			self._SMgroupbox.Text = "Solder Mask"	
			self._SMtextBox.Location = System.Drawing.Point(6, 41)		
			self._SMtextBox.Size = System.Drawing.Size(50, 26)
			self._SMunitscomboBox.Location = System.Drawing.Point(59, 41)
			self._SMunitscomboBox.Size = System.Drawing.Size(60, 26)
			self._SMErtextBox.Location = System.Drawing.Point(6, 94)
			self._SMErtextBox.Size = System.Drawing.Size(50, 26)
			self._SMTandtextBox.Location = System.Drawing.Point(6, 144)
			self._SMTandtextBox.Size = System.Drawing.Size(50, 26)
			self._SMgroupbox.Visible = True
			self._SMtextBox.Visible = True
			self._SMunitscomboBox.Visible = True
			self._SMErtextBox.Visible = True			
			
			
			####Bottom Dielectric ####	
			self._BottomDielgroupBox.Location = System.Drawing.Point(253, 89)		
			self._BottomDielgroupBox.Size = System.Drawing.Size(135, 189)
			self._BottomDielgroupBox.Text = "Bottom Dielectric"
			self._BottomDieltextBox.Location = System.Drawing.Point(6, 41)		
			self._BottomDieltextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielcomboBox.Location = System.Drawing.Point(59, 41)
			self._BottomDielcomboBox.Size = System.Drawing.Size(60, 26)
			self._BottomDielErtextBox.Location = System.Drawing.Point(6, 94)
			self._BottomDielErtextBox.Size = System.Drawing.Size(50, 26)
			self._BottomDielTandtextBox.Location = System.Drawing.Point(6, 144)
			self._BottomDielTandtextBox.Size = System.Drawing.Size(50, 26)										
			
			#### D4 Dielectric ####		
			self._D4groupBox.Visible = False
			self._D4textBox.Visible = False
			self._D4comboBox.Visible = False
			self._D4ErtextBox.Visible = False
			self._D4TandtextBox.Visible = False	
			#### D5 Dielectric ####
			self._D5groupBox.Visible = False
			self._D5dieltextBox.Visible = False
			self._D5comboBox.Visible = False
			self._D5ErtextBox.Visible = False
			self._D5TandtextBox.Visible = False			
			#### Top Dielectric ####
			self._TopDielgroupBox.Visible = False			
			
	
		
			#Set Default Values for 100 ohm diff line

			self._SolderMaskThicknessTextBox.Text = "0.5"	
			self._NumberofTracesTextbox.Text = "1"
			self._PlaneThicknessTextBox.Text = "0.85"
			self._TraceThicknessTextBox.Text = "0.85"
			self._TraceWidthTextBox.Text = "12.5"
			self._TraceSpaceTextBox.Text = "1"
			self._BottomDielectricTextBox.Text = "9"			
			self._D5textbox.Text = "36"
			self.numberoftraces = 1
			self.planethickness = 0.85
			self.tracethickness = 0.85
			self.tracewidth = 12.5
			self.tracespacing = 1
			self.bottomdielectricthickness = 9
			self.D5thickness = 36
			self.soldermaskthickness = 0.5

			self.SMdielectricfreq = 1	
			self._SMtextBox.Text = "1"
			self.SMdielectricfrequnits = 'GHz'	
			self._SMunitscomboBox.Text = "GHz"	
			self.SMEr = 4
			self._SMErtextBox.Text = "4"
			self.SMTand = 0.02
			self._SMTandtextBox.Text = "0.02"
	
			self.Bdielfreq = 1
			self._BottomDieltextBox.Text = "1"
			self.Bdielectricfrequnits = 'GHz'
			self._BottomDielcomboBox.Text = "GHz"
			self.BdielEr = 4	
			self._BottomDielErtextBox.Text = "4"
			self.BdielTand = 0.02
			self._BottomDielTandtextBox.Text = "0.02"
	
			self.Tdielfreq = 1
			self._TopDieltextBox.Text = "1"
			self.Tdielfrequnits = 'GHz'		
			self._TopDielcomboBox.Text = "GHz"
			self.TdielEr = 4
			self._TopDielErtextBox.Text = "4"
			self.TdielTand = 0.02	
			self._TopDielTandtextBox.Text = "0.02"
	
			self.D4dielfreq = 1	
			self._D4textBox.Text = "1"
			self.D4dielfrequnits = 'GHz'
			self._D4comboBox.Text = "GHz"
			self.D4dielEr = 4
			self._D4ErtextBox.Text = "4"
			self.D4dielTand = 0.02
			self._D4TandtextBox.Text = "0.02"
	
			self.D5dielfreq = 1
			self._D5dieltextBox.Text = "1"
			self.D5dielfrequnits = 'GHz'
			self._D5comboBox.Text = "GHz"
			self.D5dielEr = 4
			self._D5ErtextBox.Text = "4"
			self.D5dielTand = 0.02
			self._D5TandtextBox.Text = "0.02"


			self._Zotextbox.Text = " "
			self._ZotextboxDiff.Text = " "

#************************************#
#**** -- Help -> About message here  #			
#************************************#
		pass

	def ExitToolStripMenuItemClick(self, sender, e):
		self.Close()
		pass

	def AboutToolStripMenuItemClick(self, sender, e):
		MessageBox.Show("Notes:\n\nTransmission line equations based on IPC-2251 specification.  Grounded Coplanar Waveguide equations are from Wadell Brian C. (1991) Transmission Line Design Handbook Artech House Antennas and Propagation Library) (Artech House Microwave Library).  \n\nK(k), Elliptical integral of the first kind was approximated with a power series expansion of 25 terms for the GCPW calculations \n\nEr used for stripline Zo and Zodiff uses the bottom dielectric Er only.  The stripline equations assume stripline top and bottom dielectric materials are the same with respect to Er \n\nUpdates Comming:\nAbility to save a design and re-import\nAutomatic creation of W-element models \nPlotting of Zo(f) and Attenuation(length)\nHave a good idea for improvements? Please Let me know \n\n\n\nCreated by Guy Barnes, Lead Technical Services Engineer at Ansys Corp.  For bug submissions and or enhancement requests please contact:  guy.barnes@ansys.com\n\nBuild on: December 14, 2015" ,"ANSYS Transmission Line Toolkit Version 2.1 for ANSYS Electronics Desktop 2016.0")
		pass








#*************************************************************************************************************************************


#************************************************** ---- Event Handeling Below ----  *************************************************



#*************************************************************************************************************************************




#########################################
	#conductor roughness input handline #
	#################################################################################

	def NoRoughnessRadioButtonCheckedChanged(self, sender, e):
		self.roughnesstype = 0
		self._SurfaceRoughLabelTop.Visible = False
		self._HallHurayLabelTop.Visible = False
		self._HallHuraytTextBoxTop.Visible = False
		self._SurfaceRoughTextBoxTop.Visible = False
		self._RoughnessUnitsComboBox.Visible = False		
		
		self._SurfaceRoughLabelSides.Visible = False
		self._HallHurayLabelSides.Visible = False
		self._HallHuraytTextBoxSides.Visible = False
		self._SurfaceRoughTextBoxSides.Visible = False
		

		self._SurfaceRoughLabelBottom.Visible = False
		self._HallHurayLabelBottom.Visible = False
		self._HallHuraytTextBoxBottom.Visible = False
		self._SurfaceRoughTextBoxBottom.Visible = False
		self._ConductorExampleinputlabel.Visible = False
		self._RoughnessUnitslabel.Visible = False
		
		pass

	def HammerstadRadioButtonCheckedChanged(self, sender, e):
		self.roughnesstype = 1
		
		self._SurfaceRoughLabelTop.Text = "Surface Roughness (RMS):"	
		self._SurfaceRoughLabelSides.Text = "Surface Roughness (RMS):"	
		self._SurfaceRoughLabelBottom.Text = "Surface Roughness (RMS):"		
		
		self._SurfaceRoughLabelTop.Visible = True
		self._HallHurayLabelTop.Visible = False
		self._HallHuraytTextBoxTop.Visible = False
		self._SurfaceRoughTextBoxTop.Visible = True
		self._RoughnessUnitsComboBox.Visible = True
		
		self._SurfaceRoughLabelSides.Visible = True
		self._HallHurayLabelSides.Visible = False
		self._HallHuraytTextBoxSides.Visible = False
		self._SurfaceRoughTextBoxSides.Visible = True

		
		self._SurfaceRoughLabelBottom.Visible = True
		self._HallHurayLabelBottom.Visible = False
		self._HallHuraytTextBoxBottom.Visible = False
		self._SurfaceRoughTextBoxBottom.Visible = True

		self._TopTraceGroupBox.Visible = True
		self._SidesTraceGroupBox.Visible = True
		self._BottomTraceGroupBox.Visible = True
		self._RoughnessUnitslabel.Visible = True
		self._RoughnessUnitsComboBox.Visible = True
	
		self._ConductorExampleinputlabel.Visible = True	
		self._RoughnessUnitslabel.Visible = True
		
		self._SurfaceRoughTextBoxTop.Text = "2.5"
		self._SurfaceRoughTextBoxSides.Text = "2.5"
		self._SurfaceRoughTextBoxBottom.Text = "2.5"
		
		pass

	#typical values for Huray method:  Nodule Radius = 0.5um  Hall-Huray Surface Ratio = 2.9
	def HurayRadioButtonCheckedChanged(self, sender, e):
		self.roughnesstype = 2
		
		self._SurfaceRoughLabelTop.Text = "Nodule Radius:"	
		self._SurfaceRoughLabelSides.Text = "Nodule Radius:"	
		self._SurfaceRoughLabelBottom.Text = "Nodule Radius:"			
		self._SurfaceRoughLabelTop.Visible = True		
		self._HallHurayLabelTop.Visible = True		
		self._HallHuraytTextBoxTop.Visible = True			
		self._SurfaceRoughTextBoxTop.Visible = True		
		self._RoughnessUnitsComboBox.Visible = True		
		self._SurfaceRoughLabelSides.Visible = True		
		self._HallHurayLabelSides.Visible = True		
		self._HallHuraytTextBoxSides.Visible = True		
		self._SurfaceRoughTextBoxSides.Visible = True		
		self._SurfaceRoughLabelBottom.Visible = True		
		self._HallHurayLabelBottom.Visible = True		
		self._HallHuraytTextBoxBottom.Visible = True		
		self._SurfaceRoughTextBoxBottom.Visible = True		

		self._TopTraceGroupBox.Visible = True
		self._SidesTraceGroupBox.Visible = True
		self._BottomTraceGroupBox.Visible = True
		self._RoughnessUnitslabel.Visible = True
		self._RoughnessUnitsComboBox.Visible = True
		
		self._ConductorExampleinputlabel.Visible = True
		self._RoughnessUnitslabel.Visible = True

		self._SurfaceRoughTextBoxTop.Text = "0.5"
		self._SurfaceRoughTextBoxSides.Text = "0.5"
		self._SurfaceRoughTextBoxBottom.Text = "0.5"
		
		pass

	#Capturing Parameter Input roughness Huray Model from GUI to Design Variables 
	def HallHuraytTextBoxTopTextChanged(self, sender, e):
		self.HHsurfaceratiotop = sender.Text		
		#error trapping, make sure values entered are valid
		if self.HHsurfaceratiotop == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.HHsurfaceratiotop == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.HHsurfaceratiotop)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.HHsurfaceratiotop)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.HHsurfaceratiotop)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
	
	def SurfaceRoughTextBoxTopTextChanged(self, sender, e):
		self.noduleradiustop = sender.Text 		
		self.surfaceroughnesstop = sender.Text
		#error trapping, make sure values entered are valid
		if self.noduleradiustop == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.noduleradiustop == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.noduleradiustop)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.noduleradiustop)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.noduleradiustop)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		#error trapping, make sure values entered are valid
		if self.surfaceroughnesstop == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.surfaceroughnesstop == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.surfaceroughnesstop)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.surfaceroughnesstop)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.surfaceroughnesstop)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass


	def HallHuraytTextBoxSidesTextChanged(self, sender, e):
		self.HHsurfaceratiosides = sender.Text		
		#error trapping, make sure values entered are valid
		if self.HHsurfaceratiosides == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.HHsurfaceratiosides == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.HHsurfaceratiosides)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.HHsurfaceratiosides)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.HHsurfaceratiosides)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
	
	def SurfaceRoughTextBoxSidesTextChanged(self, sender, e):
		self.noduleradiussides = sender.Text 
		self.surfaceroughnessSides = sender.Text		
		#error trapping, make sure values entered are valid
		if self.noduleradiussides == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.noduleradiussides == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.noduleradiussides)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.noduleradiussides)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.noduleradiussides)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		#error trapping, make sure values entered are valid
		if self.surfaceroughnessSides == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.surfaceroughnessSides == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.surfaceroughnessSides)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.surfaceroughnessSides)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.surfaceroughnessSides)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass


	def HallHuraytTextBoxBottomTextChanged(self, sender, e):
		self.HHsurfaceratiobottom = sender.Text		
		#error trapping, make sure values entered are valid
		if self.HHsurfaceratiobottom == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.HHsurfaceratiobottom == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.HHsurfaceratiobottom)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.HHsurfaceratiobottom)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.HHsurfaceratiobottom)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
	
	def SurfaceRoughTextBoxBottomTextChanged(self, sender, e):
		self.noduleradiusbottom = sender.Text
		self.surfaceroughnessbottom = sender.Text		
		#error trapping, make sure values entered are valid
		if self.noduleradiusbottom == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.noduleradiusbottom == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.noduleradiusbottom)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.noduleradiusbottom)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.noduleradiusbottom)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		#error trapping, make sure values entered are valid
		if self.surfaceroughnessbottom == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.surfaceroughnessbottom == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.surfaceroughnessbottom)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.surfaceroughnessbottom)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.surfaceroughnessbottom)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass


	def RoughnessUnitsComboBoxSelectedIndexChanged(self, sender, e):
		self.surfaceroughnessunits = str(sender.Text)		
		pass








###########################################################	
	#Units: record selected radio buttons for model units #
	####################################################################
	def MillsRadioButtonCheckedChanged(self, sender, e):
		self.units = "mil"
		self.soldermaskunits= "mil"		
		self._label8.Text = self.units
		self._label9.Text = self.units
		self._label10.Text = self.units
		self._label11.Text = self.units
		self._label12.Text = self.units
		self._label13.Text = self.units
		self._label14.Text = self.units
		self._label15.Text = self.units	
		self._labelD5.Text = self.units
		pass

	def InchesRadioButtonCheckedChanged(self, sender, e):
		self.units = "in"
		self.soldermaskunits= "in"			
		self._label8.Text = self.units
		self._label9.Text = self.units
		self._label10.Text = self.units
		self._label11.Text = self.units
		self._label12.Text = self.units
		self._label13.Text = self.units
		self._label14.Text = self.units	
		self._label15.Text = self.units	
		self._labelD5.Text = self.units				
		pass

	def MicronsRadioButtonCheckedChanged(self, sender, e):	
		self.units = "um"	
		self.soldermaskunits= "um"			
		self._label8.Text = self.units
		self._label9.Text = self.units
		self._label10.Text = self.units
		self._label11.Text = self.units
		self._label12.Text = self.units
		self._label13.Text = self.units
		self._label14.Text = self.units	
		self._label15.Text = self.units
		self._labelD5.Text = self.units				
		pass

	def MillimetersRadioButtonCheckedChanged(self, sender, e):		
		self.units = "mm"
		self.soldermaskunits= "mm"			
		self._label8.Text = self.units
		self._label9.Text = self.units
		self._label10.Text = self.units
		self._label11.Text = self.units
		self._label12.Text = self.units
		self._label13.Text = self.units
		self._label14.Text = self.units	
		self._label15.Text = self.units
		self._labelD5.Text = self.units				
		pass

	
##################################
	# Show EM solver GUI or not  #
	#############################################################
	def GUIshowCheckedChanged(self, sender, e):
		GUIshow = "show"
		pass

	def GUIhideCheckedChanged(self, sender, e):
		GUIshow = "hide"
		pass



########################################
	# w-element or spice model export  #
	#############################################################
	def TabularRadioButtonCheckedChanged(self, sender, e):
		circuitmodel = "welement"
		
		pass

	def LumpedElementRadioButtonCheckedChanged(self, sender, e):
		circuitmodel = "lumped"
		pass

#not working#
##############################################################################
	# button to select directory path to deposite w or lumped element model  #
	##########################################################################################
	def ModelLocationButtonClick(self, sender, e):
		openfile = OpenFileDialog()
		openfile.RestoreDirectory = True
		if openfile.ShowDialog() != DialogResult.OK:
			return
		pass

			
		
		
		
	
####################################################
	#Solution Frequency and or Sweep info handling #
	#############################################################
	def SolutionFreqTextBoxTextChanged(self, sender, e):
		self.solutionfreq = sender.Text		
		#error trapping, make sure values entered are valid
		if self.solutionfreq == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.solutionfreq == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.solutionfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.solutionfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.solutionfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	
	
	
	def FreqStartTextBoxTextChanged(self, sender, e):
		self.solutionstartfreq = sender.Text	
		#error trapping, make sure values entered are valid
		if self.solutionstartfreq == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.solutionstartfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.solutionstartfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.solutionstartfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def FreqStopTextBoxTextChanged(self, sender, e):
		self.solutionstopfreq = sender.Text
		#error trapping, make sure values entered are valid
		if self.solutionstopfreq == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.solutionstopfreq == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.solutionstopfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.solutionstopfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.solutionstopfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def FreqStepTextBoxTextChanged(self, sender, e):
		self.solutionstepfreq = sender.Text
		#error trapping, make sure values entered are valid
		if self.solutionstepfreq == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.solutionstepfreq == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.solutionstepfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.solutionstepfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.solutionstepfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def SolutionfrequnitscomboBoxSelectedIndexChanged(self, sender, e):
		self.Solutionfrequnits = sender.Text	
		pass

	def StartFrequnitscomboBoxSelectedIndexChanged(self, sender, e):
		self.StartFrequnits = sender.Text	
		pass

	def StopFrequnitscomboBoxSelectedIndexChanged(self, sender, e):
		self.StopFrequnits = sender.Text	
		pass

	def FreqStepunitscomboBoxSelectedIndexChanged(self, sender, e):
		self.FreqStepunits = sender.Text
		pass


	def NoneRadioButtonCheckedChanged(self, sender, e):
		self.freqsweeptype = 'none'
		self._StartFreqLabel.Visible = False
		self._FreqStopLabel.Visible = False
		self._FreqStepLabel.Visible = False
		self._FreqStartTextBox.Visible = False
		self._FreqStopTextBox.Visible = False
		self._FreqStepTextBox.Visible = False
		self._StartFrequnitscomboBox.Visible = False
		self._StopFrequnitscomboBox.Visible = False
		self._FreqStepunitscomboBox.Visible = False
		pass

	def DiscreteRadioButtonCheckedChanged(self, sender, e):
		self._FreqStartTextBox.Enabled = True
		self.freqsweeptype = 'Discrete'
		self._FreqStartTextBox.Text = "0"
		self._StartFreqLabel.Visible = True
		self._FreqStopLabel.Visible = True
		self._FreqStepLabel.Visible = True
		self._FreqStartTextBox.Visible = True
		self._FreqStopTextBox.Visible = True
		self._FreqStepTextBox.Visible = True
		self._StartFrequnitscomboBox.Visible = True
		self._StopFrequnitscomboBox.Visible = True
		self._FreqStepunitscomboBox.Visible = True		
		pass		

	def InterpolatingRadioButtonCheckedChanged(self, sender, e):
		self._FreqStartTextBox.Enabled = False
		self._FreqStartTextBox.Text = "0"
		self.freqsweeptype = 'Interpolating'
		self._StartFreqLabel.Visible = True
		self._FreqStopLabel.Visible = True
		self._FreqStepLabel.Visible = True
		self._FreqStartTextBox.Visible = True
		self._FreqStopTextBox.Visible = True
		self._FreqStepTextBox.Visible = True
		self._StartFrequnitscomboBox.Visible = True
		self._StopFrequnitscomboBox.Visible = True
		self._FreqStepunitscomboBox.Visible = True		
		pass		



##########################
#     Event Handling     #---------------------------------------------------------------------------------------------------------------------------------------------------
##########################




######################################
#     Dielectrics Event Handling     #
###########################################################################################################################

	def SMtextBoxTextChanged(self, sender, e):
		self.SMdielectricfreq = sender.Text
		#error trapping, make sure values entered are valid
		if self.SMdielectricfreq == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.SMdielectricfreq == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.SMdielectricfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.SMdielectricfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.SMdielectricfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def SMunitscomboBoxSelectedIndexChanged(self, sender, e):
		self.SMdielectricfrequnits = sender.Text		
		pass

	def SMErtextBoxTextChanged(self, sender, e):
		self.SMEr = sender.Text
		#error trapping, make sure values entered are valid
		if self.SMEr == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.SMEr == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.SMEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.SMEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.SMEr)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def SMTandtextBoxTextChanged(self, sender, e):
		self.SMTand = sender.Text
		#error trapping, make sure values entered are valid
		if self.SMTand == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.SMTand == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.SMTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.SMTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.SMTand)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def BottomDieltextBoxTextChanged(self, sender, e):
		self.Bdielfreq = sender.Text
		#error trapping, make sure values entered are valid
		if self.Bdielfreq == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.Bdielfreq == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.Bdielfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.Bdielfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.Bdielfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def BottomDielcomboBoxSelectedIndexChanged(self, sender, e):
		self.Bdielectricfrequnits = sender.Text		
		pass

	def BottomDielErtextBoxTextChanged(self, sender, e):
		self.BdielEr = sender.Text
		#error trapping, make sure values entered are valid
		if self.BdielEr == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.BdielEr == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.BdielEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.BdielEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.BdielEr)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def BottomDielTandtextBoxTextChanged(self, sender, e):
		self.BdielTand  = sender.Text
		#error trapping, make sure values entered are valid
		if self.BdielTand == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.BdielTand == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.BdielTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.BdielTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.BdielTand)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def TopDieltextBoxTextChanged(self, sender, e):
		self.Tdielfreq = sender.Text
		#error trapping, make sure values entered are valid
		if self.Tdielfreq == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.Tdielfreq == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.Tdielfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.Tdielfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.Tdielfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def TopDielcomboBoxSelectedIndexChanged(self, sender, e):
		self.Tdielfrequnits = sender.Text
		pass
	

	def TopDielErtextBoxTextChanged(self, sender, e):
		self.TdielEr = sender.Text
		#error trapping, make sure values entered are valid
		if self.TdielEr == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.TdielEr == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.TdielEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.TdielEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.TdielEr)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def TopDielTandtextBoxTextChanged(self, sender, e):
		self.TdielTand = sender.Text
		#error trapping, make sure values entered are valid
		if self.TdielTand == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.TdielTand == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.TdielTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.TdielTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.TdielTand)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass



########################################
	# Design Parameter Events Handling #
	###########################################################################

	def NumberofTracesTextboxTextChanged(self, sender, e):	
		self.numberoftraces = sender.Text

		#error trapping, make sure values entered are valid
		if self.numberoftraces == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.numberoftraces == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.numberoftraces)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.numberoftraces)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[.]', str(self.numberoftraces)):
			self._errorProvider1.SetError(sender,"Error:  Entry Must Be a Whole Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [int(self.numberoftraces)] and [int(self.numberoftraces)] > 0
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass	



	def PlaneThicknessTextBoxTextChanged(self, sender, e):		
		self.planethickness = sender.Text

		#error trapping, make sure values entered are valid
		if self.planethickness == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.planethickness == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.planethickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.planethickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.planethickness)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	
	def TraceThicknessTextBoxTextChanged(self, sender, e):		
		self.tracethickness = sender.Text
		#error trapping, make sure values entered are valid
		if self.tracethickness == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.tracethickness == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.tracethickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.tracethickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.tracethickness)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def TraceWidthTextBoxTextChanged(self, sender, e):
		self.tracewidth = sender.Text
		#error trapping, make sure values entered are valid
		if self.tracewidth == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.tracewidth == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.tracewidth)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.tracewidth)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.tracewidth)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
		
	def TraceSpaceTextBoxTextChanged(self, sender, e):
		self.tracespacing = sender.Text
		#error trapping, make sure values entered are valid
		if self.tracespacing == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.tracespacing == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.tracespacing)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.tracespacing)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.tracespacing)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
	
	def BottomDielectricTextBoxTextChanged(self, sender, e):
		self.bottomdielectricthickness = sender.Text
		#error trapping, make sure values entered are valid
		if self.bottomdielectricthickness == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.bottomdielectricthickness == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.bottomdielectricthickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.bottomdielectricthickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.bottomdielectricthickness)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
		
	
	def TopDielectricTextBoxTextChanged(self, sender, e):
		self.topdielectricthickness = sender.Text
		#error trapping, make sure values entered are valid
		if self.topdielectricthickness == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.topdielectricthickness == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.topdielectricthickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.topdielectricthickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.topdielectricthickness)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
	

	def DifferentialSpacingTextBoxTextChanged(self, sender, e):
		self.diffspacing = sender.Text
		#error trapping, make sure values entered are valid
		if self.diffspacing == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.diffspacing == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.diffspacing)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.diffspacing)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.diffspacing)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
	
	def SolderMaskThicknessTextBoxTextChanged(self, sender, e):
		self.soldermaskthickness = sender.Text
		#error trapping, make sure values entered are valid
		if self.soldermaskthickness == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.soldermaskthickness == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.soldermaskthickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.soldermaskthickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.soldermaskthickness)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
	
	def D5textboxTextChanged(self, sender, e):
		self.D5thickness = sender.Text
		#error trapping, make sure values entered are valid
		if self.D5thickness == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.D5thickness == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.D5thickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.D5thickness)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.D5thickness)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass	
	

	def D4textBoxTextChanged(self, sender, e):
		self.D4dielfreq = sender.Text
		#error trapping, make sure values entered are valid
		if self.D5thickness == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.D5thickness == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.D4dielfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.D4dielfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.D4dielfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def D4comboBoxSelectedIndexChanged(self, sender, e):
		self.D4dielfrequnits = sender.Text
		pass

	def D4ErtextBoxTextChanged(self, sender, e):
		self.D4dielEr = sender.Text
		#error trapping, make sure values entered are valid
		if self.D4dielEr == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.D4dielEr == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.D4dielEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.D4dielEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.D4dielEr)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def D4TandtextBoxTextChanged(self, sender, e):
		self.D4dielTand = sender.Text
		#error trapping, make sure values entered are valid
		if self.D4dielTand == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.D4dielTand == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.D4dielTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.D4dielTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.D4dielTand)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass


	def D5dieltextBoxTextChanged(self, sender, e):
		self.D5dielfreq = sender.Text
		#error trapping, make sure values entered are valid
		if self.D5dielfreq == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.D5dielfreq == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.D5dielfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.D5dielfreq)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.D5dielfreq)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def D5comboBoxSelectedIndexChanged(self, sender, e):
		self.D5dielfrequnits = sender.Text
		pass

	def D5ErtextBoxTextChanged(self, sender, e):
		self.D5dielEr = sender.Text
		#error trapping, make sure values entered are valid
		if self.D5dielEr == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.D5dielEr == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.D5dielEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.D5dielEr)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.D5dielEr)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass

	def D5TandtextBoxTextChanged(self, sender, e):
		self.D5dielTand = sender.Text
		#error trapping, make sure values entered are valid
		if self.D5dielTand == str():
			self._errorProvider1.SetError(sender,"Error: Text Box is Empty")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if self.D5dielTand == str(0):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot be Zero")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('-', str(self.D5dielTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Be a Negative Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		if re.search('[+*/\,;!@#$%^&*()?<>:"{}_`~ ]', str(self.D5dielTand)):
			self._errorProvider1.SetError(sender,"Error: Text Box Cannot Contain Special Characters or Empty Spaces")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return
		try:
			solutionfreqinput = [float(self.D5dielTand)]
		except ValueError:
			self._errorProvider1.SetError(sender,"Error: Enter a Valid Number")
			self._SimulateButton.Enabled = False
			self._CalculateButton.Enabled = False
			return

		self._errorProvider1.SetError(sender,"")
		self._SimulateButton.Enabled = True
		self._CalculateButton.Enabled = True
		pass
	
	

##########################
# End or Event Handling  #---------------------------------------------------------------------------------------------------------------------------------------------------
##########################	
	





	
	######################################################################
	# define over or under etching #
####################################
	
	def NoetchradioButtonCheckedChanged(self, sender, e):
		self._etchpictureBox.Image = Image.FromFile(self.m_libPath+"Images/etch1.png")
		self._etchfacterlabel.Visible = False	
		self._toppercentetchlabel.Visible = False	
		self._trackBar1.Visible = False		
		self.etching = 'none'
		pass
	
	def OveretchradioButtonCheckedChanged(self, sender, e):
		self._etchpictureBox.Visible = True
		self._etchfacterlabel.Visible = True
		self._toppercentetchlabel.Visible = True	
		self._trackBar1.Visible = True
		self._etchpictureBox.Image = Image.FromFile(self.m_libPath+"Images/etch" + str(self.etchvalue) + ".png")
		self.etching = 'overetch'
		pass

	def UnderetchradioButtonCheckedChanged(self, sender, e):
		self._etchpictureBox.Visible = True	
		self._etchpictureBox.Visible = True
		self._etchfacterlabel.Visible = True
		self._toppercentetchlabel.Visible = True	
		self._trackBar1.Visible = True
		self._etchpictureBox.Image = Image.FromFile(self.m_libPath+"Images/bottometch (" + str(self.etchvalue) + ")" +".png")
		self.etching = 'underetch'
		pass
	
	##################################################################################################  
	#scroll bar for etching graphic and setting factor.               #
	#Equation in designer doesn't match.. layer thickness doesn't     #
	#seem to factor in Designer SI check into this later              #
#######################################################################	
	def TrackBar1Scroll(self, sender, e):	
		etchvalue = sender.Value
		self.etchvalue = etchvalue	
		etchpercent = float(0.0)
		etchfactor = 'none'
		topwidth = float(self.tracewidth)  	
		szPath = self.m_libPath                             
		
		if self.etching == 'overetch':
			self._etchpictureBox.Visible = True
			self._etchpictureBox.Image = Image.FromFile(self.m_libPath+"Images/etch" + str(etchvalue) + ".png")
			etchpercent = abs(100.0*(1.0-(float(etchvalue)-1.0)/50.0)-99.9)
			self.etchpercent = etchpercent


		if self.etching == 'underetch':
			self._etchpictureBox.Visible = True
			self._etchpictureBox.Image = Image.FromFile(self.m_libPath+"Images/bottometch (" + str(etchvalue) + ")" +".png")
			etchpercent = abs(100.0*(1.0-(float(etchvalue)-1.0)/50.0)-99.9)
			self.etchpercent = etchpercent			

				
		if self.etching == 'none':
			self._etchpictureBox.Visible = False
			self._etchpictureBox.Image = Image.FromFile(self.m_libPath+"Images/etch" + str(1) + ".png")					
			self.etchpercent = etchpercent	
			


		if self.etchpercent == 0:
			etchfactor = 'Infinite'
	
		if self.etchpercent != 0:
			etchfactor = round((float(self.tracethickness))/float(0.5*float(self.tracewidth)*(0.01*etchpercent)),2)


		self._etchfacterlabel.Text = "Etch Factor: " + str(etchfactor)
		self._toppercentetchlabel.Text = "Etching %, short to long: " + str(etchpercent)		
	
		pass



## note SL is for symetric SL and MS does not include Soldermask or embedded trace.  These are temporary simple calcs basically Zo ~ sqrt(l/c)
##################################################
#  Calculate transmission line characteristics   #
##################################################
	def CalculatebButtonClick(self, sender, e):
			

		if self.BdielEr == int():
			MessageBox.Show("Error:  Trace Thickness Text Box is Empty")
			return
		
		if self.BdielEr == 0:
			MessageBox.Show("Error:  Trace Thickness Text Box Cannot Equal Zero")
			return	

		if self.tracethickness == int():
			MessageBox.Show("Error:  Trace Thickness Text Box is Empty")
			return
		if self.tracethickness == 0:
			MessageBox.Show("Error:  Trace Thickness Text Box Cannot Equal Zero")
			return						
			
		if self.tracewidth == int():
			MessageBox.Show("Error:  Trace Width Text Box is Empty")
			return
		if self.tracewidth == 0:
			MessageBox.Show("Error:  Trace Width Text Box Cannot Equal Zero")
			return

		if self.differential == 1:
			if self.tracespacing == int():
				MessageBox.Show("Error:  Trace Spacing Text Box is Empty")
				return
			if self.tracespacing == 0:
				MessageBox.Show("Error:  Trace Spacing Text Box Cannot Equal Zero")
				return
			
		if self.broadside ==1:
			if self.D5thickness == int():
				MessageBox.Show("Error:  Trace Spacing Text Box is Empty")
				return
			if self.D5thickness == 0:
				MessageBox.Show("Error:  Trace Spacing Text Box Cannot Equal Zero")
				return			

		if self.bottomdielectricthickness == int():
			MessageBox.Show("Error:  Bottom Dielectric Thickness Text Box is Empty")
			return
		if self.bottomdielectricthickness == 0:
			MessageBox.Show("Error: Bottom Dielectric Thickness Spacing Text Box Cannot Equal Zero")
			return

		if self.microstrip == 0 and self.topdielectricthickness == int():
			MessageBox.Show("Error:  Top Dielectric Thickness Text Box is Empty")
			return
		if self.microstrip ==0 and self.topdielectricthickness == 0:
			MessageBox.Show("Error: Top Dielectric Thickness Spacing Text Box Cannot Equal Zero")
			return

		#######################################################################################
		#NOTE ! on Er calculatins used average the dielectrics including soldermask for diff  #
		#  ! this is not the same as effective Er                                             #
		#######################################################################################
		if self.microstrip == 0:
			Er = (float(self.BdielEr) + float(self.TdielEr))/2
			
		if self.microstrip == 1 and self.differential == 1:	
			Er = (float(self.BdielEr) + float(self.SMEr))/2
					
		if self.microstrip == 1 and self.differential == 0:	
			Er = (float(self.BdielEr))					
					
		if self.broadside == 1:
			Er = (float(self.BdielEr) + float(self.TdielEr) + float(self.SMEr) + float(self.D4dielEr) + float(self.D5dielEr))/5
		

	
		
		H = float(self.topdielectricthickness) - float(self.tracethickness)
		T = float(self.tracethickness)
		W = float(self.tracewidth)
		B = float(self.bottomdielectricthickness) + float(self.topdielectricthickness)
		H1 = float(self.bottomdielectricthickness)
		S = float(self.tracespacing)

		# Microstrip Equation for Single and Diff lines
		if self.microstrip == 1:

			if self.differential == 0:
				ZoMS = (87/math.sqrt(Er+1.41))*math.log((5.98*H1)/(0.8*W+T))
				self._Zotextbox.Text = str("%.2f" % ZoMS)
			
			if self.differential == 1:
				ZoMS = (87/math.sqrt(Er+1.41))*math.log((5.98*H1)/(0.8*W+T))
				ZoMSdiff = 2*ZoMS*(1-.48*(math.exp(-.96*(S/H1))))
				self._Zotextbox.Text = str("%.2f" % ZoMS)
				self._ZotextboxDiff.Text = str("%.2f" % ZoMSdiff)
			
			
		# Stripline Equation for Single and Diff lines	
		if self.microstrip == 0:
			
			if self.differential == 0:
				if H == H1:
					ZoSL = (60/math.sqrt(Er))*math.log((1.9*B)/(0.8*W+T))
					self._Zotextbox.Text = str("%.2f" % ZoSL)
	
	
	
				else:
					ZoSL = (80/math.sqrt(Er))*math.log((1.9*(2*H+T))/(0.8*W+T))*(1-(H/(4*H1)))	
					if ZoSL < 0:
						MessageBox.Show("Error: Dimension ratio of top and bottom dielectric are outside of the bounds of the Zo equation capabilities")
						return
					self._Zotextbox.Text = str("%.2f" % ZoSL)
			
			
			
			if self.differential == 1:
				if H == H1:
					ZoSL = (60/math.sqrt(Er))*math.log((1.9*B)/(0.8*W+T))
					self._Zotextbox.Text = str("%.2f" % ZoSL)					
					ZoSLdiff = 2*ZoSL*(1-.347*(math.exp(-2.9*(S/B))))				
					self._ZotextboxDiff.Text = str("%.2f" % ZoSLdiff)					
	
				else:
					ZoSL = (80/math.sqrt(Er))*math.log((1.9*(2*H+T))/(0.8*W+T))*(1-(H/(4*H1)))		
					if ZoSL < 0:
						MessageBox.Show("Error: Dimension ratio of top and bottom dielectric are outside of the bounds of the Zo equation capabilities")
						return
					self._Zotextbox.Text = str("%.2f" % ZoSL)								
					ZoSLdiff = 2*ZoSL*(1-.347*(math.exp(-2.9*(S/B))))				
					self._ZotextboxDiff.Text = str("%.2f" % ZoSLdiff)
				
				

		if self.broadside == 1:
				
			h1 = (float(self.topdielectricthickness)+float(self.bottomdielectricthickness)-float(self.tracethickness))
			h2 = (float(self.soldermaskthickness)+float(self.D5thickness)-float(self.tracethickness))
			h = (h1 + h2)/2
				
			ZoSL =(82.2/math.sqrt(Er))*math.log((5.98*(float(self._TraceSpaceTextBox.Text)))/(0.8*W+T))*(1-math.exp(-0.6*h))
			self._Zotextbox.Text = str("%.2f" % ZoSL)
				
		if 	self.GCPW == 1:
				
			a = float(self.tracewidth)									#Trace Width
			b = float(self.tracewidth) + 2*float(self.tracespacing)		#Trace Width + 2*TraceSpace
			h = float(self.bottomdielectricthickness)					#bottom dielectric Thickness
			Er = float(self.BdielEr)
				
			k1=float(a/b)			
			k2 = float(math.sqrt(1-math.pow(k1,2)))			
			k3 = float(math.sqrt(1-math.pow(k2,2)))
			k4 = float(math.tanh((math.pi*a)/(4.0*h))/math.tanh((math.pi*b)/(4.0*h)))

			# for Kk1 - Kk4 the for loops below are approximations to the solutons of Complete elliptic integral of the first kind K(k)
			# expressed as a power series taken to 25 iterations or n = 0 to 25
			Kk1 = float(0)
			for n in xrange(0, 25):
				Kk1 = Kk1 + (math.pi/2)*math.pow(((math.factorial(2*n))/(math.pow(2,2*n)*math.pow(math.factorial(n),2))),2)*math.pow(k1,2*n)

			Kk2 = float(0)
			for n in xrange(0, 25):
				Kk2 = Kk2 + (math.pi/2)*math.pow(((math.factorial(2*n))/(math.pow(2,2*n)*math.pow(math.factorial(n),2))),2)*math.pow(k2,2*n)
						
			Kk3 = float(0)
			for n in xrange(0, 25):
				Kk3 = Kk3 + (math.pi/2)*math.pow(((math.factorial(2*n))/(math.pow(2,2*n)*math.pow(math.factorial(n),2))),2)*math.pow(k3,2*n)					
					
			Kk4 = float(0)
			for n in xrange(0, 25):
				Kk4 = Kk4 + (math.pi/2)*math.pow(((math.factorial(2*n))/(math.pow(2,2*n)*math.pow(math.factorial(n),2))),2)*math.pow(k4,2*n)
				
			#effective Dielectric Constant
			Eeff = float((1.0+Er*((Kk2)/(Kk1))*((Kk4)/(Kk3)))/(1.0+((Kk2)/(Kk1))*((Kk4)/(Kk3))))		
				
			ZoGCPW = ((120*math.pi)/(2.0*math.sqrt(Eeff)))*(1.0/((Kk1)/(Kk2)+(Kk4)/(Kk3)))
			
			self._Zotextbox.Text = str("%.2f" % ZoGCPW)
			self._ZotextboxDiff.Text = str("%.2f" % Eeff)			
		pass


	

		
#########################################################
# When sumulate button in clicked launch Q2D and create #
# project/Design                                        #
#########################################################
	def SimulateButtonClick(self, sender, e):
		

		microstrip = int(self.microstrip)
		differential = int(self.differential)
		broadside = int(self.broadside)
		GCPW = int(self.GCPW)
		units = self.units
		designtype = ''




		if microstrip == 1 and differential ==1 and broadside ==0:
			designtype = 'Microstrip_Differential'
			
		if microstrip == 1 and differential ==0 and broadside ==0:
			designtype = 'Microstrip_SingleEnded'
			
		if microstrip == 0 and differential ==0 and broadside ==0:
			designtype = 'Stripline_SingleEnded'
			
		if microstrip == 0 and differential ==1 and broadside ==0:
			designtype = 'Stripline_Differential'	
			
		if broadside ==1:
			designtype = 'Broadside_Coupled_Stripline'
			
		if GCPW ==1:
			designtype = 'Grounded_CPW'
		
		tracespacing = self.tracespacing	
		tracewidth = self.tracewidth
		gndwidth = self._D5textbox.Text
		toptracewidth = self.toptracewidth
		bottomtracewidth = self.bottomtracewidth
		maxtracewidth = self.tracewidth
		numberoftraces = self.numberoftraces
		diffspacing = self.diffspacing
		planethickness = self.planethickness
		tracethickness = self.tracethickness		
		topdielectricthickness = self.topdielectricthickness
		bottomdielectricthickness = self.bottomdielectricthickness


		etching = self.etching
		roughnesstype = int(self.roughnesstype)
		surfaceroughnesstop = self.surfaceroughnesstop
		surfaceroughnesssides = self.surfaceroughnessSides
		surfaceroughnessbottom = self.surfaceroughnessbottom
		surfaceroughnessunits = self.surfaceroughnessunits
		HHsurfaceratiotop = self.HHsurfaceratiotop
		noduleradiustop = self.noduleradiustop
		HHsurfaceratiosides = self.HHsurfaceratiosides
		noduleradiussides = self.noduleradiussides
		HHsurfaceratiobottom = self.HHsurfaceratiobottom
		noduleradiusbottom = self.noduleradiusbottom
		plating = self.plating
		useplatingmaterial = self.useplatingmaterial
		platingmaterial = self.platingmaterial
		platingthickness = float(self.platingthickness)
		platingthicknessunits = self.platingthicknessunits
		soldermaskmaterial = self.soldermaskmaterial
		soldermaskthickness = self.soldermaskthickness
		soldermaskunits = self.soldermaskunits

		D5thickness = self.D5thickness 

		solutionfreq = self.solutionfreq
		solutionstartfreq = self.solutionstartfreq
		solutionstopfreq = self.solutionstopfreq
		solutionstepfreq = self.solutionstepfreq
		Solutionfrequnits = self.Solutionfrequnits
		StartFrequnits = self.StartFrequnits
		StopFrequnits = self.StopFrequnits
		FreqStepunits = self.FreqStepunits
		freqsweeptype = self.freqsweeptype	



		#############################
		#  Frequency Units Scaling  #
		#############################
		if freqsweeptype == 'Discrete' or 'Interpolating':  
			startf = float(solutionstartfreq)
			stepf = float(solutionstepfreq)
			stopf = float(solutionstopfreq)
			
			if StartFrequnits == 'GHz':
				startf = startf*1e9
				
			if StartFrequnits == 'MHz':
				startf = startf*1e6			
	
			if StartFrequnits == 'KHz':
				startf = startf*1e3	
					
			if FreqStepunits == 'GHz':
				stepf = stepf*1e9
				
			if FreqStepunits == 'MHz':
				stepf = stepf*1e6			
	
			if FreqStepunits == 'KHz':
				stepf = stepf*1e3				
		
			if StopFrequnits == 'GHz':
				stopf = stopf*1e9
				
			if StopFrequnits == 'MHz':
				stopf = stopf*1e6			
	
			if StopFrequnits == 'KHz':
				stopf = stopf*1e3	

			numberofsteps = (stopf-startf)/stepf

			if numberofsteps >= 10000-1:
				MessageBox.Show("Error:  The discrete sweep step size is too small.  A discrete sweep may not have 10,000 points or more.  Select a larger step size or narrow the sweep range.")
				return
			


		SMdielectricfreq = float(self.SMdielectricfreq)
		SMdielectricfrequnits = self.SMdielectricfrequnits
		SMEr = self.SMEr
		SMTand = self.SMTand
		
		
		if SMdielectricfrequnits == 'GHz':
			SMdielectricfreq = SMdielectricfreq*1e9
			
		if SMdielectricfrequnits == 'MHz':
			SMdielectricfreq = SMdielectricfreq*1e6			

		if SMdielectricfrequnits == 'KHz':
			SMdielectricfreq = SMdielectricfreq*1e3
			
		
	
		Bdielfreq = float(self.Bdielfreq)
		Bdielectricfrequnits = self.Bdielectricfrequnits
		BdielEr = self.BdielEr
		BdielTand = self.BdielTand

		if Bdielectricfrequnits == 'GHz':
			Bdielfreq = Bdielfreq*1e9
			
		if Bdielectricfrequnits == 'MHz':
			Bdielfreq = Bdielfreq*1e6			

		if Bdielectricfrequnits == 'KHz':
			Bdielfreq = Bdielfreq*1e3

		logger = logging.getLogger('TLine.MainForm.DesignSelect')
		logger.info('Bdielfreq:'+str(Bdielfreq))
		logger.info('BdielEr:'+str(BdielEr))
		logger.info('BdielTand:'+str(BdielTand))
		logger.info('Bdielfrequnits:'+Bdielectricfrequnits)


				
		Tdielfreq = float(self.Tdielfreq)
		Tdielfrequnits = self.Tdielfrequnits
		TdielEr = self.TdielEr
		TdielTand = self.TdielTand

		if Tdielfrequnits == 'GHz':
			Tdielfreq = Tdielfreq*1e9
			
		if Tdielfrequnits == 'MHz':
			Tdielfreq = Tdielfreq*1e6			

		if Tdielfrequnits == 'KHz':
			Tdielfreq = Tdielfreq*1e3


		logger.info('Tdielfreq:'+str(Tdielfreq))
		logger.info('TdielEr:'+str(TdielEr))
		logger.info('TdielTand:'+str(TdielTand))
		logger.info('Tdielfrequnits:'+Tdielfrequnits)


		D4dielfreq = float(self.D4dielfreq)
		D4dielfrequnits = self.D4dielfrequnits
		D4dielEr = self.D4dielEr 
		D4dielTand = self.D4dielTand 
		
		if D4dielfrequnits == 'GHz':
			D4dielfreq = D4dielfreq*1e9
			
		if D4dielfrequnits == 'MHz':
			D4dielfreq = D4dielfreq*1e6			

		if D4dielfrequnits == 'KHz':
			D4dielfreq = D4dielfreq*1e3
		
			
		D5dielfreq = float(self.D5dielfreq)
		D5dielfrequnits = self.D5dielfrequnits
		D5dielEr = self.D5dielEr 
		D5dielTand = self.D5dielTand 		
		
		if D5dielfrequnits == 'GHz':
			D5dielfreq = D5dielfreq*1e9
			
		if D5dielfrequnits == 'MHz':
			D5dielfreq = D5dielfreq*1e6			

		if D5dielfrequnits == 'KHz':
			D5dielfreq = D5dielfreq*1e3


		self.simulate ==1



		#create date/time string that can be used to create unique file names.  NOTE time is set in UTC, "Coordinated Universal Time"  same as GMT
		utc_datetime = datetime.datetime.utcnow()
		formated_Datetime_string = utc_datetime.strftime("%B%d%H%M%S")

		self.oDesktop.RestoreWindow()
		oProject = self.oDesktop.GetActiveProject()
		oProject.InsertDesign("2D Extractor", designtype+"_"+"Created"+"_"+formated_Datetime_string+"_"+"UTC", "", "")
		oDesign = oProject.GetActiveDesign()
			
		oEditor = oDesign.SetActiveEditor("3D Modeler")
		
		self.designcounter +=1


		#disable auto save and close all windows to speed up drawing when create is selected.  
		fAutoSave = self.oDesktop.GetAutoSaveEnabled()
		if fAutoSave == 1:
			self.oDesktop.EnableAutoSave(False)

		self.oDesktop.CloseAllWindows()



		if etching == 'overetch':									
			toptracewidth = float(tracewidth)*(1.0-float(self.etchpercent)*0.01)
			bottomtracewidth = tracewidth

		if etching == 'underetch':
			toptracewidth = tracewidth
			bottomtracewidth = float(tracewidth)*(1.0-float(self.etchpercent)*0.01)	
							
		if etching == 'none':
			toptracewidth = tracewidth
			bottomtracewidth = tracewidth
			
		numberoftraces = int(self.numberoftraces)
			

		if 	self.SLMS == 1:
			DrawTransmissionLine(oProject,oEditor,oDesign,microstrip,differential,units,tracespacing,toptracewidth,
				bottomtracewidth,maxtracewidth,numberoftraces,diffspacing,planethickness,topdielectricthickness,bottomdielectricthickness,
				tracethickness,tracewidth,etching,roughnesstype,surfaceroughnesstop,surfaceroughnesssides,surfaceroughnessbottom,
				surfaceroughnessunits,HHsurfaceratiotop,noduleradiustop,HHsurfaceratiosides,noduleradiussides,HHsurfaceratiobottom,
				noduleradiusbottom,plating,useplatingmaterial,platingmaterial,platingthickness,platingthicknessunits,soldermaskmaterial,
				soldermaskthickness,soldermaskunits,solutionfreq,solutionstartfreq,solutionstopfreq,solutionstepfreq,Solutionfrequnits,
				StartFrequnits,StopFrequnits,FreqStepunits,freqsweeptype,SMdielectricfreq,SMdielectricfrequnits,SMEr,SMTand,Bdielfreq,Bdielectricfrequnits,
				BdielEr,BdielTand,Tdielfreq,Tdielfrequnits,TdielEr,TdielTand,formated_Datetime_string,fAutoSave)
			
			
		if self.broadside == 1: 
			DrawBroadSideCoupledStripline(oProject,oEditor,oDesign,units,tracespacing,toptracewidth,
				bottomtracewidth,maxtracewidth,numberoftraces,diffspacing,planethickness,topdielectricthickness,D5thickness,bottomdielectricthickness,
				tracethickness,tracewidth,etching,roughnesstype,surfaceroughnesstop,surfaceroughnesssides,surfaceroughnessbottom,
				surfaceroughnessunits,HHsurfaceratiotop,noduleradiustop,HHsurfaceratiosides,noduleradiussides,HHsurfaceratiobottom,
				noduleradiusbottom,plating,useplatingmaterial,platingmaterial,platingthickness,platingthicknessunits,soldermaskmaterial,
				soldermaskthickness,soldermaskunits,solutionfreq,solutionstartfreq,solutionstopfreq,solutionstepfreq,Solutionfrequnits,StartFrequnits,
				StopFrequnits,FreqStepunits,freqsweeptype,SMdielectricfreq,SMdielectricfrequnits,SMEr,SMTand,Bdielfreq,Bdielectricfrequnits,
				BdielEr,BdielTand,Tdielfreq,Tdielfrequnits,TdielEr,TdielTand,D4dielfreq,D4dielfrequnits,D4dielEr,D4dielTand,D5dielfreq,D5dielfrequnits,
				D5dielEr,D5dielTand,formated_Datetime_string)

		if self.GCPW == 1:
			DrawGCPW(oProject,oEditor,oDesign,units,tracespacing,toptracewidth,
				bottomtracewidth,maxtracewidth,numberoftraces,diffspacing,planethickness,topdielectricthickness,D5thickness,bottomdielectricthickness,
				tracethickness,tracewidth,etching,roughnesstype,surfaceroughnesstop,surfaceroughnesssides,surfaceroughnessbottom,
				surfaceroughnessunits,HHsurfaceratiotop,noduleradiustop,HHsurfaceratiosides,noduleradiussides,HHsurfaceratiobottom,
				noduleradiusbottom,plating,useplatingmaterial,platingmaterial,platingthickness,platingthicknessunits,soldermaskmaterial,
				soldermaskthickness,soldermaskunits,solutionfreq,solutionstartfreq,solutionstopfreq,solutionstepfreq,Solutionfrequnits,StartFrequnits,
				StopFrequnits,FreqStepunits,freqsweeptype,SMdielectricfreq,SMdielectricfrequnits,SMEr,SMTand,Bdielfreq,Bdielectricfrequnits,
				BdielEr,BdielTand,Tdielfreq,Tdielfrequnits,TdielEr,TdielTand,D4dielfreq,D4dielfrequnits,D4dielEr,D4dielTand,D5dielfreq,D5dielfrequnits,
				D5dielEr,D5dielTand,formated_Datetime_string,gndwidth)

		#enable autosave if user origionally has it enabled and restore window
		if fAutoSave == 1:
			self.oDesktop.EnableAutoSave(True)

		oEditor.ShowWindow() 

	
	
	
				############################################################
				# DrawTransmissionLine Class draws all the model Geometry  #
#####################################################################################################################################################################################################
class DrawTransmissionLine(object):
	
	def __init__(self,oProject,oEditor,oDesign,microstrip,differential,units,tracespacing,toptracewidth,
			bottomtracewidth,maxtracewidth,numberoftraces,diffspacing,planethickness,topdielectricthickness,bottomdielectricthickness,
			tracethickness,tracewidth,etching,roughnesstype,surfaceroughnesstop,surfaceroughnesssides,surfaceroughnessbottom,
			surfaceroughnessunits,HHsurfaceratiotop,noduleradiustop,HHsurfaceratiosides,noduleradiussides,HHsurfaceratiobottom,
			noduleradiusbottom,plating,useplatingmaterial,platingmaterial,platingthickness,platingthicknessunits,soldermaskmaterial,
			soldermaskthickness,soldermaskunits,solutionfreq,solutionstartfreq,solutionstopfreq,solutionstepfreq,Solutionfrequnits,StartFrequnits,
			StopFrequnits,FreqStepunits,freqsweeptype,SMdielectricfreq,SMdielectricfrequnits,SMEr,SMTand,Bdielfreq,Bdielectricfrequnits,
			BdielEr,BdielTand,Tdielfreq,Tdielfrequnits,TdielEr,TdielTand,formated_Datetime_string,fAutoSave):




		diffshift = 0  #local variable to track when to shift sets of traces to they are diff pairs
		
		
		#Calculate Conductor Thickness even if etched
		a = float(toptracewidth)
		b = float(bottomtracewidth)
		c = float(tracethickness)
		x = 0 #triangle base lenght
		Y = 0 #trace sides length
		
		#triangle base length.
		if a > b:
			x = (a-b)/2
		if a < b:
			x = (b-a)/2
			
		if a == b:
			y = tracethickness

		else:
			y = math.sqrt(c*c + x*x)
				
		trace_perimeter = float(toptracewidth) + float(bottomtracewidth) + 2*float(y)
		Area_trapdzoid = ((float(toptracewidth) + float(bottomtracewidth)) / 2.0) * float(tracethickness)
		conductor_thickness = Area_trapdzoid / trace_perimeter
		


		bottomdielectricmaterial = ''  #variables to assign to top and bottom dielectrics
		topdielectricmaterial = ''
		
		logger = logging.getLogger('TLine.MainForm.DesignSelect')
		
		if microstrip ==1:
			
			if differential ==0:
				logger.info('Microstrip Design Created!')
			
			if differential ==1:
				logger.info('Differential Microstrip Design Created!')
			
		if microstrip ==0:
			
			if differential ==0:
				logger.info('Stripline Design Created!')
			
			if differential ==1:
				logger.info('Differential Stripline Design Created!')

		
		#Sets default Design units
		oEditor = oDesign.SetActiveEditor("3D Modeler")
		oEditor.SetModelUnits(
				[
					"NAME:Units",
					"Units:="		, units,
					"Rescale:="		, False
				])

		####################################################################
		# adding variables to project to that its parameterized            #
		##############################################################################################################################
		if microstrip == 0:
			oDesign.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:LocalVariableTab",
						[
							"NAME:PropServers", 
							"LocalVariables"
						],
						[
							"NAME:NewProps",
							[
								"NAME:topdielectricthickness",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(topdielectricthickness) + units
							],
							[
								"NAME:bottomdielectricthickness",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(bottomdielectricthickness) + units
							]							
						]
					]
				])			
	
		if microstrip == 1:
			oDesign.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:LocalVariableTab",
						[
							"NAME:PropServers", 
							"LocalVariables"
						],
						[
							"NAME:NewProps",
							[
								"NAME:soldermaskthickness",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(soldermaskthickness) + soldermaskunits
							],
							[
								"NAME:bottomdielectricthickness",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(bottomdielectricthickness) + units
							]							
						]
					]
				])	

		
		if differential ==1:
			oDesign.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:LocalVariableTab",
						[
							"NAME:PropServers", 
							"LocalVariables"
						],
						[
							"NAME:NewProps",
							[
								"NAME:diffspacing",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(diffspacing) + units
							]												
						]
					]
				])
		
		
		if roughnesstype ==  1:		
			oDesign.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:LocalVariableTab",
						[
							"NAME:PropServers", 
							"LocalVariables"
						],
						[
							"NAME:NewProps",
							[
								"NAME:platingthickness",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(platingthickness) + platingthicknessunits
							],	
							[
								"NAME:surfaceroughnesstop",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(surfaceroughnesstop) + surfaceroughnessunits
							],
							[
								"NAME:surfaceroughnesssides",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(surfaceroughnesssides) + surfaceroughnessunits
							],		
							[
								"NAME:surfaceroughnessbottom",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(surfaceroughnessbottom) + surfaceroughnessunits
							]						
						]
					]
				])		
		
		
		if roughnesstype ==  2:	
			oDesign.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:LocalVariableTab",
						[
							"NAME:PropServers", 
							"LocalVariables"
						],
						[
							"NAME:NewProps",
							[
								"NAME:platingthickness",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(platingthickness) + platingthicknessunits
							],	
							[
								"NAME:noduleradiustop",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(noduleradiustop) + surfaceroughnessunits
							],	
							[
								"NAME:noduleradiussides",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(noduleradiussides) + surfaceroughnessunits
							],	
							[
								"NAME:noduleradiusbottom",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(noduleradiusbottom) + surfaceroughnessunits
							],	
							[
								"NAME:HHsurfaceratiotop",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(HHsurfaceratiotop)
							],
							[
								"NAME:HHsurfaceratiosides",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(HHsurfaceratiosides)
							],
							[
								"NAME:HHsurfaceratiobottom",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(HHsurfaceratiobottom)
							]						
						]
					]
				])		



		oDesign.ChangeProperty(
			[
				"NAME:AllTabs",
				[
					"NAME:LocalVariableTab",
					[
						"NAME:PropServers", 
						"LocalVariables"
					],
					[
						"NAME:NewProps",
						[
							"NAME:tracespacing",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(tracespacing) + units
						],						
						[
							"NAME:toptracewidth",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(toptracewidth) + units
						],
						[
							"NAME:bottomtracewidth",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(bottomtracewidth) + units
						],	
						[
							"NAME:planethickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(planethickness) + units
						],
						[
							"NAME:tracethickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(tracethickness) + units
						],																						
					]
				]
			])

		#############################################
		# main loop, looping through trace drawing  #
		################################################################################################################################
		tracecount = 1
	
		
		while tracecount <=numberoftraces:



		#########################################################################
		# This if statement test for the first trace then drawns it             #
		#########################################################################

			if tracecount ==1:

				oEditor.CreatePolyline(
				[
					"NAME:Trace",
					"IsPolylineCovered:="	, True,
					"IsPolylineClosed:="	, True,
					[
					"NAME:PolylinePoints",
					[
						"NAME:PLPoint",
						"X:="			, "((4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")-0.5*toptracewidth)",
						"Y:="			, "((planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness)",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "((4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")+0.5*toptracewidth)",
						"Y:="			, "((planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness)",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "((4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")+0.5*bottomtracewidth)",
						"Y:="			, "((planethickness+bottomdielectricthickness+0.5*tracethickness)-0.5*tracethickness)",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "((4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")-0.5*bottomtracewidth)",
						"Y:="			, "((planethickness+bottomdielectricthickness+0.5*tracethickness)-0.5*tracethickness)",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "((4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")-0.5*toptracewidth)",
						"Y:="			, "((planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness)",
						"Z:="			, "0" + units
					]
				],
					[
						"NAME:PolylineSegments",
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 0,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 1,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 2,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 3,
							"NoOfPoints:="		, 2
						]
					],
					[
						"NAME:PolylineXSection",
						"XSectionType:="	, "None",
						"XSectionOrient:="	, "Auto",
						"XSectionWidth:="	, "0mm",
						"XSectionTopWidth:="	, "0mm",
						"XSectionHeight:="	, "0mm",
						"XSectionNumSegments:="	, "0",
						"XSectionBendType:="	, "Corner"
					]
				], 
				[
					"NAME:Attributes",
					"Name:="		, "Trace"+str(tracecount),
					"Flags:="		, "",
					"Color:="		, "(132 132 193)",
					"Transparency:="	, 0,
					"PartCoordinateSystem:=", "Global",
					"UDMId:="		, "",
					"MaterialValue:="	, "\"copper\"",
					"SolveInside:="		, False
				])

				#########################
				# Assign signal sources #
				#########################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleSignalLine(
					[
						"NAME:"+"Trace"+str(tracecount),
						"Objects:="		, ["Trace1"],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])
					
				tracecount +=1
			

		########################################################################################################
		# This if statement offsets the additional non-differential traces if there are more than one to drawn #                                                                                                  
		#####################################################################################################################################
		 
			if tracecount >1 and differential ==0 and numberoftraces !=1:
			

				oEditor.CreatePolyline(
				[
					"NAME:Trace",
					"IsPolylineCovered:="	, True,
					"IsPolylineClosed:="	, True,
					[
					"NAME:PolylinePoints",
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")"+"-0.5*toptracewidth+"+ str(tracecount-1) + "*(tracespacing+bottomtracewidth)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")"+"+0.5*toptracewidth+"+str(tracecount-1)+"*(tracespacing+bottomtracewidth)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")"+"+0.5*bottomtracewidth+"+str(tracecount-1)+"*(tracespacing+bottomtracewidth)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"-0.5*tracethickness",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")"+"-0.5*bottomtracewidth+"+str(tracecount-1)+"*(tracespacing+bottomtracewidth)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"-0.5*tracethickness",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")"+"-0.5*toptracewidth+"+str(tracecount-1)+"*(tracespacing+bottomtracewidth)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
						"Z:="			, "0" + units
					]
				],
					[
						"NAME:PolylineSegments",
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 0,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 1,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 2,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 3,
							"NoOfPoints:="		, 2
						]
					],
					[
						"NAME:PolylineXSection",
						"XSectionType:="	, "None",
						"XSectionOrient:="	, "Auto",
						"XSectionWidth:="	, "0mm",
						"XSectionTopWidth:="	, "0mm",
						"XSectionHeight:="	, "0mm",
						"XSectionNumSegments:="	, "0",
						"XSectionBendType:="	, "Corner"
					]
				], 
				[
					"NAME:Attributes",
					"Name:="		, "Trace"+str(tracecount),
					"Flags:="		, "",
					"Color:="		, "(132 132 193)",
					"Transparency:="	, 0,
					"PartCoordinateSystem:=", "Global",
					"UDMId:="		, "",
					"MaterialValue:="	, "\"copper\"",
					"SolveInside:="		, False
				])

				#########################
				# Assign signal sources #
				#########################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleSignalLine(
					[
						"NAME:"+"Trace"+str(tracecount),
						"Objects:="		, ["Trace"+str(tracecount)],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])

				tracecount +=1
				
			
				
				
				
		#####################################################################################
		# This if statement offsets the additional traces if there are more than one drawn  #
		# and differential spacing if defined, differential ==1                             #
		##########################################################################################################             	

			if tracecount >1 and differential ==1 and numberoftraces !=1:	
			
				
				if math.fmod(tracecount,2) ==1:
					diffshift = diffshift + 1
				if math.fmod(tracecount,2) ==0:
					diffshift = diffshift
					
				
				oEditor.CreatePolyline(
				[
					"NAME:Trace",
					"IsPolylineCovered:="	, True,
					"IsPolylineClosed:="	, True,
					[
					"NAME:PolylinePoints",
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")-0.5*toptracewidth+"+ str(tracecount-1) + "*(tracespacing+bottomtracewidth)+"+ str(diffshift) + "*(diffspacing-tracespacing)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")+0.5*toptracewidth+"+ str(tracecount-1) + "*(tracespacing+bottomtracewidth)+"+ str(diffshift) + "*(diffspacing-tracespacing)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")+0.5*bottomtracewidth+"+ str(tracecount-1) + "*(tracespacing+bottomtracewidth)+"+ str(diffshift) + "*(diffspacing-tracespacing)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)-0.5*tracethickness",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")-0.5*bottomtracewidth+"+ str(tracecount-1) + "*(tracespacing+bottomtracewidth)+"+ str(diffshift) + "*(diffspacing-tracespacing)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)-0.5*tracethickness",
						"Z:="			, "0" + units
					],
					[
						"NAME:PLPoint",
						"X:="			, "(4.0*"+str(maxtracewidth)+units+"+0.5*"+str(maxtracewidth)+units+")-0.5*toptracewidth+"+ str(tracecount-1) + "*(tracespacing+bottomtracewidth)+"+ str(diffshift) + "*(diffspacing-tracespacing)",
						"Y:="			, "(planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness",
						"Z:="			, "0" + units
					]
				],
					[
						"NAME:PolylineSegments",
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 0,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 1,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 2,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 3,
							"NoOfPoints:="		, 2
						]
					],
					[
						"NAME:PolylineXSection",
						"XSectionType:="	, "None",
						"XSectionOrient:="	, "Auto",
						"XSectionWidth:="	, "0mm",
						"XSectionTopWidth:="	, "0mm",
						"XSectionHeight:="	, "0mm",
						"XSectionNumSegments:="	, "0",
						"XSectionBendType:="	, "Corner"
					]
				], 
				[
					"NAME:Attributes",
					"Name:="		, "Trace"+str(tracecount),
					"Flags:="		, "",
					"Color:="		, "(132 132 193)",
					"Transparency:="	, 0,
					"PartCoordinateSystem:=", "Global",
					"UDMId:="		, "",
					"MaterialValue:="	, "\"copper\"",
					"SolveInside:="		, False
				])
			
				#########################
				# Assign signal sources #
				#########################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleSignalLine(
					[
						"NAME:"+"Trace"+str(tracecount),
						"Objects:="		, ["Trace"+str(tracecount)],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])
			
				tracecount +=1	
			
			
		tracecount = 1   #setting tracecount back to one.	
			

		###########################################################################################		
		#  Adding surface roughness to traces and plating for top and sides of traces if selected#	
		###################################################################################################################################################################

		#loop to assign finite conductivity to traces:  Hammerstadt-Jensen
		if roughnesstype ==1:
			counter = 0    #lines for assigning roughness shift by 12 for each trace do top of trace 1 = 7, top trace 2 = 19 

			while tracecount<=numberoftraces:
				#top Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessTopTrace"+str(tracecount),
						"Edges:="		, [7+counter],
						"UseCoating:="		, plating,
						"LayerThickness:="	, "platingthickness",
						"UseMaterial:="		, useplatingmaterial,
						"Material:="		, "copper",				
						"Roughness:="		, "surfaceroughnesstop"
					])

				#sides Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessSidesTrace"+str(tracecount),
						"Edges:="		, [8+counter,10+counter],
						"UseCoating:="		, plating,
						"LayerThickness:="	, "platingthickness",
						"UseMaterial:="		, useplatingmaterial,
						"Material:="		, platingmaterial,				
						"Roughness:="		, "surfaceroughnesssides"
					])
				
				#bottom Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessBottomTrace"+str(tracecount),
						"Edges:="		    , [9+counter],
						"UseCoating:="		, False,			
						"Roughness:="		, "surfaceroughnessbottom"
					])

				counter +=12
				tracecount +=1
				
		counter = 0       	#reset counter	
		tracecount = 1		#reset tracecount
				
		#loop to assign finite conductivity to traces:  Huray
		if roughnesstype ==2:
			counter = 0    #lines for assigning roughness shift by 12 for each trace do top of trace 1 = 7, top trace 2 = 19 
			
			while tracecount<=numberoftraces:
				#top Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessTopTrace"+str(tracecount),
						"Edges:="		, [7+counter],
						"UseCoating:="		, plating,
						"LayerThickness:="	, "platingthickness",
						"UseMaterial:="		, useplatingmaterial,
						"Material:="		, platingmaterial,				
						"Radius:="		, "noduleradiustop",
						"Ratio:="		, "HHsurfaceratiotop"
					])

				#sides Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessSidesTrace"+str(tracecount),
						"Edges:="		, [8+counter,10+counter],
						"UseCoating:="		, plating,
						"LayerThickness:="	, "platingthickness",
						"UseMaterial:="		, useplatingmaterial,
						"Material:="		, platingmaterial,				
						"Radius:="		, "noduleradiussides",
						"Ratio:="		, "HHsurfaceratiosides"

					])
				
				#bottom Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessBottomTrace"+str(tracecount),
						"Edges:="		, [9+counter],
						"UseCoating:="		, False,
						"Radius:="		, "noduleradiusbottom",
						"Ratio:="		, "HHsurfaceratiobottom"

					])

				counter += 12
				tracecount +=1
				
		counter = 0       	#reset counter	
		tracecount = 1		#reset tracecount		



		##########################################################################################################		
		#creating Djorjdevic-Sarkar fitted soldermask material and bottom dielectric material if microstrip = 1  #
		#########################################################################################################################################	

		if microstrip == 1:	


			#Constants
			pi = math.pi
			Freq_B = 1e12/(2*pi)
			cond_DC = 1e-12
			Eo = 8.854e-12

			###------------------Soldermask Fit----------------####	

			#inputs from user
			solnfreq = float(SMdielectricfreq)
			solnEr = float(SMEr)
			solnTand = float(SMTand)
			
			#Djorjdevic-Sarkar Equations
			K = ((solnEr*solnTand)-(cond_DC/(2*pi*Eo*solnfreq)))/((pi/2)-math.atan(solnfreq/Freq_B))		
			E_inf = solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(solnfreq*solnfreq)))/solnfreq)		
			delta_E = 10*solnTand*E_inf
			Freq_A = Freq_B/math.exp(delta_E/K)
			


			oDefinitionManager = oProject.GetDefinitionManager()
			oDefinitionManager.AddMaterial(
				[


					"NAME:Soldermask"+"_"+formated_Datetime_string,
#					"NAME:Soldermask",
					"CoordinateSystemType:=", "Cartesian",
					[
						"NAME:AttachedData"
					],
					[
						"NAME:ModifierData"
					],
					"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
					"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
					"dielectric_loss_tangent:=", "0",
					"magnetic_loss_tangent:=", "0"
				])
				
			##-------------Bottom Dielectric Fit--------------------###


			#inputs from user
			solnfreq = float(Bdielfreq)
			solnEr = float(BdielEr)
			solnTand = float(BdielTand)
			
			#Djorjdevic-Sarkar Equations
			K = ((solnEr*solnTand)-(cond_DC/(2*pi*Eo*solnfreq)))/((pi/2)-math.atan(solnfreq/Freq_B))		
			E_inf = solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(solnfreq*solnfreq)))/solnfreq)		
			delta_E = 10*solnTand*E_inf
			Freq_A = Freq_B/math.exp(delta_E/K)
			
			

			oDefinitionManager.AddMaterial(
				[
					"NAME:BottomDielectric"+"_"+formated_Datetime_string,
					"CoordinateSystemType:=", "Cartesian",
					[
						"NAME:AttachedData"
					],
					[
						"NAME:ModifierData"
					],
					"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
					"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
					"dielectric_loss_tangent:=", "0",
					"magnetic_loss_tangent:=", "0"
				])


			bottomdielectricmaterial = "\"BottomDielectric"+"_"+formated_Datetime_string+"\""
			soldermaskmaterial = "\"Soldermask"+"_"+formated_Datetime_string+"\""




		###########################################################################################################		
		#creating Djorjdevic-Sarkar fitted bottom and top dielectric material if microstrip = 0 thus is stripline #
		#########################################################################################################################################	

		if microstrip == 0:	

			#Constants
			pi = math.pi
			Freq_B = 1e12/(2*pi)
			cond_DC = 1e-12
			Eo = 8.854e-12

			###------------------Top Dielectric Fit----------------####	


			#inputs from user
			solnfreq = float(Tdielfreq)
			solnEr = float(TdielEr)
			solnTand = float(TdielTand)
#			logger = logging.getLogger('TLine.MainForm.DesignSelect')
#			logger.info('Tdielfreq:'+str(solnfreq))
#			logger.info('TdielEr:'+str(solnEr))
#			logger.info('TdielTand:'+str(solnTand))

			#Djorjdevic-Sarkar Equations
			K = ((solnEr*solnTand)-(cond_DC/(2*pi*Eo*solnfreq)))/((pi/2)-math.atan(solnfreq/Freq_B))		
			E_inf = solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(solnfreq*solnfreq)))/solnfreq)		
			delta_E = 10*solnTand*E_inf
			Freq_A = Freq_B/math.exp(delta_E/K)
			
			oDefinitionManager = oProject.GetDefinitionManager()			
			oDefinitionManager.AddMaterial(
				[
					"NAME:TopDielectric"+"_"+formated_Datetime_string,
					"CoordinateSystemType:=", "Cartesian",
					[
						"NAME:AttachedData"
					],
					[
						"NAME:ModifierData"
					],
					"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
					"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
					"dielectric_loss_tangent:=", "0",
					"magnetic_loss_tangent:=", "0"
				])
				
			##-------------Bottom Dielectric Fit--------------------###


			#inputs from user
			solnfreq = float(Bdielfreq)
			solnEr = float(BdielEr)
			solnTand = float(BdielTand)

#			logger.info('Bdielfreq:'+str(solnfreq))
#			logger.info('BdielEr:'+str(solnEr))
#			logger.info('BdielTand:'+str(solnTand))
			
			#Djorjdevic-Sarkar Equations
			K = ((solnEr*solnTand)-(cond_DC/(2*pi*Eo*solnfreq)))/((pi/2)-math.atan(solnfreq/Freq_B))		
			E_inf = solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(solnfreq*solnfreq)))/solnfreq)		
			delta_E = 10*solnTand*E_inf
			Freq_A = Freq_B/math.exp(delta_E/K)
			
			

			oDefinitionManager.AddMaterial(
				[
					"NAME:BottomDielectric"+"_"+formated_Datetime_string,
					"CoordinateSystemType:=", "Cartesian",
					[
						"NAME:AttachedData"
					],
					[
						"NAME:ModifierData"
					],
					"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
					"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
					"dielectric_loss_tangent:=", "0",
					"magnetic_loss_tangent:=", "0"
				])

			bottomdielectricmaterial = "\"BottomDielectric"+"_"+formated_Datetime_string+"\""
			topdielectricmaterial = "\"TopDielectric"+"_"+formated_Datetime_string+"\""


				
		##################################################################
		# drawing dielectrics and reference planes for differential      #
		# transmission lines                                             #
		#############################################################################################################################################################################################################

		if differential ==1:
			

			#######################
			# Create Ground Plane # 
			#######################
			oEditor.CreateRectangle(
				[
					"NAME:RectangleParameters",
					"IsCovered:="		, True,
					"XStart:="		, "0mil",
					"YStart:="		, "0mil",
					"ZStart:="		, "0mil",
					"Width:="		, "("+str(numberoftraces)+"*0.5-1)*(diffspacing)"+"+"+str(numberoftraces)+"*"+str(maxtracewidth)+units+"+8*"+str(maxtracewidth)+units+"+"+"("+str(numberoftraces)+"*0.5)"+"*tracespacing"+"+0.5*"+str(math.fmod(numberoftraces,2))+"*tracespacing",	
					"Height:="		, "planethickness",
					"WhichAxis:="		, "Z"
				], 
				[
					"NAME:Attributes",
					"Name:="		, "Ground_Plane",
					"Flags:="		, "",
					"Color:="		, "(132 132 193)",
					"Transparency:="	, 0,
					"PartCoordinateSystem:=", "Global",
					"UDMId:="		, "",
					"MaterialValue:="	, "\"copper\"",
					"SolveInside:="		, False
				])


			###########################
			#Create Bottom Dielectric #
			###########################
			oEditor.CreateRectangle(
				[
					"NAME:RectangleParameters",
					"IsCovered:="		, True,
					"XStart:="		, "0mil",
					"YStart:="		, "planethickness",
					"ZStart:="		, "0mil",
					"Width:="		, "("+str(numberoftraces)+"*0.5-1)*(diffspacing)"+"+"+str(numberoftraces)+"*"+str(maxtracewidth)+units+"+8*"+str(maxtracewidth)+units+"+"+"("+str(numberoftraces)+"*0.5)"+"*tracespacing"+"+0.5*"+str(math.fmod(numberoftraces,2))+"*tracespacing",		
					"Height:="		, "bottomdielectricthickness",
					"WhichAxis:="		, "Z"
				], 
				[
					"NAME:Attributes",
					"Name:="		, "Dielectric_Bottom",
					"Flags:="		, "",
					"Color:="		, "(253 165 2)",
					"Transparency:="	, 0,
					"PartCoordinateSystem:=", "Global",
					"UDMId:="		, "",
					"MaterialValue:="	, bottomdielectricmaterial,
					"SolveInside:="		, False
				])	




			if microstrip ==0:

			############################################	
			# is microstrip == 0 archetecture must     #
			# be stripline so now add Top Dielectric   #
			# and top ref plane                        #
			############################################
				oEditor.CreateRectangle(
					[
						"NAME:RectangleParameters",
						"IsCovered:="		, True,
						"XStart:="		, "0mil",
						"YStart:="		, "planethickness + bottomdielectricthickness",
						"ZStart:="		, "0mil",
					"Width:="		, "("+str(numberoftraces)+"*0.5-1)*(diffspacing)"+"+"+str(numberoftraces)+"*"+str(maxtracewidth)+units+"+8*"+str(maxtracewidth)+units+"+"+"("+str(numberoftraces)+"*0.5)"+"*tracespacing"+"+0.5*"+str(math.fmod(numberoftraces,2))+"*tracespacing",
						"Height:="		, "topdielectricthickness",
						"WhichAxis:="		, "Z"
					], 
					[
						"NAME:Attributes",
						"Name:="		, "Dielectric_Top",
						"Flags:="		, "",
						"Color:="		, "(255 128 0)",
						"Transparency:="	, 0,
						"PartCoordinateSystem:=", "Global",
						"UDMId:="		, "",
						"MaterialValue:="	, topdielectricmaterial,
						"SolveInside:="		, False
					])

			#######################
			#Create Top Ref Plane #
			#######################
				oEditor.CreateRectangle(
					[
						"NAME:RectangleParameters",
						"IsCovered:="		, True,
						"XStart:="		, "0mil",
						"YStart:="		, "planethickness + topdielectricthickness + bottomdielectricthickness",
						"ZStart:="		, "0mil",
					"Width:="		, "("+str(numberoftraces)+"*0.5-1)*(diffspacing)"+"+"+str(numberoftraces)+"*"+str(maxtracewidth)+units+"+8*"+str(maxtracewidth)+units+"+"+"("+str(numberoftraces)+"*0.5)"+"*tracespacing"+"+0.5*"+str(math.fmod(numberoftraces,2))+"*tracespacing",			
						"Height:="		, "planethickness",
						"WhichAxis:="		, "Z"
					], 
					[
						"NAME:Attributes",
						"Name:="		, "Top_Ref_Plane",
						"Flags:="		, "",
						"Color:="		, "(132 132 193)",
						"Transparency:="	, 0,
						"PartCoordinateSystem:=", "Global",
						"UDMId:="		, "",
						"MaterialValue:="	, "\"copper\"",
						"SolveInside:="		, False
					])		


			if microstrip ==0:
				#################################################################
				#Assign port to Top and Bottom Ref plane for stripline geometry #
				#################################################################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleReferenceGround(
					[
						"NAME:Ground_Plane",
						"Objects:="		, ["Ground_Plane","Top_Ref_Plane"],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])	
				
			if microstrip ==1:
				################################################################
				#Assign port to Ground Plane only as its a microstrip geometry #
				################################################################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleReferenceGround(
					[
						"NAME:Ground_Plane",
						"Objects:="		, ["Ground_Plane"],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])


				
		##################################################################
		# drawing dielectrics and reference planes for single ended      #
		# transmission lines                                             #
		#############################################################################################################################################################################################################

		if differential ==0:
			#######################
			# Create Ground Plane #
			#######################
			oEditor.CreateRectangle(
				[
					"NAME:RectangleParameters",
					"IsCovered:="		, True,
					"XStart:="		, "0mil",
					"YStart:="		, "0mil",
					"ZStart:="		, "0mil",
					"Width:="		, "(("+str(numberoftraces)+"*tracespacing-tracespacing)+("+str(numberoftraces)+"*"+str(maxtracewidth)+units+"-"+str(maxtracewidth)+units+")+9*"+str(maxtracewidth)+units+")",	
					"Height:="		, "planethickness",
					"WhichAxis:="		, "Z"
				], 
				[
					"NAME:Attributes",
					"Name:="		, "Ground_Plane",
					"Flags:="		, "",
					"Color:="		, "(132 132 193)",
					"Transparency:="	, 0,
					"PartCoordinateSystem:=", "Global",
					"UDMId:="		, "",
					"MaterialValue:="	, "\"copper\"",
					"SolveInside:="		, False
				])
	
				
			###########################
			#Create Bottom Dielectric #
			###########################
			oEditor.CreateRectangle(
				[
					"NAME:RectangleParameters",
					"IsCovered:="		, True,
					"XStart:="		, "0mil",
					"YStart:="		, "planethickness",
					"ZStart:="		, "0mil",
					"Width:="		, "(("+str(numberoftraces)+"*tracespacing-tracespacing)+("+str(numberoftraces)+"*"+str(maxtracewidth)+units+"-"+str(maxtracewidth)+units+")+9*"+str(maxtracewidth)+units+")",		
					"Height:="		, "bottomdielectricthickness",
					"WhichAxis:="		, "Z"
				], 
				[
					"NAME:Attributes",
					"Name:="		, "Dielectric_Bottom",
					"Flags:="		, "",
					"Color:="		, "(253 165 2)",
					"Transparency:="	, 0,
					"PartCoordinateSystem:=", "Global",
					"UDMId:="		, "",
					"MaterialValue:="	, bottomdielectricmaterial,
					"SolveInside:="		, False
				])	

			if microstrip ==1:
			##############################
			#Assign port to Ground Plane #
			##############################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleReferenceGround(
					[
						"NAME:Ground_Plane",
						"Objects:="		, ["Ground_Plane"],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])

			if microstrip ==0:

			############################################	
			# is microstrip == 0 archetecture must     #
			# be stripline so now add Top Dielectric   #
			# and top ref plane                        #
			############################################
				oEditor.CreateRectangle(
					[
						"NAME:RectangleParameters",
						"IsCovered:="		, True,
						"XStart:="		, "0mil",
						"YStart:="		, "planethickness + bottomdielectricthickness",
						"ZStart:="		, "0mil",
						"Width:="		, "(("+str(numberoftraces)+"*tracespacing-tracespacing)+("+str(numberoftraces)+"*"+str(maxtracewidth)+units+"-"+str(maxtracewidth)+units+")+9*"+str(maxtracewidth)+units+")",				   		
						"Height:="		, "topdielectricthickness",
						"WhichAxis:="		, "Z"
					], 
					[
						"NAME:Attributes",
						"Name:="		, "Dielectric_Top",
						"Flags:="		, "",
						"Color:="		, "(255 128 0)",
						"Transparency:="	, 0,
						"PartCoordinateSystem:=", "Global",
						"UDMId:="		, "",
						"MaterialValue:="	, topdielectricmaterial,
						"SolveInside:="		, False
					])

			#######################
			#Create Top Ref Plane #
			#######################
				oEditor.CreateRectangle(
					[
						"NAME:RectangleParameters",
						"IsCovered:="		, True,
						"XStart:="		, "0mil",
						"YStart:="		, "planethickness + topdielectricthickness + bottomdielectricthickness",
						"ZStart:="		, "0mil",
						"Width:="		, "(("+str(numberoftraces)+"*tracespacing-tracespacing)+("+str(numberoftraces)+"*"+str(maxtracewidth)+units+"-"+str(maxtracewidth)+units+")+9*"+str(maxtracewidth)+units+")",							
						"Height:="		, "planethickness",
						"WhichAxis:="		, "Z"
					], 
					[
						"NAME:Attributes",
						"Name:="		, "Top_Ref_Plane",
						"Flags:="		, "",
						"Color:="		, "(132 132 193)",
						"Transparency:="	, 0,
						"PartCoordinateSystem:=", "Global",
						"UDMId:="		, "",
						"MaterialValue:="	, "\"copper\"",
						"SolveInside:="		, False
					])		


			############################################################
			# Assign port to Ground Plane to top and bottom ref planes #
			############################################################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleReferenceGround(
					[
						"NAME:Ground_Plane",
						"Objects:="		, ["Ground_Plane","Top_Ref_Plane"],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])
					
					
			
		#########################################		
		#creating soldermask if microstrip = 1  #
		#########################################################################################################################################		

		if microstrip == 1:		


			########################################################
			#selects traces and bottom dielectric and makes copies #
			########################################################
			while tracecount <= numberoftraces:
				oEditor.Copy(
					[
						"NAME:Selections",
						"Selections:="		, "Trace"+str(tracecount)
					])
					
				oEditor.Paste()
				tracecount +=1
				
			oEditor.Copy(
				[
					"NAME:Selections",
					"Selections:="		, "Dielectric_Bottom"
				])
				
			oEditor.Paste()	
			tracecount = 1

			###########################################################################################################################
			#selects top and side edges of trace and Dielectric_Bottom op edge and move vertically the distance = soldemask thickness #
			###########################################################################################################################
			egdenumber1 = 0  
			egdenumber2 = 0 
			egdenumber3 = 0	
			dielectricedge = 0
			if numberoftraces == 1:
				egdenumber1 = 43  
				egdenumber2 = 44 
				egdenumber3 = 46
				dielectricedge = 57
			else: 
				egdenumber1 = 43 + (numberoftraces-1)*12  
				egdenumber2 = 44 + (numberoftraces-1)*12 
				egdenumber3 = 46 + (numberoftraces-1)*12	
				dielectricedge = 57	+ (numberoftraces-1)*24
					
			shift = 0
			while tracecount <= numberoftraces:
				oEditor.MoveEdges(
					[
						"NAME:Selections",
						"Selections:="		, "Trace"+str(tracecount+numberoftraces),
						"NewPartsModelFlag:="	, "Model"
					], 
					[
						"NAME:Parameters",
						[
							"NAME:MoveEdgesParameters",
							"MoveAlongNormalFlag:="	, True,
							"OffsetDistance:="	, "soldermaskthickness",
							"MoveVectorX:="		, "0mil",
							"MoveVectorY:="		, "0mil",
							"MoveVectorZ:="		, "0mil",
							"EdgesToMove:="		, [egdenumber1+shift,egdenumber2+shift,egdenumber3+shift]
						]
					])
				tracecount +=1
				shift +=12
			tracecount = 1


				
			oEditor.MoveEdges(
				[
					"NAME:Selections",
					"Selections:="		, "Dielectric_Bottom1",
					"NewPartsModelFlag:="	, "Model"
				], 
				[
					"NAME:Parameters",
					[
						"NAME:MoveEdgesParameters",
						"MoveAlongNormalFlag:="	, True,
						"OffsetDistance:="	, "soldermaskthickness",
						"MoveVectorX:="		, "0mil",
						"MoveVectorY:="		, "0mil",
						"MoveVectorZ:="		, "0mil",
						"EdgesToMove:="		, [dielectricedge]
					]
				])	
				
			#############################################################################	
			#booleon unite all copies and subtract from origional traces and dielectric #
			#the left over is the soldermask layer                                      #
			#############################################################################
			unitestring = ''

			while tracecount <= numberoftraces:
				unitestring = unitestring +","+ "Trace" + str(numberoftraces+tracecount)
				tracecount +=1
			tracecount = 1
				
			oEditor.Unite(
				[
					"NAME:Selections",
					"Selections:="		, "Dielectric_Bottom1"+unitestring
				], 
				[
					"NAME:UniteParameters",
					"KeepOriginals:="	, False
				])
				
				
			#####################################################	
			#Assign material properties to soldermask material  #
			#####################################################	
			oEditor.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:Geometry3DAttributeTab",
						[
							"NAME:PropServers", 
							"Dielectric_Bottom1"
						],
						[
							"NAME:ChangedProps",
							[
								"NAME:Material",
								"Value:="		, soldermaskmaterial
							]
						]
					]
				])	
				
		
			#####################################################	
			#Change name from Dielectric_Bottom1 to Soldermask  #
			#####################################################	
			oEditor.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:Geometry3DAttributeTab",
						[
							"NAME:PropServers", 
							"Dielectric_Bottom1"
						],
						[
							"NAME:ChangedProps",
							[
								"NAME:Name",
								"Value:="		, "SolderMask"
							],
							[
								"NAME:Color",
								"R:="			, 0,
								"G:="			, 255,
								"B:="			, 0
							]
						]
					]
				])	
				
				
			#########################################################	
			#subtract soldermask object from traces and dielectric  #
			#to create thin layer above traces                      #            
			#########################################################
			toolstring = ''	
			while tracecount <= numberoftraces:
				toolstring = toolstring +","+ "Trace" + str(tracecount)
				tracecount +=1
			tracecount = 1	
			oEditor.Subtract(
				[
					"NAME:Selections",
					"Blank Parts:="		, "SolderMask",
					"Tool Parts:="		, "Dielectric_Bottom" + toolstring
				], 
				[
					"NAME:SubtractParameters",
					"KeepOriginals:="	, True
				])	


		#################################
		#   Insert Solution Frequency  	#
		#################################	
		
		oModule = oDesign.GetModule("AnalysisSetup")
		oModule.InsertSetup("2DMatrix", 
			[
				"NAME:Setup1",
				"AdaptiveFreq:="	, str(solutionfreq) + Solutionfrequnits,
				"EnableDistribProbTypeOption:=", False,
				"Enabled:="		, True,
				[
					"NAME:CGDataBlock",
					"MaxPass:="		, 10,
					"MinPass:="		, 1,
					"MinConvPass:="		, 1,
					"PerError:="		, 1,
					"PerRefine:="		, 30,
					"DataType:="		, "CG",
					"Included:="		, True,
					"UseParamConv:="	, False,
					"UseLossyParamConv:="	, False,
					"PerErrorParamConv:="	, 1,
					"UseLossConv:="		, True
				],
				[
					"NAME:RLDataBlock",
					"MaxPass:="		, 10,
					"MinPass:="		, 1,
					"MinConvPass:="		, 1,
					"PerError:="		, 1,
					"PerRefine:="		, 30,
					"DataType:="		, "RL",
					"Included:="		, True,
					"UseParamConv:="	, False,
					"UseLossyParamConv:="	, False,
					"PerErrorParamConv:="	, 1,
					"UseLossConv:="		, True
				]
			])	

		#################################################
		# Insert either Discrete or Interpolating Sweep #
		#################################################

		if freqsweeptype == 'none':
			pass
		
		if freqsweeptype == 'Discrete':
			oModule.InsertSweep("Setup1", 
				[
					"NAME:Discrete_Sweep",
					"IsEnabled:="		, True,
					"SetupType:="		, "LinearStep",
					"StartValue:="		, str(solutionstartfreq) + StartFrequnits,
					"StopValue:="		, str(solutionstopfreq) + StopFrequnits,
					"StepSize:="		, str(solutionstepfreq) + FreqStepunits,
					"Type:="		, "Discrete",
					"SaveFields:="		, False,
					"ExtrapToDC:="		, False
				])

		if freqsweeptype == 'Interpolating':
			oModule.InsertSweep("Setup1", 
				[
					"NAME:Interpolating_Sweep",
					"IsEnabled:="		, True,
					"SetupType:="		, "LinearStep",
					"StartValue:="		, str(solutionstartfreq) + StartFrequnits,
					"StopValue:="		, str(solutionstopfreq) + StopFrequnits,
					"StepSize:="		, str(solutionstepfreq) + FreqStepunits,
					"Type:="		, "Interpolating",
					"SaveFields:="		, False,
					"InterpTolerance:="	, 0.5,
					"InterpMaxSolns:="	, 50,
					"InterpMinSolns:="	, 0,
					"InterpMinSubranges:="	, 1,
					"ExtrapToDC:="		, True,
					"MinSolvedFreq:="	, "100000"
				])
				









				###########################################################################
				# DrawBroadSideCoupledStripline Class draws Broad Side couples stripline  #
#####################################################################################################################################################################################################
class DrawBroadSideCoupledStripline(object):
	def __init__(self,oProject,oEditor,oDesign,units,tracespacing,toptracewidth,
			bottomtracewidth,maxtracewidth,numberoftraces,diffspacing,planethickness,topdielectricthickness,D5thickness,bottomdielectricthickness,
			tracethickness,tracewidth,etching,roughnesstype,surfaceroughnesstop,surfaceroughnesssides,surfaceroughnessbottom,
			surfaceroughnessunits,HHsurfaceratiotop,noduleradiustop,HHsurfaceratiosides,noduleradiussides,HHsurfaceratiobottom,
			noduleradiusbottom,plating,useplatingmaterial,platingmaterial,platingthickness,platingthicknessunits,soldermaskmaterial,
			soldermaskthickness,soldermaskunits,solutionfreq,solutionstartfreq,solutionstopfreq,solutionstepfreq,Solutionfrequnits,StartFrequnits,
			StopFrequnits,FreqStepunits,freqsweeptype,SMdielectricfreq,SMdielectricfrequnits,SMEr,SMTand,Bdielfreq,Bdielectricfrequnits,
			BdielEr,BdielTand,Tdielfreq,Tdielfrequnits,TdielEr,TdielTand,D4dielfreq,D4dielfrequnits,D4dielEr,D4dielTand,D5dielfreq,D5dielfrequnits,
			D5dielEr,D5dielTand,formated_Datetime_string):

		
		logger = logging.getLogger('TLine.MainForm.DesignSelect')
		logger.info('Broadside Coupled Stripline Model Created!')		
		
		

		traceoffset = 0
		
		#Handling etching
		
		if toptracewidth > bottomtracewidth:
			etchsidetracewidth = bottomtracewidth
			
		if	toptracewidth < bottomtracewidth:
			etchsidetracewidth = toptracewidth
			
		if	toptracewidth == bottomtracewidth:
			etchsidetracewidth = toptracewidth			


		#Calculate Conductor Thickness even if etched
		a = float(toptracewidth)
		b = float(bottomtracewidth)
		c = float(tracethickness)
		x = 0 #triangle base lenght
		Y = 0 #trace sides length
		
		#triangle base length.
		if a > b:
			x = (a-b)/2
		if a < b:
			x = (b-a)/2
			
		if a == b:
			y = tracethickness

		else:
			y = math.sqrt(c*c + x*x)
				
		trace_perimeter = float(toptracewidth) + float(bottomtracewidth) + 2*float(y)
		Area_trapdzoid = ((float(toptracewidth) + float(bottomtracewidth)) / 2.0) * float(tracethickness)
		conductor_thickness = Area_trapdzoid / trace_perimeter





		dielectric1thickness = topdielectricthickness
		dielectric2thickness = bottomdielectricthickness
		dielectric3thickness = tracespacing
		dielectric4thickness = soldermaskthickness
		dielectric5thickness = D5thickness


		diel1freq = SMdielectricfreq
		diel1Er = SMEr
		diel1Tand = SMTand
	
		diel2freq = Bdielfreq
		diel2Er = BdielEr
		diel2Tand = BdielTand
		
		diel3freq = Tdielfreq
		diel3Er = TdielEr
		diel3Tand = TdielTand
				
		diel4freq = D4dielfreq
		diel4Er = D4dielEr
		diel4Tand = D4dielTand
		
		diel5freq = D5dielfreq
		diel5Er = D5dielEr
		diel5Tand = D5dielTand
		
		
	
		
		diffshift = 0  #local variable to track when to shift sets of traces to they are diff pairs
		
		
	
		
		#Sets default Design units
		oEditor.SetModelUnits(
				[
					"NAME:Units",
					"Units:="		, units,
					"Rescale:="		, False
				])
		
		####################################################################
		# adding variables to project so that its parametrized            #
		##############################################################################################################################
		
		oDesign.ChangeProperty(
			[
				"NAME:AllTabs",
				[
					"NAME:LocalVariableTab",
					[
						"NAME:PropServers", 
						"LocalVariables"
					],
					[
						"NAME:NewProps",
						[
							"NAME:dielectric1thickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(dielectric1thickness) + units
						],
						[
							"NAME:dielectric2thickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(dielectric2thickness) + units
						],
						[
							"NAME:dielectric3thickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(dielectric3thickness) + units
						],
						[
							"NAME:dielectric4thickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(dielectric4thickness) + units
						],
						[
							"NAME:dielectric5thickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(dielectric5thickness) + units
						],
						[
							"NAME:diffspacing",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(diffspacing) + units
						],
						[
							"NAME:tracewidth",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(tracewidth) + units
						],					
						[
							"NAME:planethickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(planethickness) + units
						],
						[
							"NAME:tracethickness",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(tracethickness) + units
						],	
						[
							"NAME:traceoffset",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(traceoffset) + units
						],	
						[
							"NAME:etchsidetracewidth",
							"PropType:="		, "VariableProp",
							"UserDef:="		, True,
							"Value:="		, str(etchsidetracewidth) + units
						]					
					]
				]
			])			
		
		
		
		
		
		
			
		if roughnesstype ==  1:		
			oDesign.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:LocalVariableTab",
						[
							"NAME:PropServers", 
							"LocalVariables"
						],
						[
							"NAME:NewProps",
							[
								"NAME:platingthickness",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(platingthickness) + platingthicknessunits
							],	
							[
								"NAME:surfaceroughnesstop",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(surfaceroughnesstop) + surfaceroughnessunits
							],
							[
								"NAME:surfaceroughnesssides",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(surfaceroughnesssides) + surfaceroughnessunits
							],		
							[
								"NAME:surfaceroughnessbottom",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(surfaceroughnessbottom) + surfaceroughnessunits
							]						
						]
					]
				])		
		
		
		if roughnesstype ==  2:	
			oDesign.ChangeProperty(
				[
					"NAME:AllTabs",
					[
						"NAME:LocalVariableTab",
						[
							"NAME:PropServers", 
							"LocalVariables"
						],
						[
							"NAME:NewProps",
							[
								"NAME:platingthickness",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(platingthickness) + platingthicknessunits
							],	
							[
								"NAME:noduleradiustop",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(noduleradiustop) + surfaceroughnessunits
							],	
							[
								"NAME:noduleradiussides",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(noduleradiussides) + surfaceroughnessunits
							],	
							[
								"NAME:noduleradiusbottom",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(noduleradiusbottom) + surfaceroughnessunits
							],	
							[
								"NAME:HHsurfaceratiotop",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(HHsurfaceratiotop)
							],
							[
								"NAME:HHsurfaceratiosides",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(HHsurfaceratiosides)
							],
							[
								"NAME:HHsurfaceratiobottom",
								"PropType:="		, "VariableProp",
								"UserDef:="		, True,
								"Value:="		, str(HHsurfaceratiobottom)
							]						
						]
					]
				])	
			
			
			
			
			
			
			
			
			
			
		#############################################
		# main loop, looping through trace drawing  #
		################################################################################################################################
		tracecount = 1
		
		while tracecount <=numberoftraces:
		
		
		
		##############################################################
		#  This if statement test for the first trace then draws it  #
		##############################################################
		
			if tracecount ==1:
		
				oEditor.CreatePolyline(
						[
							"NAME:Trace",
							"IsPolylineCovered:="	, True,
							"IsPolylineClosed:="	, True,
							[
							"NAME:PolylinePoints",
							[
								"NAME:PLPoint",
								"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*tracewidth",
								"Y:="			, "((planethickness+dielectric1thickness+0.5*tracethickness)-0.5*tracethickness+dielectric2thickness)",
								"Z:="			, "0" + units
							],
							[
								"NAME:PLPoint",
								"X:="			,  "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth+0.5*tracewidth",
								"Y:="			, "((planethickness+dielectric1thickness+0.5*tracethickness)-0.5*tracethickness+dielectric2thickness)",
								"Z:="			, "0" + units
							],
							[
								"NAME:PLPoint",
								"X:="			,  "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth+0.5*etchsidetracewidth",
								"Y:="			, "((planethickness+dielectric1thickness+0.5*tracethickness)-1.5*tracethickness+dielectric2thickness)",
								"Z:="			, "0" + units
							],
							[
								"NAME:PLPoint",
								"X:="			,  "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*etchsidetracewidth",
								"Y:="			, "((planethickness+dielectric1thickness+0.5*tracethickness)-1.5*tracethickness+dielectric2thickness)",
								"Z:="			, "0" + units
							],
							[
								"NAME:PLPoint",
								"X:="			,  "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*tracewidth",
								"Y:="			, "((planethickness+dielectric1thickness+0.5*tracethickness)-0.5*tracethickness+dielectric2thickness)",
								"Z:="			, "0" + units
							]
				],
					[
						"NAME:PolylineSegments",
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 0,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 1,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 2,
							"NoOfPoints:="		, 2
						],
						[
							"NAME:PLSegment",
							"SegmentType:="		, "Line",
							"StartIndex:="		, 3,
							"NoOfPoints:="		, 2
						]
					],
					[
						"NAME:PolylineXSection",
						"XSectionType:="	, "None",
						"XSectionOrient:="	, "Auto",
						"XSectionWidth:="	, "0mm",
						"XSectionTopWidth:="	, "0mm",
						"XSectionHeight:="	, "0mm",
						"XSectionNumSegments:="	, "0",
						"XSectionBendType:="	, "Corner"
					]
				], 
				[
					"NAME:Attributes",
					"Name:="		, "Trace"+str(tracecount),
					"Flags:="		, "",
					"Color:="		, "(132 132 193)",
					"Transparency:="	, 0,
					"PartCoordinateSystem:=", "Global",
					"UDMId:="		, "",
					"MaterialValue:="	, "\"copper\"",
					"SolveInside:="		, False
				])
		
				#########################
				# Assign signal sources #
				#########################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleSignalLine(
					[
						"NAME:"+"Trace"+str(tracecount),
						"Objects:="		, ["Trace1"],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])
					
				tracecount +=1
			
		
		
				
		#####################################################################################
		# This if statement offsets the additional traces if there are more than one drawn  #
		# and differential spacing if defined, differential ==1                             #
		##########################################################################################################             	
		
			if tracecount >1 and numberoftraces !=1:	
			
				#finds even traces these are the top broad side trace
				if math.fmod(tracecount,2) ==0:
					diffshift = diffshift + 1
		
					oEditor.CreatePolyline(
					[
						"NAME:Trace",
						"IsPolylineCovered:="	, True,
						"IsPolylineClosed:="	, True,
						[
						"NAME:PolylinePoints",
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*etchsidetracewidth+("+str(tracecount-2)+"*(0.5*tracewidth+0.5*diffspacing)+traceoffset)",
							"Y:="			, "(planethickness+dielectric1thickness+dielectric2thickness+dielectric3thickness+0.5*tracethickness)+0.5*tracethickness",
							"Z:="			, "0" + units
						],
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth+0.5*etchsidetracewidth+("+str(tracecount-2)+"*(0.5*tracewidth+0.5*diffspacing)+traceoffset)",
							"Y:="			, "(planethickness+dielectric1thickness+dielectric2thickness+dielectric3thickness+0.5*tracethickness)+0.5*tracethickness",
							"Z:="			, "0" + units
						],
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth+0.5*tracewidth+("+str(tracecount-2)+"*(0.5*tracewidth+0.5*diffspacing)+traceoffset)",
							"Y:="			, "(planethickness+dielectric1thickness+dielectric2thickness+dielectric3thickness+0.5*tracethickness)-0.5*tracethickness",
							"Z:="			, "0" + units
						],
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*tracewidth+("+str(tracecount-2)+"*(0.5*tracewidth+0.5*diffspacing)+traceoffset)",					
							"Y:="			, "(planethickness+dielectric1thickness+dielectric2thickness+dielectric3thickness+0.5*tracethickness)-0.5*tracethickness",
							"Z:="			, "0" + units
						],
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*etchsidetracewidth+("+str(tracecount-2)+"*(0.5*tracewidth+0.5*diffspacing)+traceoffset)",				
							"Y:="			, "(planethickness+dielectric1thickness+dielectric2thickness+dielectric3thickness+0.5*tracethickness)+0.5*tracethickness",
							"Z:="			, "0" + units
						]
					],

						[
							"NAME:PolylineSegments",
							[
								"NAME:PLSegment",
								"SegmentType:="		, "Line",
								"StartIndex:="		, 0,
								"NoOfPoints:="		, 2
							],
							[
								"NAME:PLSegment",
								"SegmentType:="		, "Line",
								"StartIndex:="		, 1,
								"NoOfPoints:="		, 2
							],
							[
								"NAME:PLSegment",
								"SegmentType:="		, "Line",
								"StartIndex:="		, 2,
								"NoOfPoints:="		, 2
							],
							[
								"NAME:PLSegment",
								"SegmentType:="		, "Line",
								"StartIndex:="		, 3,
								"NoOfPoints:="		, 2
							]
						],
						[
							"NAME:PolylineXSection",
							"XSectionType:="	, "None",
							"XSectionOrient:="	, "Auto",
							"XSectionWidth:="	, "0mm",
							"XSectionTopWidth:="	, "0mm",
							"XSectionHeight:="	, "0mm",
							"XSectionNumSegments:="	, "0",
							"XSectionBendType:="	, "Corner"
						]
					], 
					[
						"NAME:Attributes",
						"Name:="		, "Trace"+str(tracecount),
						"Flags:="		, "",
						"Color:="		, "(132 132 193)",
						"Transparency:="	, 0,
						"PartCoordinateSystem:=", "Global",
						"UDMId:="		, "",
						"MaterialValue:="	, "\"copper\"",
						"SolveInside:="		, False
					])
			
			
				#finds odd traces these are the bottom broad side trace	
				if math.fmod(tracecount,2) ==1:
					diffshift = diffshift	
			
					oEditor.CreatePolyline(
					[
						"NAME:Trace",
						"IsPolylineCovered:="	, True,
						"IsPolylineClosed:="	, True,
						[
						"NAME:PolylinePoints",
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*tracewidth+("+str(tracecount-1)+"*(0.5*tracewidth+0.5*diffspacing))",
							"Y:="			, "(planethickness+dielectric1thickness+0.5*tracethickness)-0.5*tracethickness+dielectric2thickness",
							"Z:="			, "0" + units
						],
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth+0.5*tracewidth+("+str(tracecount-1)+"*(0.5*tracewidth+0.5*diffspacing))",
							"Y:="			, "(planethickness+dielectric1thickness+0.5*tracethickness)-0.5*tracethickness+dielectric2thickness",
							"Z:="			, "0" + units
						],
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth+0.5*etchsidetracewidth+("+str(tracecount-1)+"*(0.5*tracewidth+0.5*diffspacing))",
							"Y:="			, "(planethickness+dielectric1thickness+0.5*tracethickness)-1.5*tracethickness+dielectric2thickness",
							"Z:="			, "0" + units
						],
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*etchsidetracewidth+("+str(tracecount-1)+"*(0.5*tracewidth+0.5*diffspacing))",
							"Y:="			, "(planethickness+dielectric1thickness+0.5*tracethickness)-1.5*tracethickness+dielectric2thickness",
							"Z:="			, "0" + units
						],
						[
							"NAME:PLPoint",
							"X:="			, "4.0*(tracewidth+dielectric3thickness)+0.5*tracewidth-0.5*tracewidth+("+str(tracecount-1)+"*(0.5*tracewidth+0.5*diffspacing))",
							"Y:="			, "(planethickness+dielectric1thickness+0.5*tracethickness)-0.5*tracethickness+dielectric2thickness",
							"Z:="			, "0" + units
						]
					],
						[
							"NAME:PolylineSegments",
							[
								"NAME:PLSegment",
								"SegmentType:="		, "Line",
								"StartIndex:="		, 0,
								"NoOfPoints:="		, 2
							],
							[
								"NAME:PLSegment",
								"SegmentType:="		, "Line",
								"StartIndex:="		, 1,
								"NoOfPoints:="		, 2
							],
							[
								"NAME:PLSegment",
								"SegmentType:="		, "Line",
								"StartIndex:="		, 2,
								"NoOfPoints:="		, 2
							],
							[
								"NAME:PLSegment",
								"SegmentType:="		, "Line",
								"StartIndex:="		, 3,
								"NoOfPoints:="		, 2
							]
						],
						[
							"NAME:PolylineXSection",
							"XSectionType:="	, "None",
							"XSectionOrient:="	, "Auto",
							"XSectionWidth:="	, "0mm",
							"XSectionTopWidth:="	, "0mm",
							"XSectionHeight:="	, "0mm",
							"XSectionNumSegments:="	, "0",
							"XSectionBendType:="	, "Corner"
						]
					], 
					[
						"NAME:Attributes",
						"Name:="		, "Trace"+str(tracecount),
						"Flags:="		, "",
						"Color:="		, "(132 132 193)",
						"Transparency:="	, 0,
						"PartCoordinateSystem:=", "Global",
						"UDMId:="		, "",
						"MaterialValue:="	, "\"copper\"",
						"SolveInside:="		, False
					])
			
			
			
		
			
				#########################
				# Assign signal sources #
				#########################
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignSingleSignalLine(
					[
						"NAME:"+"Trace"+str(tracecount),
						"Objects:="		, ["Trace"+str(tracecount)],
						"SolveOption:="		, "Automatic",
						"Thickness:="		, str(conductor_thickness) + units
					])
			
				tracecount +=1	
			
			
		tracecount = 1   #setting trace count back to one.	
			
		
		
		
				
		#################################################################################################
		# creating dielectrics, drawing dielectrics, and reference planes for Broadside coupled traces  #
		#############################################################################################################################################################################################################
		
		
		#######################
		# Create Ground Plane # 
		#######################
		oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "0mil",
				"YStart:="		, "0mil",
				"ZStart:="		, "0mil",
				"Width:="		, "8.0*(tracewidth+dielectric3thickness)+(0.5*"+str(numberoftraces)+"-1)*(diffspacing)+"+str(numberoftraces)+"*0.5*tracewidth",	
				"Height:="		, "planethickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "Ground_Plane",
				"Flags:="		, "",
				"Color:="		, "(132 132 193)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, "\"copper\"",
				"SolveInside:="		, False
			])
		
		
		
		
		###########################################################		
		#creating Djorjdevic-Sarkar fitted dielectric materials   #
		###########################################################		
		
		#Constants
		pi = math.pi
		Freq_B = 1e12/(2*pi)
		cond_DC = 1e-12
		Eo = 8.854e-12
		
		###------------------Dielectric 1 Fit----------------####	
		#inputs from user
		d1solnfreq = float(diel1freq)
		d1solnEr = float(diel1Er)
		d1solnTand = float(diel1Tand)
		
		#Djorjdevic-Sarkar Equations
		K = ((d1solnEr*d1solnTand)-(cond_DC/(2*pi*Eo*d1solnfreq)))/((pi/2)-math.atan(d1solnfreq/Freq_B))		
		E_inf = d1solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(d1solnfreq*d1solnfreq)))/d1solnfreq)		
		delta_E = 10*d1solnTand*E_inf
		Freq_A = Freq_B/math.exp(delta_E/K)
		
		oDefinitionManager = oProject.GetDefinitionManager()			
		oDefinitionManager.AddMaterial(
			[
				"NAME:Dielectric1"+"_"+formated_Datetime_string,
				"CoordinateSystemType:=", "Cartesian",
				[
					"NAME:AttachedData"
				],
				[
					"NAME:ModifierData"
				],
				"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
				"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
				"dielectric_loss_tangent:=", "0",
				"magnetic_loss_tangent:=", "0"
			])				
						
		dielectric1material = "\"Dielectric1"+"_"+formated_Datetime_string+"\""
		
		
		###------------------Dielectric 2 Fit----------------####	
		#inputs from user
		d2solnfreq = float(diel2freq)
		d2solnEr = float(diel2Er)
		d2solnTand = float(diel2Tand)
		
		#Djorjdevic-Sarkar Equations
		K = ((d2solnEr*d2solnTand)-(cond_DC/(2*pi*Eo*d2solnfreq)))/((pi/2)-math.atan(d2solnfreq/Freq_B))		
		E_inf = d2solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(d2solnfreq*d2solnfreq)))/d2solnfreq)		
		delta_E = 10*d2solnTand*E_inf
		Freq_A = Freq_B/math.exp(delta_E/K)
		
		oDefinitionManager = oProject.GetDefinitionManager()			
		oDefinitionManager.AddMaterial(
			[
				"NAME:Dielectric2"+"_"+formated_Datetime_string,
				"CoordinateSystemType:=", "Cartesian",
				[
					"NAME:AttachedData"
				],
				[
					"NAME:ModifierData"
				],
				"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
				"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
				"dielectric_loss_tangent:=", "0",
				"magnetic_loss_tangent:=", "0"
			])				
						
		dielectric2material = "\"Dielectric2"+"_"+formated_Datetime_string+"\""
		
		
		
		###------------------Dielectric 3 Fit----------------####	
		#inputs from user
		d3solnfreq = float(diel3freq)
		d3solnEr = float(diel3Er)
		d3solnTand = float(diel3Tand)
		
		#Djorjdevic-Sarkar Equations
		K = ((d3solnEr*d3solnTand)-(cond_DC/(2*pi*Eo*d3solnfreq)))/((pi/2)-math.atan(d3solnfreq/Freq_B))		
		E_inf = d3solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(d3solnfreq*d3solnfreq)))/d3solnfreq)		
		delta_E = 10*d3solnTand*E_inf
		Freq_A = Freq_B/math.exp(delta_E/K)
		
		oDefinitionManager = oProject.GetDefinitionManager()			
		oDefinitionManager.AddMaterial(
			[
				"NAME:Dielectric3"+"_"+formated_Datetime_string,
				"CoordinateSystemType:=", "Cartesian",
				[
					"NAME:AttachedData"
				],
				[
					"NAME:ModifierData"
				],
				"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
				"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
				"dielectric_loss_tangent:=", "0",
				"magnetic_loss_tangent:=", "0"
			])				
						
		dielectric3material = "\"Dielectric3"+"_"+formated_Datetime_string+"\""
		
		
		###------------------Dielectric 4 Fit----------------####	
		#inputs from user
		d4solnfreq = float(diel4freq)
		d4solnEr = float(diel4Er)
		d4solnTand = float(diel4Tand)
		
		#Djorjdevic-Sarkar Equations
		K = ((d4solnEr*d4solnTand)-(cond_DC/(2*pi*Eo*d4solnfreq)))/((pi/2)-math.atan(d4solnfreq/Freq_B))		
		E_inf = d4solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(d4solnfreq*d4solnfreq)))/d4solnfreq)		
		delta_E = 10*d4solnTand*E_inf
		Freq_A = Freq_B/math.exp(delta_E/K)
		
		oDefinitionManager = oProject.GetDefinitionManager()			
		oDefinitionManager.AddMaterial(
			[
				"NAME:Dielectric4"+"_"+formated_Datetime_string,
				"CoordinateSystemType:=", "Cartesian",
				[
					"NAME:AttachedData"
				],
				[
					"NAME:ModifierData"
				],
				"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
				"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
				"dielectric_loss_tangent:=", "0",
				"magnetic_loss_tangent:=", "0"
			])				
						
		dielectric4material = "\"Dielectric4"+"_"+formated_Datetime_string+"\""
		
		
		###------------------Dielectric 5 Fit----------------####	
		#inputs from user
		d5solnfreq = float(diel5freq)
		d5solnEr = float(diel5Er)
		d5solnTand = float(diel5Tand)
		
		#Djorjdevic-Sarkar Equations
		K = ((d5solnEr*d5solnTand)-(cond_DC/(2*pi*Eo*d5solnfreq)))/((pi/2)-math.atan(d5solnfreq/Freq_B))		
		E_inf = d5solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(d5solnfreq*d5solnfreq)))/d5solnfreq)		
		delta_E = 10*d5solnTand*E_inf
		Freq_A = Freq_B/math.exp(delta_E/K)
		
		oDefinitionManager = oProject.GetDefinitionManager()			
		oDefinitionManager.AddMaterial(
			[
				"NAME:Dielectric5"+"_"+formated_Datetime_string,
				"CoordinateSystemType:=", "Cartesian",
				[
					"NAME:AttachedData"
				],
				[
					"NAME:ModifierData"
				],
				"permittivity:="	, str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
				"conductivity:="	, str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
				"dielectric_loss_tangent:=", "0",
				"magnetic_loss_tangent:=", "0"
			])				
						
		dielectric5material = "\"Dielectric5"+"_"+formated_Datetime_string+"\""	
		
		
		
		
		
		
		
		
		###########################
		#Create Dielectric1       #
		###########################
		oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "0mil",
				"YStart:="		, "planethickness",
				"ZStart:="		, "0mil",
				"Width:="		, "8.0*(tracewidth+dielectric3thickness)+(0.5*"+str(numberoftraces)+"-1)*(diffspacing)+"+str(numberoftraces)+"*0.5*tracewidth",	
				"Height:="		, "dielectric1thickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "d1",
				"Flags:="		, "",
				"Color:="		, "(253 165 2)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, dielectric1material,
				"SolveInside:="		, False
			])	
		
		
		
		############################################	
		#Create Dielectric2                        #
		############################################
		oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "0mil",
				"YStart:="		, "planethickness + dielectric1thickness",
				"ZStart:="		, "0mil",
				"Width:="		, "8.0*(tracewidth+dielectric3thickness)+(0.5*"+str(numberoftraces)+"-1)*(diffspacing)+"+str(numberoftraces)+"*0.5*tracewidth",
				"Height:="		, "dielectric2thickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "d2",
				"Flags:="		, "",
				"Color:="		, "(253 185 60)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, dielectric2material,
				"SolveInside:="		, False
			])
		
		############################################	
		#Create Dielectric3                        #
		############################################
		oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "0mil",
				"YStart:="		, "planethickness + dielectric1thickness + dielectric2thickness",
				"ZStart:="		, "0mil",
				"Width:="		, "8.0*(tracewidth+dielectric3thickness)+(0.5*"+str(numberoftraces)+"-1)*(diffspacing)+"+str(numberoftraces)+"*0.5*tracewidth",
				"Height:="		, "dielectric3thickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "d3",
				"Flags:="		, "",
				"Color:="		, "(253 203 109)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, dielectric3material,
				"SolveInside:="		, False
			])		
			
		############################################	
		#Create Dielectric4                        #
		############################################
		oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "0mil",
				"YStart:="		, "planethickness + dielectric1thickness + dielectric2thickness + dielectric3thickness",
				"ZStart:="		, "0mil",
				"Width:="		, "8.0*(tracewidth+dielectric3thickness)+(0.5*"+str(numberoftraces)+"-1)*(diffspacing)+"+str(numberoftraces)+"*0.5*tracewidth",
				"Height:="		, "dielectric4thickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "d4",
				"Flags:="		, "",
				"Color:="		, "(253 221 158)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, dielectric4material,
				"SolveInside:="		, False
			])			
			
		############################################	
		#Create Dielectric5                        #
		############################################
		oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "0mil",
				"YStart:="		, "planethickness + dielectric1thickness + dielectric2thickness + dielectric3thickness + dielectric4thickness",
				"ZStart:="		, "0mil",
				"Width:="		, "8.0*(tracewidth+dielectric3thickness)+(0.5*"+str(numberoftraces)+"-1)*(diffspacing)+"+str(numberoftraces)+"*0.5*tracewidth",	
				"Height:="		, "dielectric5thickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "d5",
				"Flags:="		, "",
				"Color:="		, "(253 237 200)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, dielectric5material,
				"SolveInside:="		, False
			])		
			
		#######################
		#Create Top Ref Plane #
		#######################
		oEditor.CreateRectangle(
			[
				"NAME:RectangleParameters",
				"IsCovered:="		, True,
				"XStart:="		, "0mil",
				"YStart:="		, "planethickness + dielectric1thickness + dielectric2thickness + dielectric3thickness + dielectric4thickness + dielectric5thickness",
				"ZStart:="		, "0mil",
				"Width:="		, "8.0*(tracewidth+dielectric3thickness)+(0.5*"+str(numberoftraces)+"-1)*(diffspacing)+"+str(numberoftraces)+"*0.5*tracewidth",		
				"Height:="		, "planethickness",
				"WhichAxis:="		, "Z"
			], 
			[
				"NAME:Attributes",
				"Name:="		, "Top_Ref_Plane",
				"Flags:="		, "",
				"Color:="		, "(132 132 193)",
				"Transparency:="	, 0,
				"PartCoordinateSystem:=", "Global",
				"UDMId:="		, "",
				"MaterialValue:="	, "\"copper\"",
				"SolveInside:="		, False
			])		
		###########################################################################
		#Assign port to Top Ref Plane and add additional gnd with matrix operation#
		###########################################################################
		oModule = oDesign.GetModule("BoundarySetup")
		oModule.AssignSingleReferenceGround(
			[
				"NAME:Reference_Planes",
				"Objects:="		, ["Top_Ref_Plane","Ground_Plane"],
				"SolveOption:="		, "Automatic",
				"Thickness:="		, str(conductor_thickness) + units
			])	
		
			
		###########################################################################################		
		#  Adding surface roughness to traces and plating for top and sides of traces if selected #	
		###################################################################################################################################################################
		
		#loop to assign finite conductivity to traces:  Hammerstadt-Jensen
		if roughnesstype ==1:
			counter = 0    #lines for assigning roughness shift by 12 for each trace do top of trace 1 = 7, top trace 2 = 19 
		
			while tracecount<=numberoftraces:
				#top Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessTopTrace"+str(tracecount),
						"Edges:="		, [7+counter],
						"UseCoating:="		, plating,
						"LayerThickness:="	, "platingthickness",
						"UseMaterial:="		, useplatingmaterial,
						"Material:="		, "copper",				
						"Roughness:="		, "surfaceroughnesstop"
					])
		
				#sides Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessSidesTrace"+str(tracecount),
						"Edges:="		, [8+counter,10+counter],
						"UseCoating:="		, plating,
						"LayerThickness:="	, "platingthickness",
						"UseMaterial:="		, useplatingmaterial,
						"Material:="		, platingmaterial,				
						"Roughness:="		, "surfaceroughnesssides"
					])
				
				#bottom Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessBottomTrace"+str(tracecount),
						"Edges:="		    , [9+counter],
						"UseCoating:="		, False,			
						"Roughness:="		, "surfaceroughnessbottom"
					])
		
				counter +=12
				tracecount +=1
				
		counter = 0       	#reset counter	
		tracecount = 1		#reset tracecount
				
		#loop to assign finite conductivity to traces:  Huray
		if roughnesstype ==2:
			counter = 0    #lines for assigning roughness shift by 12 for each trace do top of trace 1 = 7, top trace 2 = 19 
			
			while tracecount<=numberoftraces:
				#top Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessTopTrace"+str(tracecount),
						"Edges:="		, [7+counter],
						"UseCoating:="		, plating,
						"LayerThickness:="	, "platingthickness",
						"UseMaterial:="		, useplatingmaterial,
						"Material:="		, platingmaterial,				
						"Radius:="		, "noduleradiustop",
						"Ratio:="		, "HHsurfaceratiotop"
					])
		
				#sides Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessSidesTrace"+str(tracecount),
						"Edges:="		, [8+counter,10+counter],
						"UseCoating:="		, plating,
						"LayerThickness:="	, "platingthickness",
						"UseMaterial:="		, useplatingmaterial,
						"Material:="		, platingmaterial,				
						"Radius:="		, "noduleradiussides",
						"Ratio:="		, "HHsurfaceratiosides"
		
					])
				
				#bottom Hammerstadt roughness
				oModule = oDesign.GetModule("BoundarySetup")
				oModule.AssignFiniteCond(
					[
						"NAME:"+"RoughnessBottomTrace"+str(tracecount),
						"Edges:="		, [9+counter],
						"UseCoating:="		, False,
						"Radius:="		, "noduleradiusbottom",
						"Ratio:="		, "HHsurfaceratiobottom"
		
					])
		
				counter += 12
				tracecount +=1
				
		counter = 0       	#reset counter	
		tracecount = 1		#reset tracecount		


		#################################
		#   Insert Solution Frequency  	#
		#################################	
		
		oModule = oDesign.GetModule("AnalysisSetup")
		oModule.InsertSetup("2DMatrix", 
			[
				"NAME:Setup1",
				"AdaptiveFreq:="	, str(solutionfreq) + Solutionfrequnits,
				"EnableDistribProbTypeOption:=", False,
				"Enabled:="		, True,
				[
					"NAME:CGDataBlock",
					"MaxPass:="		, 10,
					"MinPass:="		, 1,
					"MinConvPass:="		, 1,
					"PerError:="		, 1,
					"PerRefine:="		, 30,
					"DataType:="		, "CG",
					"Included:="		, True,
					"UseParamConv:="	, False,
					"UseLossyParamConv:="	, False,
					"PerErrorParamConv:="	, 1,
					"UseLossConv:="		, True
				],
				[
					"NAME:RLDataBlock",
					"MaxPass:="		, 10,
					"MinPass:="		, 1,
					"MinConvPass:="		, 1,
					"PerError:="		, 1,
					"PerRefine:="		, 30,
					"DataType:="		, "RL",
					"Included:="		, True,
					"UseParamConv:="	, False,
					"UseLossyParamConv:="	, False,
					"PerErrorParamConv:="	, 1,
					"UseLossConv:="		, True
				]
			])	

		#################################################
		# Insert either Discrete or Interpolating Sweep #
		#################################################

		if freqsweeptype == 'none':
			pass
		
		if freqsweeptype == 'Discrete':
			oModule.InsertSweep("Setup1", 
				[
					"NAME:Discrete_Sweep",
					"IsEnabled:="		, True,
					"SetupType:="		, "LinearStep",
					"StartValue:="		, str(solutionstartfreq) + StartFrequnits,
					"StopValue:="		, str(solutionstopfreq) + StopFrequnits,
					"StepSize:="		, str(solutionstepfreq) + FreqStepunits,
					"Type:="		, "Discrete",
					"SaveFields:="		, False,
					"ExtrapToDC:="		, False
				])

		if freqsweeptype == 'Interpolating':
			oModule.InsertSweep("Setup1", 
				[
					"NAME:Interpolating_Sweep",
					"IsEnabled:="		, True,
					"SetupType:="		, "LinearStep",
					"StartValue:="		, str(solutionstartfreq) + StartFrequnits,
					"StopValue:="		, str(solutionstopfreq) + StopFrequnits,
					"StepSize:="		, str(solutionstepfreq) + FreqStepunits,
					"Type:="		, "Interpolating",
					"SaveFields:="		, False,
					"InterpTolerance:="	, 0.5,
					"InterpMaxSolns:="	, 50,
					"InterpMinSolns:="	, 0,
					"InterpMinSubranges:="	, 1,
					"ExtrapToDC:="		, True,
					"MinSolvedFreq:="	, "100000"
				])
				





                ############################################
                # Draw Grounded Coplanar Waveguides Class  #
#####################################################################################################################################################################################################
class DrawGCPW(object):
    def __init__(self,oProject,oEditor,oDesign,units,tracespacing,toptracewidth,
            bottomtracewidth,maxtracewidth,numberoftraces,diffspacing,planethickness,topdielectricthickness,D5thickness,bottomdielectricthickness,
            tracethickness,tracewidth,etching,roughnesstype,surfaceroughnesstop,surfaceroughnesssides,surfaceroughnessbottom,
            surfaceroughnessunits,HHsurfaceratiotop,noduleradiustop,HHsurfaceratiosides,noduleradiussides,HHsurfaceratiobottom,
            noduleradiusbottom,plating,useplatingmaterial,platingmaterial,platingthickness,platingthicknessunits,soldermaskmaterial,
            soldermaskthickness,soldermaskunits,solutionfreq,solutionstartfreq,solutionstopfreq,solutionstepfreq,Solutionfrequnits,StartFrequnits,
            StopFrequnits,FreqStepunits,freqsweeptype,SMdielectricfreq,SMdielectricfrequnits,SMEr,SMTand,Bdielfreq,Bdielectricfrequnits,
            BdielEr,BdielTand,Tdielfreq,Tdielfrequnits,TdielEr,TdielTand,D4dielfreq,D4dielfrequnits,D4dielEr,D4dielTand,D5dielfreq,D5dielfrequnits,
            D5dielEr,D5dielTand,formated_Datetime_string,gndwidth):        
                
                
        traceoffset = 0
        
        
        logger = logging.getLogger('TLine.MainForm.DesignSelect')
        logger.info('Grounded Coplanar Waveguide Design Created!')


        #Handling etching
        
        if toptracewidth > bottomtracewidth:
            etchsidetracewidth = bottomtracewidth
            
        if    toptracewidth < bottomtracewidth:
            etchsidetracewidth = toptracewidth
            
        if    toptracewidth == bottomtracewidth:
            etchsidetracewidth = toptracewidth
            
		#Calculate Conductor Thickness even if etched
        a = float(toptracewidth)
        b = float(bottomtracewidth)
        c = float(tracethickness)
        x = 0 #triangle base lenght
        Y = 0 #trace sides length

        #triangle base length.
        if a > b:
            x = (a-b)/2
        if a < b:
            x = (b-a)/2

        if a == b:
            y = tracethickness

        else:
                y = math.sqrt(c*c + x*x)

        trace_perimeter = float(toptracewidth) + float(bottomtracewidth) + 2*float(y)
        Area_trapdzoid = ((float(toptracewidth) + float(bottomtracewidth)) / 2.0) * float(tracethickness)
        conductor_thickness = float(Area_trapdzoid) / float(trace_perimeter)
            
        utc_datetime = datetime.datetime.utcnow()
        formated_Datetime_string = utc_datetime.strftime("%B%d%H%M%S")
        
        
        count2 = 0          #local variable to count by 2's for trace and gnd algorithm
        tracecount = 0        #local variable counter for trace and gnd algorithm
        


        oEditor.SetModelUnits(
                [
                    "NAME:Units",
                    "Units:="        , units,
                    "Rescale:="        , False
                ])
        
        ####################################################################
        # adding variables to project to that its parameterized            #
        ##############################################################################################################################
        
        
        
        oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:LocalVariableTab",
                    [
                        "NAME:PropServers", 
                        "LocalVariables"
                    ],
                    [
                        "NAME:NewProps",
                        [
                            "NAME:soldermaskthickness",
                            "PropType:="        , "VariableProp",
                            "UserDef:="        , True,
                            "Value:="        , str(soldermaskthickness) + soldermaskunits
                        ],
                        [
                            "NAME:bottomdielectricthickness",
                            "PropType:="        , "VariableProp",
                            "UserDef:="        , True,
                            "Value:="        , str(bottomdielectricthickness) + units
                        ]                            
                    ]
                ]
            ])    
        
        
        
        if roughnesstype ==  1:        
            oDesign.ChangeProperty(
                [
                    "NAME:AllTabs",
                    [
                        "NAME:LocalVariableTab",
                        [
                            "NAME:PropServers", 
                            "LocalVariables"
                        ],
                        [
                            "NAME:NewProps",
                            [
                                "NAME:platingthickness",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(platingthickness) + platingthicknessunits
                            ],    
                            [
                                "NAME:surfaceroughnesstop",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(surfaceroughnesstop) + surfaceroughnessunits
                            ],
                            [
                                "NAME:surfaceroughnesssides",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(surfaceroughnesssides) + surfaceroughnessunits
                            ],        
                            [
                                "NAME:surfaceroughnessbottom",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(surfaceroughnessbottom) + surfaceroughnessunits
                            ]                        
                        ]
                    ]
                ])        
        
        
        if roughnesstype ==  2:    
            oDesign.ChangeProperty(
                [
                    "NAME:AllTabs",
                    [
                        "NAME:LocalVariableTab",
                        [
                            "NAME:PropServers", 
                            "LocalVariables"
                        ],
                        [
                            "NAME:NewProps",
                            [
                                "NAME:platingthickness",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(platingthickness) + platingthicknessunits
                            ],    
                            [
                                "NAME:noduleradiustop",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(noduleradiustop) + surfaceroughnessunits
                            ],    
                            [
                                "NAME:noduleradiussides",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(noduleradiussides) + surfaceroughnessunits
                            ],    
                            [
                                "NAME:noduleradiusbottom",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(noduleradiusbottom) + surfaceroughnessunits
                            ],    
                            [
                                "NAME:HHsurfaceratiotop",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(HHsurfaceratiotop)
                            ],
                            [
                                "NAME:HHsurfaceratiosides",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(HHsurfaceratiosides)
                            ],
                            [
                                "NAME:HHsurfaceratiobottom",
                                "PropType:="        , "VariableProp",
                                "UserDef:="        , True,
                                "Value:="        , str(HHsurfaceratiobottom)
                            ]                        
                        ]
                    ]
                ])        
        
        
        
        oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:LocalVariableTab",
                    [
                        "NAME:PropServers", 
                        "LocalVariables"
                    ],
                    [
                        "NAME:NewProps",
                        [
                            "NAME:tracespacing",
                            "PropType:="        , "VariableProp",
                            "UserDef:="        , True,
                            "Value:="        , str(tracespacing) + units
                        ],                        
                        [
                            "NAME:toptracewidth",
                            "PropType:="        , "VariableProp",
                            "UserDef:="        , True,
                            "Value:="        , str(toptracewidth) + units
                        ],    
                        [
                            "NAME:gndwidth",
                            "PropType:="        , "VariableProp",
                            "UserDef:="        , True,
                            "Value:="        , str(gndwidth) + units
                        ],                
                        [
                            "NAME:planethickness",
                            "PropType:="        , "VariableProp",
                            "UserDef:="        , True,
                            "Value:="        , str(planethickness) + units
                        ],
                        [
                            "NAME:tracethickness",
                            "PropType:="        , "VariableProp",
                            "UserDef:="        , True,
                            "Value:="        , str(tracethickness) + units
                        ]                
                    ]
                ]
            ])
        
        #############################################
        # main loop, looping through trace drawing  #
        ################################################################################################################################
        tracecount = 1
        count2 = 2
        while tracecount <=numberoftraces:
        
            #Create traces
            oEditor.CreatePolyline(
            [
                "NAME:Trace",
                "IsPolylineCovered:="    , True,
                "IsPolylineClosed:="    , True,
                [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-1)+"*(tracespacing)+"+str(tracecount-1)+"*("+str(bottomtracewidth)+units+"+gndwidth)+0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                    "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                    "Z:="            , "0" + units
                ],
                [
                    "NAME:PLPoint",
                    "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-1)+"*(tracespacing)+"+str(tracecount-1)+"*("+str(bottomtracewidth)+units+"+gndwidth)+toptracewidth+0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                    "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                    "Z:="            , "0" + units
                ],
                [
                    "NAME:PLPoint",
                    "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-1)+"*(tracespacing)+"+str(tracecount-1)+"*("+str(bottomtracewidth)+units+"+gndwidth)+"+str(bottomtracewidth)+units+"",
                    "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"-0.5*tracethickness",
                    "Z:="            , "0" + units
                ],
                [
                    "NAME:PLPoint",
                    "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-1)+"*(tracespacing)+"+str(tracecount-1)+"*("+str(bottomtracewidth)+units+"+gndwidth)",
                    "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"-0.5*tracethickness",
                    "Z:="            , "0" + units
                ],
                [
                    "NAME:PLPoint",
                    "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-1)+"*(tracespacing)+"+str(tracecount-1)+"*("+str(bottomtracewidth)+units+"+gndwidth)+0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                    "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                    "Z:="            , "0" + units
                ]
            ],
                [
                    "NAME:PolylineSegments",
                    [
                        "NAME:PLSegment",
                        "SegmentType:="        , "Line",
                        "StartIndex:="        , 0,
                        "NoOfPoints:="        , 2
                    ],
                    [
                        "NAME:PLSegment",
                        "SegmentType:="        , "Line",
                        "StartIndex:="        , 1,
                        "NoOfPoints:="        , 2
                    ],
                    [
                        "NAME:PLSegment",
                        "SegmentType:="        , "Line",
                        "StartIndex:="        , 2,
                        "NoOfPoints:="        , 2
                    ],
                    [
                        "NAME:PLSegment",
                        "SegmentType:="        , "Line",
                        "StartIndex:="        , 3,
                        "NoOfPoints:="        , 2
                    ]
                ],
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
                "Name:="        , "Trace"+str(tracecount),
                "Flags:="        , "",
                "Color:="        , "(132 132 193)",
                "Transparency:="    , 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="        , "",
                "MaterialValue:="    , "\"copper\"",
                "SolveInside:="        , False
            ])
        
            #########################
            # Assign signal sources #
            #########################
            oModule = oDesign.GetModule("BoundarySetup")
            oModule.AssignSingleSignalLine(
                [
                    "NAME:"+"Trace"+str(tracecount),
                    "Objects:="        , ["Trace"+str(tracecount)],
                    "SolveOption:="        , "Automatic",
                    "Thickness:="        , str(conductor_thickness) + units
                ])
        
            tracecount +=1
            count2 +=2    
                    
            
            
        tracecount = 1
        count2 = 2
        while tracecount <=numberoftraces:    
            
            #Create first ground trace
            if count2 ==2:
        
                oEditor.CreatePolyline(
                [
                    "NAME:Trace",
                    "IsPolylineCovered:="    , True,
                    "IsPolylineClosed:="    , True,
                    [
                    "NAME:PolylinePoints",
                    [
                        "NAME:PLPoint",
                        "X:="            , "0",
                        "Y:="            , "((planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness)",
                        "Z:="            , "0" + units
                    ],
                    [
                        "NAME:PLPoint",
                        "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")-0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                        "Y:="            , "((planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness)",
                        "Z:="            , "0" + units
                    ],
                    [
                        "NAME:PLPoint",
                        "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")",    
                        "Y:="            , "((planethickness+bottomdielectricthickness+0.5*tracethickness)-0.5*tracethickness)",
                        "Z:="            , "0" + units
                    ],
                    [
                        "NAME:PLPoint",
                        "X:="            , "0",
                        "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")",
                        "Z:="            , "0" + units
                    ],
                    [
                        "NAME:PLPoint",
                        "X:="            , "0",
                        "Y:="            , "((planethickness+bottomdielectricthickness+0.5*tracethickness)+0.5*tracethickness)",
                        "Z:="            , "0" + units
                    ]
                ],
                    [
                        "NAME:PolylineSegments",
                        [
                            "NAME:PLSegment",
                            "SegmentType:="        , "Line",
                            "StartIndex:="        , 0,
                            "NoOfPoints:="        , 2
                        ],
                        [
                            "NAME:PLSegment",
                            "SegmentType:="        , "Line",
                            "StartIndex:="        , 1,
                            "NoOfPoints:="        , 2
                        ],
                        [
                            "NAME:PLSegment",
                            "SegmentType:="        , "Line",
                            "StartIndex:="        , 2,
                            "NoOfPoints:="        , 2
                        ],
                        [
                            "NAME:PLSegment",
                            "SegmentType:="        , "Line",
                            "StartIndex:="        , 3,
                            "NoOfPoints:="        , 2
                        ]
                    ],
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
                    "Name:="        , "GroundTrace"+str(tracecount),
                    "Flags:="        , "",
                    "Color:="        , "(132 132 193)",
                    "Transparency:="    , 0,
                    "PartCoordinateSystem:=", "Global",
                    "UDMId:="        , "",
                    "MaterialValue:="    , "\"copper\"",
                    "SolveInside:="        , False
                ])
            
        
            if tracecount >=2:
                # #Create Ground Traces N+1
                oEditor.CreatePolyline(
                    [
                     "NAME:Trace",
                     "IsPolylineCovered:="    , True,
                     "IsPolylineClosed:="    , True,
                     [
                     "NAME:PolylinePoints",
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth+0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                         "Z:="            , "0" + units
                     ],
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth+gndwidth-0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                         "Z:="            , "0" + units
                     ],
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth+gndwidth",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"-0.5*tracethickness",
                         "Z:="            , "0" + units
                     ],
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"-0.5*tracethickness",
                         "Z:="            , "0" + units
                     ],
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth+0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                         "Z:="            , "0" + units
                     ]
                 ],
                     [
                         "NAME:PolylineSegments",
                         [
                             "NAME:PLSegment",
                             "SegmentType:="        , "Line",
                             "StartIndex:="        , 0,
                             "NoOfPoints:="        , 2
                         ],
                         [
                             "NAME:PLSegment",
                             "SegmentType:="        , "Line",
                             "StartIndex:="        , 1,
                             "NoOfPoints:="        , 2
                         ],
                         [
                             "NAME:PLSegment",
                             "SegmentType:="        , "Line",
                             "StartIndex:="        , 2,
                             "NoOfPoints:="        , 2
                         ],
                         [
                             "NAME:PLSegment",
                             "SegmentType:="        , "Line",
                             "StartIndex:="        , 3,
                             "NoOfPoints:="        , 2
                         ]
                     ],
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
                     "Name:="        , "GroundTrace"+str(tracecount),
                     "Flags:="        , "",
                     "Color:="        , "(132 132 193)",
                     "Transparency:="    , 0,
                     "PartCoordinateSystem:=", "Global",
                     "UDMId:="        , "",
                     "MaterialValue:="    , "\"copper\"",
                     "SolveInside:="        , False
                 ])
            
            
            if tracecount == numberoftraces:    
                tracecount +=1
                count2 +=2    
                #Create End Ground Trace
                oEditor.CreatePolyline(
                    [
                     "NAME:Trace",
                     "IsPolylineCovered:="    , True,
                     "IsPolylineClosed:="    , True,
                     [
                     "NAME:PolylinePoints",
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth+0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                         "Z:="            , "0" + units
                     ],
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth+4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                         "Z:="            , "0" + units
                     ],
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth+4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"-0.5*tracethickness",
                         "Z:="            , "0" + units
                     ],
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"-0.5*tracethickness",
                         "Z:="            , "0" + units
                     ],
                     [
                         "NAME:PLPoint",
                         "X:="            , "4.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(count2-2)+"*tracespacing+"+str(tracecount-1)+"*"+str(bottomtracewidth)+units+"+"+str(tracecount-2)+"*gndwidth+0.5*("+str(bottomtracewidth)+units+"-toptracewidth)",
                         "Y:="            , "(planethickness+bottomdielectricthickness+0.5*tracethickness)"+"+0.5*tracethickness",
                         "Z:="            , "0" + units
                     ]
                 ],
                     [
                         "NAME:PolylineSegments",
                         [
                             "NAME:PLSegment",
                             "SegmentType:="        , "Line",
                             "StartIndex:="        , 0,
                             "NoOfPoints:="        , 2
                         ],
                         [
                             "NAME:PLSegment",
                             "SegmentType:="        , "Line",
                             "StartIndex:="        , 1,
                             "NoOfPoints:="        , 2
                         ],
                         [
                             "NAME:PLSegment",
                             "SegmentType:="        , "Line",
                             "StartIndex:="        , 2,
                             "NoOfPoints:="        , 2
                         ],
                         [
                             "NAME:PLSegment",
                             "SegmentType:="        , "Line",
                             "StartIndex:="        , 3,
                             "NoOfPoints:="        , 2
                         ]
                     ],
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
                     "Name:="        , "GroundTrace"+str(tracecount),
                     "Flags:="        , "",
                     "Color:="        , "(132 132 193)",
                     "Transparency:="    , 0,
                     "PartCoordinateSystem:=", "Global",
                     "UDMId:="        , "",
                     "MaterialValue:="    , "\"copper\"",
                     "SolveInside:="        , False
                 ])        
                
            
                
            tracecount +=1
            count2 +=2    
                
                
                
            
        
        ###########################################################################################        
        #  Adding surface roughness to traces and plating for top and sides of traces if selected#    
        ###################################################################################################################################################################
        counter = 0           #reset counter    
        tracecount = 1        #reset tracecount        
        #loop to assign finite conductivity to traces:  Hammerstadt-Jensen
        if roughnesstype ==1:
            counter = 0    #lines for assigning roughness shift by 12 for each trace do top of trace 1 = 7, top trace 2 = 19 
        
            while tracecount<=numberoftraces:
                #top Hammerstadt roughness
                oModule = oDesign.GetModule("BoundarySetup")
                oModule.AssignFiniteCond(
                    [
                        "NAME:"+"RoughnessTopTrace"+str(tracecount),
                        "Edges:="        , [7+counter],
                        "UseCoating:="        , plating,
                        "LayerThickness:="    , "platingthickness",
                        "UseMaterial:="        , useplatingmaterial,
                        "Material:="        , "copper",                
                        "Roughness:="        , "surfaceroughnesstop"
                    ])
        
                #sides Hammerstadt roughness
                oModule = oDesign.GetModule("BoundarySetup")
                oModule.AssignFiniteCond(
                    [
                        "NAME:"+"RoughnessSidesTrace"+str(tracecount),
                        "Edges:="        , [8+counter,10+counter],
                        "UseCoating:="        , plating,
                        "LayerThickness:="    , "platingthickness",
                        "UseMaterial:="        , useplatingmaterial,
                        "Material:="        , platingmaterial,                
                        "Roughness:="        , "surfaceroughnesssides"
                    ])
                
                #bottom Hammerstadt roughness
                oModule = oDesign.GetModule("BoundarySetup")
                oModule.AssignFiniteCond(
                    [
                        "NAME:"+"RoughnessBottomTrace"+str(tracecount),
                        "Edges:="            , [9+counter],
                        "UseCoating:="        , False,            
                        "Roughness:="        , "surfaceroughnessbottom"
                    ])
        
                counter +=12
                tracecount +=1
                
        counter = 0           #reset counter    
        tracecount = 1        #reset tracecount
                
        #loop to assign finite conductivity to traces:  Huray
        if roughnesstype ==2:
            counter = 0    #lines for assigning roughness shift by 12 for each trace do top of trace 1 = 7, top trace 2 = 19 
            
            while tracecount<=numberoftraces:
                #top Hall-Huray Method
                oModule = oDesign.GetModule("BoundarySetup")
                oModule.AssignFiniteCond(
                    [
                        "NAME:"+"RoughnessTopTrace"+str(tracecount),
                        "Edges:="        , [7+counter],
                        "UseCoating:="        , plating,
                        "LayerThickness:="    , "platingthickness",
                        "UseMaterial:="        , useplatingmaterial,
                        "Material:="        , platingmaterial,                
                        "Radius:="        , "noduleradiustop",
                        "Ratio:="        , "HHsurfaceratiotop"
                    ])
        
                #sides Hall-Huray Method
                oModule = oDesign.GetModule("BoundarySetup")
                oModule.AssignFiniteCond(
                    [
                        "NAME:"+"RoughnessSidesTrace"+str(tracecount),
                        "Edges:="        , [8+counter,10+counter],
                        "UseCoating:="        , plating,
                        "LayerThickness:="    , "platingthickness",
                        "UseMaterial:="        , useplatingmaterial,
                        "Material:="        , platingmaterial,                
                        "Radius:="        , "noduleradiussides",
                        "Ratio:="        , "HHsurfaceratiosides"
        
                    ])
                
                #bottom Hall-Huray Method
                oModule = oDesign.GetModule("BoundarySetup")
                oModule.AssignFiniteCond(
                    [
                        "NAME:"+"RoughnessBottomTrace"+str(tracecount),
                        "Edges:="        , [9+counter],
                        "UseCoating:="        , False,
                        "Radius:="        , "noduleradiusbottom",
                        "Ratio:="        , "HHsurfaceratiobottom"
        
                    ])
        
                counter += 12
                tracecount +=1
                
        counter = 0           #reset counter    
        tracecount = 1        #reset tracecount        
        
        
        
        ##########################################################################################################        
        #creating Djorjdevic-Sarkar fitted soldermask material and bottom dielectric material if microstrip = 1  #
        #########################################################################################################################################    
    
            #Constants
        pi = math.pi
        Freq_B = 1e12/(2*pi)
        cond_DC = 1e-12
        Eo = 8.854e-12
        
        ###------------------Soldermask Fit----------------####    
    
        #inputs from user
        solnfreq = float(SMdielectricfreq)
        solnEr = float(SMEr)
        solnTand = float(SMTand)
            
        #Djorjdevic-Sarkar Equations
        K = ((solnEr*solnTand)-(cond_DC/(2*pi*Eo*solnfreq)))/((pi/2)-math.atan(solnfreq/Freq_B))        
        E_inf = solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(solnfreq*solnfreq)))/solnfreq)        
        delta_E = 10*solnTand*E_inf
        Freq_A = Freq_B/math.exp(delta_E/K)
            
    #        oProject.InsertDesign("2D Extractor", designtype+"_"+"Created"+"_"+formated_Datetime_string+"_"+"UTC", "", "")
        
        oDefinitionManager = oProject.GetDefinitionManager()
        oDefinitionManager.AddMaterial(
            [
        
        
                "NAME:Soldermask"+"_"+formated_Datetime_string,
    
                "CoordinateSystemType:=", "Cartesian",
                [
                    "NAME:AttachedData"
                ],
                [
                    "NAME:ModifierData"
                ],
                "permittivity:="    , str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
                "conductivity:="    , str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
                "dielectric_loss_tangent:=", "0",
                "magnetic_loss_tangent:=", "0"
            ])
                
        ##-------------Bottom Dielectric Fit--------------------###
        
        
        #inputs from user
        solnfreq = float(Bdielfreq)
        solnEr = float(BdielEr)
        solnTand = float(BdielTand)
            
        #Djorjdevic-Sarkar Equations
        K = ((solnEr*solnTand)-(cond_DC/(2*pi*Eo*solnfreq)))/((pi/2)-math.atan(solnfreq/Freq_B))        
        E_inf = solnEr-K*math.log((math.sqrt((Freq_B*Freq_B)+(solnfreq*solnfreq)))/solnfreq)        
        delta_E = 10*solnTand*E_inf
        Freq_A = Freq_B/math.exp(delta_E/K)
            
            
        
        oDefinitionManager.AddMaterial(
            [
                "NAME:BottomDielectric"+"_"+formated_Datetime_string,
                "CoordinateSystemType:=", "Cartesian",
                [
                    "NAME:AttachedData"
                ],
                [
                    "NAME:ModifierData"
                ],
                "permittivity:="    , str(E_inf)+"+("+str(K)+"/2)*ln(("+str(Freq_B*Freq_B)+"+Freq*Freq)/("+str(Freq_A*Freq_A)+"+Freq*Freq))",
                "conductivity:="    , str(cond_DC)+"+"+str(2*pi*Eo*K)+"*"+"Freq"+"*("+"atan(Freq/"+str(Freq_A)+")-"+"atan(Freq/"+str(Freq_B)+"))",
                "dielectric_loss_tangent:=", "0",
                "magnetic_loss_tangent:=", "0"
            ])
        
        
        bottomdielectricmaterial = "\"BottomDielectric"+"_"+formated_Datetime_string+"\""
        soldermaskmaterial = "\"Soldermask"+"_"+formated_Datetime_string+"\""
        
        
        
        
        
                
        
                
        ##################################################################
        # drawing dielectrics and reference planes for single ended      #
        # transmission lines                                             #
        #############################################################################################################################################################################################################

        #######################
        # Create Ground Plane #
        #######################
        oEditor.CreateRectangle(
            [
                "NAME:RectangleParameters",
                "IsCovered:="        , True,
                "XStart:="        , "0mil",
                "YStart:="        , "0mil",
                "ZStart:="        , "0mil",
                "Width:="        , "8.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(2*numberoftraces)+"*tracespacing+"+str(numberoftraces)+"*"+str(bottomtracewidth)+units+"+"+str(numberoftraces-1)+"*gndwidth",
                "Height:="        , "planethickness",
                "WhichAxis:="        , "Z"
            ], 
            [
                "NAME:Attributes",
                "Name:="        , "Ground_Plane",
                "Flags:="        , "",
                "Color:="        , "(132 132 193)",
                "Transparency:="    , 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="        , "",
                "MaterialValue:="    , "\"copper\"",
                "SolveInside:="        , False
            ])
        
        ################################################
        #Assign port to Ground Plane and Ground Traces #
        ################################################
        tracecount = 1
        gnd_ref_list = (numberoftraces+2)*[""]
        gnd_ref_list[0] = "Ground_Plane"        

        while tracecount <= numberoftraces+1:
            gnd_ref_list[tracecount] = "GroundTrace" + str(tracecount)
            tracecount +=1
        tracecount = 1           
        
        oModule = oDesign.GetModule("BoundarySetup")
        oModule.AssignSingleReferenceGround(
        	[
        		"NAME:Reference_Planes",
        		"Objects:="		,  gnd_ref_list,
        		"SolveOption:="		, "Automatic",
        		"Thickness:="		, str(conductor_thickness) + units
        	])	
            
 
            
        ###########################
        #Create Bottom Dielectric #
        ###########################
        oEditor.CreateRectangle(
            [
                "NAME:RectangleParameters",
                "IsCovered:="        , True,
                "XStart:="        , "0mil",
                "YStart:="        , "planethickness",
                "ZStart:="        , "0mil",
                "Width:="        , "8.0*(bottomdielectricthickness+"+str(maxtracewidth)+units+")+"+str(2*numberoftraces)+"*tracespacing+"+str(numberoftraces)+"*"+str(bottomtracewidth)+units+"+"+str(numberoftraces-1)+"*gndwidth",
                "Height:="        , "bottomdielectricthickness",
                "WhichAxis:="        , "Z"
            ], 
            [
                "NAME:Attributes",
                "Name:="        , "Dielectric_Bottom",
                "Flags:="        , "",
                "Color:="        , "(253 165 2)",
                "Transparency:="    , 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="        , "",
                "MaterialValue:="    , bottomdielectricmaterial,
                "SolveInside:="        , False
            ])    
        
        
        #######################      
        #creating soldermask  #
        #########################################################################################################################################        
        

        ########################################################
        #selects traces and bottom dielectric and makes copies #
        ########################################################
        while tracecount <= numberoftraces:
            oEditor.Copy(
                [
                    "NAME:Selections",
                    "Selections:="        , "Trace"+str(tracecount)
                ])
            oEditor.Paste()    
            tracecount +=1
        tracecount = 1
        
        while tracecount <= numberoftraces+1:
            oEditor.Copy(
                [
                    "NAME:Selections",
                    "Selections:="        , "GroundTrace"+str(tracecount)
                ])            
            oEditor.Paste()
            tracecount +=1
            
            
        oEditor.Copy(
            [
                "NAME:Selections",
                "Selections:="        , "Dielectric_Bottom"
            ])
            
        oEditor.Paste()    
        tracecount = 1
    
        ###########################################################################################################################
        #selects top and side edges of trace and Dielectric_Bottom op edge and move vertically the distance = soldemask thickness #
        ###########################################################################################################################
    
        edgecounter = 2*numberoftraces+1
        egdenumber1 = 0  
        egdenumber2 = 0 
        egdenumber3 = 0    
        Gegdenumber1 = 0  
        Gegdenumber2 = 0 
        Gegdenumber3 = 0        
        dielectricedge = 0
        
        if numberoftraces == 1:
            egdenumber1 = 67 
            egdenumber2 = 68
            egdenumber3 = 70
            Gegdenumber1 = 79  
            Gegdenumber2 = 80
            Gegdenumber3 = 82        
            dielectricedge = 105
        else: 
            egdenumber1 = 43 + (2*numberoftraces)*12  
            egdenumber2 = 44 + (2*numberoftraces)*12 
            egdenumber3 = 46 + (2*numberoftraces)*12    
            Gegdenumber1 = 43 + (3*numberoftraces)*12  
            Gegdenumber2 = 44 + (3*numberoftraces)*12 
            Gegdenumber3 = 46 + (3*numberoftraces)*12        
            dielectricedge = 57    + (2*numberoftraces)*24
                
        shift = 0
        
        while tracecount <= numberoftraces:
            oEditor.MoveEdges(
                [
                    "NAME:Selections",
                    "Selections:="        , "Trace"+str(tracecount+numberoftraces),
                    "NewPartsModelFlag:="    , "Model"
                ], 
                [
                    "NAME:Parameters",
                    [
                        "NAME:MoveEdgesParameters",
                        "MoveAlongNormalFlag:="    , True,
                        "OffsetDistance:="    , "soldermaskthickness",
                        "MoveVectorX:="        , "0mil",
                        "MoveVectorY:="        , "0mil",
                        "MoveVectorZ:="        , "0mil",
                        "EdgesToMove:="        , [egdenumber1+shift,egdenumber2+shift,egdenumber3+shift]
                    ]
                ])
            tracecount +=1
            shift +=12
        
        tracecount = 1
        shift = 0
        
        while tracecount <= numberoftraces+1:
            #handles first ground trace copy
            if tracecount == 1:
                oEditor.MoveEdges(
                    [
                        "NAME:Selections",
                        "Selections:="        , "GroundTrace"+str(tracecount+numberoftraces+1),
                        "NewPartsModelFlag:="    , "Model"
                    ], 
                    [
                        "NAME:Parameters",
                        [
                            "NAME:MoveEdgesParameters",
                            "MoveAlongNormalFlag:="    , True,
                            "OffsetDistance:="    , "soldermaskthickness",
                            "MoveVectorX:="        , "0mil",
                            "MoveVectorY:="        , "0mil",
                            "MoveVectorZ:="        , "0mil",
                            "EdgesToMove:="        , [Gegdenumber1+shift,Gegdenumber2+shift]
                        ]
                    ])
                tracecount +=1
                shift +=12
            #handles last ground trace copy
            if tracecount == numberoftraces+1:
                oEditor.MoveEdges(
                    [
                        "NAME:Selections",
                        "Selections:="        , "GroundTrace"+str(tracecount+numberoftraces+1),
                        "NewPartsModelFlag:="    , "Model"
                    ], 
                    [
                        "NAME:Parameters",
                        [
                            "NAME:MoveEdgesParameters",
                            "MoveAlongNormalFlag:="    , True,
                            "OffsetDistance:="    , "soldermaskthickness",
                            "MoveVectorX:="        , "0mil",
                            "MoveVectorY:="        , "0mil",
                            "MoveVectorZ:="        , "0mil",
                            "EdgesToMove:="        , [Gegdenumber1+shift,Gegdenumber3+shift]
                        ]
                    ])
                tracecount +=1
                shift +=12
                
            else:  #handles all other ground trace copies under main while loop
                oEditor.MoveEdges(
                    [
                        "NAME:Selections",
                        "Selections:="        , "GroundTrace"+str(tracecount+numberoftraces+1),
                        "NewPartsModelFlag:="    , "Model"
                    ], 
                    [
                        "NAME:Parameters",
                        [
                            "NAME:MoveEdgesParameters",
                            "MoveAlongNormalFlag:="    , True,
                            "OffsetDistance:="    , "soldermaskthickness",
                            "MoveVectorX:="        , "0mil",
                            "MoveVectorY:="        , "0mil",
                            "MoveVectorZ:="        , "0mil",
                            "EdgesToMove:="        , [Gegdenumber1+shift,Gegdenumber2+shift,Gegdenumber3+shift]
                        ]
                    ])
                tracecount +=1
                shift +=12
                
            
            
        tracecount = 1
        shift = 0
    
            
        oEditor.MoveEdges(
            [
                "NAME:Selections",
                "Selections:="        , "Dielectric_Bottom1",
                "NewPartsModelFlag:="    , "Model"
            ], 
            [
                "NAME:Parameters",
                [
                    "NAME:MoveEdgesParameters",
                    "MoveAlongNormalFlag:="    , True,
                    "OffsetDistance:="    , "soldermaskthickness",
                    "MoveVectorX:="        , "0mil",
                    "MoveVectorY:="        , "0mil",
                    "MoveVectorZ:="        , "0mil",
                    "EdgesToMove:="        , [dielectricedge]
                ]
            ])    
            
        #############################################################################    
        #booleon unite all copies and subtract from origional traces and dielectric #
        #the left over is the soldermask layer                                      #
        #############################################################################
        unitestring = ''
    
        while tracecount <= numberoftraces:
            unitestring = unitestring +","+ "Trace" + str(numberoftraces+tracecount)
            tracecount +=1
        tracecount = 1
            
        while tracecount <= numberoftraces+1:
            unitestring = unitestring +","+ "GroundTrace" + str(numberoftraces+tracecount+1)
            tracecount +=1
        tracecount = 1        
            
        oEditor.Unite(
            [
                "NAME:Selections",
                "Selections:="        , "Dielectric_Bottom1"+unitestring
            ], 
            [
                "NAME:UniteParameters",
                "KeepOriginals:="    , False
            ])
            
            
        #####################################################    
        #Assign material properties to soldermask material  #
        #####################################################    
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers", 
                        "Dielectric_Bottom1"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Material",
                            "Value:="        , soldermaskmaterial
                        ]
                    ]
                ]
            ])    
            
    
        #####################################################    
        #Change name from Dielectric_Bottom1 to Soldermask  #
        #####################################################    
        oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers", 
                        "Dielectric_Bottom1"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Name",
                            "Value:="        , "SolderMask"
                        ],
                        [
                            "NAME:Color",
                            "R:="            , 0,
                            "G:="            , 255,
                            "B:="            , 0
                        ]
                    ]
                ]
            ])    
            
            
        #########################################################    
        #subtract soldermask object from traces and dielectric  #
        #to create thin layer above traces                      #            
        #########################################################
        toolstring = ''
        
        tracecount = 1

        while tracecount <= numberoftraces:
            toolstring = toolstring +","+ "Trace" + str(tracecount)
            tracecount +=1
        tracecount = 1

        while tracecount <= numberoftraces+1:
            toolstring = toolstring +","+ "GroundTrace" + str(tracecount)
            tracecount +=1
        tracecount = 1 

        oEditor.Subtract(
            [
                "NAME:Selections",
                "Blank Parts:="        , "SolderMask",
                "Tool Parts:="        , "Dielectric_Bottom" + toolstring
            ], 
            [
                "NAME:SubtractParameters",
                "KeepOriginals:="    , True
            ])    
    

        #################################
        #   Insert Solution Frequency      #
        #################################    
        
        oModule = oDesign.GetModule("AnalysisSetup")
        oModule.InsertSetup("2DMatrix", 
            [
                "NAME:Setup1",
                "AdaptiveFreq:="    , str(solutionfreq) + Solutionfrequnits,
                "EnableDistribProbTypeOption:=", False,
                "Enabled:="        , True,
                [
                    "NAME:CGDataBlock",
                    "MaxPass:="        , 10,
                    "MinPass:="        , 1,
                    "MinConvPass:="        , 1,
                    "PerError:="        , 1,
                    "PerRefine:="        , 30,
                    "DataType:="        , "CG",
                    "Included:="        , True,
                    "UseParamConv:="    , False,
                    "UseLossyParamConv:="    , False,
                    "PerErrorParamConv:="    , 1,
                    "UseLossConv:="        , True
                ],
                [
                    "NAME:RLDataBlock",
                    "MaxPass:="        , 10,
                    "MinPass:="        , 1,
                    "MinConvPass:="        , 1,
                    "PerError:="        , 1,
                    "PerRefine:="        , 30,
                    "DataType:="        , "RL",
                    "Included:="        , True,
                    "UseParamConv:="    , False,
                    "UseLossyParamConv:="    , False,
                    "PerErrorParamConv:="    , 1,
                    "UseLossConv:="        , True
                ]
            ])    
        
        #################################################
        # Insert either Discrete or Interpolating Sweep #
        #################################################
        
        if freqsweeptype == 'none':
            pass
        
        if freqsweeptype == 'Discrete':
            oModule.InsertSweep("Setup1", 
                [
                    "NAME:Discrete_Sweep",
                    "IsEnabled:="        , True,
                    "SetupType:="        , "LinearStep",
                    "StartValue:="        , str(solutionstartfreq) + StartFrequnits,
                    "StopValue:="        , str(solutionstopfreq) + StopFrequnits,
                    "StepSize:="        , str(solutionstepfreq) + FreqStepunits,
                    "Type:="        , "Discrete",
                    "SaveFields:="        , False,
                    "ExtrapToDC:="        , False
                ])
        
        if freqsweeptype == 'Interpolating':
            oModule.InsertSweep("Setup1", 
                [
                    "NAME:Interpolating_Sweep",
                    "IsEnabled:="        , True,
                    "SetupType:="        , "LinearStep",
                    "StartValue:="        , str(solutionstartfreq) + StartFrequnits,
                    "StopValue:="        , str(solutionstopfreq) + StopFrequnits,
                    "StepSize:="        , str(solutionstepfreq) + FreqStepunits,
                    "Type:="        , "Interpolating",
                    "SaveFields:="        , False,
                    "InterpTolerance:="    , 0.5,
                    "InterpMaxSolns:="    , 50,
                    "InterpMinSolns:="    , 0,
                    "InterpMinSubranges:="    , 1,
                    "ExtrapToDC:="        , True,
                    "MinSolvedFreq:="    , "100000"
                ])
                
         
