import bpy
from bpy.types import Panel
from ..nodes.n8n_node_tree import N8nNodeTree
from ..nodes.n8n_node_base import N8nNodeBase
from ..execution.n8n_workflow import N8nWorkflow

class N8N_PT_workflow_panel(Panel):
    """
n8n工作流面板，显示在节点编辑器的侧边栏
    """
    bl_label = "n8n Workflow"
    bl_idname = "N8N_PT_workflow_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "n8n"
    
    @classmethod
    def poll(cls, context):
        """
        检查是否显示面板
        """
        return context.space_data.tree_type == "N8nNodeTreeType"
    
    def draw(self, context):
        """
        绘制面板
        """
        layout = self.layout
        scene = context.scene
        node_tree = context.space_data.edit_tree
        
        if not isinstance(node_tree, N8nNodeTree):
            return
        
        # 工作流信息
        box = layout.box()
        box.label(text="Workflow Information", icon="NODETREE")
        box.prop(node_tree, "workflow_name")
        box.prop(node_tree, "workflow_description")
        
        # 工作流状态
        box = layout.box()
        box.label(text="Workflow State", icon="PLAY")
        box.prop(node_tree, "workflow_state")
        if node_tree.workflow_state == "SUCCESS":
            box.label(text=f"Execution Time: {node_tree.execution_time:.2f}s", icon="TIME")
        
        # 工作流操作
        box = layout.box()
        box.label(text="Workflow Operations", icon="TOOL_SETTINGS")
        row = box.row()
        row.operator("n8n.execute_workflow", text="Execute", icon="PLAY")
        row.operator("n8n.reset_workflow", text="Reset", icon="LOOP_BACK")
        
        # 导入/导出
        row = box.row()
        row.operator("n8n.import_workflow", text="Import", icon="IMPORT")
        row.operator("n8n.export_workflow", text="Export", icon="EXPORT")
        
        # 新建工作流
        box.operator("n8n.new_workflow", text="New Workflow", icon="FILE_NEW")

class N8N_PT_node_properties_panel(Panel):
    """
n8n节点属性面板，显示在节点编辑器的侧边栏
    """
    bl_label = "n8n Node Properties"
    bl_idname = "N8N_PT_node_properties_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "n8n"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        """
        检查是否显示面板
        """
        return (context.space_data.tree_type == "N8nNodeTreeType" and 
                context.active_node and 
                isinstance(context.active_node, N8nNodeBase))
    
    def draw(self, context):
        """
        绘制面板
        """
        layout = self.layout
        active_node = context.active_node
        
        if not isinstance(active_node, N8nNodeBase):
            return
        
        # 节点基本信息
        box = layout.box()
        box.label(text="Node Information", icon="NODE")
        box.label(text=f"Type: {active_node.bl_label}")
        box.prop(active_node, "name")
        
        # 执行状态
        box = layout.box()
        box.label(text="Execution Status", icon="STATUS")
        box.prop(active_node, "execution_state")
        if active_node.execution_state == "SUCCESS" and active_node.execution_result:
            box.label(text="Result:")
            box.label(text=active_node.execution_result, icon="CHECKMARK")
        elif active_node.execution_state == "ERROR" and active_node.error_message:
            box.label(text="Error:")
            box.label(text=active_node.error_message, icon="ERROR")
        
        # 节点特定属性
        box = layout.box()
        box.label(text="Node Properties", icon="PROPERTIES")
        
        # 绘制节点的自定义属性
        self.draw_node_properties(active_node, box)
    
    def draw_node_properties(self, node, layout):
        """
        绘制节点的自定义属性
        """
        # 获取节点的所有属性
        for prop_name in dir(node):
            # 跳过内置属性和方法
            if prop_name.startswith('_') or callable(getattr(node, prop_name)):
                continue
            
            # 跳过已经显示过的属性
            if prop_name in ['execution_state', 'execution_result', 'error_message', 'name']:
                continue
            
            # 尝试绘制属性
            try:
                layout.prop(node, prop_name)
            except Exception:
                # 如果无法绘制（比如是复杂类型），跳过
                continue

class N8N_PT_workflow_list_panel(Panel):
    """
n8n工作流列表面板，显示在3D视图的侧边栏
    """
    bl_label = "n8n Workflows"
    bl_idname = "N8N_PT_workflow_list_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "n8n"
    
    def draw(self, context):
        """
        绘制面板
        """
        layout = self.layout
        scene = context.scene
        
        # 工作流列表
        box = layout.box()
        box.label(text="Workflows", icon="NODETREE")
        
        # 获取所有n8n工作流
        workflows = N8nWorkflow.get_all_workflows()
        
        for workflow in workflows:
            workflow_item = box.box()
            workflow_item.label(text=workflow.node_tree.workflow_name, icon="NODETREE")
            workflow_item.label(text=workflow.node_tree.workflow_state, icon=self._get_state_icon(workflow.node_tree.workflow_state))
            
            # 操作按钮
            row = workflow_item.row()
            row.operator("n8n.open_workflow", text="Open", icon="SCREEN_BACK")
            row.prop(workflow.node_tree, "workflow_name", text="")
            
            row = workflow_item.row()
            row.operator("n8n.duplicate_workflow", text="Duplicate", icon="DUPLICATE").workflow_name = workflow.node_tree.name
            row.operator("n8n.delete_workflow", text="Delete", icon="TRASH").workflow_name = workflow.node_tree.name
    
    def _get_state_icon(self, state):
        """
        获取状态对应的图标
        """
        icon_map = {
            "IDLE": "INFO",
            "RUNNING": "PLAY",
            "SUCCESS": "CHECKMARK",
            "ERROR": "ERROR"
        }
        return icon_map.get(state, "INFO")
