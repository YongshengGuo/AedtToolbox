# ImportCSVStackup
## 菜单位置
Stackup->ImportCSVStackup

## 功能描述
通过CSV文件快速导入加工厂给定的叠层。可以把工厂提供的xlsx文件按照提供的CSV模板格式输出成文件做输入即可。列的顺序不限，不在定义内的列会被忽略。

## 操作说明
需要按照提供的CSV模板填写叠层信息。然后在Toolbox上右键，选择Stackup->ImportCSVStackup，选择已经填写好的CSV叠层模板，进行导入。  
在ImportCSVStackup.py目录下提供了"CsvStackupTemp_full.csv" 和 "CsvStackupTemp_simple.csv"两个模板可供使用。

## 模板格式

| Layer       | Type       | Thickness(mil) | Cond | DK  | DF    | Roughness |
|-------------|------------|----------------|------|-----|-------|-----------|
| UNNAMED_000 | dielectric | 0              |      | 3.7 | 0.15  | 0.5um     |
| TOP         | signal     | 1.9            |      | 3.7 | 0.15  | 0.5um     |
| UNNAMED_002 | dielectric | 2.65           |      | 3.5 | 0.004 | 0.5um     |
| PWR         | signal     | 1.3            |      | 3.5 | 0.004 | 0.5um     |
| UNNAMED_004 | dielectric | 50             |      | 3.5 | 0.004 | 0.5um     |
| LYR_1       | signal     | 1.2            |      | 3.5 | 0.004 | 0.5um     |
| UNNAMED_006 | dielectric | 8              |      | 3.5 | 0.004 | 0.5um     |
| LYR_2       | signal     | 1.2            |      | 3.5 | 0.004 | 0.5um     |
| UNNAMED_008 | dielectric | 8              |      | 3.5 | 0.004 | 0.5um     |
| GND         | signal     | 1.3            |      | 3.5 | 0.004 | 0.5um     |
| UNNAMED_010 | dielectric | 2.65           |      | 3.5 | 0.004 | 0.5um     |
| BOTTOM      | signal     | 1.9            |      | 3.7 | 0.15  | 0.5um     |
| UNNAMED_012 | dielectric | 0              |      | 3.7 | 0.15  | 0.5um     |

说明：
1. Layer, Type,Thickness必须指定, 未指定的行将被忽略。
2. Cond, DK, DF如果缺失或者为给定数值，默认会使用Copper和FR4_epoxy替代
3. Thickness可以使用()指定单位，或者在数值中直接使用单位。
4. Roughness为可选属性，Groiss格式: 0.5um, huray格式: 0.5um;2.9


## 可选属性

- Thickness：厚度，需要带单位。或者在标题上使用全局单位，比如Thickness(mil) or Thickness(mm)
- Material：指定系统库里面的材料名称，比如Copper，此时Cond/DK/DF被忽略
- FillMaterial:指定系统库里面的材料名称，比如FR-4，此时Cond/DK/DF被忽略
- Cond/DK/DF 如果指定，且未指定Material或FillMaterial，自动根据参数生成新材料
- Roughness：指定粗糙度，Groiss格式0.5um, huray格式：0.5um;2.9 or 0.5um,2.9 
- EtchFactor: 蚀刻系数，正值为Top蚀刻，负值为Bottom蚀刻

## 注意事项
- CSV中的金属层数量必须和PCB里面的相同，否则无法更新。
- CSV的介质层数量不要求和PCB里面的相同，如果介质层数不同，CSV的介质层强制覆盖PCB中的介质层。


## 附加说明
此选项可以配合ExportCSVStackup使用，先快速导出CSV文件模板，然后按照现有的叠层文件信息进行修改，再使用ImportCSVStackup导入。

## 案例展示

1. 从加工厂获取的Excel叠层文件 
![Excel stackup](images/image%5B4%5D.png)
2. 使用ExportCSVStackup导出现有叠层模板 
![ExportCSVStackup](images/image-1%5B3%5D.png)
3. 使用ImportCSVStackup导入修改后的CSV文件 
![ImportCSVStackup](images/image-2%5B1%5D.png)
4. 日志信息 
![log](images/image-3%5B1%5D.png)

