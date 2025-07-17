# DissloveInvalidRLC
## 菜单位置
Component->DissloveInvalidRLC(<2pins)
Component->deleteInvalidComponents(<2pins)

## 功能描述
删除只存在1个有效网络的RLC器件。对Layout进行Cutout和网络删除后，部分RLC的网络被删除，处于无效状态，此命令可以清除无效的RLC器件。  

- DissloveInvalidRLC(<2pins) 只Disslove RLC器件，不删除pad
- deleteInvalidComponents(<2pins) 删除所有小于2pins的器件(RLC和其它器件)，并删除

## 操作说明
确保3D Layout工程处于选中状态，然后在Toolbox上右键，选择 Component->deleteInvalidRLC. 脚本会自动在当前激活的AEDT里面执行，检测RLC的Net状态，并删除无效的网络。

![Alt text](images/image%5B11%5D.png)