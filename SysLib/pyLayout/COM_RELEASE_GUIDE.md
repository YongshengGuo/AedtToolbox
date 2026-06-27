# AEDT COM 资源释放指南

## 问题背景

当使用pyLayout控制AEDT后，经常遇到以下错误：
```
Electronics Desktop cannot be closed right now because it is being used 
by another application, script or extension wizard.
```

这意味着：
- AEDT COM接口资源仍被Python进程持有
- 其他应用或脚本无法获得对AEDT的控制权
- AEDT窗口被"锁定"，无法由其他源控制

## 解决方案

### 核心概念

**释放 ≠ 关闭**
- **释放COM资源** ✓ 推荐 - 归还AEDT控制权，AEDT保持打开
- **关闭AEDT** - 不推荐 - 关闭应用程序

### 正确的释放方式

#### 方式1：使用 `Circuit.release()` （推荐）

```python
from pyLayout.circuit import Circuit

# 创建并使用Circuit
layout = Circuit()
layout.initDesign("MyProject", "MyDesign")
# ... 执行设计操作 ...

# 完成后，释放COM资源
layout.release()  # AEDT保持打开，但其他应用可以控制它
```

**效果**：
- ✓ COM资源被释放
- ✓ AEDT保持打开
- ✓ 其他应用或脚本可以访问AEDT
- ✓ 项目保持打开

#### 方式2：使用 `releaseDesktop()` 

```python
from pyLayout.desktop import releaseDesktop

# ... 使用AEDT ...

releaseDesktop()  # 释放COM资源
```

**效果**：
- ✓ COM资源被释放
- ✓ AEDT保持打开
- ✓ 其他应用或脚本可以访问AEDT
- ✓ 项目和窗口保持打开

#### 方式3：使用 PyLayout

```python
from pyLayout import PyLayout

layout = PyLayout()
layout.initDesign("MyProject", "MyDesign")
# ... 操作 ...

layout.release()  # 释放COM资源
```

## 关键改进

### 1. 正确的COM资源释放

**新增：`_releaseComObjects()` 函数**
```python
# 对于IronPython：使用 Marshal.ReleaseComObject()
# 对于CPython：删除引用
# 调用垃圾收集
```

**改进：`_delete_objects()` 函数**
- 先释放COM对象
- 再删除引用
- 强制垃圾回收

### 2. 纯净的释放逻辑

**`releaseDesktop()` 专注于释放COM资源**
```python
# 仅释放COM资源，AEDT保持打开
releaseDesktop()
```

### 3. 清晰的语义

- `releaseDesktop()` - 释放COM资源，AEDT保持打开
- `Circuit.release()` - 释放Circuit对象和COM资源
- `Circuit.quitAedt()` - 关闭AEDT应用程序

## 使用场景

### 场景1：脚本完成，释放AEDT给其他用户

```python
# Python脚本自动化生成PCB设计
layout = Circuit()
layout.initDesign("BoardDesign", "MainLayout")
# ... 自动设计 ...
layout.save()

# 释放AEDT给用户手动调整
layout.release()
print("设计完成，AEDT已可供使用")
```

### 场景2：多个脚本交替使用AEDT

```python
# 脚本A
from pyLayout.circuit import Circuit

layout_a = Circuit()
layout_a.initDesign("Project_A", "Design_A")
# ... 操作 ...
layout_a.release()  # 释放给脚本B

# 脚本B
from pyLayout.circuit import Circuit

layout_b = Circuit()
layout_b.initDesign("Project_B", "Design_B")
# ... 操作 ...
layout_b.release()
```

### 场景3：脚本+用户交互

```python
# 脚本自动完成初始设置
layout = Circuit()
layout.initDesign("BaseProject", "BaseDesign")
# ... 自动设置 ...

# 释放AEDT给用户进行手动操作
layout.release()

# 用户操作后，脚本继续处理
# ...

# 脚本继续使用（获得新的COM引用）
layout.initDesign("BaseProject", "BaseDesign")
# ... 继续操作 ...
layout.release()
```

