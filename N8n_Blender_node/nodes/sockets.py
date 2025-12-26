import bpy
from bpy.types import NodeSocket
from bpy.props import BoolProperty, StringProperty, FloatProperty, EnumProperty

# 基础套接字类
class N8nSocketBase(NodeSocket):
    """n8n节点套接字基类"""
    bl_label = "n8n Socket"
    
    # 套接字颜色
    socket_color = (0.5, 0.5, 0.5, 1.0)
    
    # 是否为必需的输入
    is_required: BoolProperty(
        name="Required",
        description="Whether this socket is required",
        default=False
    )
    
    # 套接字值
    value: StringProperty(
        name="Value",
        description="Value of the socket",
        default=""
    )
    
    def draw(self, context, layout, node, text):
        """绘制套接字"""
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "value", text=text)
    
    def draw_color(self, context, node):
        """返回套接字颜色"""
        return self.socket_color

# 主数据流套接字
class N8nSocketMain(N8nSocketBase):
    """n8n主数据流套接字"""
    bl_idname = "N8nSocketMain"
    bl_label = "Main"
    
    socket_color = (0.6, 0.8, 1.0, 1.0)
    
    # 数据类型
    data_type: EnumProperty(
        name="Data Type",
        description="Type of data flowing through this socket",
        items=[
            ('JSON', 'JSON', 'JSON data'),
            ('TEXT', 'Text', 'Plain text data'),
            ('BINARY', 'Binary', 'Binary data'),
            ('UNKNOWN', 'Unknown', 'Unknown data type'),
        ],
        default='JSON'
    )

# 通用数据套接字
class N8nSocketGeneric(N8nSocketBase):
    """n8n通用数据套接字"""
    bl_idname = "N8nSocketGeneric"
    bl_label = "Generic"
    
    socket_color = (0.8, 0.6, 1.0, 1.0)
    
    # 数据类型
    data_type: EnumProperty(
        name="Data Type",
        description="Type of data flowing through this socket",
        items=[
            ('STRING', 'String', 'String data'),
            ('NUMBER', 'Number', 'Number data'),
            ('BOOLEAN', 'Boolean', 'Boolean data'),
            ('ARRAY', 'Array', 'Array data'),
            ('OBJECT', 'Object', 'Object data'),
            ('UNKNOWN', 'Unknown', 'Unknown data type'),
        ],
        default='UNKNOWN'
    )

# 特定类型套接字
class N8nSocketString(N8nSocketBase):
    """n8n字符串套接字"""
    bl_idname = "N8nSocketString"
    bl_label = "String"
    
    socket_color = (0.8, 0.8, 0.2, 1.0)
    
    # 字符串值
    value: StringProperty(
        name="Value",
        description="String value",
        default=""
    )

class N8nSocketNumber(N8nSocketBase):
    """n8n数字套接字"""
    bl_idname = "N8nSocketNumber"
    bl_label = "Number"
    
    socket_color = (0.2, 0.8, 0.8, 1.0)
    
    # 数字值
    value: FloatProperty(
        name="Value",
        description="Number value",
        default=0.0
    )

class N8nSocketBoolean(N8nSocketBase):
    """n8n布尔套接字"""
    bl_idname = "N8nSocketBoolean"
    bl_label = "Boolean"
    
    socket_color = (0.8, 0.2, 0.2, 1.0)
    
    # 布尔值
    value: BoolProperty(
        name="Value",
        description="Boolean value",
        default=False
    )

class N8nSocketArray(N8nSocketBase):
    """n8n数组套接字"""
    bl_idname = "N8nSocketArray"
    bl_label = "Array"
    
    socket_color = (0.2, 0.8, 0.2, 1.0)
    
    # 数组值（JSON字符串）
    value: StringProperty(
        name="Value",
        description="Array value (JSON string)",
        default="[]"
    )

class N8nSocketObject(N8nSocketBase):
    """n8n对象套接字"""
    bl_idname = "N8nSocketObject"
    bl_label = "Object"
    
    socket_color = (0.8, 0.5, 0.2, 1.0)
    
    # 对象值（JSON字符串）
    value: StringProperty(
        name="Value",
        description="Object value (JSON string)",
        default="{}"
    )

# 套接字类型映射
SOCKET_TYPE_MAP = {
    'main': N8nSocketMain,
    'generic': N8nSocketGeneric,
    'string': N8nSocketString,
    'number': N8nSocketNumber,
    'boolean': N8nSocketBoolean,
    'array': N8nSocketArray,
    'object': N8nSocketObject,
}

def get_socket_class(socket_type: str):
    """根据类型获取套接字类"""
    return SOCKET_TYPE_MAP.get(socket_type, N8nSocketGeneric)

def register_socket_classes():
    """注册所有套接字类"""
    socket_classes = [
        N8nSocketMain,
        N8nSocketGeneric,
        N8nSocketString,
        N8nSocketNumber,
        N8nSocketBoolean,
        N8nSocketArray,
        N8nSocketObject,
    ]
    
    for socket_class in socket_classes:
        bpy.utils.register_class(socket_class)

def unregister_socket_classes():
    """注销所有套接字类"""
    socket_classes = [
        N8nSocketMain,
        N8nSocketGeneric,
        N8nSocketString,
        N8nSocketNumber,
        N8nSocketBoolean,
        N8nSocketArray,
        N8nSocketObject,
    ]
    
    for socket_class in socket_classes:
        bpy.utils.unregister_class(socket_class)