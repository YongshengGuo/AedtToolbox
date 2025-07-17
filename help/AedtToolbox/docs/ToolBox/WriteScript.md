# 编写用户自定义脚本

## python脚本的编写
python脚本可以按照正常的模式进行开发，将需要运行到功能包装成一个函数，最终在菜单的xml里面指定未入口函数即可。  
默认的入口函数未mian()函数，建议使用main()函数作为入口。

下面的案例中，python文件定义了多个函数，可以在xml里面分别指定不同的函数作为入口函数，完成不同的功能。  
另外也可以通过传递不同的Arguments来完成类似的功能。

```python

import sys,os

Module = sys.modules['__main__']
if hasattr(Module, "oDesktop"):
    oDesktop = getattr(Module, "oDesktop")
else:
    raise Exception("oDesktop intial error.")


def closeAndSave():
    oProject = oDesktop.GetActiveProject()
    oProject.Save()
    oProject.Close() 
    
def closeNotSave():
    oProject = oDesktop.GetActiveProject()
    # oProject.Save()
    oProject.Close() #Unsaved changes will be lost.

def closeAllProjectWithSave():
    projects = oDesktop.GetProjects()
    for oProject in projects:
        oProject.Save()
        oProject.Close()
        
def closeAllProjectWithoutSave():
    projects = oDesktop.GetProjects()
    for oProject in projects:
        # oProject.Save()
        oProject.Close() #Unsaved changes will be lost.

def ForceQuitAedt():
    oDesktop.QuitApplication()

def Reload():
    oProject = oDesktop.GetActiveProject()
    aedtPath = os.path.join(oProject.GetPath(),oProject.GetName()+".aedt")
    oProject.Close()
    print("Reload aedt:%s"%aedtPath)
    oDesktop.OpenProject(aedtPath)

```
XML菜单配置

```xml
	<SubMenu Name="Close">
		<SubMenu Type="MenuItem" Name="QuitAedt" ExecuteType="Python" Path="$UserLib/Desktop/Close.py" EntryFunc="ForceQuitAedt"></SubMenu>
		<SubMenu Type="MenuItem" Name="CloseProjectAndSave" ExecuteType="Python" Path="$UserLib/Desktop/Close.py" EntryFunc="closeAndSave"></SubMenu>
		<SubMenu Type="MenuItem" Name="CloseProjectNotSave" ExecuteType="Python" Path="$UserLib/Desktop/Close.py" EntryFunc="closeNotSave"></SubMenu>
		<SubMenu Type="MenuItem" Name="CloseAllProjectAndSave" ExecuteType="Python" Path="$UserLib/Desktop/Close.py" EntryFunc="closeAllProjectWithSave"></SubMenu>
		<SubMenu Type="MenuItem" Name="CloseAllProjectNotSave" ExecuteType="Python" Path="$UserLib/Desktop/Close.py" EntryFunc="closeAllProjectWithoutSave"></SubMenu>
		<SubMenu Type="MenuItem" Name="ReloadProject" ExecuteType="IronPython" Path="$UserLib/Desktop/Close.py" EntryFunc="Reload"></SubMenu>
	</SubMenu>
```