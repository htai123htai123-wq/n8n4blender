"""
N8n Blender Node - 国际化支持
提供插件的多语言支持功能
"""

import bpy
import os
from bpy.app.translations import locale

# 尝试导入翻译字典
try:
    from .dictionary import dictionary
except ImportError:
    dictionary = {}

def _(text):
    """
    翻译函数
    根据当前语言环境返回对应的翻译文本
    """
    # 获取当前语言环境
    current_language = locale.language
    
    # 如果当前语言在字典中，返回对应的翻译
    if current_language in dictionary and text in dictionary[current_language]:
        return dictionary[current_language][text]
    
    # 如果没有找到翻译，返回原文
    return text

def register():
    """
    注册国际化支持
    """
    # 注册翻译字典到Blender
    if dictionary:
        bpy.app.translations.register(__name__, dictionary)

def unregister():
    """
    注销国际化支持
    """
    # 从Blender注销翻译字典
    if dictionary:
        bpy.app.translations.unregister(__name__)