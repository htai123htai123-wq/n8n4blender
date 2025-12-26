import bpy
from .n8n_node_base import (
    N8nNodeTree,
    N8nNodeBase,
    register_node_categories,
    unregister_node_categories
)
from .sockets import (
    register_socket_classes,
    unregister_socket_classes,
    get_socket_class
)
from .node_factory import (
    register_node_classes,
    unregister_node_classes,
    get_nodes_data
)

# 注册所有组件
def register():
    # 注册套接字类
    register_socket_classes()
    
    # 注册节点树
    bpy.utils.register_class(N8nNodeTree)
    
    # 注册节点类
    register_node_classes()
    
    # 注册节点类别
    register_node_categories()

# 注销所有组件
def unregister():
    # 注销节点类别
    unregister_node_categories()
    
    # 注销节点类
    unregister_node_classes()
    
    # 注销节点树
    bpy.utils.unregister_class(N8nNodeTree)
    
    # 注销套接字类
    unregister_socket_classes()