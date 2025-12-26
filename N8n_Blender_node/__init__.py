import bpy
import os

from .config import __addon_name__

# 尝试导入翻译字典
try:
    from .i18n.dictionary import dictionary
except ImportError:
    dictionary = {}

# 尝试导入自动加载器
try:
    from ...common.class_loader import auto_load
    from ...common.class_loader.auto_load import add_properties, remove_properties
    from ...common.i18n.dictionary import common_dictionary
    from ...common.i18n.i18n import load_dictionary
except ImportError:
    # 如果无法导入common模块，则使用备用方法
    auto_load = None
    
    def add_properties(properties):
        """备用属性添加函数"""
        for cls, props in properties.items():
            for name, prop in props.items():
                setattr(cls, name, prop)
    
    def remove_properties(properties):
        """备用属性移除函数"""
        for cls, props in properties.items():
            for name in props:
                if hasattr(cls, name):
                    delattr(cls, name)
    
    def load_dictionary(dictionary):
        """备用字典加载函数"""
        pass
    
    common_dictionary = {}

# Add-on info
bl_info = {
    "name": "n8n Workflow Editor",
    "author": "n8n Community",
    "blender": (3, 5, 0),
    "version": (0, 1, 0),
    "description": "n8n workflow editor for Blender",
    "warning": "",
    "doc_url": "https://docs.n8n.io/",
    "tracker_url": "https://github.com/n8n-io/n8n",
    "support": "COMMUNITY",
    "category": "Node"
}

_addon_properties = {
    bpy.types.Scene: {
        "n8n_active_workflow_index": bpy.props.IntProperty(
            name="Active Workflow Index",
            description="Index of the active workflow in the list",
            default=0
        ),
    },
}

def register():
    # Register classes
    if auto_load:
        auto_load.init()
        auto_load.register()
    else:
        # 备用注册方法
        import importlib
        
        # 注册所有模块
        modules = [
            ".operators",
            ".nodes",
            ".ui",
            ".panels",
            ".preference",
            ".utils",
            ".i18n",
        ]
        
        for module in modules:
            try:
                mod = importlib.import_module(module, package=__package__)
                if hasattr(mod, "register"):
                    mod.register()
            except ImportError:
                print(f"Warning: Could not import module {module}")
    
    add_properties(_addon_properties)

    # Internationalization
    load_dictionary(dictionary)
    if dictionary:
        bpy.app.translations.register(__addon_name__, dictionary)
    if common_dictionary:
        bpy.app.translations.register(__addon_name__, common_dictionary)

    # Add node tree type to menu
    bpy.types.NODE_MT_add.append(menu_func_add)
    
    # Add keymap
    add_node_editor_keymap()

    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # Remove keymap
    remove_node_editor_keymap()
    
    # Remove node tree type from menu
    bpy.types.NODE_MT_add.remove(menu_func_add)
    
    # Internationalization
    if dictionary:
        bpy.app.translations.unregister(__addon_name__)
    if common_dictionary:
        bpy.app.translations.unregister(__addon_name__)
    
    # Unregister classes
    if auto_load:
        auto_load.unregister()
    else:
        # 备用注销方法
        import importlib
        
        # 注销所有模块
        modules = [
            ".i18n",
            ".utils",
            ".preference",
            ".panels",
            ".ui",
            ".nodes",
            ".operators",
        ]
        
        for module in modules:
            try:
                mod = importlib.import_module(module, package=__package__)
                if hasattr(mod, "unregister"):
                    mod.unregister()
            except ImportError:
                print(f"Warning: Could not import module {module}")
    
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))

def menu_func_add(self, context):
    """添加n8n节点树类型到菜单"""
    layout = self.layout
    layout.operator("node.n8n_node_tree_add", text="n8n Workflow", icon='NODETREE')

def add_node_editor_keymap():
    """添加节点编辑器快捷键"""
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Node Editor", space_type='NODE_EDITOR')
    
    # 添加快捷键
    kmi = km.keymap_items.new("n8n.add_node_menu", 'A', 'PRESS', shift=True)
    kmi = km.keymap_items.new("n8n.execute_workflow", 'E', 'PRESS', ctrl=True)
    kmi = km.keymap_items.new("n8n.reset_workflow", 'R', 'PRESS', ctrl=True)
    
    # 存储快捷键引用以便后续删除
    addon_keymaps.append(km)

def remove_node_editor_keymap():
    """移除节点编辑器快捷键"""
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

# 存储快捷键引用
addon_keymaps = []