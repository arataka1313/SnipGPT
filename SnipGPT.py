import os
import sys
import platform
import base64
import openai
import tkinter as tk
from dotenv import load_dotenv
from PIL import ImageGrab

# WindowsのDPI補正（Mac不要）
if platform.system() == "Windows":
    try:
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

start_x = start_y = end_x = end_y = 0

def select_area():
    def on_mouse_down(event):
        nonlocal rect
        canvas.delete("rect")
        global start_x, start_y
        start_x, start_y = event.x, event.y
        rect = canvas.create_rectangle(
            start_x, start_y, start_x, start_y,
            outline='blue', width=3, tag="rect"
        )

    def on_mouse_move(event):
        if rect:
            canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        global end_x, end_y
        end_x, end_y = event.x, event.y
        root.quit()

    root = tk.Tk()
    root.attributes('-alpha', 0.3)
    root.attributes('-fullscreen', True)
    root.configure(background='black')
    canvas = tk.Canvas(root, cursor="cross", bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    rect = None

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_move)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()
    root.destroy()


def ensure_problem_dir():
    if not os.path.exists("problems"):
        os.makedirs("problems")


def get_next_problem_filename():
    ensure_problem_dir()
    i = 1
    while True:
        filename = f"problems/problem{i}.png"
        if not os.path.exists(filename):
            return filename
        i += 1


def capture_selected_area():
    x1, y1 = min(start_x, end_x), min(start_y, end_y)
    x2, y2 = max(start_x, end_x), max(start_y, end_y)
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    filename = get_next_problem_filename()
    img.save(filename)
    return filename


def ensure_answer_dir():
    if not os.path.exists("answer"):
        os.makedirs("answer")


def get_next_answer_filename():
    i = 1
    while True:
        filename = f"answer/answer{i}.txt"
        if not os.path.exists(filename):
            return filename
        i += 1


def save_answer_to_file(text):
    ensure_answer_dir()
    filename = get_next_answer_filename()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"回答を {filename} に保存しました。")


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ask_chatgpt_with_image(image_path, prompt="この画像の問題に答えてください。"):
    encoded_image = encode_image_to_base64(image_path)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    return response.choices[0].message["content"]


def main():
    print("範囲をドラッグして選択してください...")
    select_area()
    print("選択範囲をキャプチャ中...")
    path = capture_selected_area()

    user_input = input("指示を入力してください（空でEnterするとデフォルト文が使われます）:\n> ")
    default_prompt = "この画像の問題に対して適切に答えてください。"
    prompt = user_input.strip() or default_prompt

    print("ChatGPTに送信中...")
    answer = ask_chatgpt_with_image(path, prompt)
    print("\n ChatGPTの回答:\n")
    print(answer)

    save_answer_to_file(answer)


if __name__ == "__main__":
    main()
