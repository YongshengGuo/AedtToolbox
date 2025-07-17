# Welcome to Aedt Toolbox

## 工具说明
Aedt Toolbox提供了一种便捷的方式，让用户在AEDT中迅速运行脚本或外部程序。它通过悬浮图标和自定义菜单的组合，实现高效操作。用户可以借助XML文件快速定制菜单内容，对脚本进行管理，一旦更新，这些变化将实时反映在右键菜单中，确保用户始终拥有个性化的操作体验。   
整体实现效果如下：   
![picture 0](images/e16036167a36bbd1acba40dffe3aeb83b4235325f7cdb85114ffc94150541123%5B1%5D.png)  

当对应菜单被点击时，Toolbox会将脚本发送至最近一次打开的AEDT窗口并执行其内容。由于Toolbox不区分AEDT的版本，因此可以兼容不同版本的AEDT，使得同一个脚本可以在不同版本的AEDT中执行。

Toolbox支持外部程序和脚本的执行，包括Exe、Python和Ironpython三种类型。目前Toolbox仅支持Windows系统。
## 工具启动
通过目录下的"AedtToolbox.exe"启动Toolbox，启动后Toolbox以悬浮窗口的形式显示，默认显示在所有窗体的最前面。

![Alt text](images/image%5B9%5D.png)

可以通过两种方式弹出右键菜单： 
1. 通过在悬浮窗口点击右键  
   ![picture 0](images/e16036167a36bbd1acba40dffe3aeb83b4235325f7cdb85114ffc94150541123%5B1%5D.png)  
2. 通过通知图标点击右键。  
   ![Alt text](images/8EmzaBAqZv%5B1%5D.png)

## Python环境配置
python和Ironpython的目录必须配置到系统的Path变量里，以确保工具的正确运行。如下图：
![Alt text](images/SystemPropertiesAdvanced_GWZr6hXk2E%5B1%5D.png)

对于python脚本的执行，pyaedt必须按照，可以通过在命令窗口中输入：`pip install pyaedt`

![Alt text](images/image%5B10%5D.png)