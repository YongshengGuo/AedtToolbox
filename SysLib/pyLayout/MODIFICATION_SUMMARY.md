# AEDT 释放问题 - 修复总结

## 问题描述
执行 `releaseDesktop()` 后无法正常关闭AEDT，出现错误：
```
Electronics Desktop cannot be closed right now because it is being used 
by another application, script or extension wizard.
```

## 根本原因分析

### 原始实现的缺陷
1. **不完整的释放流程**
   - `releaseDesktop()` 只删除了Python模块中的对象引用
   - 没有调用AEDT API来关闭窗口或应用程序
   - AEDT进程仍在后台运行

2. **持久的资源占用**
   - Circuit 或 PyLayout 对象仍持有 `_oDesktop` 引用
   - 打开的项目 (`oProject`) 和设计 (`oDesign`) 仍未关闭
   - 这些活跃对象阻止了AEDT的正常关闭

3. **缺失关键步骤**
   - 没有调用 `oDesktop.CloseAllWindows()`
   - 没有调用 `oDesktop.QuitApplication()`

## 实施的修复

### 1. desktop.py 修改

#### 新增函数：`_closeAllProjects()`
```python
def _closeAllProjects():
    '''关闭所有打开的AEDT窗口'''
    # 获取oDesktop引用
    # 调用 oDesktop.CloseAllWindows()
    # 异常处理和日志记录
```
**作用**: 在删除引用前，先释放AEDT的所有窗口资源

#### 改进函数：`_delete_objects()`
```python
def _delete_objects():
    module = sys.modules["__main__"]
    
    # 首先关闭所有窗口
    _closeAllProjects()
    
    # 然后删除引用（包括新增的 _oDesktop）
    # ...
```
**改动**:
- 调用 `_closeAllProjects()` 关闭窗口
- 删除 `module._oDesktop` 引用（新增）

#### 完整函数：`releaseDesktop()`
```python
def releaseDesktop():
    module = sys.modules['__main__']
    try:
        # 1. 获取 oDesktop 引用（尝试 _oDesktop 和 oDesktop）
        oDesktop = getattr(module, "_oDesktop", None) or getattr(module, "oDesktop", None)
        
        if oDesktop:
            # 2. 关闭所有窗口
            oDesktop.CloseAllWindows()
            
            # 3. 退出AEDT应用
            oDesktop.QuitApplication()
        
        # 4. 清理所有引用
        _delete_objects()
        return True
        
    except Exception as e:
        # 异常处理
        try:
            _delete_objects()
        except Exception:
            pass
        return False
```
**改动**:
- 尝试获取两种引用方式
- 显式调用 `CloseAllWindows()` 和 `QuitApplication()`
- 更好的异常处理

### 2. circuit.py 修改

#### 改进函数：`Circuit.release()`
```python
def release(self):
    '''正确释放所有Circuit资源'''
    try:
        # 1. 先关闭打开的项目
        if self._oProject is not None:
            self.close(save=True)
    except Exception as e:
        log.warning("Error closing project: %s" % str(e))
    
    try:
        # 2. 清理内部引用
        self._info = None
        self._oEditor = None
        self._oDesign = None
        self._oProject = None
        self._oDesktop = None
        import gc
        gc.collect()
    except AttributeError:
        pass
    
    # 3. 最后释放AEDT
    releaseDesktop()
```
**改动**:
- 先关闭项目（如果存在）
- 再清理内部引用
- 最后释放全局AEDT

#### 修改函数：`Circuit.__del__()`
**原代码**: 直接调用 `releaseDesktop()`
**新代码**: 空实现（只有注释）

**原因**: 
- `__del__` 在垃圾回收时触发，时机不确定
- 不应该在析构函数中关闭全局AEDT实例
- 用户应该显式调用 `release()` 方法

## 修复效果

### 释放流程图
```
新的释放流程（改进后）：
━━━━━━━━━━━━━━━━━━━━━━━
Circuit.release()
  ↓
检查 _oProject 是否存在
  ↓ (存在)
调用 circuit.close(save=True)
  ↓
清理内部引用
  ↓
调用 releaseDesktop()
  ├─ 获取 oDesktop 引用
  ├─ 调用 oDesktop.CloseAllWindows() ← 关键改进
  ├─ 调用 oDesktop.QuitApplication() ← 关键改进
  └─ 调用 _delete_objects()
      ├─ 调用 _closeAllProjects()
      └─ 删除所有引用（包括 _oDesktop）
      
结果：AEDT完全关闭 ✓
```

### 解决的问题
1. ✓ AEDT 窗口会被正确关闭
2. ✓ AEDT 进程会被正确终止
3. ✓ 所有资源会被正确释放
4. ✓ 不再出现"被另一个应用使用"的错误

## 使用建议

### 推荐用法（最安全）
```python
from pyLayout.circuit import Circuit

layout = Circuit()
try:
    layout.initDesign("MyProject", "MyDesign")
    # ... 进行设计操作 ...
finally:
    layout.release()  # 确保释放
```

### 其他用法
```python
# 方式1：仅使用 Circuit 对象
layout.release()

# 方式2：仅关闭AEDT
from pyLayout.desktop import releaseDesktop
releaseDesktop()

# 方式3：使用 PyLayout
from pyLayout import PyLayout
layout = PyLayout()
layout.release()

# 方式4：仅关闭AEDT窗口
Circuit.quitAedt()
```

## 相关文件

1. **修复文件**
   - `/desktop.py` - AEDT 初始化和释放
   - `/circuit/circuit.py` - Circuit 类释放方法

2. **文档文件**
   - `/AEDT_RELEASE_GUIDE.md` - 详细使用指南
   - `/test_aedt_release.py` - 测试脚本

3. **记忆文件**
   - `/memories/repo/aedt_release_issue.md` - 详细分析

## 测试方法

运行提供的测试脚本：
```bash
python test_aedt_release.py
```

这将测试4种释放方式的效果。

## 注意事项

1. **多实例问题**
   - 所有Circuit对象共享同一个全局 `oDesktop`
   - 不要同时创建多个Circuit对象
   - 如需多个独立实例，使用 `newDesktop=True`

2. **时序问题**
   - `QuitApplication()` 是异步操作
   - 释放后可能需要等待：`time.sleep(2)`

3. **异常处理**
   - `release()` 已包含异常处理
   - 即使项目关闭失败，也会继续释放AEDT

4. **隐式释放**
   - `PyLayout.__del__()` 会在析构时调用 `_safeReleaseDesktop()`
   - 但不应该依赖此行为，显式调用 `release()` 更安全
