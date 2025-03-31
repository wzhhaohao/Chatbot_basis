# 功能介绍

## 项目概述

Chatbot是一个大模型api调用的简短代码，实际上没什么卵用,这跟就是自己瞎琢磨着玩的，因为有很多开源的项目已经做过了，例如CherryStudio等等。

## 功能特点

### 1. **文本与文件处理**
（这一块内容并没有一一实验过）
- 支持读取多种文件格式：
  - `.txt`、`.md`：纯文本文件
  - `.csv`、`.xls`、`.xlsx`：表格文件
  - `.json`：JSON 文件
  - `.docx`：Word 文档
  - `.pdf`：PDF 文件（支持 OCR 图像文字识别）
  - `.png`、`.jpg`、`.jpeg`：图片文件（通过 OCR 提取文本）
  
### 2. **助手设置**
- 主要就是自定义了一下助手的功能，可以自己改一下。

### 3. **文件提取功能**
- 从 PDF 文件提取文本，如果 PDF 中包含图像，自动执行 OCR 进行文字识别。
- 从图像文件（如 `.png`, `.jpg`, `.jpeg`）中提取文本。

### 4. **流式输出支持**
- 可选择开启流式输出，逐段显示生成的内容，适用于长文本的实时交互式展示。

### 5. **对话记录保存**
- 可以将整个对话过程保存为 Markdown 格式文件，便于后续查看或文献管理。
- 支持自动生成对话标题，并将对话历史存储在本地 `history` 文件夹中。

## 安装依赖

1. 克隆此项目到本地：
   ```bash
   git clone https://github.com/yourusername/chimera-chatbot.git
   ```

2. 安装所需的 Python 包：
   ```bash
   pip install -r requirements.txt
   ```

3. 创建一个 `.env` 文件，填入 DeepSeek API 密钥：
   ```bash
   DEEPSEEK_API_KEY=your_api_key
   DEEPSEEK_API_URL=your_api_url
   ```

## 使用说明

1. 运行 `chat.py` 文件以启动聊天机器人：
   ```bash
   python chat.py
   ```

2. 输入文本或文件路径与机器人进行对话，您可以：
   - 输入文件路径，机器人会自动读取文件内容并进行分析。
   - 输入文本，机器人将根据输入内容进行响应。
   - 输入 `exit` 或 `quit` 结束对话。

3. 支持开启流式输出，逐段显示机器人返回的内容。

4. 可以选择将对话记录保存为 Markdown 文件。

## 项目结构

- `chatbot.py`: 主程序文件，包含聊天机器人功能。
- `requirements.txt`: 所需 Python 包列表。
- `.env`: 环境变量文件，存储 DeepSeek API 密钥和 URL。
- `history/`: 存储保存的对话记录。
- `README.md`: 项目说明文件。


