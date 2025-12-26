#!/usr/bin/env python3
"""
N8n Blender插件安装脚本

此脚本帮助用户将N8n Blender插件安装到Blender中。
使用方法:
1. 在命令行中运行: python install.py
2. 或者在Blender脚本窗口中运行此脚本

注意: 需要管理员权限才能写入Blender安装目录
"""

import os
import sys
import shutil
import platform
from pathlib import Path

# 插件名称
ADDON_NAME = "N8n_Blender_node"

def get_blender_addon_paths():
    """获取可能的Blender插件安装路径"""
    system = platform.system()
    paths = []
    
    if system == "Windows":
        # Windows系统路径
        paths.append(Path(os.environ.get("APPDATA", "")) / "Blender Foundation" / "Blender")
    elif system == "Darwin":  # macOS
        # macOS系统路径
        paths.append(Path.home() / "Library" / "Application Support" / "Blender")
    elif system == "Linux":
        # Linux系统路径
        paths.append(Path.home() / ".config" / "blender")
    
    # 查找所有可能的Blender版本目录
    addon_paths = []
    for base_path in paths:
        if base_path.exists():
            for blender_version in base_path.iterdir():
                scripts_path = blender_version / "scripts" / "addons"
                if scripts_path.exists():
                    addon_paths.append(scripts_path)
    
    return addon_paths

def install_addon(addon_path, source_dir):
    """安装插件到指定路径"""
    target_dir = addon_path / ADDON_NAME
    
    # 如果目标目录已存在，先删除
    if target_dir.exists():
        print(f"删除现有插件目录: {target_dir}")
        shutil.rmtree(target_dir)
    
    # 复制插件目录
    print(f"安装插件到: {target_dir}")
    shutil.copytree(source_dir, target_dir)
    
    return True

def main():
    """主安装函数"""
    # 获取当前脚本所在目录
    script_dir = Path(__file__).parent
    source_dir = script_dir
    
    # 获取所有可能的Blender插件路径
    addon_paths = get_blender_addon_paths()
    
    if not addon_paths:
        print("错误: 未找到Blender安装目录")
        print("请确保已安装Blender，或手动将插件复制到Blender插件目录")
        return False
    
    print(f"找到 {len(addon_paths)} 个Blender插件安装路径:")
    for i, path in enumerate(addon_paths, 1):
        print(f"{i}. {path}")
    
    # 如果只有一个路径，直接安装
    if len(addon_paths) == 1:
        try:
            success = install_addon(addon_paths[0], source_dir)
            if success:
                print("\n插件安装成功!")
                print("请在Blender中启用插件:")
                print("1. 打开Blender")
                print("2. 进入 编辑 > 偏好设置 > 插件")
                print("3. 搜索 'N8n'")
                print("4. 勾选启用插件")
                return True
        except Exception as e:
            print(f"安装失败: {e}")
            return False
    else:
        # 多个路径，让用户选择
        print("\n请选择要安装的Blender版本 (输入数字):")
        for i, path in enumerate(addon_paths, 1):
            version = path.parent.parent.name
            print(f"{i}. Blender {version}")
        
        try:
            choice = int(input("请输入选项: ")) - 1
            if 0 <= choice < len(addon_paths):
                success = install_addon(addon_paths[choice], source_dir)
                if success:
                    print("\n插件安装成功!")
                    print("请在Blender中启用插件:")
                    print("1. 打开Blender")
                    print("2. 进入 编辑 > 偏好设置 > 插件")
                    print("3. 搜索 'N8n'")
                    print("4. 勾选启用插件")
                    return True
            else:
                print("无效的选择")
                return False
        except ValueError:
            print("请输入有效的数字")
            return False
        except Exception as e:
            print(f"安装失败: {e}")
            return False

if __name__ == "__main__":
    main()