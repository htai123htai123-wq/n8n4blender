import bpy
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty, FloatProperty, IntProperty
from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

# Optional imports with fallbacks
try:
    from ..utils import get_nodes_data
except ImportError:
    def get_nodes_data():
        return {}

try:
    from ..i18n.dictionary import _
except ImportError:
    def _(text):
        return text

# 节点树类型
class N8nNodeTree(NodeTree):
    """n8n节点树"""
    bl_idname = "N8nNodeTreeType"
    bl_label = "n8n Workflow"
    bl_icon = "NODETREE"
    
    # 工作流属性
    workflow_name: StringProperty(
        name="Workflow Name",
        description="Name of the n8n workflow",
        default="New Workflow"
    )
    
    workflow_description: StringProperty(
        name="Description",
        description="Description of the workflow",
        default=""
    )
    
    # 执行状态
    execution_state: EnumProperty(
        name="Execution State",
        description="Current execution state of the workflow",
        items=[
            ('IDLE', 'Idle', 'Workflow is idle'),
            ('RUNNING', 'Running', 'Workflow is running'),
            ('SUCCESS', 'Success', 'Workflow executed successfully'),
            ('ERROR', 'Error', 'Workflow execution failed'),
        ],
        default='IDLE'
    )
    
    # 最后执行时间
    last_execution_time: StringProperty(
        name="Last Execution Time",
        description="Last time the workflow was executed",
        default=""
    )
    
    # 最后执行结果
    last_execution_result: StringProperty(
        name="Last Execution Result",
        description="Result of the last workflow execution",
        default=""
    )
    
    def get_nodes_by_type(self, node_type: str) -> List['N8nNode']:
        """获取指定类型的所有节点"""
        return [node for node in self.nodes if hasattr(node, 'node_type') and node.node_type == node_type]
    
    def get_execution_order(self) -> List['N8nNode']:
        """计算节点执行顺序（拓扑排序）"""
        # 创建节点依赖图
        dependencies = {}
        for node in self.nodes:
            if hasattr(node, 'node_type'):
                dependencies[node] = []
                
                # 检查输入连接
                for input_socket in node.inputs:
                    for link in self.links:
                        if link.to_socket == input_socket:
                            dependencies[node].append(link.from_node)
        
        # 拓扑排序
        visited = set()
        temp_visited = set()
        execution_order = []
        
        def visit(node):
            if node in temp_visited:
                raise ValueError("Circular dependency detected in workflow")
            if node not in visited:
                temp_visited.add(node)
                for dependency in dependencies[node]:
                    visit(dependency)
                temp_visited.remove(node)
                visited.add(node)
                execution_order.append(node)
        
        for node in self.nodes:
            if hasattr(node, 'node_type') and node not in visited:
                visit(node)
        
        return execution_order
    
    def reset_nodes_state(self):
        """重置所有节点状态"""
        for node in self.nodes:
            if hasattr(node, 'execution_state'):
                node.execution_state = 'IDLE'
            if hasattr(node, 'execution_result'):
                node.execution_result = ""
            if hasattr(node, 'error_message'):
                node.error_message = ""
    
    def serialize_workflow(self) -> Dict[str, Any]:
        """序列化工作流为JSON格式"""
        workflow = {
            "name": self.workflow_name,
            "description": self.workflow_description,
            "nodes": [],
            "connections": []
        }
        
        # 序列化节点
        for node in self.nodes:
            if hasattr(node, 'node_type'):
                node_data = {
                    "id": node.name,
                    "type": node.node_type,
                    "position": [node.location.x, node.location.y],
                    "parameters": {}
                }
                
                # 添加节点参数
                if hasattr(node, 'get_parameters'):
                    node_data["parameters"] = node.get_parameters()
                
                workflow["nodes"].append(node_data)
        
        # 序列化连接
        for link in self.links:
            if hasattr(link.from_node, 'node_type') and hasattr(link.to_node, 'node_type'):
                connection = {
                    "from": [link.from_node.name, link.from_socket.name],
                    "to": [link.to_node.name, link.to_socket.name]
                }
                workflow["connections"].append(connection)
        
        return workflow
    
    def deserialize_workflow(self, workflow_data: Dict[str, Any]):
        """从JSON数据反序列化工作流"""
        # 清空现有节点和连接
        self.nodes.clear()
        
        # 设置工作流属性
        self.workflow_name = workflow_data.get("name", "New Workflow")
        self.workflow_description = workflow_data.get("description", "")
        
        # 创建节点
        node_map = {}
        for node_data in workflow_data.get("nodes", []):
            node_type = node_data.get("type")
            position = node_data.get("position", [0, 0])
            parameters = node_data.get("parameters", {})
            
            # 创建节点
            node = self.nodes.new(type=f"N8nNode_{node_type}")
            node.location.x = position[0]
            node.location.y = position[1]
            
            # 设置节点参数
            if hasattr(node, 'set_parameters'):
                node.set_parameters(parameters)
            
            node_map[node_data.get("id")] = node
        
        # 创建连接
        for connection in workflow_data.get("connections", []):
            from_node_id = connection["from"][0]
            from_socket_name = connection["from"][1]
            to_node_id = connection["to"][0]
            to_socket_name = connection["to"][1]
            
            if from_node_id in node_map and to_node_id in node_map:
                from_node = node_map[from_node_id]
                to_node = node_map[to_node_id]
                
                # 查找对应的socket
                from_socket = None
                for socket in from_node.outputs:
                    if socket.name == from_socket_name:
                        from_socket = socket
                        break
                
                to_socket = None
                for socket in to_node.inputs:
                    if socket.name == to_socket_name:
                        to_socket = socket
                        break
                
                if from_socket and to_socket:
                    self.links.new(from_socket, to_socket)

