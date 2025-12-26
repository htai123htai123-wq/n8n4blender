import bpy
from typing import Dict, Any, List, Set
from ..nodes.n8n_node_base import N8nNodeBase
from ..nodes.n8n_node_tree import N8nNodeTree
from ..nodes.n8n_socket import N8nSocket

class N8nManager:
    """
n8n节点和连接管理器，负责管理节点实例和连接关系
    """
    
    def __init__(self):
        """
        初始化管理器
        """
        self.nodes: Dict[str, N8nNodeBase] = {}
        self.node_trees: Dict[str, N8nNodeTree] = {}
        self.connections: Set[tuple] = set()
        self.node_blueprints: Dict[str, Any] = {}
        self.node_blueprints_by_group: Dict[str, List[Dict[str, Any]]] = {}
    
    def register_node_tree(self, node_tree: N8nNodeTree) -> None:
        """
        注册节点树
        
        参数:
            node_tree: 要注册的节点树
        """
        self.node_trees[node_tree.name] = node_tree
        self._register_nodes_from_tree(node_tree)
    
    def unregister_node_tree(self, node_tree_name: str) -> None:
        """
        注销节点树
        
        参数:
            node_tree_name: 要注销的节点树名称
        """
        if node_tree_name in self.node_trees:
            node_tree = self.node_trees.pop(node_tree_name)
            self._unregister_nodes_from_tree(node_tree)
    
    def _register_nodes_from_tree(self, node_tree: N8nNodeTree) -> None:
        """
        从节点树中注册所有节点
        
        参数:
            node_tree: 节点树
        """
        for node in node_tree.nodes:
            if isinstance(node, N8nNodeBase):
                node_key = f"{node_tree.name}.{node.name}"
                self.nodes[node_key] = node
    
    def _unregister_nodes_from_tree(self, node_tree: N8nNodeTree) -> None:
        """
        从节点树中注销所有节点
        
        参数:
            node_tree: 节点树
        """
        for node in node_tree.nodes:
            if isinstance(node, N8nNodeBase):
                node_key = f"{node_tree.name}.{node.name}"
                if node_key in self.nodes:
                    self.nodes.pop(node_key)
    
    def update_node_registry(self) -> None:
        """
        更新节点注册表，重新扫描所有节点树
        """
        # 清空当前注册表
        self.nodes.clear()
        self.node_trees.clear()
        
        # 重新注册所有节点树和节点
        for node_tree in bpy.data.node_groups:
            if isinstance(node_tree, N8nNodeTree):
                self.register_node_tree(node_tree)
    
    def get_node(self, node_tree_name: str, node_name: str) -> N8nNodeBase:
        """
        获取节点
        
        参数:
            node_tree_name: 节点树名称
            node_name: 节点名称
            
        返回:
            节点对象，如果不存在返回None
        """
        node_key = f"{node_tree_name}.{node_name}"
        return self.nodes.get(node_key, None)
    
    def get_node_tree(self, node_tree_name: str) -> N8nNodeTree:
        """
        获取节点树
        
        参数:
            node_tree_name: 节点树名称
            
        返回:
            节点树对象，如果不存在返回None
        """
        return self.node_trees.get(node_tree_name, None)
    
    def register_node_blueprint(self, blueprint_id: str, blueprint: Dict[str, Any]) -> None:
        """
        注册节点蓝图
        
        参数:
            blueprint_id: 蓝图ID
            blueprint: 蓝图数据
        """
        self.node_blueprints[blueprint_id] = blueprint
        
        # 按组分类注册
        group = blueprint.get("group", "general")
        if group not in self.node_blueprints_by_group:
            self.node_blueprints_by_group[group] = []
        
        # 确保蓝图只被添加一次
        blueprint_with_id = blueprint.copy()
        blueprint_with_id["id"] = blueprint_id
        
        # 检查蓝图是否已经存在
        if blueprint_with_id not in self.node_blueprints_by_group[group]:
            self.node_blueprints_by_group[group].append(blueprint_with_id)
    
    def unregister_node_blueprint(self, blueprint_id: str) -> None:
        """
        注销节点蓝图
        
        参数:
            blueprint_id: 蓝图ID
        """
        if blueprint_id in self.node_blueprints:
            blueprint = self.node_blueprints.pop(blueprint_id)
            
            # 从分类注册表中移除
            group = blueprint.get("group", "general")
            if group in self.node_blueprints_by_group:
                # 查找并移除蓝图
                blueprint_with_id = blueprint.copy()
                blueprint_with_id["id"] = blueprint_id
                
                if blueprint_with_id in self.node_blueprints_by_group[group]:
                    self.node_blueprints_by_group[group].remove(blueprint_with_id)
                
                # 如果分类为空，移除分类
                if not self.node_blueprints_by_group[group]:
                    self.node_blueprints_by_group.pop(group)
    
    def get_node_blueprint(self, blueprint_id: str) -> Dict[str, Any]:
        """
        获取节点蓝图
        
        参数:
            blueprint_id: 蓝图ID
            
        返回:
            蓝图数据，如果不存在返回None
        """
        return self.node_blueprints.get(blueprint_id, None)
    
    def get_all_blueprints(self) -> List[Dict[str, Any]]:
        """
        获取所有节点蓝图
        
        返回:
            蓝图列表，每个蓝图包含id字段
        """
        blueprints = []
        for blueprint_id, blueprint in self.node_blueprints.items():
            blueprint_with_id = blueprint.copy()
            blueprint_with_id["id"] = blueprint_id
            blueprints.append(blueprint_with_id)
        return blueprints
    
    def get_blueprints_by_group(self, group: str) -> List[Dict[str, Any]]:
        """
        获取指定组的节点蓝图
        
        参数:
            group: 组名
            
        返回:
            指定组的蓝图列表
        """
        return self.node_blueprints_by_group.get(group, [])
    
    def get_all_groups(self) -> List[str]:
        """
        获取所有节点蓝图组
        
        返回:
            组名列表
        """
        return list(self.node_blueprints_by_group.keys())
    
    def create_node_from_blueprint(self, node_tree: N8nNodeTree, blueprint_id: str, location: tuple = (0, 0)) -> N8nNodeBase:
        """
        从蓝图创建节点
        
        参数:
            node_tree: 要添加节点的节点树
            blueprint_id: 蓝图ID
            location: 节点位置
            
        返回:
            创建的节点对象，如果创建失败返回None
        """
        blueprint = self.get_node_blueprint(blueprint_id)
        if not blueprint:
            print(f"Blueprint {blueprint_id} not found")
            return None
        
        try:
            # 获取节点类型
            node_type = blueprint.get("node_type", "N8nNodeBase")
            
            # 创建节点
            node = node_tree.nodes.new(type=node_type)
            node.location = location
            
            # 设置节点属性
            if "properties" in blueprint:
                for prop_name, prop_value in blueprint["properties"].items():
                    if hasattr(node, prop_name):
                        setattr(node, prop_name, prop_value)
            
            # 创建输入套接字
            if "inputs" in blueprint:
                for socket_data in blueprint["inputs"]:
                    socket_name = socket_data.get("name", "input")
                    data_type = socket_data.get("data_type", "ANY")
                    default_value = socket_data.get("default_value", "")
                    use_default = socket_data.get("use_default", False)
                    
                    socket = node.inputs.new("N8nSocketType", socket_name)
                    socket.data_type = data_type
                    socket.default_value = default_value
                    socket.use_default_value = use_default
            
            # 创建输出套接字
            if "outputs" in blueprint:
                for socket_data in blueprint["outputs"]:
                    socket_name = socket_data.get("name", "output")
                    data_type = socket_data.get("data_type", "ANY")
                    
                    socket = node.outputs.new("N8nSocketType", socket_name)
                    socket.data_type = data_type
            
            # 注册节点
            node_key = f"{node_tree.name}.{node.name}"
            self.nodes[node_key] = node
            
            return node
        except Exception as e:
            print(f"Failed to create node from blueprint: {e}")
            return None
    
    def validate_connection(self, from_socket: N8nSocket, to_socket: N8nSocket) -> bool:
        """
        验证连接是否有效
        
        参数:
            from_socket: 源套接字
            to_socket: 目标套接字
            
        返回:
            连接有效返回True，否则返回False
        """
        # 检查套接字类型
        if not isinstance(from_socket, N8nSocket) or not isinstance(to_socket, N8nSocket):
            return False
        
        # 检查方向
        if from_socket.is_output == to_socket.is_output:
            return False
        
        # 检查数据类型兼容性
        return from_socket.can_connect(to_socket)
    
    def get_node_connections(self, node: N8nNodeBase) -> List[tuple]:
        """
        获取节点的所有连接
        
        参数:
            node: 节点
            
        返回:
            连接列表，每个连接是一个元组(from_socket, to_socket)
        """
        connections = []
        
        # 检查输入连接
        for socket in node.inputs:
            if socket.is_linked:
                for link in socket.links:
                    connections.append((link.from_socket, socket))
        
        # 检查输出连接
        for socket in node.outputs:
            if socket.is_linked:
                for link in socket.links:
                    connections.append((socket, link.to_socket))
        
        return connections
    
    def update(self) -> None:
        """
        更新管理器状态
        """
        self.update_node_registry()
    
    def clear(self) -> None:
        """
        清空管理器
        """
        self.nodes.clear()
        self.node_trees.clear()
        self.connections.clear()
        self.node_blueprints.clear()
        self.node_blueprints_by_group.clear()

# 全局管理器实例
global_manager = N8nManager()
