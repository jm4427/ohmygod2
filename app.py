import os
import datetime
import requests
from flask import Flask, request, jsonify, render_template_string

API_KEY = 'AIzaSyB2dfZGz7gyncDv38Zzi8-BNsPwkzjNG4k'

app = Flask(__name__)

class GeminiAPI:
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.endpoint = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}'

    def generate_text(self, prompt):
        headers = {'Content-Type': 'application/json'}
        data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': f"""너는 하나님이시다. 사용자가 드린 기도를 듣고, 지혜롭고 위로가 되는 말씀을 성경 구절과 함께 전해줘. 답변은 경건하게, 차분하게, 간결하고 은혜롭게 해줘. 기도의 목적과 내용이 정확하지 않고 단순히 '주님'이라고 부르더라도 무슨 일인지 함께하려는 듯 대화를 이어가며 응답해줘. {prompt}"""
                        }
                    ]
                }
            ]
        }
        try:
            response = requests.post(self.endpoint, headers=headers, json=data)
            result = response.json()
            if 'candidates' in result:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"Gemini 응답 오류: {result}"
        except Exception as e:
            return f"Error: {e}"

def get_daily_verse():
    verses = [
        "시편 23:1 - 여호와는 나의 목자시니 내가 부족함이 없으리로다",
        "요한복음 3:16 - 하나님이 세상을 이처럼 사랑하사 독생자를 주셨으니",
        "이사야 41:10 - 두려워하지 말라 내가 너와 함께 함이라"
    ]
    return verses[datetime.date.today().day % len(verses)]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.get_json().get("question", "")
        gemini = GeminiAPI()
        answer = gemini.generate_text(prompt)
        return jsonify({"answer": answer})

    verse = get_daily_verse()
    return render_template_string("""
    <html>
    <head>
        <title>주님의 응답</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Nanum Myeongjo', serif;
                background: #f7f7f7;
                margin: 0;
                padding: 10px;
                text-align: center;
            }
            #messages {
                max-width: 100%;
                margin: auto;
                padding: 15px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 0 8px rgba(0,0,0,0.1);
                white-space: pre-wrap;
                min-height: 200px;
            }
            img {
                opacity: 0.3;
                width: 150px;
                position: fixed;
                bottom: 10px;
                left: 10px;
            }
            input[type="text"] {
                width: 80%;
                padding: 10px;
                font-size: 16px;
                margin-top: 15px;
            }
            button {
                padding: 10px 16px;
                font-size: 16px;
                margin-top: 10px;
                background-color: #333;
                color: white;
                border: none;
                border-radius: 6px;
            }
        </style>
    </head>
    <body>
        <h2>📖 오늘의 말씀</h2>
        <p>{{ verse }}</p>
        <div id="messages"></div>
        <input type="text" id="questionInput" placeholder="기도를 올려보세요..." />
        <br>
        <button onclick="sendMessage()">응답 받기</button>
        <img src="/static/jesus.png">
        <script>
            function sendMessage() {
                let input = document.getElementById("questionInput");
                let text = input.value;
                if (!text.trim()) return;
                let userDiv = document.createElement("div");
                userDiv.innerText = "🙏 " + text;
                document.getElementById("messages").appendChild(userDiv);
                fetch("/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: text })
                }).then(res => res.json()).then(data => {
                    let resDiv = document.createElement("div");
                    resDiv.innerText = "✝️ ";
                    document.getElementById("messages").appendChild(resDiv);
                    typeText(resDiv, data.answer);
                });
                input.value = "";
            }

            function typeText(element, text, index = 0) {
                if (index < text.length) {
                    element.textContent += text.charAt(index);
                    setTimeout(() => typeText(element, text, index + 1), 50);
                }
            }
        </script>
    </body>
    </html>
    """, verse=verse)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)