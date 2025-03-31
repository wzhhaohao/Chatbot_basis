import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import pandas as pd
from docx import Document
import json
import zipfile
from PIL import Image
import pytesseract
import fitz  # pymupdf
from pdf2image import convert_from_path


# 加载环境变量
load_dotenv("my.env")

# 获取 DeepSeek API 密钥
deepseek_api_key = os.getenv("DeepSeek_API_KEY")

# DeepSeek API 的 URL（请根据实际的 API 路径修改）
deepseek_api_url = os.getenv("DeepSeek_API_URL")

# 检查 API 密钥和 URL 是否存在
client = OpenAI(api_key = deepseek_api_key, base_url = deepseek_api_url)

# 想使用的模型
model = input("请输入模型名称（如：deepseek-V3:0, deepseek-r1:1）：")
if model == 0:
    model = "deepseek-chat"  # 默认模型
elif model == 1:
    print("使用深度推理模型 deepseek-reasoner。但是在api的调用中暂时没有打开思维链，因为贵")
    model = deepseek-reasoner
else:
    print("无效的模型名称，使用默认模型 deepseek-chat。")
    model = "deepseek-chat"

# 初始化对话上下文
messages = [
    {
        "role": "system", 
        "content": """#### 定位
        - 智能助手名称 ：统计学与公共卫生专家
        - 主要任务 ：提供统计建模、数学公式推导、流行病问题分析、临床医学与基础医学、预防医学领域的咨询与分析，同时提供中英文论文写作指导。

        #### 能力
        - **统计建模** ：能够进行复杂的统计建模，包括回归分析、贝叶斯分析等，应用于流行病学和公共卫生数据分析。
        - **数学公式推导** ：能够理解和推导统计学、流行病学和医学领域的数学公式，并进行实际应用。
        - **流行病学问题分析** ：深入分析流行病学问题，结合现有的公共卫生数据进行预测、趋势分析及干预效果评估。
        - **临床医学与基础医学** ：具备临床医学和基础医学知识，能够分析医学研究中的数据，推导临床试验结果。
        - **预防医学知识** ：了解并能够运用预防医学的基本原理和方法，提供预防策略的建议。
        - **代码能力** ：擅长使用 Python 和 R 语言进行数据分析、统计建模、机器学习和深度学习算法的实现。
        - **深度学习与机器学习** ：具备深度学习和机器学习的基础知识，能够在实际问题中应用这些技术。
        - **文献分析与提取关键点** ：能够高效阅读医学与公共卫生领域的文献，提取关键点，分析研究成果。
        - **文献分类与识别** ：能够对文献进行分类和识别，区分不同类型的研究（如临床研究、流行病学研究、基础医学研究等）。
        - **中英文论文写作能力**：
        - **英文论文写作** ：能够帮助撰写医学与公共卫生领域的英文论文，包括结构建议（如引言、方法、结果、讨论），语言表达优化，语法校正，以及参考文献格式化。
        - **中文论文写作** ：能够帮助撰写医学与公共卫生领域的中文论文，提供中文论文结构建议，语言优化，常见写作错误修正，以及符合中文期刊要求的格式化建议。
        - **文献综述** ：能够编写和优化文献综述，帮助整合相关领域的研究成果，进行批判性分析和比较。

        #### 使用说明
        - 输入 ：一段与统计学、公共卫生、临床医学或流行病学相关的问题或数据，或提出与论文写作相关的请求（例如论文结构、语言修改、文献综述等）。
        - 输出 ：提供问题的解答、分析结果或相关建议，包含详细的统计建模步骤、数学推导过程、代码实现或论文写作指导。

        #### 输出格式
        - 所有回复请使用 **Markdown 格式**，包括标题、列表、公式、代码块、强调等。
        """
    }
]

# 获取当前时间字符串
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")  # e.g., 2025-03-31_15-42-00

# 函数块
# 读取文件内容或者读取用户输入的文本
def process_user_input(user_input):
    """检查用户输入并处理（文件或文本）"""
    global messages  # 声明 messages 是全局变量
    if os.path.isfile(user_input):
        # 读取文件内容
        file_content = read_file(user_input)
        print(f"文件内容：\n{file_content}")
        messages.append({"role": "user", "content": file_content})
    else:
        # 用户直接输入文本
        messages.append({"role": "user", "content": user_input})

    return messages  # 返回更新后的 messages

# 读取文件内容
def read_file(file_path):
    """读取支持的多种格式文件：.txt, .md, .csv, .docx, .pdf, .png, .jpg, .json"""
    ext = os.path.splitext(file_path)[-1].lower()

    try:
        if ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

        elif ext == '.csv':
            df = pd.read_csv(file_path)
            return df.to_string(index=False)

        elif ext in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
            return df.to_string(index=False)

        elif ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return json.dumps(data, indent=2, ensure_ascii=False)

        elif ext == '.docx':
            doc = Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])

        elif ext == '.pdf':
            text = extract_text_from_pdf(file_path)
            return text.strip()

        elif ext in ['.png', '.jpg', '.jpeg']:
            img = Image.open(file_path)
            return pytesseract.image_to_string(img)

        elif ext == '.doc':
            return "暂不支持 .doc 格式，请转换为 .docx"

        else:
            return f"不支持的文件类型：{ext}"

    except Exception as e:
        return f"读取文件时出错：{e}"


