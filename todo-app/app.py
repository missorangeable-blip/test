from flask import Flask, render_template, request
import json
                                           #requestはフォームに入力されたデータを受け取るための部品
app = Flask(__name__)

try:
    with open("tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

except FileNotFoundError:
    tasks = []

def save_tasks():
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(
            tasks,
            file,
            ensure_ascii=False,
            indent=4
        )

@app.route("/", methods=["GET", "POST"])  #GET..普通にページを開く　POST..フォーム送信
def home():

    if request.method == "POST":  #追加ボタンが押された？

        task = request.form["task"]  #HTMLの name="task" に入っていた文字を取得

        if task:
            tasks.append(task)  #リストの最後に追加
            save_tasks()

    return render_template(
        "index.html",
        tasks=tasks
    )

if __name__ == "__main__":
    app.run(debug=True)