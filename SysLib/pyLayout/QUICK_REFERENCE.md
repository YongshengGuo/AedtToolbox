# 快速参考：AEDT 释放

## ✓ 正确做法

### 最简单的方式
```python
from pyLayout.circuit import Circuit

layout = Circuit()
# ... 使用layout ...
layout.release()  # 完成！
```

### 更安全的方式（推荐生产环境）
```python
from pyLayout.circuit import Circuit

layout = Circuit()
try:
    # ... 使用layout ...
finally:
    layout.release()
```

### 使用 PyLayout
```python
from pyLayout import PyLayout

layout = PyLayout()
# ... 使用layout ...
layout.release()  # 自动处理所有清理
```

## ✗ 错误做法

### ❌ 不要这样做
```python
# 错误1：期望 __del__ 自动释放
layout = Circuit()
# ... 使用 ...
del layout  # 可能不会立即释放！

# 错误2：直接删除引用
from pyLayout.desktop import releaseDesktop
# ... 使用 ...
del layout
releaseDesktop()  # layout可能仍在保持AEDT锁定

# 错误3：只关闭项目，不释放AEDT
layout.close()  # AEDT进程仍在运行

# 错误4：混合使用多个Circuit对象
layout1 = Circuit()
layout2 = Circuit()  # 会干扰layout1！
```

## 关键点

| 问题 | 原因 | 解决方案 |
|------|------|--------|
| AEDT 窗口无法关闭 | `releaseDesktop()` 未调用 `QuitApplication()` | 已修复，现在自动调用 |
| 进程仍在运行 | 没有关闭所有打开的窗口 | 已修复，现在自动调用 `CloseAllWindows()` |
| 引用仍被保持 | 删除了 `oDesktop` 但保留了 `_oDesktop` | 已修复，现在删除两个引用 |
| 项目未关闭 | 直接释放而不关闭活跃项目 | 改进 `Circuit.release()` 先关闭项目 |

## 释放清单

- [ ] 完成所有设计操作
- [ ] 调用 `layout.close(save=True)` （可选，`release()` 会做）
- [ ] 调用 `layout.release()` ✓ **关键**
- [ ] 等待 2-3 秒（确保AEDT完全退出）
- [ ] 验证 AEDT 进程已消失

## 常见错误消息

### ❌ "Electronics Desktop cannot be closed right now"
**原因**: 有对象仍在持有AEDT资源
**解决**: 确保调用了 `layout.release()`，不是只删除引用

### ❌ "Project is open"
**原因**: 项目仍未关闭
**解决**: `release()` 会自动关闭，或显式调用 `layout.close(save=True)`

### ❌ "Permission denied"（在删除文件时）
**原因**: AEDT 仍在使用文件
**解决**: 先调用 `layout.release()`，再删除文件

## 相关方法速查表

```python
# Circuit 类方法
Circuit.quitAedt()          # 只关闭AEDT，不清理对象
Circuit.release()           # 完整释放（推荐）
circuit.close(save=True)    # 关闭项目，保留AEDT
circuit.release()           # 实例方法版本

# desktop 模块函数
releaseDesktop()            # 低级函数，通常不需要直接调用
initializeDesktop()         # 初始化AEDT

# PyLayout 类方法
layout.release()            # 自动判断是否需要释放AEDT
```

## 完整示例

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyLayout.circuit import Circuit
import time

def main():
    # 创建对象
    layout = Circuit()
    
    try:
        # 初始化设计
        layout.initDesign("MyProject", "MyDesign")
        print("Project: %s" % layout.ProjectPath)
        
        # 执行设计操作
        # layout.xxx_operations()
        
        # 保存项目
        layout.save()
        print("Project saved")
        
    finally:
        # 释放资源
        print("Releasing AEDT...")
        layout.release()
        print("✓ Released successfully")
        
        # 可选：等待确保AEDT完全退出
        time.sleep(2)

if __name__ == "__main__":
    main()
```

## 更多帮助

详见文档：
- `AEDT_RELEASE_GUIDE.md` - 完整使用指南
- `MODIFICATION_SUMMARY.md` - 技术细节
- `test_aedt_release.py` - 测试示例
