import bpy
from bpy.types import Operator

class N8N_OT_add_node_tree(Operator):
    """添加n8n节点树"""
    bl_idname = "node.n8n_node_tree_add"
    bl_label = "Add n8n Workflow"
    bl_description = "Add a new n8n workflow node tree"
    
    def execute(self, context):
        # 创建新的节点树
        node_tree = bpy.data.node_trees.new("n8n Workflow", type="N8nNodeTreeType")
        
        # 切换到节点编辑器并显示新工作流
        if context.area.type != 'NODE_EDITOR':
            context.area.type = 'NODE_EDITOR'
        
        context.space_data.node_tree = node_tree
        
        return {'FINISHED'}

class N8N_OT_add_node_menu(Operator):
    """打开n8n节点菜单"""
    bl_idname = "n8n.add_node_menu"
    bl_label = "Add n8n Node"
    bl_description = "Open the n8n node menu"
    
    def execute(self, context):
        # 打开节点菜单
        bpy.ops.wm.call_menu(name="N8N_MT_node_menu")
        return {'FINISHED'}

# 导入其他操作模块
from .workflow_ops import register as register_workflow_ops, unregister as unregister_workflow_ops
from .node_ops import register as register_node_ops, unregister as unregister_node_ops

classes = [
    N8N_OT_add_node_tree,
    N8N_OT_add_node_menu,
]

def register():
    # 注册基础操作类
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # 注册其他操作模块
    register_workflow_ops()
    register_node_ops()
  
def unregister():
    # 注销其他操作模块
    unregister_workflow_ops()
    unregister_node_ops()
    
    # 注销基础操作类
    for cls in classes:
        bpy.utils.unregister_class(cls)