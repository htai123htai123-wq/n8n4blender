import bpy
from bpy.types import NodeSocket
from typing import Any, Dict

class N8nSocket(NodeSocket):
    """
n8n自定义套接字，支持多种数据类型
    """
    bl_idname = "N8nSocketType"
    bl_label = "n8n Socket"
    
    # 数据类型枚举
    data_type: bpy.props.EnumProperty(
        name="Data Type",
        items=[
            ("STRING", "String", "String data type", "TEXT", 1),
            ("NUMBER", "Number", "Number data type", "DECORATE", 2),
            ("BOOLEAN", "Boolean", "Boolean data type", "CHECKBOX", 3),
            ("OBJECT", "Object", "Object data type", "OBJECT_DATA", 4),
            ("ARRAY", "Array", "Array data type", "FILE_FOLDER", 5),
            ("JSON", "JSON", "JSON data type", "SCRIPT", 6),
            ("ANY", "Any", "Any data type", "NODETREE", 7),
        ],
        default="ANY",
        description="Data type of the socket"
    )
    
    # 默认值
    default_value: bpy.props.StringProperty(
        name="Default Value",
        default="",
        description="Default value for the socket"
    )
    
    # 是否使用默认值
    use_default_value: bpy.props.BoolProperty(
        name="Use Default",
        default=False,
        description="Use default value if no connection is present"
    )
    
    def draw(self, context, layout, node, text):
        """
        绘制套接字
        """
        if self.is_output or self.is_linked:
            layout.label(text=text, icon=self.get_icon())
        else:
            row = layout.row(align=True)
            row.label(text=text, icon=self.get_icon())
            row.prop(self, "use_default_value", text="")
            if self.use_default_value:
                row.prop(self, "default_value", text="")
    
    def draw_color(self, context, node):
        """
        设置套接字颜色
        """
        return self.get_color()
    
    def get_color(self) -> tuple:
        """
        根据数据类型返回颜色
        """
        color_map = {
            "STRING": (0.8, 0.8, 0.2, 1.0),  # 黄色
            "NUMBER": (0.2, 0.8, 0.2, 1.0),  # 绿色
            "BOOLEAN": (0.8, 0.2, 0.2, 1.0),  # 红色
            "OBJECT": (0.2, 0.6, 0.8, 1.0),  # 蓝色
            "ARRAY": (0.6, 0.2, 0.8, 1.0),  # 紫色
            "JSON": (0.8, 0.4, 0.2, 1.0),  # 橙色
            "ANY": (0.5, 0.5, 0.5, 1.0),  # 灰色
        }
        return color_map.get(self.data_type, (0.5, 0.5, 0.5, 1.0))
    
    def get_icon(self) -> str:
        """
        根据数据类型返回图标
        """
        icon_map = {
            "STRING": "TEXT",
            "NUMBER": "DECORATE",
            "BOOLEAN": "CHECKBOX",
            "OBJECT": "OBJECT_DATA",
            "ARRAY": "FILE_FOLDER",
            "JSON": "SCRIPT",
            "ANY": "NODETREE",
        }
        return icon_map.get(self.data_type, "NODETREE")
    
    def can_connect(self, other_socket: 'N8nSocket') -> bool:
        """
        检查两个套接字是否可以连接
        
        参数:
            other_socket: 要连接的另一个套接字
            
        返回:
            如果可以连接返回True，否则返回False
        """
        # 检查输入输出方向
        if self.is_output == other_socket.is_output:
            return False
        
        # 检查数据类型兼容性
        if self.data_type == "ANY" or other_socket.data_type == "ANY":
            return True
        
        return self.data_type == other_socket.data_type
    
    def get_value(self) -> Any:
        """
        获取套接字的值
        
        返回:
            套接字的值
        """
        if self.is_linked:
            # 如果有连接，值将从连接中获取
            return None
        elif self.use_default_value:
            # 使用默认值
            return self.parse_default_value()
        else:
            return None
    
    def parse_default_value(self) -> Any:
        """
        解析默认值
        
        返回:
            解析后的默认值
        """
        value = self.default_value
        
        if self.data_type == "STRING":
            return value
        elif self.data_type == "NUMBER":
            try:
                return float(value) if "." in value else int(value)
            except ValueError:
                return 0
        elif self.data_type == "BOOLEAN":
            return value.lower() in ("true", "1", "yes", "y", "on")
        elif self.data_type == "JSON":
            try:
                import json
                return json.loads(value)
            except json.JSONDecodeError:
                return {}
        elif self.data_type == "ARRAY":
            try:
                import json
                return json.loads(value)
            except json.JSONDecodeError:
                return []
        else:
            return value
    
    def serialize(self) -> Dict[str, Any]:
        """
        序列化套接字数据
        """
        return {
            "name": self.name,
            "data_type": self.data_type,
            "default_value": self.default_value,
            "use_default_value": self.use_default_value
        }
    
    def deserialize(self, data: Dict[str, Any]) -> None:
        """
        反序列化套接字数据
        """
        self.name = data.get("name", self.name)
        self.data_type = data.get("data_type", "ANY")
        self.default_value = data.get("default_value", "")
        self.use_default_value = data.get("use_default_value", False)

# 注册套接字属性到节点
class N8nSocketMixin:
    """
    节点套接字混合类，用于简化节点添加套接字的操作
    """
    
    @staticmethod
    def add_input_socket(node, name: str, data_type: str = "ANY", default_value: Any = "", use_default: bool = False) -> N8nSocket:
        """
        添加输入套接字
        """
        socket = node.inputs.new("N8nSocketType", name)
        socket.data_type = data_type
        socket.default_value = str(default_value)
        socket.use_default_value = use_default
        return socket
    
    @staticmethod
    def add_output_socket(node, name: str, data_type: str = "ANY") -> N8nSocket:
        """
        添加输出套接字
        """
        socket = node.outputs.new("N8nSocketType", name)
        socket.data_type = data_type
        return socket
    
    @staticmethod
    def get_input_value(node, socket_name: str) -> Any:
        """
        获取输入套接字的值
        """
        for socket in node.inputs:
            if socket.name == socket_name:
                return socket.get_value()
        return None
    
    @staticmethod
    def set_output_value(node, socket_name: str, value: Any) -> None:
        """
        设置输出套接字的值
        """
        # 注意：Blender节点套接字不能直接设置值，值通过连接传递
        pass
