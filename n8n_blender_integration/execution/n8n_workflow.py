import bpy
import json
import os
from typing import Dict, Any, List
from .n8n_executor import N8nExecutor
from ..nodes.n8n_node_tree import N8nNodeTree

class N8nWorkflow:
    """
n8n工作流管理类，负责工作流的导入、导出和执行
    """
    
    def __init__(self, node_tree: N8nNodeTree = None):
        """
        初始化工作流
        
        参数:
            node_tree: 要管理的节点树，如果为None则创建新的节点树
        """
        self.node_tree = node_tree or self._create_new_node_tree()
        self.executor = N8nExecutor(self.node_tree)
    
    @staticmethod
    def _create_new_node_tree() -> N8nNodeTree:
        """
        创建新的节点树
        
        返回:
            新创建的节点树
        """
        # 创建新的节点树
        node_tree = bpy.data.node_groups.new(
            name="New n8n Workflow",
            type="N8nNodeTreeType"
        )
        return node_tree
    
    def execute(self) -> bool:
        """
        执行工作流
        
        返回:
            执行成功返回True，失败返回False
        """
        return self.executor.execute()
    
    async def execute_async(self) -> bool:
        """
        异步执行工作流
        
        返回:
            执行成功返回True，失败返回False
        """
        return await self.executor.execute_async()
    
    def save_to_file(self, file_path: str) -> bool:
        """
        将工作流保存到文件
        
        参数:
            file_path: 保存文件的路径
            
        返回:
            保存成功返回True，失败返回False
        """
        try:
            # 序列化工作流
            workflow_data = self.node_tree.serialize()
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Failed to save workflow: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'N8nWorkflow':
        """
        从文件加载工作流
        
        参数:
            file_path: 加载文件的路径
            
        返回:
            加载的工作流对象
        """
        try:
            # 从文件加载数据
            with open(file_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            # 创建新的工作流
            workflow = cls()
            
            # 反序列化工作流
            workflow.node_tree.deserialize(workflow_data)
            
            return workflow
        except Exception as e:
            print(f"Failed to load workflow: {e}")
            raise
    
    def import_from_n8n(self, n8n_workflow_data: Dict[str, Any]) -> bool:
        """
        从n8n工作流数据导入
        
        参数:
            n8n_workflow_data: n8n工作流数据
            
        返回:
            导入成功返回True，失败返回False
        """
        try:
            # 这里需要实现n8n工作流到Blender节点树的转换逻辑
            # 目前只是一个占位符
            print("Importing from n8n workflow data...")
            return True
        except Exception as e:
            print(f"Failed to import from n8n: {e}")
            return False
    
    def export_to_n8n(self) -> Dict[str, Any]:
        """
        导出为n8n工作流数据
        
        返回:
            n8n工作流数据
        """
        try:
            # 这里需要实现Blender节点树到n8n工作流的转换逻辑
            # 目前只是一个占位符
            print("Exporting to n8n workflow data...")
            return {}
        except Exception as e:
            print(f"Failed to export to n8n: {e}")
            raise
    
    def reset(self) -> None:
        """
        重置工作流
        """
        self.node_tree.reset_all_nodes()
        self.executor.execution_results.clear()
    
    def duplicate(self, new_name: str = None) -> 'N8nWorkflow':
        """
        复制工作流
        
        参数:
            new_name: 新工作流的名称
            
        返回:
            复制的工作流对象
        """
        # 序列化当前工作流
        workflow_data = self.node_tree.serialize()
        
        # 创建新的工作流
        new_workflow = self.__class__()
        
        # 设置新名称
        if new_name:
            new_workflow.node_tree.workflow_name = new_name
        
        # 反序列化到新工作流
        new_workflow.node_tree.deserialize(workflow_data)
        
        return new_workflow
    
    def get_nodes_by_type(self, node_type: str) -> List[Any]:
        """
        根据类型获取节点
        
        参数:
            node_type: 节点类型
            
        返回:
            节点列表
        """
        return [node for node in self.node_tree.nodes if node.bl_idname == node_type]
    
    def delete(self) -> None:
        """
        删除工作流
        """
        if self.node_tree in bpy.data.node_groups:
            bpy.data.node_groups.remove(self.node_tree)
    
    @staticmethod
    def get_all_workflows() -> List['N8nWorkflow']:
        """
        获取所有n8n工作流
        
        返回:
            工作流列表
        """
        workflows = []
        for node_group in bpy.data.node_groups:
            if node_group.bl_idname == "N8nNodeTreeType":
                workflows.append(N8nWorkflow(node_group))
        return workflows
    
    @staticmethod
    def get_workflow_by_name(name: str) -> 'N8nWorkflow':
        """
        根据名称获取工作流
        
        参数:
            name: 工作流名称
            
        返回:
            工作流对象，如果不存在返回None
        """
        for node_group in bpy.data.node_groups:
            if node_group.bl_idname == "N8nNodeTreeType" and node_group.name == name:
                return N8nWorkflow(node_group)
        return None
