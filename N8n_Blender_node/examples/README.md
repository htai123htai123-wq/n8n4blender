# N8n Blender插件示例

本目录包含了N8n Blender插件的示例工作流和使用案例，帮助您快速了解插件的功能和使用方法。

## 示例文件

### 1. sample_workflow.json
这是一个完整的Blender渲染工作流示例，展示了如何使用N8n插件自动化Blender渲染流程。

#### 工作流说明
此工作流包含以下节点：
1. **Start** - 工作流开始节点
2. **设置渲染参数** - 配置Blender渲染引擎、分辨率等参数
3. **检查场景** - 验证场景是否包含必要的对象（物体、灯光、摄像机）
4. **渲染场景** - 通过API调用执行渲染操作
5. **错误处理** - 当场景不完整时添加默认对象
6. **保存结果** - 将渲染结果保存到指定路径
7. **发送通知** - 渲染完成后发送通知
8. **End** - 工作流结束节点

#### 如何使用
1. 在Blender中打开N8n插件
2. 点击"导入工作流"按钮
3. 选择`sample_workflow.json`文件
4. 根据需要修改工作流参数
5. 点击"执行工作流"按钮

## 自定义工作流

### 创建新工作流
1. 在Blender中打开N8n插件
2. 点击"新建工作流"按钮
3. 从节点面板拖拽所需节点到工作区
4. 连接节点并配置参数
5. 保存工作流

### 工作流最佳实践
1. **使用描述性名称** - 为节点和工作流使用清晰的名称
2. **添加注释** - 在关键节点添加描述性注释
3. **错误处理** - 为可能失败的操作添加错误处理节点
4. **模块化设计** - 将复杂工作流分解为可重用的子工作流
5. **测试验证** - 在生产环境使用前充分测试工作流

## 常见工作流模式

### 1. 批量渲染工作流
用于批量渲染多个场景或文件：
```
Start → 读取文件列表 → 循环处理 → 渲染场景 → 保存结果 → End
```

### 2. 场景优化工作流
用于自动优化Blender场景：
```
Start → 分析场景 → 优化设置 → 应用优化 → 保存场景 → End
```

### 3. 资源管理工作流
用于管理Blender项目资源：
```
Start → 扫描资源 → 分类整理 → 清理未使用资源 → 更新链接 → End
```

## API集成示例

### 与外部渲染农场集成
```json
{
  "id": "render_farm",
  "name": "提交到渲染农场",
  "type": "http_request",
  "parameters": {
    "url": "https://renderfarm.example.com/api/submit",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer {{$credentials.apiKey}}",
      "Content-Type": "application/json"
    },
    "body": {
      "blend_file": "{{$json.file_path}}",
      "settings": "{{$json.render_settings}}",
      "priority": "high"
    }
  }
}
```

### 与云存储集成
```json
{
  "id": "upload_to_cloud",
  "name": "上传到云存储",
  "type": "http_request",
  "parameters": {
    "url": "https://storage.example.com/upload",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer {{$credentials.apiKey}}"
    },
    "body": {
      "file": "{{$json.render_result}}",
      "path": "renders/{{$now}}.png"
    }
  }
}
```

## 故障排除

### 常见问题
1. **工作流执行失败** - 检查节点连接和参数配置
2. **API调用错误** - 验证API端点和认证信息
3. **文件路径问题** - 确保文件路径正确且可访问
4. **权限问题** - 确保Blender有足够权限执行所需操作

### 调试技巧
1. 使用"调试模式"查看详细执行日志
2. 在关键节点添加中间输出检查数据流
3. 使用"测试执行"验证单个节点功能
4. 检查Blender控制台输出获取错误信息

## 更多资源

- [N8n官方文档](https://docs.n8n.io/)
- [Blender Python API文档](https://docs.blender.org/api/current/)
- [插件Wiki](https://github.com/your-repo/n8n-blender-plugin/wiki)
- [社区论坛](https://forum.example.com/n8n-blender)

## 贡献示例

欢迎提交您的工作流示例！请确保：
1. 工作流功能完整且可正常执行
2. 包含清晰的说明文档
3. 使用通用场景，避免依赖特定资源
4. 遵循命名和结构约定

提交示例请创建Pull Request或联系开发团队。