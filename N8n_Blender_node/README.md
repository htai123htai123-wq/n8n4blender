# N8n Blender Node

N8n Blender Node 是一个 Blender 插件，它允许您在 Blender 中创建和管理 n8n 工作流。

## 功能特性

- 在 Blender 中创建和编辑 n8n 工作流
- 可视化节点编辑器界面
- 工作流执行和调试
- 多语言支持（英语、简体中文、繁体中文）
- 工作流导入/导出功能
- 节点搜索和分类浏览
- 自定义快捷键支持

## 安装方法

1. 下载插件压缩包
2. 打开 Blender，进入 `编辑 > 偏好设置 > 插件`
3. 点击 `安装...` 按钮，选择下载的插件压缩包
4. 启用 "N8n Workflow Editor" 插件

## 使用方法

### 创建新工作流

1. 在 Blender 中切换到 `脚本编写` 工作区
2. 打开 `节点编辑器`
3. 点击 `添加 > n8n Workflow` 创建新的 n8n 节点树
4. 使用快捷键 `Shift+A` 打开节点菜单，添加节点
5. 连接节点创建工作流

### 执行工作流

1. 选择要执行的工作流
2. 点击 `执行` 按钮或使用快捷键 `Ctrl+E`
3. 查看执行结果和状态

### 导入/导出工作流

1. 在工作流面板中点击 `导入` 或 `导出` 按钮
2. 选择文件路径并确认操作

## 快捷键

- `Shift+A`: 打开节点菜单
- `Ctrl+E`: 执行工作流
- `Ctrl+R`: 重置工作流

## 配置选项

在插件偏好设置中，您可以配置：

- API URL: n8n 实例的地址
- API 密钥: 用于身份验证的密钥
- 自动连接: 启动时自动连接到 n8n
- 调试模式: 启用调试日志
- 主题: UI 主题选择
- 语言: 界面语言选择

## 支持的节点类型

- HTTP Request: 发送 HTTP 请求
- Set: 设置数据属性
- If: 条件分支
- Switch: 多路分支
- Merge: 合并数据流
- Code: 执行 JavaScript 代码
- Webhook: Webhook 触发器
- Manual Trigger: 手动触发器
- Schedule Trigger: 定时触发器
- Function: 自定义函数
- Function Item: 每项数据处理函数
- No Operation: 空操作
- Start: 工作流开始
- Stop and Error: 停止并报错

## 开发

如果您想为这个插件贡献代码，请遵循以下步骤：

1. Fork 这个仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 GPL-3.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

如果您有任何问题或建议，请通过以下方式联系我们：

- 官方文档: [https://docs.n8n.io/](https://docs.n8n.io/)
- 社区论坛: [https://community.n8n.io/](https://community.n8n.io/)
- GitHub 仓库: [https://github.com/n8n-io/n8n](https://github.com/n8n-io/n8n)

## 致谢

感谢 n8n 社区的所有贡献者，以及 Blender 社区提供的优秀平台。