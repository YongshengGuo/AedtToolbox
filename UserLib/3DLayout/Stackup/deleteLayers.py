#--- coding:utf-8
#--- @Author: Yongsheng.Guo@ansys.com
#--- @Time: 2024-11-13


'''
功能描述：
1. 使用layerNames = layout.Layers.getStackLayerNames() 获取层的名称
2. 生成一个窗体展示layerNames供用户选择，采用列表形式，前面方式checkbox，用户可以选择多个层，放置确定和取消按钮，确定时返回用户选择的layerNames，取消时返回空列表
3. 将用户选择的layerNames传入deleteLayer(fromLayer,toLayer)函数，使用layout.Layers[layerName].delete()删除layer
'''



import sys,os

appPath = os.path.realpath(__file__)
appDir = os.path.split(appPath)[0] 
sys.path.append(appDir)
sys.path.append(r"C:\work\Study\Script\Ansys\quickAnalyze\FastSim")
# MessageBox.Show(appDir)

from pyLayout import Layout,log

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Windows.Forms import (
    Form,
    CheckedListBox,
    Button,
    DialogResult,
    MessageBox,
    FormStartPosition,
    AnchorStyles,
)
from System.Drawing import Point, Size


def selectLayers(layerNames):
    if not layerNames:
        return []

    form = Form()
    form.Text = "Delete Layers"
    form.StartPosition = FormStartPosition.CenterScreen
    form.Size = Size(460, 560)
    form.MinimumSize = Size(380, 420)

    checkedList = CheckedListBox()
    checkedList.Location = Point(12, 12)
    checkedList.Size = Size(420, 460)
    checkedList.CheckOnClick = True
    checkedList.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right
    for name in layerNames:
        checkedList.Items.Add(str(name), False)

    btnOk = Button()
    btnOk.Text = "OK"
    btnOk.DialogResult = DialogResult.OK
    btnOk.Size = Size(90, 30)
    btnOk.Location = Point(242, 485)
    btnOk.Anchor = AnchorStyles.Bottom | AnchorStyles.Right

    btnCancel = Button()
    btnCancel.Text = "Cancel"
    btnCancel.DialogResult = DialogResult.Cancel
    btnCancel.Size = Size(90, 30)
    btnCancel.Location = Point(342, 485)
    btnCancel.Anchor = AnchorStyles.Bottom | AnchorStyles.Right

    btnSelectAll = Button()
    btnSelectAll.Text = "Select All"
    btnSelectAll.Size = Size(90, 30)
    btnSelectAll.Location = Point(12, 485)
    btnSelectAll.Anchor = AnchorStyles.Bottom | AnchorStyles.Left

    btnClearAll = Button()
    btnClearAll.Text = "Clear All"
    btnClearAll.Size = Size(90, 30)
    btnClearAll.Location = Point(112, 485)
    btnClearAll.Anchor = AnchorStyles.Bottom | AnchorStyles.Left

    def onSelectAll(sender, args):
        for i in range(checkedList.Items.Count):
            checkedList.SetItemChecked(i, True)

    def onClearAll(sender, args):
        for i in range(checkedList.Items.Count):
            checkedList.SetItemChecked(i, False)

    btnSelectAll.Click += onSelectAll
    btnClearAll.Click += onClearAll

    form.Controls.Add(checkedList)
    form.Controls.Add(btnSelectAll)
    form.Controls.Add(btnClearAll)
    form.Controls.Add(btnOk)
    form.Controls.Add(btnCancel)
    form.AcceptButton = btnOk
    form.CancelButton = btnCancel

    if form.ShowDialog() != DialogResult.OK:
        return []

    return [str(item) for item in checkedList.CheckedItems]


def deleteLayer(layout, layerNames):
    deleted = []
    failed = []
    for layerName in layerNames:
        try:
            layout.Layers[layerName].delete()
            deleted.append(layerName)
        except Exception as e:
            failed.append((layerName, str(e)))
    return deleted, failed


def main():
    layout = Layout()
    layout.initDesign()
    layerNames = layout.Layers.getStackLayerNames()
    selectedLayerNames = selectLayers(layerNames)

    if not selectedLayerNames:
        log.info("No layer selected. Canceled by user.")
        return

    deleted, failed = deleteLayer(layout, selectedLayerNames)

    if deleted:
        log.info("Deleted layers: %s" % ", ".join(deleted))
    if failed:
        for layerName, err in failed:
            log.error("Failed to delete layer %s: %s" % (layerName, err))

    msg = "Delete finished.\nDeleted: %d\nFailed: %d" % (len(deleted), len(failed))
    MessageBox.Show(msg)


if __name__ == '__main__':
    main()
    print("finished.")
    
