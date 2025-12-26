import bpy
from bpy.types import Node
from typing import Dict, Any

class N8nNodeBase(Node):
    """
n8n节点基类，所有n8n节点都继承自此类
    """
    bl_idname = "N8nNodeBase"
    bl_label = "n8n Node Base"
    bl_icon = "NODETREE"
    bl_width_default = 200
    
    # 节点执行状态
    execution_state: bpy.props.EnumProperty(
        name="Execution State",
        items=[
            ("IDLE", "Idle", "Node is idle"),
            ("RUNNING", "Running", "Node is executing"),
            ("SUCCESS", "Success", "Node executed successfully"),
            ("ERROR", "Error", "Node execution failed"),
        ],
        default="IDLE",
        description="Current execution state of the node"
    )
    
    # 执行结果
    execution_result: bpy.props.StringProperty(
        name="Execution Result",
        default="",
        description="Result of node execution"
    )
    
    # 错误信息
    error_message: bpy.props.StringProperty(
        name="Error Message",
        default="",
        description="Error message if execution failed"
    )
    
    def init(self, context):
        """
        初始化节点，创建输入和输出套接字
        """
        pass
    
    def draw_buttons(self, context, layout):
        """
        绘制节点属性面板
        """
        layout.prop(self, "execution_state")
        if self.execution_state == "SUCCESS" and self.execution_result:
            layout.label(text="Result:")
            layout.label(text=self.execution_result, icon="CHECKMARK")
        elif self.execution_state == "ERROR" and self.error_message:
            layout.label(text="Error:")
            layout.label(text=self.error_message, icon="ERROR")
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行节点逻辑
        
        参数:
            input_data: 输入数据字典
            
        返回:
            输出数据字典
        """
        # 子类需要重写此方法
        return {}
    
    def serialize(self) -> Dict[str, Any]:
        """
        序列化节点数据
        """
        return {
            "bl_idname": self.bl_idname,
            "name": self.name,
            "location": [self.location.x, self.location.y],
            "execution_state": self.execution_state,
            "execution_result": self.execution_result,
            "error_message": self.error_message
        }
    
    def deserialize(self, data: Dict[str, Any]) -> None:
        """
        反序列化节点数据
        """
        self.name = data.get("name", self.name)
        self.location = data.get("location", self.location)
        self.execution_state = data.get("execution_state", "IDLE")
        self.execution_result = data.get("execution_result", "")
        self.error_message = data.get("error_message", "")
    
    def reset(self):
        """
        重置节点状态
        """
        self.execution_state = "IDLE"
        self.execution_result = ""
        self.error_message = ""
