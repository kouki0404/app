import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# =====================
# ゲーム設定
# =====================
NUM_COUNT = 5
TIME_LIMIT = 30  # 秒

# =====================
# HTML テンプレート
# =====================
def generate_html(numbers, rule_description, selected, score, remaining_time, cleared):
    buttons_html = ""
    for i, num in enumerate(numbers):
        if num not in selected:
            x = random.randint(10, 80)
            y = random.randint(10, 80)
            buttons_html += f"<button class='moving-button' onclick=\"window.location='/?btn={num}'\" style='left:{x}%; top:{y}%;'>{num}</button>"

    if remaining_time <= 0 and not cleared:
        result = "<h2 style='color:red'>🕒 タイムオーバー！ゲームオーバー</h2><a href='/'>もう一度遊ぶ</a>"
    elif cleared:
        result = f"<h2 style='color:green'>🎉 クリア！</h2><p>✅ あなたのスコア: <strong>{score}点</strong></p><a href='/'>もう一度遊ぶ</a>"
    else:
        result = f"<p>⏱ 残り時間: {remaining_time}秒</p><p>🎯 スコア: {score}点</p>"

    return f"""
    <html>
    <head>
        <title>数字ハンター</title>
        <style>
            body {{ font-family: sans-serif; text-align: center; }}
            .container {{ position: relative; width: 100%; height: 300px; background: #f0f0f0; overflow: hidden; }}
            .moving-button {{ position: absolute; animation: float 3s ease-in-out infinite; padding: 10px 20px; font-size: 18px; }}
            @keyframes float {{ 0% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} 100% {{ transform: translateY(0); }} }}
        </style>
    </head>
    <body>
        <h1>🎯 数字ハンター</h1>
        <h3>{rule_description}</h3>
        {result}
        <div class='container'>
            {buttons_html}
        </div>
    </body>
    </html>
    """

# =====================
# ゲームルール生成
# =====================
def generate_rule():
    rule_type = random.choice(["random", "ordered"])

    if rule_type == "random":
        numbers = random.sample(range(1, 20), NUM_COUNT)
        description = "好きな順に全ての数字をタップせよ"
        sequence = numbers
    else:
        start = random.randint(1, 10)
        ordered = [start + i for i in range(NUM_COUNT)]
        if random.choice([True, False]):
            ordered.reverse()
            description = "数字を大きい順にタップせよ"
        else:
            description = "数字を小さい順にタップせよ"
        numbers = ordered.copy()
        random.shuffle(numbers)
        sequence = ordered

    return rule_type, numbers, description, sequence

# =====================
# グローバルゲーム状態
# =====================
rule_type, numbers, description, sequence = generate_rule()
selected = []
tap_index = 0
start_time = time.time()
score = 0
cleared = False

# =====================
# サーバーハンドラ
# =====================
class GameHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global selected, tap_index, cleared, score
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        current_time = time.time()
        remaining_time = int(TIME_LIMIT - (current_time - start_time))

        if "btn" in params and not cleared and remaining_time > 0:
            try:
                btn = int(params["btn"][0])
                if rule_type == "random" and btn not in selected:
                    selected.append(btn)
                    score += 10
                elif rule_type == "ordered" and btn == sequence[tap_index]:
                    selected.append(btn)
                    score += 10
                    tap_index += 1
                else:
                    score -= 5
            except:
                pass

        if len(selected) == NUM_COUNT and not cleared:
            cleared = True
            time_taken = int(current_time - start_time)
            score += max(TIME_LIMIT - time_taken, 0)

        html = generate_html(numbers, description, selected, score, remaining_time, cleared)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

# =====================
# サーバー起動
# =====================
PORT = 8000
with HTTPServer(("", PORT), GameHandler) as server:
    print(f"サーバーを起動しました: http://localhost:{PORT}")
    server.serve_forever()
