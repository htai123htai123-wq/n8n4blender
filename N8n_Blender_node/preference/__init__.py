"""
N8n Blender Node - 偏好设置
提供插件的配置选项
"""

import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import AddonPreferences

# 尝试导入翻译函数
try:
    from ..i18n import _
except ImportError:
    def _(text):
        return text

class N8nAddonPreferences(AddonPreferences):
    """N8n插件偏好设置"""
    bl_idname = __package__

    # API URL
    api_url: StringProperty(
        name=_("API URL"),
        description=_("N8n API URL"),
        default="http://localhost:5678",
    )

    # API密钥
    api_key: StringProperty(
        name=_("API Key"),
        description=_("N8n API Key"),
        default="",
        subtype="PASSWORD"
    )

    # 自动连接
    auto_connect: BoolProperty(
        name=_("Auto Connect"),
        description=_("Automatically connect to N8n on startup"),
        default=True,
    )

    # 调试模式
    debug_mode: BoolProperty(
        name=_("Debug Mode"),
        description=_("Enable debug logging"),
        default=False,
    )

    # 主题
    theme: EnumProperty(
        name=_("Theme"),
        description=_("UI Theme"),
        items=[
            ("DEFAULT", _("Default"), _("Default theme")),
            ("DARK", _("Dark"), _("Dark theme")),
            ("LIGHT", _("Light"), _("Light theme")),
        ],
        default="DEFAULT",
    )

    # 语言
    language: EnumProperty(
        name=_("Language"),
        description=_("Interface Language"),
        items=[
            ("en", _("English"), _("English")),
            ("zh_CN", _("Chinese (Simplified)"), _("Chinese (Simplified)")),
            ("zh_TW", _("Chinese (Traditional)"), _("Chinese (Traditional)")),
        ],
        default="en",
    )

    def draw(self, context):
        """绘制偏好设置界面"""
        layout = self.layout

        # API设置
        box = layout.box()
        box.label(text=_("API Settings"))
        box.prop(self, "api_url")
        box.prop(self, "api_key")

        # 连接设置
        box = layout.box()
        box.label(text=_("Connection Settings"))
        box.prop(self, "auto_connect")

        # UI设置
        box = layout.box()
        box.label(text=_("UI Settings"))
        box.prop(self, "theme")
        box.prop(self, "language")

        # 高级设置
        box = layout.box()
        box.label(text=_("Advanced Settings"))
        box.prop(self, "debug_mode")

def register():
    """注册偏好设置"""
    bpy.utils.register_class(N8nAddonPreferences)

def unregister():
    """注销偏好设置"""
    bpy.utils.unregister_class(N8nAddonPreferences)