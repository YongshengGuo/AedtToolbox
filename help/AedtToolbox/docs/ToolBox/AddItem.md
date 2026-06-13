# 用户自定义菜单和脚本
## 用户子定义菜单和脚本
用户可以根据自身的需要添加菜单和脚本，定制符合本公司需求的Toolbox工具集合。可以参照下面的方法对菜单和脚本内容继续增加和删除。

## 菜单的设定更新
用户菜单可以通过目录下的menu.xml进行更新和设定。Toolbox发布时已经附带了一些功能和菜单项，用户可以根据需要进行删减和添加自己的菜单内容。

菜单格式如下：
``` xml
<Menu>
	<SubMenu Name="test">
		<SubMenu Type="MenuItem" Name="showProjectName_python" ExecuteType="Python" Path="$UserLib/Template/showProjectName.py" Arguments ="" PythonPath="" LogWindow="True"></SubMenu>
		<SubMenu Type="MenuItem" Name="showProjectName_Ironpython" ExecuteType="IronPython" Path="$UserLib/Template/showProjectName.py" Arguments ="" EntryFunc="main" PythonPath=""></SubMenu>
	</SubMenu>
</Menu>
```
### 参数说明
- <SubMenu> </SubMenu> 时对菜单项的声明，允许进行嵌套，嵌套将以子菜单的形式呈现。子菜单的深度未作限定，但是不建议嵌套的过深，影响用户体验。
- Type：取值可以为 "MenuItem"（菜单项）,"Separator"(分隔符), 省略时默认为"MenuItem"
- Name：菜单显示的名称
- ExecuteType：可执行程序的类型，可选值：Python，IronPython，EXE。 其中Command类型为内部保留类型，用户无法进行定义。
- Path: 可执行程序，脚本的路径。可以使用绝对路径值。如果使用相对路径，可以使用"$+目录"的形式引入当面目录下的文件夹。
- Arguments: 允许传递参数给可执行脚本，多个参数以空格隔开。
- PythonPath： 可以指定Python的执行路径，特别是存在多个版本时可以按照路径区分版本。省略时会从Path变量中查找Python执行文件。
- EntryFunc： 针对Python，IronPython指定运行脚本的入口函数，默认为"main"函数（可以省略），如果为其它函数则需要指定函数名称。
- LogWindow: 运行脚本时是否显示运行日志，默认为True 显示日志窗口（命令行输出）， 设置为False 则不显示日志窗口。

### 注意事项
- 设计到文件路径的位置，空格和中文字符可能会导致执行错误，请尽量避免使用。  
- XML里面的文件路径注意使用\\或者使用/。
- XML的语法可以自行搜寻，修改后的温度不能存在语法错误。
- 已知XML注释会导致菜单加载错误，请不用在XML文档中使用注释。
- XML文件编辑保持后，Toolbox会自动重新加载。
- LogWindow: 运行脚本时是否显示运行日志，默认为True 显示日志窗口（命令行输出）， 设置为False 则不显示日志窗口。
## Exe文件的添加

``` xml
<SubMenu Type="MenuItem" Name="Notepad" ExecuteType="EXE" Path="Notepad.exe" Arguments =""/>
```
属性定义如下：  

- Name：菜单显示的名称
- ExecuteType： "EXE"
- Path：可执行文件路径。如果这里指定文档，且系统有默认执行程序，也可以顺利打开，比如Path指定xxx.docx文档。
- Arguments: 传递参数，多个参数以空格隔开。
- LogWindow: 运行脚本时是否显示运行日志，默认为True 显示日志窗口（命令行输出）， 设置为False 则不显示日志窗口。
## Python脚本的添加

``` xml
<SubMenu Type="MenuItem" Name="QuitAedt" ExecuteType="Python" Path="$UserLib/Desktop/Close.py" EntryFunc="ForceQuitAedt" Arguments ="" PythonPath=""></SubMenu>
```
属性定义如下：  

- Name：菜单显示的名称
- ExecuteType：Python
- Path: 脚本的路径。可以使用绝对路径值。如果使用相对路径，可以使用"$+目录"的形式引入当面目录下的文件夹。
- Arguments: 可选，允许传递参数给可执行脚本，多个参数以空格隔开。
- PythonPath： 可选，可以指定Python的执行路径，特别是存在多个版本时可以按照路径区分版本。省略时会从Path变量中查找Python执行文件。
- EntryFunc： 可选，针对Python，IronPython指定运行脚本的入口函数，默认为"main"函数（可以省略），如果为其它函数则需要指定函数名称。
- LogWindow: 运行脚本时是否显示运行日志，默认为True 显示日志窗口（命令行输出）， 设置为False 则不显示日志窗口。

## IronPython脚本的添加

``` xml
<SubMenu Type="MenuItem" Name="QuitAedt" ExecuteType="Python" Path="$UserLib/Desktop/Close.py" EntryFunc="ForceQuitAedt" Arguments ="" PythonPath=""></SubMenu>
```
属性定义如下：  

- Name：菜单显示的名称
- ExecuteType：Python
- Path: 脚本的路径。可以使用绝对路径值。如果使用相对路径，可以使用"$+目录"的形式引入当面目录下的文件夹。
- Arguments: 可选，允许传递参数给可执行脚本，多个参数以空格隔开。
- PythonPath： 可选，可以指定Python的执行路径，特别是存在多个版本时可以按照路径区分版本。省略时会从Path变量中查找Python执行文件。
- EntryFunc： 可选，针对Python，IronPython指定运行脚本的入口函数，默认为"main"函数（可以省略），如果为其它函数则需要指定函数名称。
- LogWindow: 运行脚本时是否显示运行日志，默认为True 显示日志窗口（命令行输出）， 设置为False 则不显示日志窗口。