import requests
import os
import json
import random
import google.generativeai as genai
from datetime import datetime, timedelta, timezone

# Function to check if the current time is within a specific time window
def is_time_in_window(target_time_str, window_minutes=30):
    # Define China Standard Time offset
    cst_offset = timezone(timedelta(hours=8))
    # Parse the target time string into a time object
    target_time = datetime.strptime(target_time_str, "%H:%M").time()
    # Get the current time in UTC and convert it to CST
    now = datetime.now(timezone.utc).astimezone(cst_offset).time()

    # Define the start and end of the time window
    window_start = (datetime.combine(datetime.today(), target_time) - timedelta(minutes=window_minutes)).time()
    window_end = (datetime.combine(datetime.today(), target_time) + timedelta(minutes=window_minutes)).time()

    # Check if the current time is within the window
    return window_start <= now <= window_end

def get_generated_message():
    GOOGLE_API_KEY=os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        "convince me to drink water immediately using the following methods:\n"
        "1. Internet slang.\n"
        "2. Gen Z lingo.\n"
        "3. use Ellipsis.\n"
        "4. use Abbreviations and acronyms.\n"
        "5. Don't output quotes, don’t output as list\n"
        "6. Insert emoji\n"
        "7. Quote popular meme lines\n"
        "8. Like you’re tweeting"
    )
    if random.random() > 0.6:
        prompt = (
            "用以下方法说服我立即喝水：\n"
            "- 网络俚语。\n"
            "- Z 世代行话。\n"
            "- 使用缩略语和首字母缩写词。\n"
            "- 不要输出引号，不要以列表形式输出\n"
            "- 插入表情符号\n"
            "- 引用流行语\n"
            "- 像在发微博一样"
        )
    if random.random() > 0.7:
        prompt = (
            "生成一句有趣并且能够引人发笑的话，目的是以一种幽默和轻松的方式鼓励人们多喝水。请在文本中巧妙地融入网络流行语和梗，使内容既现代又引人入胜。"
            "1. 主题要凸出劝人喝水\n"
            "2. 使用网络上流行的比喻或夸张的表达\n"
            "3. 插入一些你自己觉得合适的emoji，并且要放在合适的位置\n"
            "4. 插入一些幽默的夸张比喻\n"
            "5. 创造性地利用流行的网络段子\n"
            "6. 结合一些经典网络迷因\n"
            "7. 不要输出引号\n\n"
            "请注意保持整体文本风趣幽默，同时确保信息传达清晰，鼓励人们多喝水的意图不被幽默元素所掩盖。"
        )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
        return '稍等一下，机器人正在喝水补充能量'

# Function to send a message to a webhook
def send_message_to_webhook(webhook_url, message):
    headers = {'Content-Type': 'application/json'}
    payload = ''
    if isinstance(message, str):
        payload = {
            "msgtype": "text",
            "text": {
                "content": message,
            }
        }
    else:
        payload = message
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        print("Message sent successfully")
    except Exception as e:
        print(f'{type(e).__name__}: {e}')

# Main function
def main():
    beforenoon_webhook_url = os.getenv("BEFORE_WEBHOOK_URL")
    afternoon_webhook_url = os.getenv("AFTERNOON_WEBHOOK_URL")
    print(beforenoon_webhook_url,afternoon_webhook_url,os.getenv("GEMINI_API_KEY"))
    print("script is running!")
    if is_time_in_window("10:45"):
        message = get_generated_message()
        print(message)
        send_message_to_webhook(beforenoon_webhook_url, message)
    else:
        message = get_generated_message()
        print(message)
        send_message_to_webhook(afternoon_webhook_url, message)

if __name__ == "__main__":
    main()
