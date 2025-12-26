import bpy
import time
import json
from bpy.types import Operator, Panel
from bpy.props import StringProperty, BoolProperty, EnumProperty
from ..nodes.n8n_node_base import N8nNodeTree

# Optional import with fallback
try:
    from ..i18n.dictionary import _
except ImportError:
    def _(text):
        return text

# 工作流执行操作
class N8N_OT_execute_workflow(Operator):
    """执行n8n工作流"""
    bl_idname = "n8n.execute_workflow"
    bl_label = "Execute Workflow"
    bl_description = "Execute the current n8n workflow"
    
    def execute(self, context):
        # 获取当前节点树
        node_tree = context.space_data.node_tree
        
        if not node_tree or not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "No n8n workflow found")
            return {'CANCELLED'}
        
        # 设置工作流状态为运行中
        node_tree.execution_state = 'RUNNING'
        start_time = time.time()
        
        try:
            # 重置所有节点状态
            node_tree.reset_nodes_state()
            
            # 获取执行顺序
            execution_order = node_tree.get_execution_order()
            
            # 执行节点
            for node in execution_order:
                if hasattr(node, 'execute'):
                    success = node.execute()
                    if not success:
                        raise Exception(f"Node {node.name} execution failed")
            
            # 计算执行时间
            execution_time = time.time() - start_time
            
            # 设置工作流状态为成功
            node_tree.execution_state = 'SUCCESS'
            node_tree.last_execution_time = time.strftime("%Y-%m-%d %H:%M:%S")
            node_tree.last_execution_result = f"Workflow executed successfully in {execution_time:.2f} seconds"
            
            self.report({'INFO'}, f"Workflow executed successfully in {execution_time:.2f} seconds")
            
        except Exception as e:
            # 设置工作流状态为错误
            node_tree.execution_state = 'ERROR'
            node_tree.last_execution_time = time.strftime("%Y-%m-%d %H:%M:%S")
            node_tree.last_execution_result = f"Error: {str(e)}"
            
            self.report({'ERROR'}, f"Workflow execution failed: {str(e)}")
        
        return {'FINISHED'}

# 工作流重置操作
class N8N_OT_reset_workflow(Operator):
    """重置n8n工作流"""
    bl_idname = "n8n.reset_workflow"
    bl_label = "Reset Workflow"
    bl_description = "Reset the current n8n workflow"
    
    def execute(self, context):
        # 获取当前节点树
        node_tree = context.space_data.node_tree
        
        if not node_tree or not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "No n8n workflow found")
            return {'CANCELLED'}
        
        # 重置工作流状态
        node_tree.execution_state = 'IDLE'
        node_tree.last_execution_time = ""
        node_tree.last_execution_result = ""
        
        # 重置所有节点状态
        node_tree.reset_nodes_state()
        
        self.report({'INFO'}, "Workflow reset successfully")
        
        return {'FINISHED'}

# 新建工作流操作
class N8N_OT_new_workflow(Operator):
    """创建新的n8n工作流"""
    bl_idname = "n8n.new_workflow"
    bl_label = "New Workflow"
    bl_description = "Create a new n8n workflow"
    
    workflow_name: StringProperty(
        name="Workflow Name",
        description="Name of the new workflow",
        default="New Workflow"
    )
    
    def execute(self, context):
        # 创建新的节点树
        node_tree = bpy.data.node_trees.new(self.workflow_name, type="N8nNodeTreeType")
        
        # 切换到节点编辑器并显示新工作流
        if context.area.type != 'NODE_EDITOR':
            context.area.type = 'NODE_EDITOR'
        
        context.space_data.node_tree = node_tree
        
        self.report({'INFO'}, f"Created new workflow: {self.workflow_name}")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# 打开工作流操作
class N8N_OT_open_workflow(Operator):
    """打开n8n工作流"""
    bl_idname = "n8n.open_workflow"
    bl_label = "Open Workflow"
    bl_description = "Open an existing n8n workflow"
    
    workflow_name: StringProperty(
        name="Workflow Name",
        description="Name of the workflow to open"
    )
    
    def execute(self, context):
        # 查找工作流
        node_tree = None
        for tree in bpy.data.node_trees:
            if tree.bl_idname == "N8nNodeTreeType" and tree.name == self.workflow_name:
                node_tree = tree
                break
        
        if not node_tree:
            self.report({'ERROR'}, f"Workflow not found: {self.workflow_name}")
            return {'CANCELLED'}
        
        # 切换到节点编辑器并显示工作流
        if context.area.type != 'NODE_EDITOR':
            context.area.type = 'NODE_EDITOR'
        
        context.space_data.node_tree = node_tree
        
        self.report({'INFO'}, f"Opened workflow: {self.workflow_name}")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # 获取所有n8n工作流
        workflows = [tree.name for tree in bpy.data.node_trees if tree.bl_idname == "N8nNodeTreeType"]
        
        if not workflows:
            self.report({'ERROR'}, "No n8n workflows found")
            return {'CANCELLED'}
        
        # 创建枚举属性
        items = [(name, name, "") for name in workflows]
        
        # 设置枚举属性
        bpy.types.Scene.n8n_workflow_enum = EnumProperty(
            name="Workflow",
            description="Select a workflow to open",
            items=items
        )
        
        # 显示对话框
        return context.window_manager.invoke_props_dialog(self)

