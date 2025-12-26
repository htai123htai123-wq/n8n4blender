import bpy
import time
import asyncio
from typing import Dict, Any, List
from ..nodes.n8n_node_tree import N8nNodeTree
from ..nodes.n8n_node_base import N8nNodeBase

class N8nExecutor:
    """
n8n工作流执行器，负责执行工作流中的节点
    """
    
    def __init__(self, node_tree: N8nNodeTree):
        """
        初始化执行器
        
        参数:
            node_tree: 要执行的节点树
        """
        self.node_tree = node_tree
        self.execution_results: Dict[str, Any] = {}
        self.is_running = False
    
    def execute(self) -> bool:
        """
        同步执行工作流
        
        返回:
            执行成功返回True，失败返回False
        """
        try:
            self._pre_execute()
            execution_order = self.node_tree.calculate_execution_order()
            
            # 执行每个节点
            for node in execution_order:
                if not self._execute_node(node):
                    self.node_tree.workflow_state = "ERROR"
                    return False
            
            self.node_tree.workflow_state = "SUCCESS"
            return True
        except Exception as e:
            self.node_tree.workflow_state = "ERROR"
            print(f"Workflow execution failed: {e}")
            return False
        finally:
            self.is_running = False
    
    async def execute_async(self) -> bool:
        """
        异步执行工作流
        
        返回:
            执行成功返回True，失败返回False
        """
        try:
            self._pre_execute()
            execution_order = self.node_tree.calculate_execution_order()
            
            # 异步执行每个节点
            for node in execution_order:
                if not await self._execute_node_async(node):
                    self.node_tree.workflow_state = "ERROR"
                    return False
            
            self.node_tree.workflow_state = "SUCCESS"
            return True
        except Exception as e:
            self.node_tree.workflow_state = "ERROR"
            print(f"Workflow execution failed: {e}")
            return False
        finally:
            self.is_running = False
    
    def _pre_execute(self) -> None:
        """
        执行前准备
        """
        self.is_running = True
        self.node_tree.workflow_state = "RUNNING"
        self.node_tree.reset_all_nodes()
        self.execution_results.clear()
        self.start_time = time.time()
    
    def _execute_node(self, node: N8nNodeBase) -> bool:
        """
        执行单个节点
        
        参数:
            node: 要执行的节点
            
        返回:
            执行成功返回True，失败返回False
        """
        try:
            # 设置节点状态为运行中
            node.execution_state = "RUNNING"
            
            # 收集输入数据
            input_data = self._collect_input_data(node)
            
            # 执行节点
            output_data = node.execute(input_data)
            
            # 保存执行结果
            self.execution_results[node.name] = output_data
            
            # 设置节点状态为成功
            node.execution_state = "SUCCESS"
            node.execution_result = str(output_data) if output_data else "Success"
            
            return True
        except Exception as e:
            # 设置节点状态为错误
            node.execution_state = "ERROR"
            node.error_message = str(e)
            print(f"Node {node.name} execution failed: {e}")
            return False
    
    async def _execute_node_async(self, node: N8nNodeBase) -> bool:
        """
        异步执行单个节点
        
        参数:
            node: 要执行的节点
            
        返回:
            执行成功返回True，失败返回False
        """
        try:
            # 设置节点状态为运行中
            node.execution_state = "RUNNING"
            
            # 收集输入数据
            input_data = self._collect_input_data(node)
            
            # 异步执行节点
            loop = asyncio.get_event_loop()
            output_data = await loop.run_in_executor(None, node.execute, input_data)
            
            # 保存执行结果
            self.execution_results[node.name] = output_data
            
            # 设置节点状态为成功
            node.execution_state = "SUCCESS"
            node.execution_result = str(output_data) if output_data else "Success"
            
            return True
        except Exception as e:
            # 设置节点状态为错误
            node.execution_state = "ERROR"
            node.error_message = str(e)
            print(f"Node {node.name} execution failed: {e}")
            return False
    
    def _collect_input_data(self, node: N8nNodeBase) -> Dict[str, Any]:
        """
        收集节点的输入数据
        
        参数:
            node: 要收集输入数据的节点
            
        返回:
            输入数据字典
        """
        input_data = {}
        
        # 遍历所有输入套接字
        for socket in node.inputs:
            # 检查是否有连接
            if socket.is_linked:
                # 获取连接的源节点和套接字
                link = socket.links[0]
                from_node = link.from_node
                from_socket = link.from_socket
                
                # 从源节点的执行结果中获取数据
                if from_node.name in self.execution_results:
                    from_results = self.execution_results[from_node.name]
                    # 尝试从源节点结果中获取对应套接字的数据
                    if isinstance(from_results, dict):
                        input_data[socket.name] = from_results.get(from_socket.name, None)
                    else:
                        # 如果结果不是字典，直接使用整个结果
                        input_data[socket.name] = from_results
            else:
                # 没有连接，检查是否使用默认值
                if hasattr(socket, "use_default_value") and socket.use_default_value:
                    input_data[socket.name] = socket.get_value()
        
        return input_data
    
    def get_execution_result(self, node_name: str) -> Any:
        """
        获取节点执行结果
        
        参数:
            node_name: 节点名称
            
        返回:
            节点执行结果
        """
        return self.execution_results.get(node_name, None)
    
    def stop(self) -> None:
        """
        停止执行
        """
        self.is_running = False
        self.node_tree.workflow_state = "ERROR"
    
    def get_execution_time(self) -> float:
        """
        获取执行时间
        
        返回:
            执行时间（秒）
        """
        if hasattr(self, "start_time"):
            return time.time() - self.start_time
        return 0.0
