from common.i18n.dictionary import preprocess_dictionary

dictionary = {
    "zh_CN": {
        # 界面元素
        "title": "N8n 工作流节点",
        
        # 面板标题
        "workflow_panel": "N8n 工作流",
        "node_panel": "N8n 节点",
        "help_panel": "帮助与文档",
        
        # 按钮文本
        "execute": "执行",
        "reset": "重置",
        "new": "新建",
        "open": "打开",
        "save": "保存",
        "delete": "删除",
        "export": "导出",
        "import": "导入",
        "copy": "复制",
        "add_node": "添加节点",
        "search": "搜索",
        
        # 状态信息
        "status": "状态",
        "running": "运行中",
        "completed": "已完成",
        "failed": "失败",
        "idle": "空闲",
        
        # 消息提示
        "no_workflow_selected": "未选择工作流",
        "workflow_executed": "工作流执行成功",
        "workflow_failed": "工作流执行失败",
        "node_added": "节点添加成功",
        "node_deleted": "节点删除成功",
        "workflow_saved": "工作流保存成功",
        "workflow_loaded": "工作流加载成功",
        
        # 帮助文档
        "documentation": "文档",
        "api_reference": "API参考",
        "examples": "示例",
        "community": "社区",
        
        # 节点类别
        "regular": "常规",
        "trigger": "触发器",
        "webhook": "Webhook",
        "transform": "转换",
        "action": "动作",
        "utility": "工具",
        
        # 属性标签
        "name": "名称",
        "description": "描述",
        "version": "版本",
        "author": "作者",
        "category": "类别",
        "parameters": "参数",
        "credentials": "凭证",
        "webhook_url": "Webhook URL",
        "execution_time": "执行时间",
        "last_run": "上次运行",
        
        # 错误信息
        "error": "错误",
        "warning": "警告",
        "info": "信息",
        "connection_failed": "连接失败",
        "invalid_parameters": "无效参数",
        "file_not_found": "文件未找到",
        "permission_denied": "权限被拒绝",
        
        # 其他
        "loading": "加载中...",
        "please_wait": "请稍候...",
        "cancel": "取消",
        "confirm": "确认",
        "yes": "是",
        "no": "否",
        "ok": "确定",
    },
    
    "en": {
        # 界面元素
        "title": "N8n Workflow Nodes",
        
        # 面板标题
        "workflow_panel": "N8n Workflow",
        "node_panel": "N8n Nodes",
        "help_panel": "Help & Documentation",
        
        # 按钮文本
        "execute": "Execute",
        "reset": "Reset",
        "new": "New",
        "open": "Open",
        "save": "Save",
        "delete": "Delete",
        "export": "Export",
        "import": "Import",
        "copy": "Copy",
        "add_node": "Add Node",
        "search": "Search",
        
        # 状态信息
        "status": "Status",
        "running": "Running",
        "completed": "Completed",
        "failed": "Failed",
        "idle": "Idle",
        
        # 消息提示
        "no_workflow_selected": "No workflow selected",
        "workflow_executed": "Workflow executed successfully",
        "workflow_failed": "Workflow execution failed",
        "node_added": "Node added successfully",
        "node_deleted": "Node deleted successfully",
        "workflow_saved": "Workflow saved successfully",
        "workflow_loaded": "Workflow loaded successfully",
        
        # 帮助文档
        "documentation": "Documentation",
        "api_reference": "API Reference",
        "examples": "Examples",
        "community": "Community",
        
        # 节点类别
        "regular": "Regular",
        "trigger": "Trigger",
        "webhook": "Webhook",
        "transform": "Transform",
        "action": "Action",
        "utility": "Utility",
        
        # 属性标签
        "name": "Name",
        "description": "Description",
        "version": "Version",
        "author": "Author",
        "category": "Category",
        "parameters": "Parameters",
        "credentials": "Credentials",
        "webhook_url": "Webhook URL",
        "execution_time": "Execution Time",
        "last_run": "Last Run",
        
        # 错误信息
        "error": "Error",
        "warning": "Warning",
        "info": "Info",
        "connection_failed": "Connection failed",
        "invalid_parameters": "Invalid parameters",
        "file_not_found": "File not found",
        "permission_denied": "Permission denied",
        
        # 其他
        "loading": "Loading...",
        "please_wait": "Please wait...",
        "cancel": "Cancel",
        "confirm": "Confirm",
        "yes": "Yes",
        "no": "No",
        "ok": "OK",
    }
}

dictionary = preprocess_dictionary(dictionary)

dictionary["zh_HANS"] = dictionary["zh_CN"]