def extract_text_from_pdf(file_path):
    """从 PDF 提取文本，包括图像中的 OCR 文本"""
    text = ""
    doc = fitz.open(file_path)
    
    # 提取 PDF 中的文本
    for page in doc:
        text += page.get_text()

    # 如果提取的文本为空，尝试从 PDF 页面图像中进行 OCR 提取
    if not text.strip():
        images_text = extract_text_from_pdf_images(file_path)
        text += images_text

    return text


def extract_text_from_pdf_images(file_path):
    """从 PDF 页面中的图像提取文本（OCR）"""
    text = ""
    # 使用 pdf2image 将每个页面转换为图像
    pages = convert_from_path(file_path, 300)  # 300 dpi 是较高质量的转换

    # 对每一页图像执行 OCR 识别
    for page_num, page in enumerate(pages):
        print(f"正在处理 PDF 第 {page_num + 1} 页的图像...")
        page_text = pytesseract.image_to_string(page)
        text += f"\n--- 第 {page_num + 1} 页 ---\n{page_text}"

    return text



def chat():
    print("欢迎Chimera的chatbot001号！")
    print("请注意：\n1. 输入 'exit' 或 'quit' 或 'q' 或 ‘退出’ 或 '结束' 退出聊天。\n2. 输入文件路径以读取文件内容。\n3. 输入文本进行交互。")
    
    stream = input("是否开启流式输出？（y/n）")
    if stream.lower() == 'y':
        stream = True
    else:
        stream = False

    while True:
        # 获取用户输入（也可以是一个文件路径）
        user_input = input("请输入文本（或文件路径）：")
        
        # 如果输入 'exit' 或 'quit' 或 'q' 或 ‘退出’ 或 '结束'，退出聊天
        if user_input.lower() in ['exit', 'quit', '退出', '结束', 'q']:
            print("聊天结束。")
            break
    
        # 处理用户输入（文本或者文件）
        messages = process_user_input(user_input)

        # 准备请求数据
        response = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = 0.6,  # 控制生成文本的多样性,腾讯云的API建议是0.6，一般在0.5-0.7之间
        max_tokens = 4000,  # 限制生成的文本最大长度 这里是测试版本，自己用可以调高 3000
        stream = stream,  # 是否开启流式输出
    )
        print("Chimera的chatbot001号：")
        # 如果开启流式输出，打印每一段返回的内容
        if stream:
            # 初始化一个变量来保存完整的生成内容
            full_reply = ""

            for chunk in response:
                # print(chunk)
                chunk_content = ""
                if chunk.choices:
                    chunk_content = chunk.choices[0].delta.content
                    print(chunk_content, end='', flush=True)  # 打印当前块的内容
                    full_reply += chunk_content
            print()  # 打印换行符
                    
        else:       
            # 如果没有开启流式输出，直接打印返回的内容
            if response.choices[0].message.content == "":
                print("没有返回内容")
            else:
                full_reply = response.choices[0].message.content
                print(full_reply)

        # 将返回的内容添加到消息列表中
        messages.append({"role": "assistant", "content": f"/n {full_reply}"})

        # 提示用户继续输入
        print("请继续输入文本或文件路径，或者输入 'exit' 或 'quit' 退出聊天。")


def save_conversation():
    # 请求生成标题
    response = client.chat.completions.create(
        model = model,
        messages=messages,
        temperature=0.5,
        max_tokens=20,
        stream=False,
    )

    messages.append({"role": "user", "content": "严格用10个token以内的标题总结以上全部对话内容"})

    # 获取标题并清理非法字符
    title = response.choices[0].message.content.strip()
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    if not title:
        title = "conversation_summary"

    # 创建 history 目录（如不存在则创建）
    history_dir = os.path.join(os.getcwd(), "history")
    os.makedirs(history_dir, exist_ok=True)

    # 拼接文件路径（带时间戳）
    filename = f"{timestamp}_{title}.md"
    file_path = os.path.join(history_dir, filename)

    del messages[0]
    messages.pop(0)

    # 写入文件
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"# {title}\n\n")
        file.write(f"## 使用模型{model}\n\n")
        for message in messages:
            file.write(f"{message['role']}: {message['content']}\n")

    print(f"对话记录已保存为 {file_path}")


# 启动聊天
if __name__ == "__main__":
    chat()  
    if input("是否保存本次对话记录？(y/n) ").lower() == 'y':
        save_conversation()

