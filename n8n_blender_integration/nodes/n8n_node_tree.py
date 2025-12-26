import bpy
from bpy.types import NodeTree
from typing import List, Dict, Any

class N8nNodeTree(NodeTree):
    """
n8n节点树，用于管理n8n工作流
    """
    bl_idname = "N8nNodeTreeType"
    bl_label = "n8n Node Tree"
    bl_icon = "NODETREE"
    bl_description = "n8n Workflow Node Tree"
    
    # 工作流名称
    workflow_name: bpy.props.StringProperty(
        name="Workflow Name",
        default="New Workflow",
        description="Name of the n8n workflow"
    )
    
    # 工作流描述
    workflow_description: bpy.props.StringProperty(
        name="Workflow Description",
        default="",
        description="Description of the n8n workflow"
    )
    
    # 工作流执行状态
    workflow_state: bpy.props.EnumProperty(
        name="Workflow State",
        items=[
            ("IDLE", "Idle", "Workflow is idle"),
            ("RUNNING", "Running", "Workflow is executing"),
            ("SUCCESS", "Success", "Workflow executed successfully"),
            ("ERROR", "Error", "Workflow execution failed"),
        ],
        default="IDLE",
        description="Current execution state of the workflow"
    )
    
    # 执行结果
    execution_time: bpy.props.FloatProperty(
        name="Execution Time",
        default=0.0,
        description="Time taken to execute the workflow in seconds"
    )
    
    def get_nodes(self) -> List[Any]:
        """
        获取所有节点
        """
        return list(self.nodes)
    
    def get_connections(self) -> List[Any]:
        """
        获取所有连接
        """
        return list(self.links)
    
    def get_node_by_name(self, name: str) -> Any:
        """
        根据名称获取节点
        """
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def calculate_execution_order(self) -> List[Any]:
        """
        计算节点执行顺序
        
        返回:
            按执行顺序排列的节点列表
        """
        # 实现拓扑排序算法
        from collections import deque
        
        # 构建邻接表和入度表
        adjacency = {}
        in_degree = {}
        
        # 初始化
        for node in self.nodes:
            adjacency[node] = []
            in_degree[node] = 0
        
        # 构建图
        for link in self.links:
            from_node = link.from_node
            to_node = link.to_node
            adjacency[from_node].append(to_node)
            in_degree[to_node] += 1
        
        # 找到所有入度为0的节点
        queue = deque()
        for node, degree in in_degree.items():
            if degree == 0:
                queue.append(node)
        
        # 执行拓扑排序
        execution_order = []
        while queue:
            current = queue.popleft()
            execution_order.append(current)
            
            for neighbor in adjacency[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # 检查是否存在循环依赖
        if len(execution_order) != len(self.nodes):
            raise ValueError("Workflow contains circular dependencies")
        
        return execution_order
    
    def reset_all_nodes(self):
        """
        重置所有节点状态
        """
        for node in self.nodes:
            if hasattr(node, "reset"):
                node.reset()
        self.workflow_state = "IDLE"
        self.execution_time = 0.0
    
    def serialize(self) -> Dict[str, Any]:
        """
        序列化工作流
        """
        workflow_data = {
            "name": self.workflow_name,
            "description": self.workflow_description,
            "nodes": [],
            "connections": [],
            "state": self.workflow_state,
            "execution_time": self.execution_time
        }
        
        # 序列化节点
        node_map = {}
        for i, node in enumerate(self.nodes):
            node_data = node.serialize() if hasattr(node, "serialize") else {}
            node_data["index"] = i
            workflow_data["nodes"].append(node_data)
            node_map[node] = i
        
        # 序列化连接
        for link in self.links:
            from_node_index = node_map.get(link.from_node, -1)
            to_node_index = node_map.get(link.to_node, -1)
            if from_node_index >= 0 and to_node_index >= 0:
                connection_data = {
                    "from_node": from_node_index,
                    "from_socket": link.from_socket.name,
                    "to_node": to_node_index,
                    "to_socket": link.to_socket.name
                }
                workflow_data["connections"].append(connection_data)
        
        return workflow_data
    
    def deserialize(self, data: Dict[str, Any]) -> None:
        """
        反序列化工作流
        """
        # 重置当前工作流
        self.nodes.clear()
        self.links.clear()
        
        # 设置工作流属性
        self.workflow_name = data.get("name", "New Workflow")
        self.workflow_description = data.get("description", "")
        self.workflow_state = data.get("state", "IDLE")
        self.execution_time = data.get("execution_time", 0.0)
        
        # 反序列化节点
        nodes_data = data.get("nodes", [])
        node_index_map = {}
        
        for node_data in nodes_data:
            bl_idname = node_data.get("bl_idname", "N8nNodeBase")
            node = self.nodes.new(bl_idname)
            if hasattr(node, "deserialize"):
                node.deserialize(node_data)
            node_index_map[node_data["index"]] = node
        
        # 反序列化连接
        connections_data = data.get("connections", [])
        for conn_data in connections_data:
            from_node = node_index_map.get(conn_data["from_node"])
            to_node = node_index_map.get(conn_data["to_node"])
            
            if from_node and to_node:
                # 查找套接字
                from_socket = None
                to_socket = None
                
                for socket in from_node.outputs:
                    if socket.name == conn_data["from_socket"]:
                        from_socket = socket
                        break
                
                for socket in to_node.inputs:
                    if socket.name == conn_data["to_socket"]:
                        to_socket = socket
                        break
                
                if from_socket and to_socket:
                    self.links.new(from_socket, to_socket)

# 节点树空间
# class N8nNodeTreeSpace(bpy.types.SpaceNodeEditor):
#     """n8n节点编辑器空间"""
#     bl_idname = "NODE_EDITOR"
#     bl_label = "n8n Node Editor"
#
#     @classmethod
#     def poll(cls, context):
#         return context.space_data.tree_type == "N8nNodeTreeType"
