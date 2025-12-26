#!/usr/bin/env python3
"""
N8n Blender插件打包脚本

此脚本用于将N8n Blender插件打包为Blender可用的ZIP格式。
使用方法:
1. 在命令行中运行: python build.py
2. 生成的ZIP文件将保存在dist目录中

注意: 需要安装zip命令行工具或Python的zipfile模块
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
import json
from datetime import datetime

# 插件信息
ADDON_NAME = "N8n_Blender_node"
VERSION = "0.1.0"

def get_version_info():
    """从blender_manifest.toml获取版本信息"""
    manifest_path = Path(__file__).parent / "blender_manifest.toml"
    
    if not manifest_path.exists():
        return VERSION
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 简单解析版本号
        for line in content.split('\n'):
            if line.startswith('version = '):
                version_str = line.split('=')[1].strip().strip('"')
                return version_str
    except Exception:
        pass
    
    return VERSION

def create_dist_dir():
    """创建分发目录"""
    dist_dir = Path(__file__).parent / "dist"
    dist_dir.mkdir(exist_ok=True)
    return dist_dir

def create_package(addon_dir, dist_dir, version):
    """创建插件包"""
    # 构建ZIP文件名
    zip_name = f"{ADDON_NAME}_v{version}.zip"
    zip_path = dist_dir / zip_name
    
    # 创建ZIP文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历插件目录中的所有文件
        for root, dirs, files in os.walk(addon_dir):
            # 跳过构建和分发目录
            if 'dist' in dirs:
                dirs.remove('dist')
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')
            if '.git' in dirs:
                dirs.remove('.git')
                
            for file in files:
                # 跳过不需要的文件
                if file.endswith('.pyc') or file.endswith('.pyo'):
                    continue
                if file == '.DS_Store':
                    continue
                if file == 'build.py':
                    continue
                    
                file_path = Path(root) / file
                # 计算相对路径，确保ZIP文件中包含插件根目录
                arcname = ADDON_NAME / file_path.relative_to(addon_dir)
                
                # 添加文件到ZIP
                zipf.write(file_path, arcname)
    
    return zip_path

def create_package_info(dist_dir, version, zip_path):
    """创建包信息文件"""
    info = {
        "name": ADDON_NAME,
        "version": version,
        "filename": zip_path.name,
        "size": zip_path.stat().st_size,
        "created": datetime.now().isoformat(),
        "blender_version_min": "3.5.0",
        "description": "N8n工作流编辑器Blender插件"
    }
    
    info_path = dist_dir / f"{ADDON_NAME}_v{version}_info.json"
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    
    return info_path

def main():
    """主函数"""
    print(f"正在构建 {ADDON_NAME} 插件包...")
    
    # 获取插件目录
    addon_dir = Path(__file__).parent
    
    # 获取版本信息
    version = get_version_info()
    print(f"插件版本: {version}")
    
    # 创建分发目录
    dist_dir = create_dist_dir()
    print(f"分发目录: {dist_dir}")
    
    # 创建插件包
    zip_path = create_package(addon_dir, dist_dir, version)
    print(f"插件包已创建: {zip_path}")
    
    # 创建包信息文件
    info_path = create_package_info(dist_dir, version, zip_path)
    print(f"包信息文件已创建: {info_path}")
    
    print("\n构建完成!")
    print(f"文件大小: {zip_path.stat().st_size / 1024:.2f} KB")
    print("\n安装方法:")
    print("1. 打开Blender")
    print("2. 进入 编辑 > 偏好设置 > 插件")
    print("3. 点击 '安装...' 按钮")
    print(f"4. 选择生成的ZIP文件: {zip_path}")
    print("5. 启用插件")

if __name__ == "__main__":
    main()