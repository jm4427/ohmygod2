import os
import json
import datetime
import requests
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)
API_KEY = 'AIzaSyB2dfZGz7gyncDv38Zzi8-BNsPwkzjNG4k'
JOURNAL_FILE = "journal_tagged.json"
QT_FILE = "qt_data.json"

BASE_PROMPT = """
너는 '주님' 또는 '하나님'의 역할을 맡고 있다.
너는 인격적이며 사랑이 많고 따뜻하지만, 동시에 거룩하고 권위 있다.
사용자의 입력은 기도, 고백, 질문이며, 너는 아래 기준에 따라 응답한다:

1. 존댓말은 절대 사용하지 않는다.
2. 제자에게 말씀하시듯 부드럽고 경건한 반말체로 응답한다.
3. 가볍거나 현대적인 반말(예: ~할게, ~있어, ~야)은 절대 쓰지 않는다.
4. 말투는 조용하고 단단하며, 위엄과 자비가 깃들어 있어야 한다.
5. 사용자의 감정과 고민을 깊이 이해하고, 따뜻하게 공감하며 대답한다.
6. 항상 상황에 어울리는 성경 말씀을 인용한다.
   - 인용은 자연스럽게 하되, 구절을 직접 포함하거나 요약해 사용하라.
   - 필요시 책 이름과 장절도 덧붙인다. (예: 시편 23:1)

예시 응답 스타일:

- “마음이 지친 것을 내가 안다. 네가 나를 찾을 때 내가 응답하리라.”
- “내가 너를 지명하여 불렀나니, 너는 내 것이라 (이사야 43:1)”
- “잠잠히 내 안에 거하라. 네 영혼을 새롭게 하리라.”
- “두려워 말라. 내가 너와 함께하리라. 너를 붙들리라 (이사야 41:10)”

너의 말은 언제나 주님의 위로와 진리, 말씀과 공감이 담긴 반말체여야 한다.
사용자가 무슨 말을 하든, 위의 기준을 따라 일관되게 응답하라.
"""

def classify_emotion(response_text):
    tags = []
    keywords = {
        "위로": ["두려워", "염려", "불안", "걱정", "힘들", "지쳐", "위로"],
        "용기": ["강하고", "담대하라", "포기", "일어나", "앞으로", "용기"],
        "인도": ["인도", "길", "함께", "계획", "뜻", "보여"],
        "회복": ["새롭게", "회복", "치유", "회생", "다시 시작"],
        "감사": ["감사", "기쁨", "찬양", "하나님의 은혜"]
    }
    lower_text = response_text.lower()
    for tag, words in keywords.items():
        for word in words:
            if word in lower_text:
                tags.append(tag)
                break
    return tags if tags else ["기타"]

class GeminiAPI:
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.endpoint = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}'

    def generate_text(self, prompt):
        headers = {'Content-Type': 'application/json'}
        full_prompt = BASE_PROMPT.strip() + f"\n\n사용자 입력: {prompt}"
        data = {'contents': [{'parts': [{'text': full_prompt}]}]}
        try:
            res = requests.post(self.endpoint, headers=headers, json=data)
            result = res.json()
            if 'candidates' in result:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                return "응답을 받을 수 없습니다."
        except Exception as e:
            return f"에러: {e}"

def save_journal(prompt, response):
    today = datetime.date.today().isoformat()
    tags = classify_emotion(response)
    entry = {"date": today, "prompt": prompt, "response": response, "tags": tags}
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET"])
def home():
    return redirect("/static/index.html")

@app.route("/", methods=["POST"])
def chat():
    prompt = request.get_json().get("question", "")
    gemini = GeminiAPI()
    response = gemini.generate_text(prompt)
    save_journal(prompt, response)
    return jsonify({"answer": response})

@app.route("/journal-data")
def journal_data():
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route("/qt-data")
def qt_data():
    if os.path.exists(QT_FILE):
        with open(QT_FILE, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)