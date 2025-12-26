import bpy
from bpy.types import Operator
from ..manager.n8n_manager import global_manager
from ..nodes.n8n_blueprints import node_blueprints

class N8N_OT_add_node(Operator):
    """添加n8n节点"""
    bl_idname = "n8n.add_node"
    bl_label = "Add n8n Node"
    bl_description = "Add a new n8n node to the workflow"
    bl_options = {'REGISTER', 'UNDO'}
    
    # 节点蓝图ID
    blueprint_id: bpy.props.StringProperty(
        name="Blueprint ID",
        description="ID of the node blueprint to use",
        default=""
    )
    
    def execute(self, context):
        """
        执行添加节点操作
        """
        # 检查是否有活动的节点树
        if not context.space_data.node_tree:
            self.report({'ERROR'}, "No active node tree")
            return {'CANCELLED'}
        
        # 检查节点树类型
        if context.space_data.node_tree.bl_idname != "N8nNodeTreeType":
            self.report({'ERROR'}, "Active node tree is not an n8n node tree")
            return {'CANCELLED'}
        
        # 检查蓝图是否存在
        if self.blueprint_id not in node_blueprints:
            self.report({'ERROR'}, f"Blueprint '{self.blueprint_id}' not found")
            return {'CANCELLED'}
        
        # 创建节点
        node_tree = context.space_data.node_tree
        
        # 计算节点位置（在鼠标位置附近）
        location = (0, 0)
        if context.space_data.cursor_location:
            location = context.space_data.cursor_location
        
        # 从蓝图创建节点
        node = global_manager.create_node_from_blueprint(node_tree, self.blueprint_id, location)
        
        if not node:
            self.report({'ERROR'}, f"Failed to create node from blueprint '{self.blueprint_id}'")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"Node '{node.name}' created successfully")
        return {'FINISHED'}

# 注册运算符
def register():
    bpy.utils.register_class(N8N_OT_add_node)

# 注销运算符
def unregister():
    bpy.utils.unregister_class(N8N_OT_add_node)
