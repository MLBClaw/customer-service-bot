# 🤖 智能客服机器人

一个基于 Python Flask 的智能客服机器人，支持意图识别、知识库问答和多轮对话。

## ✨ 功能特性

- **🎯 意图识别**：基于关键词和模式匹配的智能意图识别
- **💬 多轮对话**：支持上下文理解和追问
- **📚 知识库**：可配置的知识库，支持多种问题类型
- **🎨 精美界面**：现代化的聊天界面，支持移动端
- **🔊 语音输入**：支持语音识别输入（浏览器支持）
- **📊 会话管理**：支持会话历史和上下文保存

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行服务

```bash
python app.py
```

或者使用 gunicorn（生产环境）：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. 访问应用

打开浏览器访问：`http://localhost:5000`

## 📁 项目结构

```
customer-service-bot/
├── app.py                 # Flask Web 服务
├── bot.py                 # 机器人核心逻辑
├── requirements.txt       # 依赖列表
├── templates/
│   └── chat.html         # 聊天界面
├── knowledge_base.json   # 知识库（可选）
└── README.md             # 项目说明
```

## 🔧 配置说明

### 知识库配置

知识库支持以下意图类型：

| 意图 | 关键词 | 说明 |
|------|--------|------|
| greeting | 你好、您好、在吗 | 问候语 |
| price | 价格、多少钱、费用 | 价格咨询 |
| hours | 上班时间、工作时间 | 工作时间咨询 |
| refund | 退款、退货、退钱 | 退款问题 |
| shipping | 物流、快递、发货 | 物流查询 |
| complaint | 投诉、不满意、差评 | 投诉反馈 |
| technical | bug、报错、错误 | 技术问题 |
| goodbye | 再见、拜拜、谢谢 | 结束对话 |
| human | 人工、找客服、转人工 | 转人工服务 |

### 自定义知识库

创建 `knowledge_base.json` 文件：

```json
{
    "custom_intent": {
        "keywords": ["关键词1", "关键词2"],
        "responses": [
            "回复内容1",
            "回复内容2"
        ],
        "follow_up": "追问内容（可选）"
    }
}
```

## 📡 API 接口

### 1. 聊天接口

```http
POST /api/chat
Content-Type: application/json

{
    "message": "产品价格是多少？",
    "session_id": "optional-session-id"
}
```

响应：

```json
{
    "success": true,
    "session_id": "session-id",
    "message": "我们的产品价格根据套餐不同有所差异...",
    "intent": "price",
    "confidence": 0.9,
    "suggestions": ["基础版", "专业版", "企业版"],
    "action": null
}
```

### 2. 获取会话历史

```http
GET /api/sessions/{session_id}
```

### 3. 清空会话

```http
DELETE /api/sessions/{session_id}
```

### 4. 获取统计信息

```http
GET /api/stats
```

### 5. 获取知识库

```http
GET /api/knowledge
```

### 6. 健康检查

```http
GET /health
```

## 🐳 Docker 部署

```bash
# 构建镜像
docker build -t customer-service-bot .

# 运行容器
docker run -d -p 5000:5000 customer-service-bot
```

## ☁️ 部署到云平台

### Heroku

```bash
# 创建应用
heroku create your-bot-name

# 推送代码
git push heroku main
```

### Railway / Render

直接连接 GitHub 仓库即可自动部署。

## 🔧 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| PORT | 服务端口 | 5000 |
| DEBUG | 调试模式 | False |

## 📈 扩展开发

### 接入大模型 API

可以修改 `bot.py` 中的 `reply` 方法，接入 ChatGPT、Claude 等大模型：

```python
def reply(self, user_message: str, session_id: str = "default") -> dict:
    # 调用大模型 API
    response = call_llm_api(user_message, session_history)
    return {
        "message": response,
        "intent": "llm",
        "confidence": 1.0
    }
```

### 接入数据库

可以将会话数据存储到 Redis、MongoDB 等数据库中，支持分布式部署。

## 📝 更新日志

### v1.0.0
- ✅ 基础意图识别
- ✅ Web 聊天界面
- ✅ 会话管理
- ✅ 知识库支持
- ✅ RESTful API

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**提示**：如需接入真实的大模型（GPT-4、Claude 等），只需修改 `bot.py` 中的回复逻辑即可。
