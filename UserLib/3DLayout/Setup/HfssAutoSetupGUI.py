#coding:utf-8
#--- coding=utf-8
#--- @author: yongsheng.guo@synopsys.com, henryhe@synopsys.com
#--- @Time: 20260304

"""
Config Selector based on Config.csv (Windows Forms version)
For Ansys Electronics Desktop IronPython environment
"""


import os
import sys
import re
import csv
from collections import defaultdict

isIronpython = "IronPython" in sys.version
isPython = not isIronpython
is_linux = "posix" in os.name
if isIronpython:
    import clr as _clr # @UnresolvedImport
elif is_linux:
    try:
        from ansys.aedt.core.generic.clr_module import _clr # @UnresolvedImport
    except:
#         log.info("Make sure pyaedt have installed on linux: pip install pyaedt")
        from ansys.aedt.core.internal.clr_module import _clr # @UnresolvedImport
else:
    #for windows
    import clr as _clr # @UnresolvedImport


_clr.AddReference('System')
_clr.AddReference('System.Windows.Forms')
_clr.AddReference('System.Drawing')

import System
from System import Array
from System.Drawing import Point, Size, Color, Font, FontStyle
from System.Windows.Forms import (
    Application, Form, Label, ComboBox, Button, TextBox,
    MessageBox, FormStartPosition, ScrollBars, FormBorderStyle, ComboBoxStyle, AnchorStyles
)

# 之後才是你的 SCRIPT_DIR、CSV_FILE、函數定義、class ConfigForm ...

# 之後才是你的 SCRIPT_DIR、CSV_FILE、函數定義、class ConfigForm ...

# ─── 取得腳本所在目錄 ────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
# MessageBox.Show(SCRIPT_DIR)
sys.path.append(SCRIPT_DIR)

from autoSetup import HfssAutoSetup


