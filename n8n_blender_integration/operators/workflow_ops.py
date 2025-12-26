import bpy
import os
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty, FloatProperty, EnumProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ..execution.n8n_workflow import N8nWorkflow
from ..nodes.n8n_node_tree import N8nNodeTree

class N8N_OT_execute_workflow(Operator):
    """
    执行n8n工作流操作符
    """
    bl_idname = "n8n.execute_workflow"
    bl_label = "Execute n8n Workflow"
    bl_description = "Execute the current n8n workflow"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """
        检查是否可以执行操作
        """
        return (context.space_data.tree_type == "N8nNodeTreeType" and 
                context.space_data.edit_tree)
    
    def execute(self, context):
        """
        执行操作
        """
        node_tree = context.space_data.edit_tree
        
        if not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "Not an n8n node tree")
            return {'CANCELLED'}
        
        try:
            # 创建工作流并执行
            workflow = N8nWorkflow(node_tree)
            start_time = bpy.context.scene.frame_current
            
            if workflow.execute():
                # 计算执行时间
                execution_time = bpy.context.scene.frame_current - start_time
                node_tree.execution_time = execution_time
                self.report({'INFO'}, "Workflow executed successfully")
            else:
                self.report({'ERROR'}, "Workflow execution failed")
            
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Execution failed: {e}")
            return {'CANCELLED'}

class N8N_OT_reset_workflow(Operator):
    """
    重置n8n工作流操作符
    """
    bl_idname = "n8n.reset_workflow"
    bl_label = "Reset n8n Workflow"
    bl_description = "Reset the current n8n workflow"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """
        检查是否可以执行操作
        """
        return (context.space_data.tree_type == "N8nNodeTreeType" and 
                context.space_data.edit_tree)
    
    def execute(self, context):
        """
        执行操作
        """
        node_tree = context.space_data.edit_tree
        
        if not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "Not an n8n node tree")
            return {'CANCELLED'}
        
        try:
            # 重置工作流
            node_tree.reset_all_nodes()
            self.report({'INFO'}, "Workflow reset successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Reset failed: {e}")
            return {'CANCELLED'}

class N8N_OT_new_workflow(Operator):
    """
    新建n8n工作流操作符
    """
    bl_idname = "n8n.new_workflow"
    bl_label = "New n8n Workflow"
    bl_description = "Create a new n8n workflow"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """
        执行操作
        """
        try:
            # 创建新的n8n工作流
            workflow = N8nWorkflow()
            
            # 打开节点编辑器并显示新工作流
            for area in bpy.context.screen.areas:
                if area.type == 'NODE_EDITOR':
                    area.spaces.active.tree_type = "N8nNodeTreeType"
                    area.spaces.active.node_tree = workflow.node_tree
                    break
            
            self.report({'INFO'}, "New workflow created")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create new workflow: {e}")
            return {'CANCELLED'}

class N8N_OT_open_workflow(Operator):
    """
    打开n8n工作流操作符
    """
    bl_idname = "n8n.open_workflow"
    bl_label = "Open n8n Workflow"
    bl_description = "Open an existing n8n workflow"
    bl_options = {'REGISTER', 'UNDO'}
    
    workflow_name: StringProperty(
        name="Workflow Name",
        description="Name of the workflow to open",
        default=""
    )
    
    def execute(self, context):
        """
        执行操作
        """
        try:
            # 查找工作流
            workflow = N8nWorkflow.get_workflow_by_name(self.workflow_name)
            if not workflow:
                self.report({'ERROR'}, f"Workflow '{self.workflow_name}' not found")
                return {'CANCELLED'}
            
            # 打开节点编辑器并显示工作流
            for area in bpy.context.screen.areas:
                if area.type == 'NODE_EDITOR':
                    area.spaces.active.tree_type = "N8nNodeTreeType"
                    area.spaces.active.node_tree = workflow.node_tree
                    break
            
            self.report({'INFO'}, f"Workflow '{self.workflow_name}' opened")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to open workflow: {e}")
            return {'CANCELLED'}