# 复制工作流操作
class N8N_OT_duplicate_workflow(Operator):
    """复制n8n工作流"""
    bl_idname = "n8n.duplicate_workflow"
    bl_label = "Duplicate Workflow"
    bl_description = "Duplicate the current n8n workflow"
    
    new_name: StringProperty(
        name="New Name",
        description="Name of the duplicated workflow",
        default=""
    )
    
    def execute(self, context):
        # 获取当前节点树
        source_tree = context.space_data.node_tree
        
        if not source_tree or not isinstance(source_tree, N8nNodeTree):
            self.report({'ERROR'}, "No n8n workflow found")
            return {'CANCELLED'}
        
        # 设置新名称
        if not self.new_name:
            self.new_name = f"{source_tree.name} Copy"
        
        # 复制节点树
        new_tree = source_tree.copy()
        new_tree.name = self.new_name
        
        # 切换到新工作流
        context.space_data.node_tree = new_tree
        
        self.report({'INFO'}, f"Duplicated workflow: {self.new_name}")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # 获取当前节点树
        node_tree = context.space_data.node_tree
        
        if not node_tree or not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "No n8n workflow found")
            return {'CANCELLED'}
        
        # 设置默认名称
        self.new_name = f"{node_tree.name} Copy"
        
        return context.window_manager.invoke_props_dialog(self)

# 删除工作流操作
class N8N_OT_delete_workflow(Operator):
    """删除n8n工作流"""
    bl_idname = "n8n.delete_workflow"
    bl_label = "Delete Workflow"
    bl_description = "Delete the current n8n workflow"
    
    def execute(self, context):
        # 获取当前节点树
        node_tree = context.space_data.node_tree
        
        if not node_tree or not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "No n8n workflow found")
            return {'CANCELLED'}
        
        workflow_name = node_tree.name
        
        # 删除节点树
        bpy.data.node_trees.remove(node_tree)
        
        self.report({'INFO'}, f"Deleted workflow: {workflow_name}")
        
        return {'FINISHED'}

# 导出工作流操作
class N8N_OT_export_workflow(Operator):
    """导出n8n工作流"""
    bl_idname = "n8n.export_workflow"
    bl_label = "Export Workflow"
    bl_description = "Export the current n8n workflow to a JSON file"
    
    filepath: StringProperty(
        name="File Path",
        description="Path to save the workflow file",
        subtype='FILE_PATH'
    )
    
    def execute(self, context):
        # 获取当前节点树
        node_tree = context.space_data.node_tree
        
        if not node_tree or not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "No n8n workflow found")
            return {'CANCELLED'}
        
        try:
            # 序列化工作流
            workflow_data = node_tree.serialize_workflow()
            
            # 保存到文件
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, indent=2, ensure_ascii=False)
            
            self.report({'INFO'}, f"Workflow exported to: {self.filepath}")
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export workflow: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # 获取当前节点树
        node_tree = context.space_data.node_tree
        
        if not node_tree or not isinstance(node_tree, N8nNodeTree):
            self.report({'ERROR'}, "No n8n workflow found")
            return {'CANCELLED'}
        
        # 设置默认文件名
        self.filepath = f"{node_tree.name}.json"
        
        # 显示文件浏览器
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# 导入工作流操作
class N8N_OT_import_workflow(Operator):
    """导入n8n工作流"""
    bl_idname = "n8n.import_workflow"
    bl_label = "Import Workflow"
    bl_description = "Import a n8n workflow from a JSON file"
    
    filepath: StringProperty(
        name="File Path",
        description="Path to the workflow file",
        subtype='FILE_PATH'
    )
    
    def execute(self, context):
        try:
            # 从文件加载工作流数据
            with open(self.filepath, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            # 创建新的节点树
            workflow_name = workflow_data.get("name", "Imported Workflow")
            node_tree = bpy.data.node_trees.new(workflow_name, type="N8nNodeTreeType")
            
            # 反序列化工作流
            node_tree.deserialize_workflow(workflow_data)
            
            # 切换到节点编辑器并显示新工作流
            if context.area.type != 'NODE_EDITOR':
                context.area.type = 'NODE_EDITOR'
            
            context.space_data.node_tree = node_tree
            
            self.report({'INFO'}, f"Workflow imported from: {self.filepath}")
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import workflow: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # 显示文件浏览器
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# 注册操作类
classes = [
    N8N_OT_execute_workflow,
    N8N_OT_reset_workflow,
    N8N_OT_new_workflow,
    N8N_OT_open_workflow,
    N8N_OT_duplicate_workflow,
    N8N_OT_delete_workflow,
    N8N_OT_export_workflow,
    N8N_OT_import_workflow,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)