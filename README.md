# 轻量级 Agent 学习项目

这是一个用于理解 Agent 核心流程的小项目。项目重点是看清楚：

- 用户输入如何进入程序
- LLM 如何接收 messages 和 tools
- LLM 如何返回 tool_calls
- Python 程序如何真正执行工具
- Tool Result 如何写回 messages
- Agent Loop 如何继续运行直到得到最终回答

## 当前功能

- 循环交互式输入
- 运行期间的多轮聊天记忆
- DeepSeek API 调用
- Agent Loop
- 本地 Python Tool
  - calculator
- MCP Tools
  - get_weather
  - get_hot_news
- Tool Schema
- Tool Calling / Function Calling
- Tool Result 回传给 LLM
- Agent Trace 执行轨迹
- MAX_STEPS 最大步数保护

## 运行方式

安装依赖：

```powershell
pip install -r requirements.txt
```

复制配置文件：

```powershell
copy .env.example .env
```

然后编辑 `.env`，填入自己的 DeepSeek API Key。

启动：

```powershell
python src\main.py
```

退出：

```text
exit
```

当前记忆范围：

```text
程序运行期间：会记住前面聊过的内容
程序退出以后：不会保存长期记忆
```

## 可以尝试的问题

```text
请计算 12 * 8 + 5
```

```text
请查询上海现在的天气
```

```text
帮我做一个上海周末两日游攻略，可以结合当前天气
```

```text
帮我获取今天三条热点新闻
```

## 项目结构

```text
src/
  main.py
  config.py

  llms/
    base.py
    deepseek_client.py
    ollama_client.py

  agent/
    loop.py
    trace.py

  tools/
    calculator.py
    registry.py

  mcp_servers/
    simple_server.py

  mcp_client/
    client.py
```

## 核心流程

```text
用户输入
↓
main.py
↓
run_agent()
↓
messages + tool schemas
↓
LLM
↓
tool_calls?
├─ 没有：最终回答
└─ 有：
   ↓
   registry.py
   ↓
   本地 calculator 或 MCP tool
   ↓
   Tool Result
   ↓
   写回 messages
   ↓
   再次调用 LLM
```

## 工具分工

本地 Python Tool：

```text
calculator
```

MCP Tool：

```text
get_weather
get_hot_news
```

`registry.py` 负责根据 LLM 返回的工具名，把调用分发到本地 Python 函数或 MCP Client。

## 项目边界

本项目暂时不使用：

- LangChain
- LangGraph
- FastAPI
- 数据库
- 复杂前端
- RAG

项目重点是理解 Agent 的核心机制，而不是依赖高级框架封装。