class N8N_OT_duplicate_workflow(Operator):
    """
    复制n8n工作流操作符
    """
    bl_idname = "n8n.duplicate_workflow"
    bl_label = "Duplicate n8n Workflow"
    bl_description = "Duplicate an existing n8n workflow"
    bl_options = {'REGISTER', 'UNDO'}
    
    workflow_name: StringProperty(
        name="Workflow Name",
        description="Name of the workflow to duplicate",
        default=""
    )
    
    def execute(self, context):
        """
        执行操作
        """
        try:
            # 查找工作流
            original_workflow = N8nWorkflow.get_workflow_by_name(self.workflow_name)
            if not original_workflow:
                self.report({'ERROR'}, f"Workflow '{self.workflow_name}' not found")
                return {'CANCELLED'}
            
            # 复制工作流
            new_name = f"{original_workflow.node_tree.workflow_name} (Copy)"
            new_workflow = original_workflow.duplicate(new_name)
            
            self.report({'INFO'}, f"Workflow duplicated as '{new_name}'")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to duplicate workflow: {e}")
            return {'CANCELLED'}

class N8N_OT_delete_workflow(Operator):
    """
    删除n8n工作流操作符
    """
    bl_idname = "n8n.delete_workflow"
    bl_label = "Delete n8n Workflow"
    bl_description = "Delete an existing n8n workflow"
    bl_options = {'REGISTER', 'UNDO'}
    
    workflow_name: StringProperty(
        name="Workflow Name",
        description="Name of the workflow to delete",
        default=""
    )
    
    def execute(self, context):
        """
        执行操作
        """
        try:
            # 查找工作流
            workflow = N8nWorkflow.get_workflow_by_name(self.workflow_name)
            if not workflow:
                self.report({'ERROR'}, f"Workflow '{self.workflow_name}' not found")
                return {'CANCELLED'}
            
            # 删除工作流
            workflow.delete()
            
            self.report({'INFO'}, f"Workflow '{self.workflow_name}' deleted")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to delete workflow: {e}")
            return {'CANCELLED'}

class N8N_OT_export_workflow(Operator, ExportHelper):
    """
    导出n8n工作流操作符
    """
    bl_idname = "n8n.export_workflow"
    bl_label = "Export n8n Workflow"
    bl_description = "Export the current n8n workflow to a file"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = ".json"
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    @classmethod
    def poll(cls, context):
        """
        检查是否可以执行操作
        """
        return (context.space_data.tree_type == "N8nNodeTreeType" and 
                context.space_data.edit_tree)
    
    def execute(self, context):
        """
        执行操作
        """
        node_tree = context.space_data.edit_tree
        
        if not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "Not an n8n node tree")
            return {'CANCELLED'}
        
        try:
            # 创建工作流并导出
            workflow = N8nWorkflow(node_tree)
            if workflow.save_to_file(self.filepath):
                self.report({'INFO'}, f"Workflow exported to {self.filepath}")
            else:
                self.report({'ERROR'}, "Failed to export workflow")
            
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}

class N8N_OT_import_workflow(Operator, ImportHelper):
    """
    导入n8n工作流操作符
    """
    bl_idname = "n8n.import_workflow"
    bl_label = "Import n8n Workflow"
    bl_description = "Import an n8n workflow from a file"
    bl_options = {'REGISTER', 'UNDO'}
    
    filename_ext = ".json"
    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    def execute(self, context):
        """
        执行操作
        """
        try:
            # 从文件加载工作流
            workflow = N8nWorkflow.load_from_file(self.filepath)
            
            # 打开节点编辑器并显示工作流
            for area in bpy.context.screen.areas:
                if area.type == 'NODE_EDITOR':
                    area.spaces.active.tree_type = "N8nNodeTreeType"
                    area.spaces.active.node_tree = workflow.node_tree
                    break
            
            self.report({'INFO'}, f"Workflow imported from {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {e}")
            return {'CANCELLED'}

class N8N_OT_open_workflow(Operator):
    """
    在节点编辑器中打开工作流
    """
    bl_idname = "n8n.open_workflow"
    bl_label = "Open Workflow"
    bl_description = "Open the workflow in the node editor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        """
        执行操作
        """
        # 获取当前选中的工作流
        # 这个操作符通常从列表中调用，所以工作流名称会作为属性传入
        # 这里简化处理，实际应该从UI列表中获取
        return {'FINISHED'}