# ─── Windows Forms GUI ─────────────────────────────────────────────────
class ConfigForm(Form):
    def __init__(self):
        Form.__init__(self) 
        self.Text = "HFSS AutoSetup Config Selector"
        self.Size = Size(680, 540)
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.Sizable
        self.MaximizeBox = True
        self.current_Config = None

        self.all_configs = {}
        self._init_controls()

    def _init_controls(self):
        # ── 標題 ───────────────────────────────────────────────────────
        lbl_title = Label()
        lbl_title.Text = "HFSS Auto Setup Configuration"
        lbl_title.Font = Font("Microsoft YaHei", 12, FontStyle.Bold)
        lbl_title.AutoSize = True
        lbl_title.Location = Point(20, 15)
        self.Controls.Add(lbl_title)

        # ── 類型選擇 ───────────────────────────────────────────────────
        lbl_type = Label()
        lbl_type.Text = "Select Type:"
        lbl_type.Location = Point(20, 60)
        lbl_type.AutoSize = True
        self.Controls.Add(lbl_type)

        self.combo_type = ComboBox()
        self.combo_type.Location = Point(120, 58)
        self.combo_type.DropDownStyle = ComboBoxStyle.DropDownList
        self.combo_type.Width = 140
        self.combo_type.Anchor = AnchorStyles.Top | AnchorStyles.Left
        self.combo_type.SelectedIndexChanged += self.on_type_changed
        self.Controls.Add(self.combo_type)

        # ── 配置名稱選擇 ───────────────────────────────────────────────
        lbl_name = Label()
        lbl_name.Text = "Select Config:"
        lbl_name.Location = Point(280, 60)
        lbl_name.AutoSize = True
        self.Controls.Add(lbl_name)

        self.combo_name = ComboBox()
        self.combo_name.Location = Point(380, 58)
        self.combo_name.DropDownStyle = ComboBoxStyle.DropDownList
        self.combo_name.Width = 260
        self.combo_name.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
        self.combo_name.SelectedIndexChanged += self.on_name_changed
        self.Controls.Add(self.combo_name)

        # ── 預覽標籤 ───────────────────────────────────────────────────
        lbl_preview = Label()
        lbl_preview.Text = "Config Preview:"
        lbl_preview.Location = Point(20, 140)
        lbl_preview.AutoSize = True
        self.Controls.Add(lbl_preview)

        # ── 確定 & 取消按鈕（放在預覽標籤右上方） ──────────────────────
        btn_ok = Button()
        btn_ok.Text = "OK"
        btn_ok.Location = Point(550, 100)  # 交換位置後放在右側
        btn_ok.Size = Size(100, 35)
        btn_ok.Font = Font("Microsoft YaHei", 11, FontStyle.Bold)
        btn_ok.BackColor = Color.FromArgb(76, 175, 80)  # 綠色
        btn_ok.ForeColor = Color.White
        btn_ok.Anchor = AnchorStyles.Top | AnchorStyles.Right
        btn_ok.Click += self.on_apply
        self.Controls.Add(btn_ok)

        btn_cancel = Button()
        btn_cancel.Text = "Cancel"
        btn_cancel.Location = Point(440, 100)  # 交換位置後放在左側
        btn_cancel.Size = Size(100, 35)
        btn_cancel.Font = Font("Microsoft YaHei", 11)
        btn_cancel.BackColor = Color.FromArgb(240, 240, 240)
        btn_cancel.Anchor = AnchorStyles.Top | AnchorStyles.Right
        btn_cancel.Click += self.on_cancel
        self.Controls.Add(btn_cancel)

        # ── 預覽區域 ───────────────────────────────────────────────────
        self.txt_preview = TextBox()
        self.txt_preview.Multiline = True
        self.txt_preview.ReadOnly = True
        self.txt_preview.ScrollBars = ScrollBars.Both
        self.txt_preview.WordWrap = False
        self.txt_preview.Location = Point(20, 175)  # 稍微往下移一點，避免與按鈕重疊
        self.txt_preview.Size = Size(640, 250)  # 高度略微調整
        self.txt_preview.Font = Font("Consolas", 10)
        self.txt_preview.BackColor = Color.White
        self.txt_preview.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
        self.Controls.Add(self.txt_preview)

        # ── 狀態標籤 ───────────────────────────────────────────────────
        self.lbl_status = Label()
        self.lbl_status.Text = ""
        self.lbl_status.Location = Point(20, 440)
        self.lbl_status.AutoSize = True
        self.lbl_status.ForeColor = Color.Blue
        self.lbl_status.Anchor = AnchorStyles.Left | AnchorStyles.Bottom
        self.Controls.Add(self.lbl_status)

        # 第一次載入資料
        self.load_data()

    # ── 新增取消按鈕的事件 ────────────────────────────────────────────
    def on_cancel(self, sender, args):
        self.Close()

    def load_data(self):
        # Clear all UI elements
        self.combo_type.Items.Clear()
        self.combo_name.Items.Clear()
        self.txt_preview.Text = ""
        self.lbl_status.Text = ""

        # Scan config folder for CSV files
        config_folder = os.path.join(SCRIPT_DIR, "config")

        if not os.path.exists(config_folder):
            self.lbl_status.Text = "Config folder not found"
            self.lbl_status.ForeColor = Color.OrangeRed
            return

        # Find all CSV files and extract filenames without extension
        csv_files = [f[:-4] for f in os.listdir(config_folder) if f.endswith('.csv')]
        csv_files.sort()

        # Populate combo_type with sorted filenames
        for filename in csv_files:
            self.combo_type.Items.Add(filename)

        if csv_files:
            self.combo_type.SelectedIndex = 0
        else:
            self.lbl_status.Text = "No CSV files found in config folder"
            self.lbl_status.ForeColor = Color.OrangeRed

    def _get_config_data(self, type_name, config_name):
        """Extract data dictionary for selected type and configuration."""
        csv_path = os.path.join(SCRIPT_DIR, "config", type_name + ".csv")

        if not os.path.exists(csv_path):
            self.lbl_status.Text = "CSV file not found: " + csv_path
            self.lbl_status.ForeColor = Color.OrangeRed
            return {}

        try:
            # with open(csv_path, 'r', encoding='utf-8') as f:
            #     reader = csv.reader(f)
            #     rows = list(reader)
            # Branch based on Python version for CSV compatibility
            if sys.version_info[0] >= 3:
                # Python 3: Text mode with encoding
                with open(csv_path, 'r', encoding='utf-8', newline='') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
            else:
                # Python 2: Binary mode (csv module expects bytes)
                with open(csv_path, 'rb') as f:
                    reader = csv.reader(f)
                    rows = list(reader)


            if not rows:
                self.lbl_status.Text = "CSV file is empty"
                self.lbl_status.ForeColor = Color.OrangeRed
                return {}

            # Parse first row to get config names (skip first cell)
            header = rows[0]
            config_names = [n.strip() for n in header[1:] if n.strip()]

            # Find index of config_name
            if config_name not in config_names:
                self.lbl_status.Text = "Config not found: " + config_name
                self.lbl_status.ForeColor = Color.OrangeRed
                return {}

            index = config_names.index(config_name)

            # Build result dict from subsequent rows
            result = {}
            for row in rows[1:]:
                key = row[0].strip() if row[0] else ""
                if key and index + 1 < len(row):
                    value = row[index + 1].strip() if row[index + 1] else ""
                else:
                    value = ""
                if key and value:
                    result[key] = value

            return result
        except Exception as e:
            self.lbl_status.Text = "Failed to read CSV: " + str(e)
            self.lbl_status.ForeColor = Color.OrangeRed
            return {}

    def on_type_changed(self, sender, args):
        self.combo_name.Items.Clear()
        self.txt_preview.Text = ""

        typ = str(self.combo_type.SelectedItem) if self.combo_type.SelectedItem else ""
        if not typ:
            return

        csv_path = os.path.join(SCRIPT_DIR, "config", typ + ".csv")
        if not os.path.exists(csv_path):
            self.lbl_status.Text = "CSV file not found: " + csv_path
            self.lbl_status.ForeColor = Color.OrangeRed
            return

        try:
