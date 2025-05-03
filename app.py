import os
import datetime
import requests
from flask import Flask, request, jsonify, render_template_string

API_KEY = 'YOUR_GEMINI_API_KEY'
app = Flask(__name__)

# Gemini 호출 클래스
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
                            'text': f"""너는 하나님이시다. 사용자가 드린 고민을 듣고, 지혜롭고 위로가 되는 말씀을 성경 구절과 함께 전해줘. 답변은 경건하게, 차분하게, 은혜롭게 해줘. 상황 설명이 부족해도 마음의 안정을 줄 수 있도록 따뜻하게 응답해줘. {prompt}"""
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
                return "응답을 받을 수 없습니다. 다시 시도해주세요."
        except Exception as e:
            return f"에러 발생: {e}"

# 날짜별 QT
qt_daily_map = {
    1: "🕊 주님의 사랑 안에서 새롭게 시작하는 하루입니다.",
    2: "📖 주는 나의 반석이시오 나의 요새시라. (시 18:2)",
    3: "🙏 주님, 오늘도 주의 뜻을 따르게 하소서.",
    4: "🌿 주의 은혜가 오늘도 나를 덮습니다.",
    5: "✝️ 그리스도 안에서 우리는 새로운 피조물입니다.",
    6: "🕊 순종은 믿음의 열매입니다. 주님을 믿고 맡기세요.",
    7: "📖 주의 말씀은 능력입니다. 묵상하며 하루를 여세요.",
    8: "🙏 주님과 동행하는 삶, 그것이 최고의 축복입니다.",
    9: "🌿 세상 끝날까지 함께하시는 하나님을 신뢰하세요.",
    10: "✝️ 너희는 먼저 그의 나라와 의를 구하라. (마 6:33)",
    11: "🕊 하나님의 시간은 완벽합니다. 기다림도 은혜입니다.",
    12: "📖 내 영혼아 잠잠히 하나님만 바라라. (시 62:5)",
    13: "🙏 주님 앞에 정직하게 나아가는 하루 되게 하소서.",
    14: "🌿 주님의 임재가 오늘도 우리와 함께합니다.",
    15: "✝️ 모든 것을 합력하여 선을 이루시는 하나님을 믿습니다.",
    16: "🕊 너희 염려를 다 주께 맡기라. (벧전 5:7)",
    17: "📖 주의 인자하심은 아침마다 새롭습니다. (애 3:23)",
    18: "🙏 오늘도 주님과 동행하는 삶을 소망합니다.",
    19: "🌿 주의 음성에 귀 기울이며 하루를 시작하세요.",
    20: "✝️ 주께서 인도하시는 길은 가장 선한 길입니다.",
    21: "🕊 주님은 피난처이시며 힘이 되십니다. (시 46:1)",
    22: "📖 주의 말씀은 영원하며 변하지 않습니다. (사 40:8)",
    23: "🙏 항상 기뻐하라, 쉬지 말고 기도하라. (살전 5:16-17)",
    24: "🌿 오늘도 주 안에서 기쁨이 넘치게 하소서.",
    25: "✝️ 십자가의 능력으로 살아가는 자가 되게 하소서.",
    26: "🕊 나의 평안은 세상이 줄 수 없는 것이라. (요 14:27)",
    27: "📖 말씀을 가까이하는 자가 복이 있습니다.",
    28: "🙏 매 순간 주를 의지하며 걷게 하소서.",
    29: "🌿 주님의 손이 항상 나를 붙드십니다.",
    30: "✝️ 오늘도 십자가 앞에서 나를 비워냅니다.",
    31: "🕊 하루의 시작과 끝에 주님이 계십니다. 아멘."
}

@app.route("/qt")
def qt_page():
    day = datetime.date.today().day
    qt = qt_daily_map.get(day, "💡 오늘도 말씀과 함께 은혜로운 하루 보내세요.")
    return render_template_string("""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>오늘의 QT</title>
        <style>
            body { font-family: 'Nanum Myeongjo', serif; background: #f9f9f9; padding: 20px; text-align: center; }
            .qt-box {
                padding: 20px;
                border: 2px dashed #888;
                background: #fff;
                margin-top: 40px;
                border-radius: 10px;
                font-size: 18px;
                max-width: 500px;
                margin-left: auto;
                margin-right: auto;
            }
            a { text-decoration: none; margin: 20px; color: #333; }
        </style>
    </head>
    <body>
        <h2>📘 오늘의 QT 말씀</h2>
        <div class="qt-box">{{ qt }}</div>
        <br><br>
        <a href="/">← 주님의 응답으로 돌아가기</a>
    </body>
    </html>
    """, qt=qt)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.get_json().get("question", "")
        gemini = GeminiAPI()
        answer = gemini.generate_text(prompt)
        return jsonify({"answer": answer})

    return render_template_string("""
    <html>
    <head>
        <title>주님의 응답</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Nanum Myeongjo', serif;
                background: #f1f1f1;
                padding: 20px;
                text-align: center;
            }
            #messages {
                max-width: 700px;
                margin: 20px auto;
                padding: 20px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 0 8px rgba(0,0,0,0.1);
                white-space: pre-wrap;
                min-height: 200px;
                overflow-y: auto;
                position: relative;
            }
            .message {
                text-align: left;
                margin: 8px 0;
                padding: 10px;
                border-radius: 6px;
            }
            .user {
                background-color: #e0f7fa;
                color: #006064;
            }
            .lord {
                background-color: #fce4ec;
                color: #880e4f;
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
            a {
                display: inline-block;
                margin: 10px;
                font-size: 14px;
                text-decoration: none;
                color: #006064;
            }
        </style>
    </head>
    <body>
        <h2>✝️ 주님의 응답</h2>
        <a href="/qt">📘 오늘의 QT</a>
        <div id="messages"></div>
        <input type="text" id="questionInput" placeholder="고민이나 기도를 입력해보세요..." />
        <br>
        <button onclick="sendMessage()">응답 받기</button>
        <audio autoplay loop>
            <source src="/static/background.mp3" type="audio/mpeg">
        </audio>
        <script>
            function scrollToBottom() {
                const msgDiv = document.getElementById("messages");
                msgDiv.scrollTop = msgDiv.scrollHeight;
            }

            function sendMessage() {
                const input = document.getElementById("questionInput");
                const text = input.value;
                if (!text.trim()) return;

                const userDiv = document.createElement("div");
                userDiv.className = "message user";
                userDiv.innerText = "🙏 " + text;
                document.getElementById("messages").appendChild(userDiv);
                scrollToBottom();

                fetch("/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: text })
                }).then(res => res.json()).then(data => {
                    const resDiv = document.createElement("div");
                    resDiv.className = "message lord";
                    resDiv.innerText = "✝️ ";
                    document.getElementById("messages").appendChild(resDiv);
                    typeText(resDiv, data.answer);
                });

                input.value = "";
            }

            function typeText(element, text, index = 0) {
                if (index < text.length) {
                    element.textContent += text.charAt(index);
                    scrollToBottom();
                    setTimeout(() => typeText(element, text, index + 1), 50);
                }
            }
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)