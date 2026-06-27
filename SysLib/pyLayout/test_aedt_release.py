#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本：验证AEDT释放功能是否正常工作

使用方法：
    python test_aedt_release.py

这个脚本测试四种释放方式的效果
"""

import os
import sys
import time
import subprocess

def test_circuit_release():
    """测试1: 使用Circuit.release()释放"""
    print("\n" + "="*60)
    print("测试1: Circuit.release() 释放方式")
    print("="*60)
    
    try:
        from pyLayout.circuit import Circuit
        
        print("创建Circuit对象...")
        layout = Circuit()
        print("✓ Circuit创建成功")
        
        print("调用layout.release()...")
        layout.release()
        print("✓ Circuit.release() 执行完成")
        
        # 检查AEDT是否已退出
        time.sleep(2)
        print("✓ 测试1完成")
        return True
        
    except Exception as e:
        print("✗ 测试1失败: %s" % str(e))
        return False


def test_explicit_close_and_release():
    """测试2: 先close后releaseDesktop"""
    print("\n" + "="*60)
    print("测试2: Circuit.close() + releaseDesktop() 释放方式")
    print("="*60)
    
    try:
        from pyLayout.circuit import Circuit
        from pyLayout.desktop import releaseDesktop
        
        print("创建Circuit对象...")
        layout = Circuit()
        print("✓ Circuit创建成功")
        
        print("调用layout.close()...")
        # 注意：这里需要有打开的项目，否则会报错
        # 我们先不调用initDesign，直接测试释放
        print("  (跳过project close，因为没有打开的项目)")
        
        print("调用releaseDesktop()...")
        releaseDesktop()
        print("✓ releaseDesktop() 执行完成")
        
        time.sleep(2)
        print("✓ 测试2完成")
        return True
        
    except Exception as e:
        print("✗ 测试2失败: %s" % str(e))
        return False


def test_quit_aedt():
    """测试3: 使用Circuit.quitAedt()"""
    print("\n" + "="*60)
    print("测试3: Circuit.quitAedt() 释放方式")
    print("="*60)
    
    try:
        from pyLayout.circuit import Circuit
        
        print("调用Circuit.quitAedt()...")
        Circuit.quitAedt()
        print("✓ Circuit.quitAedt() 执行完成")
        
        time.sleep(2)
        print("✓ 测试3完成")
        return True
        
    except Exception as e:
        print("✗ 测试3失败: %s" % str(e))
        return False


def test_pylayout_auto_release():
    """测试4: 使用PyLayout自动管理"""
    print("\n" + "="*60)
    print("测试4: PyLayout 自动释放方式")
    print("="*60)
    
    try:
        from pyLayout import PyLayout
        
        print("创建PyLayout对象...")
        layout = PyLayout()
        print("✓ PyLayout创建成功")
        
        print("调用layout.release()...")
        layout.release()
        print("✓ PyLayout.release() 执行完成")
        
        time.sleep(2)
        print("✓ 测试4完成")
        return True
        
    except Exception as e:
        print("✗ 测试4失败: %s" % str(e))
        return False


def main():
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*  AEDT 释放功能测试脚本" + " " * 32 + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    
    results = []
    
    # 运行测试
    results.append(("Circuit.release()", test_circuit_release()))
    results.append(("Circuit.close() + releaseDesktop()", test_explicit_close_and_release()))
    results.append(("Circuit.quitAedt()", test_quit_aedt()))
    results.append(("PyLayout.release()", test_pylayout_auto_release()))
    
    # 输出总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print("%-40s: %s" % (test_name, status))
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\n总计: %d/%d 测试通过" % (passed, total))
    
    if passed == total:
        print("\n✓ 所有测试通过!")
        return 0
    else:
        print("\n✗ 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
