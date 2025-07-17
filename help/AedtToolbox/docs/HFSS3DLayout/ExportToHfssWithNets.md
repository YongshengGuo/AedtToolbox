# ExportToHfssWithNets
## 菜单位置
Export->ExportToHfssWithNets

## 功能描述
将3D Layout中的3D模型导出到HFSS后，可以按照Net对物体进行分组，这样更便于查看和设定物体。

## 操作说明
确保3D Layout工程处于选中状态，并且已经设定完成（叠层，端口，Cutout等），确保设置了HFSS Setup(建议最好只有1个setup)。然后在Toolbox上右键，选择Export->ExportToHfssWithNets 
![picture 2](images/d9a71467adb7e8a26b8b8a3ad42281c32685dbc3ffad2c3233b8aefbfce40a18%5B3%5D.png)  

## 完成效果
等待脚本执行完成，最终效果如下：

![picture 3](images/db57ebbdf39c351e5a01e393d281acb67fa550a7bc5c7ae52ce314dd202c3918%5B3%5D.png)  

## Overlapping Stackup的支持
2.5D/3DIC Package在3D Layout中使用了Overlapping叠层，ExportToHfssWithNets命令可以支持Overlapping的导出。但是如果有2个及以上的金属层位于同一高度时，对Nets的识别会存在一些问题。  

### Interposer 导出案例：
1. Overlapping Stackup 且所有金属层处于不同高度
![Alt text](images/image%5B5%5D.png) 
2. 导出之前Design Mode需要使用General Mode，不然脚本执行会出错。
![Alt text](images/image-1%5B2%5D.png)
3. 导出效果
![Alt text](images/image%5B6%5D.png)

## 特别说明
3D Layout使用HFSS求解器，可以和HFSS精度保持一致，设置和操作上要比HFSS 3D方便和快速。大部分场景下并不建议把3D Layout导出HFSS 3D进行求解。  


