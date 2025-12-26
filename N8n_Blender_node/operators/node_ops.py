import bpy
from bpy.types import Operator, Menu
from bpy.props import StringProperty, EnumProperty
from ..nodes.n8n_node_base import N8nNodeBase

# Optional imports with fallbacks
try:
    from ..nodes.node_factory import get_nodes_data
except ImportError:
    def get_nodes_data():
        try:
            import json
            import os
            # 获取nodes.json文件路径
            nodes_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nodes", "nodes.json")
            
            with open(nodes_file, 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)
            
            return nodes_data
        except Exception as e:
            print(f"Error loading nodes data: {e}")
            return {}

try:
    from ..i18n.dictionary import _
except ImportError:
    def _(text):
        return text

# 添加节点操作
class N8N_OT_add_node(Operator):
    """添加n8n节点"""
    bl_idname = "n8n.add_node"
    bl_label = "Add Node"
    bl_description = "Add a new n8n node to the workflow"
    
    node_type: StringProperty(
        name="Node Type",
        description="Type of the node to add"
    )
    
    def execute(self, context):
        # 获取当前节点树
        node_tree = context.space_data.node_tree
        
        if not node_tree:
            self.report({'ERROR'}, "No active node tree")
            return {'CANCELLED'}
        
        # 创建节点
        node_class_name = f"N8nNode_{self.node_type}"
        
        # 检查节点类是否存在
        if not hasattr(bpy.types, node_class_name):
            self.report({'ERROR'}, f"Node type not found: {self.node_type}")
            return {'CANCELLED'}
        
        # 添加节点
        node = node_tree.nodes.new(type=node_class_name)
        
        # 设置节点位置为光标位置
        if hasattr(context, 'cursor_location'):
            node.location = context.cursor_location
        else:
            # 如果没有光标位置，使用视图中心
            for area in context.screen.areas:
                if area.type == 'NODE_EDITOR':
                    node.location = area.regions[0].view2d.region_to_view(0, 0)
                    break
        
        self.report({'INFO'}, f"Added node: {self.node_type}")
        
        return {'FINISHED'}

# 删除节点操作
class N8N_OT_delete_node(Operator):
    """删除n8n节点"""
    bl_idname = "n8n.delete_node"
    bl_label = "Delete Node"
    bl_description = "Delete the selected n8n node"
    
    def execute(self, context):
        # 获取选中的节点
        selected_nodes = context.selected_nodes
        
        if not selected_nodes:
            self.report({'ERROR'}, "No nodes selected")
            return {'CANCELLED'}
        
        # 删除选中的节点
        for node in selected_nodes:
            if isinstance(node, N8nNodeBase):
                node_tree = node.id_data
                node_tree.nodes.remove(node)
        
        self.report({'INFO', 'INFO'}, f"Deleted {len(selected_nodes)} node(s)")
        
        return {'FINISHED'}

# 复制节点操作
class N8N_OT_duplicate_node(Operator):
    """复制n8n节点"""
    bl_idname = "n8n.duplicate_node"
    bl_label = "Duplicate Node"
    bl_description = "Duplicate the selected n8n node"
    
    def execute(self, context):
        # 获取选中的节点
        selected_nodes = context.selected_nodes
        
        if not selected_nodes:
            self.report({'ERROR'}, "No nodes selected")
            return {'CANCELLED'}
        
        # 复制选中的节点
        for node in selected_nodes:
            if isinstance(node, N8nNodeBase):
                node_tree = node.id_data
                new_node = node.copy()
                # 稍微偏移位置
                new_node.location.x += 50
                new_node.location.y += 50
        
        self.report({'INFO', 'INFO'}, f"Duplicated {len(selected_nodes)} node(s)")
        
        return {'FINISHED'}

# 执行节点操作
class N8N_OT_execute_node(Operator):
    """执行n8n节点"""
    bl_idname = "n8n.execute_node"
    bl_label = "Execute Node"
    bl_description = "Execute the selected n8n node"
    
    def execute(self, context):
        # 获取选中的节点
        selected_nodes = context.selected_nodes
        
        if not selected_nodes:
            self.report({'ERROR'}, "No nodes selected")
            return {'CANCELLED'}
        
        # 执行选中的节点
        for node in selected_nodes:
            if isinstance(node, N8nNodeBase):
                success = node.execute()
                if not success:
                    self.report({'ERROR'}, f"Node {node.name} execution failed")
                    return {'CANCELLED'}
        
        self.report({'INFO', 'INFO'}, f"Executed {len(selected_nodes)} node(s)")
        
        return {'FINISHED'}