# 节点基类
class N8nNodeBase(Node):
    """n8n节点基类"""
    bl_label = "n8n Node"
    
    # 节点类型
    node_type: StringProperty(
        name="Node Type",
        description="Type of the n8n node",
        default=""
    )
    
    # 执行状态
    execution_state: EnumProperty(
        name="Execution State",
        description="Current execution state of the node",
        items=[
            ('IDLE', 'Idle', 'Node is idle'),
            ('RUNNING', 'Running', 'Node is running'),
            ('SUCCESS', 'Success', 'Node executed successfully'),
            ('ERROR', 'Error', 'Node execution failed'),
        ],
        default='IDLE'
    )
    
    # 执行结果
    execution_result: StringProperty(
        name="Execution Result",
        description="Result of the node execution",
        default=""
    )
    
    # 错误信息
    error_message: StringProperty(
        name="Error Message",
        description="Error message if execution failed",
        default=""
    )
    
    def init(self, context):
        """初始化节点"""
        self.width = 200
        
        # 根据节点类型创建输入和输出
        self.create_sockets()
    
    def create_sockets(self):
        """根据节点类型创建输入和输出"""
        nodes_data = get_nodes_data()
        node_data = nodes_data.get(self.node_type, {})
        
        # 创建输入
        inputs = node_data.get("inputs", [])
        for input_data in inputs:
            input_name = input_data.get("name", "input")
            input_type = input_data.get("type", "main")
            input_required = input_data.get("required", False)
            
            socket_type = "N8nSocketMain" if input_type == "main" else "N8nSocketGeneric"
            socket = self.inputs.new(socket_type, input_name)
            socket.is_required = input_required
        
        # 创建输出
        outputs = node_data.get("outputs", [])
        for output_data in outputs:
            output_name = output_data.get("name", "output")
            output_type = output_data.get("type", "main")
            
            socket_type = "N8nSocketMain" if output_type == "main" else "N8nSocketGeneric"
            self.outputs.new(socket_type, output_name)
    
    def draw_buttons(self, context, layout):
        """绘制节点属性面板"""
        # 显示节点类型
        if self.node_type:
            box = layout.box()
            box.label(text=f"Type: {self.node_type}")
        
        # 显示执行状态
        if self.execution_state != 'IDLE':
            status_box = layout.box()
            status_box.label(text=f"Status: {self.execution_state}")
            
            if self.execution_state == 'ERROR' and self.error_message:
                status_box.label(text=f"Error: {self.error_message}")
            elif self.execution_state == 'SUCCESS' and self.execution_result:
                status_box.label(text=f"Result: {self.execution_result[:50]}...")
        
        # 绘制参数面板
        self.draw_parameters(context, layout)
    
    def draw_parameters(self, context, layout):
        """绘制节点参数面板"""
        nodes_data = get_nodes_data()
        node_data = nodes_data.get(self.node_type, {})
        parameters = node_data.get("parameters", {})
        
        for param_name, param_config in parameters.items():
            param_type = param_config.get("type", "string")
            param_label = param_config.get("label", param_name)
            param_default = param_config.get("default", "")
            param_options = param_config.get("options", [])
            
            if param_type == "string":
                row = layout.row()
                row.prop(self, f'param_{param_name}', text=param_label)
            elif param_type == "number":
                row = layout.row()
                row.prop(self, f'param_{param_name}', text=param_label)
            elif param_type == "boolean":
                row = layout.row()
                row.prop(self, f'param_{param_name}', text=param_label)
            elif param_type == "enum" and param_options:
                items = [(opt, opt, "") for opt in param_options]
                enum_prop = EnumProperty(
                    name=param_label,
                    description=param_label,
                    items=items,
                    default=param_default
                )
                setattr(self.__class__, f'param_{param_name}', enum_prop)
                row = layout.row()
                row.prop(self, f'param_{param_name}', text=param_label)
    
    def get_parameters(self) -> Dict[str, Any]:
        """获取节点参数"""
        parameters = {}
        nodes_data = get_nodes_data()
        node_data = nodes_data.get(self.node_type, {})
        param_configs = node_data.get("parameters", {})
        
        for param_name, param_config in param_configs.items():
            if hasattr(self, f'param_{param_name}'):
                parameters[param_name] = getattr(self, f'param_{param_name}')
        
        return parameters
    
    def set_parameters(self, parameters: Dict[str, Any]):
        """设置节点参数"""
        for param_name, param_value in parameters.items():
            if hasattr(self, f'param_{param_name}'):
                setattr(self, f'param_{param_name}', param_value)
    
    def execute(self) -> bool:
        """执行节点"""
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
    
    def reset(self):
        """重置节点状态"""
        self.execution_state = 'IDLE'
        self.execution_result = ""
        self.error_message = ""

# 节点类别
class N8nNodeCategory(NodeCategory):
    """n8n节点类别"""
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "N8nNodeTreeType"

# 节点注册函数
node_categories = [
    N8nNodeCategory("N8N_TRANSFORM", "Transform", items=[]),
    N8nNodeCategory("N8N_DATA", "Data", items=[]),
    N8nNodeCategory("N8N_AI", "AI", items=[]),
    N8nNodeCategory("N8N_TRIGGER", "Trigger", items=[]),
    N8nNodeCategory("N8N_FLOW", "Flow", items=[]),
]

def register_node_categories():
    """注册节点类别"""
    register_node_categories("N8N_NODES", node_categories)

def unregister_node_categories():
    """注销节点类别"""
    unregister_node_categories("N8N_NODES")