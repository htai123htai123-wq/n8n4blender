from .n8n_node_base import N8nNodeBase
from .n8n_node_tree import N8nNodeTree, N8nNodeTreeSpace
from .n8n_socket import N8nSocket, N8nSocketMixin
from .n8n_blueprints import node_blueprints, register_builtin_blueprints, N8nNodeBlueprint
from .n8n_node_menu import register as register_menu, unregister as unregister_menu
from ..manager.n8n_parser import N8nParser
import os

# 确保蓝图被注册
register_builtin_blueprints()

# 加载nodes.json文件
parser = N8nParser()
nodes_json_path = os.path.join(os.path.dirname(__file__), 'nodes.json')

if os.path.exists(nodes_json_path):
    parser.load_node_definitions_from_file(nodes_json_path)
    
    # 将解析后的节点定义注册为蓝图
    for node_key, node_def in parser.node_definitions.items():
        try:
            blueprint = parser.parse_node_definition(node_def)
            if blueprint:
                # 创建蓝图对象
                node_blueprint = N8nNodeBlueprint(
                    blueprint_id=node_key,
                    name=blueprint['name'],
                    description=blueprint['description'],
                    group=blueprint.get('group', 'general')
                )
                
                # 添加属性
                for prop_name, prop_data in blueprint['properties'].items():
                    node_blueprint.add_property(
                        name=prop_name,
                        value=prop_data['value'],
                        description=prop_data['description']
                    )
                
                # 添加输入套接字
                for input_data in blueprint['inputs']:
                    node_blueprint.add_input(
                        name=input_data['name'],
                        data_type=input_data['data_type'],
                        default_value=input_data['default_value'],
                        use_default=input_data['use_default'],
                        description=input_data['description']
                    )
                
                # 添加输出套接字
                for output_data in blueprint['outputs']:
                    node_blueprint.add_output(
                        name=output_data['name'],
                        data_type=output_data['data_type'],
                        description=output_data['description']
                    )
                
                # 注册蓝图
                node_blueprint.register()
        except Exception as e:
            print(f"Failed to register blueprint for node {node_key}: {e}")