#             with open(csv_path, 'r', encoding='utf-8') as f:
                
            if sys.version_info[0] >= 3:
                # Python 3: Text mode with encoding
                with open(csv_path, 'r', encoding='utf-8', newline='') as f:
                    reader = csv.reader(f)
#                     rows = list(reader)
                    for row in reader:
                        # Get header row and extract config names (skip first cell)
                        names = [n.strip() for n in row[1:] if n.strip()]
                        self.combo_name.Items.Clear()
                        for name in names:
                            self.combo_name.Items.Add(name)
                        if names:
                            self.combo_name.SelectedIndex = 0
                        break  # Only process first row (header)
            else:
                # Python 2: Binary mode (csv module expects bytes)
                with open(csv_path, 'rb') as f:
                    reader = csv.reader(f)
#                     rows = list(reader)
                    for row in reader:
                        # Get header row and extract config names (skip first cell)
                        names = [n.strip() for n in row[1:] if n.strip()]
                        self.combo_name.Items.Clear()
                        for name in names:
                            self.combo_name.Items.Add(name)
                        if names:
                            self.combo_name.SelectedIndex = 0
                        break  # Only process first row (header)
        except Exception as e:
            self.lbl_status.Text = "Failed to read CSV: " + str(e)
            self.lbl_status.ForeColor = Color.OrangeRed

    def on_name_changed(self, sender, args):
        typ = str(self.combo_type.SelectedItem) if self.combo_type.SelectedItem else ""
        name = str(self.combo_name.SelectedItem) if self.combo_name.SelectedItem else ""
        self.current_Config = self._get_config_data(typ, name)
        self.update_preview()

    def update_preview(self):
        self.txt_preview.Text = ""

        typ = str(self.combo_type.SelectedItem) if self.combo_type.SelectedItem else ""
        name = str(self.combo_name.SelectedItem) if self.combo_name.SelectedItem else ""

        if not typ or not name:
            return

        data = self.current_Config

        if not data:
            return

        lines = []
        lines.append("   Type: {typ}    Config: {name}".format(typ=typ,name=name))
        lines.append("--------------------------")

        align_width = 30

        for key, value in sorted(data.items()):
            line = "{key:>{align_width}} : {value}".format(key=key, value=value, align_width=align_width)
            lines.append(line)

        self.txt_preview.Text = "\r\n".join(lines)

#        self.lbl_status.Text = "行數：" + str(len(lines)) + " 行已寫入預覽區"
    def on_reload(self, sender, args):
        self.load_data()
        MessageBox.Show("CSV reloaded", "Complete")

    def on_apply(self, sender, args):
        typ = str(self.combo_type.SelectedItem) if self.combo_type.SelectedItem else ""
        name = str(self.combo_name.SelectedItem) if self.combo_name.SelectedItem else ""

        if not typ or not name:
            MessageBox.Show("Please select type and config", "Prompt")
            return
        
        data = self.current_Config
        if not data:
            MessageBox.Show("Selected config has no data", "Prompt")
            return
        try:
            hfssSetup = HfssAutoSetup(data)
            hfssSetup.run()
        except Exception as e:
            MessageBox.Show("Failed to setup: " + str(e), "Prompt")
            return
        else:
            print("Finish setup.")
            self.Close()
        

def main():
    Application.EnableVisualStyles()
    form = ConfigForm()
    Application.Run(form)

# ─── 主程式 ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    Application.EnableVisualStyles()
    #Application.SetCompatibleTextRenderingDefault(False)
    form = ConfigForm()
    Application.Run(form)