import bpy
from typing import Dict, Any, List
from .n8n_node_base import N8nNodeBase
from .n8n_socket import N8nSocket

# 节点蓝图注册表
node_blueprints: Dict[str, Any] = {}

# 按组分类的节点蓝图
node_blueprints_by_group: Dict[str, List[Dict[str, Any]]] = {}

class N8nNodeBlueprint:
    """
n8n节点蓝图类，用于定义节点的结构和属性
    """
    
    def __init__(self, blueprint_id: str, name: str, description: str, group: str = "general"):
        """
        初始化蓝图
        
        参数:
            blueprint_id: 蓝图ID
            name: 节点名称
            description: 节点描述
            group: 节点所属组
        """
        self.blueprint_id = blueprint_id
        self.name = name
        self.description = description
        self.node_type = "N8nNodeBase"
        self.group = group
        self.properties = {}
        self.inputs = []
        self.outputs = []
    
    def add_property(self, name: str, value: Any, description: str = "") -> 'N8nNodeBlueprint':
        """
        添加节点属性
        
        参数:
            name: 属性名称
            value: 属性值
            description: 属性描述
            
        返回:
            自身实例，用于链式调用
        """
        self.properties[name] = {
            "value": value,
            "description": description
        }
        return self
    
    def add_input(self, name: str, data_type: str = "ANY", default_value: Any = "", use_default: bool = False, description: str = "") -> 'N8nNodeBlueprint':
        """
        添加输入套接字
        
        参数:
            name: 套接字名称
            data_type: 数据类型
            default_value: 默认值
            use_default: 是否使用默认值
            description: 描述
            
        返回:
            自身实例，用于链式调用
        """
        self.inputs.append({
            "name": name,
            "data_type": data_type,
            "default_value": str(default_value),
            "use_default": use_default,
            "description": description
        })
        return self
    
    def add_output(self, name: str, data_type: str = "ANY", description: str = "") -> 'N8nNodeBlueprint':
        """
        添加输出套接字
        
        参数:
            name: 套接字名称
            data_type: 数据类型
            description: 描述
            
        返回:
            自身实例，用于链式调用
        """
        self.outputs.append({
            "name": name,
            "data_type": data_type,
            "description": description
        })
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式
        
        返回:
            蓝图字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "node_type": self.node_type,
            "group": self.group,
            "properties": self.properties,
            "inputs": self.inputs,
            "outputs": self.outputs
        }
    
    def register(self) -> None:
        """
        注册蓝图到全局注册表
        """
        blueprint_dict = self.to_dict()
        node_blueprints[self.blueprint_id] = blueprint_dict
        
        # 按组分类注册
        group = blueprint_dict.get("group", "general")
        if group not in node_blueprints_by_group:
            node_blueprints_by_group[group] = []
        node_blueprints_by_group[group].append(blueprint_dict)

# 内置节点蓝图定义

