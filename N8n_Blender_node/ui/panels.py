import bpy
from bpy.types import Panel, UIList
from bpy.props import StringProperty, BoolProperty, EnumProperty
from ..nodes.n8n_node_base import N8nNodeTree

# Optional import with fallback
try:
    from ..i18n.dictionary import _
except ImportError:
    def _(text):
        return text

# 工作流列表UI
class N8N_UL_workflows(UIList):
    """工作流列表UI"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # 获取节点树
        node_tree = item
        
        # 检查是否为n8n工作流
        if node_tree.bl_idname != "N8nNodeTreeType":
            return
        
        # 绘制工作流名称
        row = layout.row()
        row.prop(node_tree, "name", text="", emboss=False)
        
        # 显示执行状态
        status_icon = 'QUESTION'
        if node_tree.execution_state == 'SUCCESS':
            status_icon = 'CHECKMARK'
        elif node_tree.execution_state == 'ERROR':
            status_icon = 'ERROR'
        elif node_tree.execution_state == 'RUNNING':
            status_icon = 'TIME'
        
        row.prop(node_tree, "execution_state", text="", icon_only=True)
        
        # 显示最后执行时间
        if node_tree.last_execution_time:
            row.label(text=node_tree.last_execution_time)

# 工作流面板
class N8N_PT_workflow_panel(Panel):
    """n8n工作流面板"""
    bl_label = "n8n Workflows"
    bl_idname = "N8N_PT_workflow_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "n8n"
    
    def draw(self, context):
        layout = self.layout
        
        # 工作流列表
        row = layout.row()
        row.template_list(
            "N8N_UL_workflows", "",
            bpy.data, "node_trees",
            context.scene, "n8n_active_workflow_index",
            rows=5
        )
        
        # 工作流操作按钮
        col = row.column(align=True)
        col.operator("n8n.new_workflow", text="", icon='ADD')
        col.operator("n8n.open_workflow", text="", icon='FILEBROWSER')
        col.operator("n8n.duplicate_workflow", text="", icon='DUPLICATE')
        col.operator("n8n.delete_workflow", text="", icon='TRASH')
        
        layout.separator()
        
        # 获取当前工作流
        node_tree = context.space_data.node_tree
        
        if not node_tree or node_tree.bl_idname != "N8nNodeTreeType":
            layout.label(text="No n8n workflow selected")
            return
        
        # 工作流属性
        box = layout.box()
        box.label(text="Workflow Properties:")
        box.prop(node_tree, "workflow_name")
        box.prop(node_tree, "workflow_description")
        
        layout.separator()
        
        # 工作流执行
        exec_box = layout.box()
        exec_box.label(text="Execution:")
        
        # 显示执行状态
        row = exec_box.row()
        row.label(text="Status:")
        status_icon = 'QUESTION'
        if node_tree.execution_state == 'SUCCESS':
            status_icon = 'CHECKMARK'
        elif node_tree.execution_state == 'ERROR':
            status_icon = 'ERROR'
        elif node_tree.execution_state == 'RUNNING':
            status_icon = 'TIME'
        
        row.prop(node_tree, "execution_state", text="", icon_only=True)
        
        # 显示最后执行时间
        if node_tree.last_execution_time:
            exec_box.label(text=f"Last execution: {node_tree.last_execution_time}")
        
        # 显示最后执行结果
        if node_tree.last_execution_result:
            exec_box.label(text=f"Result: {node_tree.last_execution_result[:50]}...")
        
        # 执行按钮
        row = exec_box.row(align=True)
        row.operator("n8n.execute_workflow", icon='PLAY')
        row.operator("n8n.reset_workflow", icon='FILE_REFRESH')
        
        layout.separator()
        
        # 工作流导入导出
        io_box = layout.box()
        io_box.label(text="Import/Export:")
        io_box.operator("n8n.export_workflow", icon='EXPORT')
        io_box.operator("n8n.import_workflow", icon='IMPORT')

# 节点面板
class N8N_PT_node_panel(Panel):
    """n8n节点面板"""
    bl_label = "n8n Nodes"
    bl_idname = "N8N_PT_node_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "n8n"
    
    def draw(self, context):
        layout = self.layout
        
        # 添加节点按钮
        layout.label(text="Add Node:")
        layout.menu("N8N_MT_node_menu", text="Node Library", icon='OUTLINER_OB_GROUP_INSTANCE')
        layout.operator("n8n.search_nodes", icon='VIEWZOOM')
        
        layout.separator()
        
        # 获取选中的节点
        selected_nodes = context.selected_nodes
        
        if not selected_nodes:
            layout.label(text="No nodes selected")
            return
        
        # 显示选中节点数量
        layout.label(text=f"Selected: {len(selected_nodes)} node(s)")
        
        # 节点操作
        ops_box = layout.box()
        ops_box.label(text="Node Operations:")
        
        # 执行和重置
        row = ops_box.row(align=True)
        row.operator("n8n.execute_node", icon='PLAY')
        row.operator("n8n.reset_node", icon='FILE_REFRESH')
        
        # 复制和删除
        row = ops_box.row(align=True)
        row.operator("n8n.duplicate_node", icon='DUPLICATE')
        row.operator("n8n.delete_node", icon='TRASH')
        
        layout.separator()
        
        # 显示选中节点的详细信息
        if len(selected_nodes) == 1:
            node = selected_nodes[0]
            
            # 节点信息
            info_box = layout.box()
            info_box.label(text="Node Info:")
            
            if hasattr(node, 'node_type') and node.node_type:
                info_box.label(text=f"Type: {node.node_type}")
            
            info_box.label(text=f"Name: {node.name}")
            
            # 显示执行状态
            if hasattr(node, 'execution_state'):
                status_icon = 'QUESTION'
                if node.execution_state == 'SUCCESS':
                    status_icon = 'CHECKMARK'
                elif node.execution_state == 'ERROR':
                    status_icon = 'ERROR'
                elif node.execution_state == 'RUNNING':
                    status_icon = 'TIME'
                
                row = info_box.row()
                row.label(text="Status:")
                row.prop(node, "execution_state", text="", icon_only=True)
            
            # 显示错误信息
            if hasattr(node, 'error_message') and node.error_message:
                info_box.label(text=f"Error: {node.error_message}")
            
            # 显示执行结果
            if hasattr(node, 'execution_result') and node.execution_result:
                info_box.label(text=f"Result: {node.execution_result[:50]}...")

# 帮助面板
class N8N_PT_help_panel(Panel):
    """n8n帮助面板"""
    bl_label = "Help"
    bl_idname = "N8N_PT_help_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "n8n"
    
    def draw(self, context):
        layout = self.layout
        
        # 帮助信息
        help_box = layout.box()
        help_box.label(text="n8n Workflow Editor")
        help_box.separator()
        help_box.label(text="Shortcuts:")
        help_box.label(text="  Shift+A: Add Node")
        help_box.label(text="  Delete: Delete Node")
        help_box.label(text="  Shift+D: Duplicate Node")
        help_box.separator()
        help_box.label(text="Documentation:")
        help_box.operator("wm.url_open", text="n8n Documentation", icon='HELP').url = "https://docs.n8n.io/"
        help_box.operator("wm.url_open", text="Blender Nodes", icon='HELP').url = "https://docs.blender.org/manual/en/latest/modeling/modifiers/nodes/introduction.html"

# 注册面板类
classes = [
    N8N_UL_workflows,
    N8N_PT_workflow_panel,
    N8N_PT_node_panel,
    N8N_PT_help_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # 添加场景属性
    bpy.types.Scene.n8n_active_workflow_index = bpy.props.IntProperty(
        name="Active Workflow Index",
        description="Index of the active workflow in the list",
        default=0
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # 删除场景属性
    del bpy.types.Scene.n8n_active_workflow_index