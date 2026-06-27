# AEDT 释放指南

## 问题背景
原有的 `releaseDesktop()` 函数无法正常释放AEDT窗口，导致错误：
```
Electronics Desktop cannot be closed right now because it is being used 
by another application, script or extension wizard.
```

## 修复说明

### 1. desktop.py 改进
- **新增 `_closeAllProjects()`**: 在删除引用前关闭所有打开的AEDT窗口
- **改进 `_delete_objects()`**: 调用新增函数关闭窗口，并删除 `_oDesktop` 引用
- **完整 `releaseDesktop()`**: 
  - 尝试获取 `_oDesktop` 和 `oDesktop` 引用
  - 调用 `CloseAllWindows()` 关闭所有窗口
  - 调用 `QuitApplication()` 退出AEDT
  - 清理所有引用

### 2. circuit.py 改进
- **改进 `Circuit.release()`**: 
  - 在释放前先关闭打开的项目
  - 清理所有内部引用
  - 最后调用 `releaseDesktop()`
- **修改 `Circuit.__del__()`**: 
  - 不再直接调用 `releaseDesktop()`
  - 避免在垃圾回收时关闭全局AEDT实例

## 正确使用方式

### 方式1：使用 Circuit.release()（推荐）
```python
from pyLayout.circuit import Circuit

# 创建和使用Circuit
layout = Circuit()
layout.initDesign("MyProject", "MyDesign")
# ... 进行设计操作 ...

# 完成后显式释放
layout.release()  # 自动关闭项目并释放AEDT
```

### 方式2：使用 Circuit.close() 然后 releaseDesktop()
```python
from pyLayout.circuit import Circuit
from pyLayout.desktop import releaseDesktop

layout = Circuit()
layout.initDesign("MyProject", "MyDesign")
# ... 进行设计操作 ...

layout.close(save=True)     # 关闭项目
releaseDesktop()             # 释放AEDT
```

### 方式3：使用 Circuit.quitAedt()（仅关闭AEDT）
```python
from pyLayout.circuit import Circuit

layout = Circuit()
layout.initDesign("MyProject", "MyDesign")
# ... 进行设计操作 ...

Circuit.quitAedt()  # 直接关闭AEDT，不关闭项目
```

### 方式4：使用 PyLayout (自动管理)
```python
from pyLayout import PyLayout

layout = PyLayout()
layout.initDesign("MyProject", "MyDesign")
# ... 进行设计操作 ...

# 超出作用域时自动释放（通过__del__）
# 或手动调用：
layout.release()
```

## 关键改进点

1. **清晰的释放层级**
   - 应用级：`releaseDesktop()` → 关闭AEDT
   - 项目级：`Circuit.close()` → 关闭项目
   - 对象级：`_delete_objects()` → 清理引用

2. **更好的异常处理**
   - 各层级都有try-except保护
   - 即使某个步骤失败也会继续释放后续资源

3. **两个引用的处理**
   - `Module._oDesktop`：内部使用的AEDT引用
   - `Module.oDesktop`：用户可访问的AEDT引用
   - 两个都会被删除

4. **日志增强**
   - 记录关键操作步骤
   - 帮助调试释放过程

## 常见问题

### Q: 为什么不在 `__del__` 中自动释放？
A: `__del__` 在垃圾回收时触发，时机不确定。显式调用 `release()` 能确保正确的释放顺序。

### Q: 多个Circuit对象会互相干扰吗？
A: 是的。所有Circuit对象共享同一个全局oDesktop。建议：
- 同一时间只使用一个Circuit对象
- 或使用 `newDesktop=True` 创建新的独立AEDT实例

### Q: 如何在脚本中确保AEDT被正常释放？
A: 使用try-finally结构：
```python
from pyLayout.circuit import Circuit

layout = Circuit()
try:
    layout.initDesign("MyProject", "MyDesign")
    # ... 操作 ...
finally:
    layout.release()  # 确保执行
```

### Q: 为什么修改后需要等待？
A: AEDT.QuitApplication() 是异步的。使用者可能需要在释放后添加短暂延迟：
```python
import time
layout.release()
time.sleep(2)  # 等待AEDT完全关闭
```

## 技术细节

### _closeAllProjects() 的作用
- 在删除Python引用前，先释放AEDT资源
- 调用 `oDesktop.CloseAllWindows()` 关闭所有项目和设计
- 这是避免"被另一个应用使用"错误的关键

### QuitApplication() 的必要性
- 原有代码只删除引用，AEDT进程仍在运行
- 显式调用QuitApplication()才能真正关闭应用
- 结合CloseAllWindows()能确保完全释放

### 为什么要删除 _oDesktop？
- `_oDesktop` 是initializeDesktop()设置的内部引用
- 不删除它会导致模块保持对oDesktop的引用
- 即使删除了 `oDesktop`，_oDesktop仍会保持连接
