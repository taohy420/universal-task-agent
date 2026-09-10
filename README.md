# 通用任务执行 Agent

这是一个从零实现的轻量级 AI Agent 项目，支持 DeepSeek API、Ollama 本地模型、Function Calling、本地 Python 工具和 MCP 工具接入。

本项目重点不是堆复杂框架，而是证明我理解 Agent 的核心原理：LLM 负责决策，工具负责执行，Agent Loop 负责把工具结果重新放回上下文，让模型继续推理。

## 功能特性

- 支持 DeepSeek API 云端模型
- 支持 Ollama 本地模型
- 统一 LLM 调用接口
- 支持 Function Calling / Tool Calling
- 自己实现 Agent Loop
- 支持多步骤工具调用
- 本地 Python 工具：
  - calculator
  - get_weather
  - save_note
- 支持 MCP Server / Client
- 统一本地工具和 MCP 工具调用
- 支持 Agent Trace 执行轨迹
- 支持 MAX_STEPS 最大步数保护
- 支持基础工具异常处理

## Demo Cases
Case 1：计算 + 保存笔记
请计算 12 * 8 + 5，并把结果保存成笔记。

Case 2：天气查询 + 条件判断 + 保存笔记
请查询 Shanghai 的天气，如果下雨，就把今天带伞保存成笔记。

Case 3：MCP 工具 + 本地工具混合调用
请调用 echo_text 工具发送 hello mcp agent，然后把返回结果保存成笔记。
```powershell
python src\main.py 1
python src\main.py 2
python src\main.py 3

核心流程
User -> LLM -> Tool Call -> Tool Execution -> Observation -> LLM -> Final Answer

项目结构
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
    weather.py
    save_note.py
    registry.py

  mcp_servers/
    simple_server.py

  mcp_client/
    client.py

快速开始

安装依赖：
pip install -r requirements.txt
复制配置文件：
copy .env.example .env
然后编辑 .env，填入自己的 DeepSeek API Key。
项目边界
本项目暂时不使用：
- LangChain
- LangGraph
- FastAPI
- 数据库
- 复杂前端
- RAG
项目重点是理解和实现 Agent 的核心机制，而不是依赖高级框架封装。
Known Limitations
- calculator 当前使用 eval，真实项目中应替换为更安全的表达式解析方案。
- weather 当前是假数据，用于演示工具调用流程。
- MCP 工具 schema 当前为手动合并，后续可以改为动态发现。
- Ollama 小模型在复杂多步骤工具调用中可能不如云端大模型稳定。