## 常见问题

### Q: 为什么还是无法访问AEDT？

**A:** 确保调用了 `release()`：
```python
# ✓ 正确
layout.release()

# ✗ 错误（只删除引用不释放COM）
del layout
```

### Q: 能否在不关闭项目的情况下释放？

**A:** 可以，`release()` 默认不关闭项目：
```python
layout.release()  # 项目保持打开，其他应用可以控制
```

### Q: 释放后还能继续使用layout吗？

**A:** 可以，但需要重新初始化设计：
```python
layout.release()
# ... 其他代码或其他应用操作 ...
layout.initDesign("Project", "Design")  # 重新获得COM引用
```

### Q: 如何确认COM资源已释放？

**A:** 查看日志输出：
```
[INFO] Releasing COM resources...
[INFO] Released _oDesktop COM object (IronPython)
[INFO] COM resources released. AEDT window control relinquished.
```

### Q: 需要立即关闭AEDT吗？

**A:** 使用专用方法：
```python
# 保持项目打开，只关闭AEDT应用
Circuit.quitAedt()

# 或者释放后立即关闭
layout.release()
Circuit.quitAedt()
```

## 技术细节

### COM 资源释放过程

```
releaseDesktop()
  └─ 释放COM资源
      ├─ _releaseComObjects()
      │  ├─ Marshal.ReleaseComObject(_oDesktop) [IronPython]
      │  ├─ Marshal.ReleaseComObject(oDesktop) [IronPython]
      │  └─ 删除引用 [CPython]
      └─ _delete_objects()
         ├─ 删除所有模块引用
         └─ gc.collect() [垃圾回收]
```

### IronPython vs CPython

| 方面 | IronPython | CPython |
|------|-----------|---------|
| COM释放 | Marshal.ReleaseComObject() | 删除引用 |
| 垃圾回收 | 立即 | gc.collect() |
| 引用计数 | 精确 | 定时 |

## 最佳实践

### ✓ 推荐做法

```python
from pyLayout.circuit import Circuit
import time

def design_automation():
    layout = Circuit()
    try:
        layout.initDesign("Project", "Design")
        # ... 设计操作 ...
        layout.save()
    finally:
        layout.release()  # 确保释放
        time.sleep(1)     # 可选：给COM时间清理

design_automation()
```

### ✗ 要避免的做法

```python
# 错误1：期望__del__自动释放
layout = Circuit()
del layout  # 可能不会立即释放COM

# 错误2：混合多个circuit对象
a = Circuit()
b = Circuit()  # 共享同一个COM对象，会冲突

# 错误3：不释放直接关闭
layout.quitAedt()  # 没有释放，直接关闭

# 错误4：使用过期引用
layout.release()
time.sleep(10)
layout.initDesign()  # 可能失败，引用已释放
```

## 相关方法速查

| 方法 | 作用 | 何时使用 |
|------|------|--------|
| `layout.release()` | 释放COM资源 | 完成设计后 |
| `releaseDesktop()` | 低级释放函数 | 不常用 |
| `layout.close()` | 关闭项目 | 保存前 |
| `Circuit.quitAedt()` | 关闭AEDT应用 | 完全退出时 |

## 故障排除

### 症状：仍然无法访问AEDT

1. 确认调用了 `release()`
2. 检查日志中是否有错误信息
3. 等待1-2秒让COM完全释放
4. 检查是否有其他Python进程持有AEDT引用
5. 最后手段：重启AEDT

### 症状：释放后AEDT消失

- 可能意外调用了 `QuitApplication()`
- 检查是否调用了 `Circuit.quitAedt()`

### 症状：项目意外关闭

- 检查是否调用了 `close()` 方法
- `releaseDesktop()` 不会关闭项目
