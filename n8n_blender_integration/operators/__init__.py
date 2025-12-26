import bpy
from .workflow_ops import (
    N8N_OT_execute_workflow,
    N8N_OT_reset_workflow,
    N8N_OT_new_workflow,
    N8N_OT_open_workflow,
    N8N_OT_duplicate_workflow,
    N8N_OT_delete_workflow,
    N8N_OT_export_workflow,
    N8N_OT_import_workflow
)

from .node_ops import (
    N8N_OT_add_node
)

classes = [
    N8N_OT_execute_workflow,
    N8N_OT_reset_workflow,
    N8N_OT_new_workflow,
    N8N_OT_open_workflow,
    N8N_OT_duplicate_workflow,
    N8N_OT_delete_workflow,
    N8N_OT_export_workflow,
    N8N_OT_import_workflow,
    N8N_OT_add_node
]

def register():
    """
    注册所有运算符
    """
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    """
    注销所有运算符
    """
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
