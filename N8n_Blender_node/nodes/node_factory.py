import bpy
import json
import os
from typing import Dict, List, Any, Optional
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from .n8n_node_base import N8nNodeBase

# Optional import with fallback
try:
    from ..utils import get_nodes_data
except ImportError:
    def get_nodes_data():
        try:
            # 获取nodes.json文件路径
            nodes_file = os.path.join(os.path.dirname(__file__), "nodes.json")
            
            with open(nodes_file, 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)
            
            return nodes_data
        except Exception as e:
            print(f"Error loading nodes data: {e}")
            return {}

# 节点类型映射
NODE_TYPE_MAP = {}

def load_nodes_data() -> Dict[str, Any]:
    """加载节点数据"""
    try:
        # 获取nodes.json文件路径
        nodes_file = os.path.join(os.path.dirname(__file__), "nodes.json")
        
        with open(nodes_file, 'r', encoding='utf-8') as f:
            nodes_data = json.load(f)
        
        return nodes_data
    except Exception as e:
        print(f"Error loading nodes data: {e}")
        return {}

def get_nodes_data() -> Dict[str, Any]:
    """获取节点数据"""
    if not NODE_TYPE_MAP:
        NODE_TYPE_MAP.update(load_nodes_data())
    return NODE_TYPE_MAP

def create_node_class(node_type: str, node_data: Dict[str, Any]) -> type:
    """根据节点数据创建节点类"""
    class_name = f"N8nNode_{node_type}"
    
    # 创建节点类属性
    class_dict = {
        'bl_idname': class_name,
        'bl_label': node_data.get('displayName', node_type),
        'node_type': node_type,
        '__annotations__': {}
    }
    
    # 添加参数属性
    parameters = node_data.get('parameters', [])
    for param in parameters:
        param_name = param.get('name', '')
        param_type = param.get('type', 'string')
        param_default = param.get('default', '')
        param_display_name = param.get('displayName', param_name)
        param_description = param.get('description', '')
        param_options = param.get('options', [])
        
        if param_type == 'string':
            if param_options:
                # 枚举类型
                items = [(opt['value'], opt['name'], opt.get('description', '')) for opt in param_options]
                prop = EnumProperty(
                    name=param_display_name,
                    description=param_description,
                    items=items,
                    default=param_default
                )
            else:
                # 字符串类型
                prop = StringProperty(
                    name=param_display_name,
                    description=param_description,
                    default=param_default
                )
        elif param_type == 'number':
            # 数字类型
            prop = FloatProperty(
                name=param_display_name,
                description=param_description,
                default=float(param_default) if param_default else 0.0
            )
        elif param_type == 'integer':
            # 整数类型
            prop = IntProperty(
                name=param_display_name,
                description=param_description,
                default=int(param_default) if param_default else 0
            )
        elif param_type == 'boolean':
            # 布尔类型
            prop = BoolProperty(
                name=param_display_name,
                description=param_description,
                default=bool(param_default)
            )
        else:
            # 默认为字符串类型
            prop = StringProperty(
                name=param_display_name,
                description=param_description,
                default=str(param_default)
            )
        
        class_dict['__annotations__'][f'param_{param_name}'] = prop
    
    # 创建节点类
    node_class = type(class_name, (N8nNodeBase,), class_dict)
    
    # 重写init方法以处理节点特定初始化
    def init(self, context):
        N8nNodeBase.init(self, context)
        # 可以在这里添加节点特定的初始化逻辑
    
    # 重写execute方法以实现节点特定执行逻辑
    def execute(self):
        self.execution_state = 'RUNNING'
        self.error_message = ""
        
        try:
            # 这里应该实现具体的节点执行逻辑
            # 暂时只模拟执行
            import time
            time.sleep(0.5)  # 模拟执行时间
            
            # 模拟成功执行
            self.execution_state = 'SUCCESS'
            self.execution_result = f"Node {self.node_type} executed successfully"
            return True
            
        except Exception as e:
            self.execution_state = 'ERROR'
            self.error_message = str(e)
            return False
    
    # 重写draw_buttons方法以显示节点特定参数
    def draw_buttons(self, context, layout):
        # 显示节点类型
        if self.node_type:
            box = layout.box()
            box.label(text=f"Type: {self.bl_label}")
        
        # 显示执行状态
        if self.execution_state != 'IDLE':
            status_box = layout.box()
            status_box.label(text=f"Status: {self.execution_state}")
            
            if self.execution_state == 'ERROR' and self.error_message:
                status_box.label(text=f"Error: {self.error_message}")
            elif self.execution_state == 'SUCCESS' and self.execution_result:
                status_box.label(text=f"Result: {self.execution_result[:50]}...")
        
        # 绘制参数面板
        parameters = node_data.get('parameters', [])
        if parameters:
            param_box = layout.box()
            param_box.label(text="Parameters:")
            
            for param in parameters:
                param_name = param.get('name', '')
                param_display_name = param.get('displayName', param_name)
                
                if hasattr(self, f'param_{param_name}'):
                    param_box.prop(self, f'param_{param_name}', text=param_display_name)
    
    # 将方法绑定到类
    node_class.init = init
    node_class.execute = execute
    node_class.draw_buttons = draw_buttons
    
    return node_class

def generate_node_classes():
    """生成所有节点类"""
    nodes_data = get_nodes_data()
    node_classes = {}
    
    for node_type, node_data in nodes_data.items():
        try:
            node_class = create_node_class(node_type, node_data)
            node_classes[node_type] = node_class
        except Exception as e:
            print(f"Error creating node class for {node_type}: {e}")
    
    return node_classes

def register_node_classes():
    """注册所有节点类"""
    node_classes = generate_node_classes()
    
    for node_type, node_class in node_classes.items():
        try:
            bpy.utils.register_class(node_class)
        except Exception as e:
            print(f"Error registering node class {node_type}: {e}")

def unregister_node_classes():
    """注销所有节点类"""
    nodes_data = get_nodes_data()
    
    for node_type in nodes_data.keys():
        try:
            class_name = f"N8nNode_{node_type}"
            if hasattr(bpy.types, class_name):
                bpy.utils.unregister_class(getattr(bpy.types, class_name))
        except Exception as e:
            print(f"Error unregistering node class {node_type}: {e}")