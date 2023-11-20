import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import requests

# 默认的提交内容
default_text = """
君不见，黄河之水天上来，奔流到海不复回。
君不见，高堂明镜悲白发，朝如青丝暮成雪。
人生得意须尽欢，莫使金樽空对月。
天生我材必有用，千金散尽还复来。
"""

def send_request(text, file_path, voice):
    # OpenAI的API密钥，你需要替换为你自己的密钥
    api_key = "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"

    # 设置请求头部
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # 设置请求的正文（body）
    data = {
        "model": "tts-1",
        "voice": voice,  # 使用用户选择的声音
        "input": text
    }

    # OpenAI的文本转语音API URL
    url = "https://api.openai.com/v1/audio/speech"

    # 发送POST请求
    response = requests.post(url, json=data, headers=headers)

    # 如果请求成功，保存文件
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return "Success", file_path
    else:
        return "Error", response.text

def on_submit():
    text = text_input.get("1.0", "end-1c")
    file_path = file_path_var.get()
    selected_voice = voice_var.get()  # 获取用户选择的声音
    result_label.config(text="正在生成语音，请稍候...")
    status, message = send_request(text, file_path, selected_voice)
    if status == "Success":
        result_label.config(text=f"语音文件已保存到: {message}")
    else:
        messagebox.showerror("错误", message)

def browse_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        file_path_var.set(file_path)

# 创建窗口
root = tk.Tk()
root.title("文本转语音")

# 设置窗口尺寸
root.geometry("500x650")
root.resizable(True, True)

# 使用现代化的主题
style = ttk.Style(root)
style.theme_use("clam")

# 设置颜色和样式
style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
style.configure("TButton", font=('Arial', 10))
style.configure("TEntry", font=('Arial', 10))

# 设置窗口背景色
root.configure(background="#f0f0f0")

# 创建文本输入框
text_input = tk.Text(root, font=('Arial', 12))
text_input.insert("1.0", default_text)  # 设置默认文本内容
text_input.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))

# 创建声音选择框架
voice_frame = ttk.Frame(root)
voice_frame.pack(fill=tk.BOTH, padx=20, pady=(0, 10))

# 创建声音选择标签
voice_label = ttk.Label(voice_frame, text="选择声音:", background="#f0f0f0")
voice_label.pack(side=tk.LEFT, padx=(0, 5))

# 创建声音选择下拉菜单
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
voice_var = tk.StringVar()
voice_var.set(voices[0])  # 设置默认选项
voice_combobox = ttk.Combobox(voice_frame, textvariable=voice_var, values=voices)
voice_combobox.pack(side=tk.LEFT, padx=(5, 0))

# 创建输出目录和浏览按钮的框架
output_frame = ttk.Frame(root)
output_frame.pack(fill=tk.BOTH, padx=20, pady=(0, 10))

# 创建文件路径输入框
file_path_label = ttk.Label(output_frame, text="输出目录:", background="#f0f0f0")
file_path_label.pack(side=tk.LEFT, padx=(0, 5))

file_path_var = tk.StringVar()
file_path_var.set(os.path.join(os.path.dirname(os.path.abspath(__file__)), "speech.mp3"))
file_path_entry = ttk.Entry(output_frame, textvariable=file_path_var)
file_path_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 创建浏览按钮
browse_button = ttk.Button(output_frame, text="浏览", command=browse_file)
browse_button.pack(side=tk.LEFT, padx=(5, 0))

# 创建提交按钮，并使其居中
submit_button = ttk.Button(root, text="提交", command=on_submit)
submit_button.pack(padx=20, pady=(0, 20), ipadx=50)  # 使用ipadx来设置按钮宽度

# 创建结果标签
result_label = ttk.Label(root, text="", background="#f0f0f0")
result_label.pack(fill=tk.BOTH, padx=20, pady=(0, 20))

# 运行事件循环
root.mainloop()
