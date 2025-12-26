import bpy
from .n8n_blueprints import node_blueprints, node_blueprints_by_group

# 节点添加菜单集成
def draw_add_menu(self, context):
    layout = self.layout
    layout.menu("N8N_MT_node_menu", text="n8n")

# 注册函数，完全手动控制菜单类的注册
# 将菜单类定义在函数内部，避免auto_load模块扫描到它
def register():
    """注册菜单"""
    try:
        # 检查菜单类是否已经注册
        if not hasattr(bpy.types, "N8N_MT_node_menu"):
            # 定义菜单类
            class N8N_MT_node_menu(bpy.types.Menu):
                """n8n节点菜单"""
                bl_idname = "N8N_MT_node_menu"
                bl_label = "n8n Nodes"
                
                def draw(self, context):
                    layout = self.layout
                    
                    # 按组显示节点
                    for group in sorted(node_blueprints_by_group.keys()):
                        # 创建子菜单
                        box = layout.box()
                        box.label(text=group.capitalize())
                        
                        # 添加该组的所有节点
                        for blueprint in node_blueprints_by_group[group]:
                            operator = box.operator("n8n.add_node", text=blueprint["name"])
                            operator.blueprint_id = blueprint["id"]
            
            # 注册菜单类
            bpy.utils.register_class(N8N_MT_node_menu)
        
        # 添加到节点添加菜单
        bpy.types.NODE_MT_add.prepend(draw_add_menu)
    except Exception as e:
        # 忽略已存在的错误
        pass

# 注销函数，完全手动控制菜单类的注销
def unregister():
    """注销菜单"""
    try:
        # 从节点添加菜单移除
        bpy.types.NODE_MT_add.remove(draw_add_menu)
        
        # 注销菜单类
        if hasattr(bpy.types, "N8N_MT_node_menu"):
            menu_cls = getattr(bpy.types, "N8N_MT_node_menu")
            if hasattr(menu_cls, "is_registered") and menu_cls.is_registered:
                bpy.utils.unregister_class(menu_cls)
            elif not hasattr(menu_cls, "is_registered"):
                # 对于没有is_registered属性的类，直接尝试注销
                bpy.utils.unregister_class(menu_cls)
    except Exception as e:
        # 忽略移除失败的错误
        pass