# 重置节点操作
class N8N_OT_reset_node(Operator):
    """重置n8n节点"""
    bl_idname = "n8n.reset_node"
    bl_label = "Reset Node"
    bl_description = "Reset the selected n8n node"
    
    def execute(self, context):
        # 获取选中的节点
        selected_nodes = context.selected_nodes
        
        if not selected_nodes:
            self.report({'ERROR'}, "No nodes selected")
            return {'CANCELLED'}
        
        # 重置选中的节点
        for node in selected_nodes:
            if isinstance(node, N8nNodeBase):
                node.reset()
        
        self.report({'INFO', 'INFO'}, f"Reset {len(selected_nodes)} node(s)")
        
        return {'FINISHED'}

# 节点菜单
class N8N_MT_node_menu(Menu):
    """n8n节点菜单"""
    bl_idname = "N8N_MT_node_menu"
    bl_label = "n8n Nodes"
    
    def draw(self, context):
        layout = self.layout
        
        # 获取节点数据
        nodes_data = get_nodes_data()
        
        # 按类别分组
        categories = {}
        for node_type, node_data in nodes_data.items():
            category = node_data.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append((node_type, node_data.get('displayName', node_type)))
        
        # 绘制菜单
        for category, nodes in sorted(categories.items()):
            # 添加类别标题
            layout.label(text=category)
            
            # 添加节点
            for node_type, display_name in sorted(nodes):
                op = layout.operator(N8N_OT_add_node.bl_idname, text=display_name)
                op.node_type = node_type
            
            # 添加分隔符
            layout.separator()

# 节点搜索菜单
class N8N_MT_node_search_menu(Menu):
    """n8n节点搜索菜单"""
    bl_idname = "N8N_MT_node_search_menu"
    bl_label = "Search n8n Nodes"
    
    def draw(self, context):
        layout = self.layout
        
        # 添加搜索框
        layout.operator("n8n.search_nodes", text="Search Nodes...")
        
        layout.separator()
        
        # 添加最近使用的节点
        layout.label(text="Recent Nodes:")
        
        # 这里可以添加最近使用的节点逻辑
        layout.label(text="No recent nodes")

# 搜索节点操作
class N8N_OT_search_nodes(Operator):
    """搜索n8n节点"""
    bl_idname = "n8n.search_nodes"
    bl_label = "Search Nodes"
    bl_description = "Search for n8n nodes"
    
    search_query: StringProperty(
        name="Search Query",
        description="Query to search for nodes",
        default=""
    )
    
    def execute(self, context):
        # 这里可以实现搜索逻辑
        # 暂时只显示搜索结果
        self.report({'INFO'}, f"Searching for: {self.search_query}")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # 显示搜索对话框
        return context.window_manager.invoke_props_dialog(self)

# 节点上下文菜单
class N8N_MT_node_context_menu(Menu):
    """n8n节点上下文菜单"""
    bl_idname = "N8N_MT_node_context_menu"
    bl_label = "n8n Node"
    
    def draw(self, context):
        layout = self.layout
        
        # 添加节点操作
        layout.operator(N8N_OT_execute_node.bl_idname, text="Execute")
        layout.operator(N8N_OT_reset_node.bl_idname, text="Reset")
        layout.separator()
        layout.operator(N8N_OT_duplicate_node.bl_idname, text="Duplicate")
        layout.operator(N8N_OT_delete_node.bl_idname, text="Delete")

# 注册操作类
classes = [
    N8N_OT_add_node,
    N8N_OT_delete_node,
    N8N_OT_duplicate_node,
    N8N_OT_execute_node,
    N8N_OT_reset_node,
    N8N_MT_node_menu,
    N8N_MT_node_search_menu,
    N8N_OT_search_nodes,
    N8N_MT_node_context_menu,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)