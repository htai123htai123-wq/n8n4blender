import json
import requests
from typing import Dict, Any, List
from ..nodes.n8n_node_base import N8nNodeBase

class N8nParser:
    """
n8n节点解析器，负责解析n8n节点定义
    """
    
    def __init__(self):
        """
        初始化解析器
        """
        self.node_definitions: Dict[str, Any] = {}
    
    def load_node_definitions_from_file(self, file_path: str) -> bool:
        """
        从文件加载节点定义
        
        参数:
            file_path: 节点定义文件路径
            
        返回:
            加载成功返回True，失败返回False
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                node_definitions = json.load(f)
            
            # 处理数组格式的节点定义
            if isinstance(node_definitions, list):
                for node_def in node_definitions:
                    # 使用节点名称或displayName作为键
                    node_key = node_def.get("name", node_def.get("displayName", f"node_{len(self.node_definitions)}"))
                    self.node_definitions[node_key] = node_def
            else:
                # 处理对象格式的节点定义
                self.node_definitions.update(node_definitions)
            
            return True
        except Exception as e:
            print(f"Failed to load node definitions from file: {e}")
            return False
    
    def load_node_definitions_from_url(self, url: str) -> bool:
        """
        从URL加载节点定义
        
        参数:
            url: 节点定义URL
            
        返回:
            加载成功返回True，失败返回False
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            node_definitions = response.json()
            
            self.node_definitions.update(node_definitions)
            return True
        except Exception as e:
            print(f"Failed to load node definitions from URL: {e}")
            return False
    
    def get_node_definition(self, node_type: str) -> Dict[str, Any]:
        """
        获取节点定义
        
        参数:
            node_type: 节点类型
            
        返回:
            节点定义，如果不存在返回None
        """
        return self.node_definitions.get(node_type, None)
    
    def parse_node_definition(self, node_def: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析节点定义，转换为Blender节点蓝图格式
        
        参数:
            node_def: n8n节点定义
            
        返回:
            Blender节点蓝图
        """
        blueprint = {
            "name": node_def.get("displayName", "Unnamed Node"),
            "description": node_def.get("description", ""),
            "node_type": "N8nNodeBase",  # 默认使用基础节点类型
            "group": node_def.get("group", ["general"])[0],  # 取第一个组作为分类
            "properties": {},
            "inputs": [],
            "outputs": []
        }
        
        # 解析节点属性
        if "properties" in node_def:
            for prop_data in node_def["properties"]:
                prop_name = prop_data.get("name", "")
                if prop_name:
                    blueprint["properties"][prop_name] = self._parse_property(prop_data)
        
        # 解析输入参数
        if "inputs" in node_def:
            for input_data in node_def["inputs"]:
                socket_data = self._parse_input_output(input_data)
                if socket_data:
                    blueprint["inputs"].append(socket_data)
        
        # 解析输出参数
        if "outputs" in node_def:
            for output_data in node_def["outputs"]:
                socket_data = self._parse_input_output(output_data)
                if socket_data:
                    blueprint["outputs"].append(socket_data)
        
        return blueprint
    
    def _parse_property(self, prop_data: Dict[str, Any]) -> Any:
        """
        解析属性数据
        
        参数:
            prop_data: 属性数据
            
        返回:
            解析后的属性值和配置
        """
        # 提取属性基本信息
        prop_info = {
            "value": prop_data.get("default", ""),
            "description": prop_data.get("description", ""),
            "type": prop_data.get("type", "string"),
            "display_name": prop_data.get("displayName", prop_data.get("name", "")),
            "required": prop_data.get("required", False)
        }
        
        # 根据属性类型设置默认值
        prop_type = prop_info["type"]
        default_value = prop_info["value"]
        
        if prop_type == "boolean":
            prop_info["value"] = bool(default_value)
        elif prop_type == "number":
            if isinstance(default_value, str):
                prop_info["value"] = float(default_value) if "." in default_value else int(default_value)
            else:
                prop_info["value"] = default_value
        elif prop_type == "array":
            prop_info["value"] = list(default_value) if default_value else []
        elif prop_type == "object" or prop_type == "json":
            prop_info["value"] = dict(default_value) if default_value else {}
        elif prop_type == "string":
            prop_info["value"] = str(default_value)
        else:
            prop_info["value"] = str(default_value)
        
        return prop_info
    
    def _parse_input_output(self, io_data: Any) -> Dict[str, Any]:
        """
        解析输入或输出数据
        
        参数:
            io_data: 输入或输出数据（可能是字符串或对象）
            
        返回:
            套接字数据
        """
        # 确定套接字名称
        socket_name = ""
        if isinstance(io_data, str):
            socket_name = io_data
        else:
            # 如果是对象，尝试获取name属性，否则使用默认名称
            socket_name = getattr(io_data, "name", str(io_data)) if hasattr(io_data, "name") else "output"
        
        # 默认使用ANY类型
        data_type = "ANY"
        
        socket_data = {
            "name": socket_name,
            "data_type": data_type,
            "description": f"{socket_name} data",
            "default_value": "",
            "use_default": False
        }
        
        return socket_data
    
    def _map_n8n_type_to_blender(self, n8n_type: str) -> str:
        """
        将n8n数据类型映射到Blender套接字数据类型
        
        参数:
            n8n_type: n8n数据类型
            
        返回:
            Blender套接字数据类型
        """
        type_map = {
            "string": "STRING",
            "number": "NUMBER",
            "integer": "NUMBER",
            "boolean": "BOOLEAN",
            "array": "ARRAY",
            "object": "JSON",
            "json": "JSON",
            "binary": "STRING",
            "date": "STRING"
        }
        
        return type_map.get(n8n_type, "ANY")
    
    def parse_workflow_definition(self, workflow_def: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析工作流定义
        
        参数:
            workflow_def: n8n工作流定义
            
        返回:
            Blender工作流数据
        """
        workflow_data = {
            "name": workflow_def.get("name", "New Workflow"),
            "description": workflow_def.get("description", ""),
            "nodes": [],
            "connections": []
        }
        
        # 解析节点
        if "nodes" in workflow_def:
            for node_def in workflow_def["nodes"]:
                node_data = self._parse_workflow_node(node_def)
                if node_data:
                    workflow_data["nodes"].append(node_data)
        
        # 解析连接
        if "connections" in workflow_def:
            for connection_def in workflow_def["connections"]:
                connection_data = self._parse_workflow_connection(connection_def)
                if connection_data:
                    workflow_data["connections"].append(connection_data)
        
        return workflow_data
    
    def _parse_workflow_node(self, node_def: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析工作流中的节点
        
        参数:
            node_def: 工作流节点定义
            
        返回:
            节点数据
        """
        # 获取节点类型
        node_type = node_def.get("type", "")
        
        # 获取节点定义
        node_definition = self.get_node_definition(node_type)
        if not node_definition:
            # 如果没有找到节点定义，使用基础节点类型
            node_definition = {
                "name": node_type,
                "description": f"Node type {node_type}",
                "properties": {},
                "inputs": {},
                "outputs": {}
            }
        
        # 解析节点为蓝图
        blueprint = self.parse_node_definition(node_definition)
        
        # 添加节点位置
        position = node_def.get("position", [0, 0])
        
        return {
            "id": node_def.get("id", ""),
            "name": node_def.get("name", blueprint["name"]),
            "type": node_type,
            "blueprint": blueprint,
            "position": position,
            "properties": node_def.get("parameters", {})
        }
    
    def _parse_workflow_connection(self, connection_def: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析工作流连接
        
        参数:
            connection_def: 连接定义
            
        返回:
            连接数据
        """
        return {
            "from_node": connection_def.get("from", {}).get("node", ""),
            "from_socket": connection_def.get("from", {}).get("socket", "output"),
            "to_node": connection_def.get("to", {}).get("node", ""),
            "to_socket": connection_def.get("to", {}).get("socket", "input")
        }
    
    def clear(self) -> None:
        """
        清空所有节点定义
        """
        self.node_definitions.clear()
