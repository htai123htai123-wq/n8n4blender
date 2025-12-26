import os
import json
import bpy
from typing import Dict, List, Any, Optional

def get_nodes_data() -> Dict[str, Any]:
    """获取节点数据"""
    try:
        # 获取nodes.json文件路径
        nodes_file = os.path.join(os.path.dirname(__file__), "..", "nodes", "nodes.json")
        
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes_data = json.load(f)
        
        return nodes_data
    except Exception as e:
        print(f"Error loading nodes data: {e}")
        return {}

def get_node_categories() -> Dict[str, List[str]]:
    """获取节点类别"""
    nodes_data = get_nodes_data()
    categories = {}
    
    for node_type, node_data in nodes_data.items():
        category = node_data.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(node_type)
    
    return categories

def get_node_display_name(node_type: str) -> str:
    """获取节点显示名称"""
    nodes_data = get_nodes_data()
    node_data = nodes_data.get(node_type, {})
    return node_data.get('displayName', node_type)

def get_node_description(node_type: str) -> str:
    """获取节点描述"""
    nodes_data = get_nodes_data()
    node_data = nodes_data.get(node_type, {})
    return node_data.get('description', '')

def get_node_parameters(node_type: str) -> List[Dict[str, Any]]:
    """获取节点参数"""
    nodes_data = get_nodes_data()
    node_data = nodes_data.get(node_type, {})
    return node_data.get('parameters', [])

def get_node_inputs(node_type: str) -> List[Dict[str, Any]]:
    """获取节点输入"""
    nodes_data = get_nodes_data()
    node_data = nodes_data.get(node_type, {})
    return node_data.get('inputs', [])

def get_node_outputs(node_type: str) -> List[Dict[str, Any]]:
    """获取节点输出"""
    nodes_data = get_nodes_data()
    node_data = nodes_data.get(node_type, {})
    return node_data.get('outputs', [])

def get_node_icon(node_type: str) -> str:
    """获取节点图标"""
    nodes_data = get_nodes_data()
    node_data = nodes_data.get(node_type, {})
    return node_data.get('icon', 'NODETREE')

def validate_node_parameters(node_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """验证节点参数"""
    nodes_data = get_nodes_data()
    node_data = nodes_data.get(node_type, {})
    param_configs = node_data.get('parameters', [])
    
    validated_params = {}
    
    for param_config in param_configs:
        param_name = param_config.get('name', '')
        param_type = param_config.get('type', 'string')
        param_default = param_config.get('default', '')
        param_required = param_config.get('required', False)
        
        # 检查参数是否存在
        if param_name not in parameters:
            if param_required:
                # 必需参数缺失，使用默认值
                validated_params[param_name] = param_default
            continue
        
        param_value = parameters[param_name]
        
        # 类型验证
        if param_type == 'string':
            validated_params[param_name] = str(param_value)
        elif param_type == 'number':
            try:
                validated_params[param_name] = float(param_value)
            except (ValueError, TypeError):
                validated_params[param_name] = float(param_default)
        elif param_type == 'integer':
            try:
                validated_params[param_name] = int(param_value)
            except (ValueError, TypeError):
                validated_params[param_name] = int(param_default)
        elif param_type == 'boolean':
            if isinstance(param_value, str):
                validated_params[param_name] = param_value.lower() in ('true', '1', 'yes')
            else:
                validated_params[param_name] = bool(param_value)
        else:
            # 默认为字符串
            validated_params[param_name] = str(param_value)
    
    return validated_params

def format_execution_time(seconds: float) -> str:
    """格式化执行时间"""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.2f}s"

def truncate_string(text: str, max_length: int = 50) -> str:
    """截断字符串"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_node_execution_color(execution_state: str) -> tuple:
    """获取节点执行状态颜色"""
    if execution_state == 'SUCCESS':
        return (0.2, 0.8, 0.2, 1.0)  # 绿色
    elif execution_state == 'ERROR':
        return (0.8, 0.2, 0.2, 1.0)  # 红色
    elif execution_state == 'RUNNING':
        return (0.8, 0.8, 0.2, 1.0)  # 黄色
    else:
        return (0.5, 0.5, 0.5, 1.0)  # 灰色

def show_error_dialog(title: str, message: str):
    """显示错误对话框"""
    def draw(self, context):
        layout = self.layout
        layout.label(text=message)
    
    bpy.context.window_manager.invoke_popup(draw, title=title)

def show_info_dialog(title: str, message: str):
    """显示信息对话框"""
    def draw(self, context):
        layout = self.layout
        layout.label(text=message)
    
    bpy.context.window_manager.invoke_popup(draw, title=title)

def get_node_tree_execution_summary(node_tree) -> Dict[str, Any]:
    """获取节点树执行摘要"""
    if not hasattr(node_tree, 'nodes'):
        return {"total": 0, "success": 0, "error": 0, "idle": 0, "running": 0}
    
    total = 0
    success = 0
    error = 0
    idle = 0
    running = 0
    
    for node in node_tree.nodes:
        if hasattr(node, 'execution_state'):
            total += 1
            if node.execution_state == 'SUCCESS':
                success += 1
            elif node.execution_state == 'ERROR':
                error += 1
            elif node.execution_state == 'RUNNING':
                running += 1
            else:
                idle += 1
    
    return {
        "total": total,
        "success": success,
        "error": error,
        "idle": idle,
        "running": running
    }