def register_builtin_blueprints():
    """
    注册内置节点蓝图
    """
    # HTTP Request Node  HTTP请求节点
    http_request_blueprint = N8nNodeBlueprint(
        "http_request",
        "HTTP Request",
        "Make HTTP requests to external APIs",
        group="transform"
    )
    http_request_blueprint.add_property("method", "GET", "HTTP method (GET, POST, PUT, DELETE, etc.)")
    http_request_blueprint.add_property("url", "https://", "URL to make the request to")
    http_request_blueprint.add_property("headers", "{}", "HTTP headers in JSON format")
    http_request_blueprint.add_property("body", "{}", "Request body in JSON format")
    http_request_blueprint.add_property("timeout", 30, "Request timeout in seconds")
    http_request_blueprint.add_input("url", "STRING", "", False, "URL override")
    http_request_blueprint.add_input("headers", "JSON", "{}", False, "Headers override")
    http_request_blueprint.add_input("body", "JSON", "{}", False, "Body override")
    http_request_blueprint.add_output("response", "JSON", "HTTP response")
    http_request_blueprint.add_output("status_code", "NUMBER", "HTTP status code")
    http_request_blueprint.register()
    
    # Data Transform Node 数据转换节点
    data_transform_blueprint = N8nNodeBlueprint(
        "data_transform",
        "Data Transform",
        "Transform data using Python expressions",
        group="transform"
    )
    data_transform_blueprint.add_property("expression", "data", "Python expression to transform data")
    data_transform_blueprint.add_input("input_data", "ANY", "", False, "Data to transform")
    data_transform_blueprint.add_output("output_data", "ANY", "Transformed data")
    data_transform_blueprint.register()
    
    # JSON Parse Node  JSON解析节点
    json_parse_blueprint = N8nNodeBlueprint(
        "json_parse",
        "JSON Parse",
        "Parse JSON string to object",
        group="transform"
    )
    json_parse_blueprint.add_input("json_string", "STRING", "{}", False, "JSON string to parse")
    json_parse_blueprint.add_output("parsed_data", "JSON", "Parsed JSON object")
    json_parse_blueprint.register()
    
    # JSON Stringify Node  JSON字符串化节点
    json_stringify_blueprint = N8nNodeBlueprint(
        "json_stringify",
        "JSON Stringify",
        "Convert object to JSON string",
        group="transform"
    )
    json_stringify_blueprint.add_property("indent", 2, "Indentation level for formatted output")
    json_stringify_blueprint.add_input("input_data", "ANY", "", False, "Data to convert to JSON string")
    json_stringify_blueprint.add_output("json_string", "STRING", "JSON string representation")
    json_stringify_blueprint.register()
    
    # File Read Node  文件读取节点
    file_read_blueprint = N8nNodeBlueprint(
        "file_read",
        "File Read",
        "Read content from a file",
        group="input"
    )
    file_read_blueprint.add_property("file_path", "", "Path to the file to read")
    file_read_blueprint.add_property("encoding", "utf-8", "File encoding")
    file_read_blueprint.add_input("file_path", "STRING", "", False, "File path override")
    file_read_blueprint.add_output("content", "STRING", "File content")
    file_read_blueprint.add_output("success", "BOOLEAN", "Whether the file was read successfully")
    file_read_blueprint.register()
    
    # File Write Node  文件写入节点
    file_write_blueprint = N8nNodeBlueprint(
        "file_write",
        "File Write",
        "Write content to a file",
        group="output"
    )
    file_write_blueprint.add_property("file_path", "", "Path to the file to write")
    file_write_blueprint.add_property("content", "", "Content to write to the file")
    file_write_blueprint.add_property("mode", "w", "File mode (w, a, x, etc.)")
    file_write_blueprint.add_property("encoding", "utf-8", "File encoding")
    file_write_blueprint.add_input("file_path", "STRING", "", False, "File path override")
    file_write_blueprint.add_input("content", "STRING", "", False, "Content override")
    file_write_blueprint.add_output("success", "BOOLEAN", "Whether the file was written successfully")
    file_write_blueprint.add_output("file_path", "STRING", "Path to the written file")
    file_write_blueprint.register()
    
    # Logic Branch Node  逻辑分支节点
    logic_branch_blueprint = N8nNodeBlueprint(
        "logic_branch",
        "Logic Branch",
        "Branch execution based on a condition",
        group="logic"
    )
    logic_branch_blueprint.add_property("condition", "input == true", "Condition expression to evaluate")
    logic_branch_blueprint.add_input("input", "BOOLEAN", True, False, "Input value to evaluate")
    logic_branch_blueprint.add_output("true", "ANY", "Output when condition is true")
    logic_branch_blueprint.add_output("false", "ANY", "Output when condition is false")
    logic_branch_blueprint.register()
    
    # Wait Node  等待节点
    wait_blueprint = N8nNodeBlueprint(
        "wait",
        "Wait",
        "Wait for a specified amount of time",
        group="utility"
    )
    wait_blueprint.add_property("seconds", 5, "Number of seconds to wait")
    wait_blueprint.add_input("seconds", "NUMBER", 5, False, "Seconds override")
    wait_blueprint.add_output("completed", "BOOLEAN", "Whether the wait completed successfully")
    wait_blueprint.register()
    
    # Log Node  日志节点
    log_blueprint = N8nNodeBlueprint(
        "log",
        "Log",
        "Log data to the console",
        group="utility"
    )
    log_blueprint.add_property("message", "Hello World", "Log message")
    log_blueprint.add_property("level", "info", "Log level (debug, info, warning, error)")
    log_blueprint.add_input("data", "ANY", "", False, "Data to log")
    log_blueprint.add_output("logged", "BOOLEAN", "Whether the data was logged successfully")
    log_blueprint.register()

# 初始化时注册内置蓝图
register_builtin_blueprints()
