#!/usr/bin/env python3
"""
N8n Blender插件卸载脚本

此脚本帮助用户从Blender中卸载N8n Blender插件。
使用方法:
1. 在命令行中运行: python uninstall.py
2. 或者在Blender脚本窗口中运行此脚本

注意: 需要管理员权限才能删除Blender安装目录中的文件
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

def find_installed_addons(addon_paths):
    """查找已安装的插件"""
    installed_addons = []
    
    for addon_path in addon_paths:
        addon_dir = addon_path / ADDON_NAME
        if addon_dir.exists():
            installed_addons.append((addon_path, addon_dir))
    
    return installed_addons

def uninstall_addon(addon_dir):
    """卸载插件"""
    try:
        print(f"删除插件目录: {addon_dir}")
        shutil.rmtree(addon_dir)
        return True
    except Exception as e:
        print(f"卸载失败: {e}")
        return False

def main():
    """主卸载函数"""
    # 获取所有可能的Blender插件路径
    addon_paths = get_blender_addon_paths()
    
    if not addon_paths:
        print("错误: 未找到Blender安装目录")
        return False
    
    # 查找已安装的插件
    installed_addons = find_installed_addons(addon_paths)
    
    if not installed_addons:
        print("未找到已安装的N8n Blender插件")
        return True
    
    print(f"找到 {len(installed_addons)} 个已安装的插件实例:")
    for i, (addon_path, addon_dir) in enumerate(installed_addons, 1):
        version = addon_path.parent.parent.name
        print(f"{i}. Blender {version} - {addon_dir}")
    
    # 如果只有一个实例，直接卸载
    if len(installed_addons) == 1:
        try:
            success = uninstall_addon(installed_addons[0][1])
            if success:
                print("\n插件卸载成功!")
                print("建议重启Blender以确保完全卸载")
                return True
        except Exception as e:
            print(f"卸载失败: {e}")
            return False
    else:
        # 多个实例，让用户选择
        print("\n请选择要卸载的Blender版本 (输入数字):")
        for i, (addon_path, addon_dir) in enumerate(installed_addons, 1):
            version = addon_path.parent.parent.name
            print(f"{i}. Blender {version}")
        
        try:
            choice = int(input("请输入选项: ")) - 1
            if 0 <= choice < len(installed_addons):
                success = uninstall_addon(installed_addons[choice][1])
                if success:
                    print("\n插件卸载成功!")
                    print("建议重启Blender以确保完全卸载")
                    return True
            else:
                print("无效的选择")
                return False
        except ValueError:
            print("请输入有效的数字")
            return False
        except Exception as e:
            print(f"卸载失败: {e}")
            return False

if __name__ == "__main__":
    main()