from flask import Flask, render_template, request, redirect
from datetime import date
import json
                                           #requestはフォームに入力されたデータを受け取るための部品
app = Flask(__name__)

# 起動時にJSONを読み込む
try:
    with open("tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file) # JSONからPythonへ

except FileNotFoundError:
    tasks = []

# タスク保存関数
def save_tasks():
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(
            tasks,
            file,
            ensure_ascii=False,     # PythonからJSONへ
            indent=4
        )

# トップページ
@app.route("/", methods=["GET", "POST"])  #GET..普通にページを開く　POST..フォーム送信
def home():

    if request.method == "POST":  #追加ボタンが押された？

        task = request.form["task"]  #HTMLの name="task" に入っていた文字を取得

        deadline = request.form["deadline"]  #HTMLの name="deadline" に入っていた文字を取得

        priority = request.form["priority"]  #HTMLの name="priority" に入っていた文字を取得

        if task:              # 実際にJSONファイルに記録される際の書き方の指定
            tasks.append(
                {
                    "id": len(tasks) + 1,
                    "task": task,
                    "done": False,
                    "deadline": deadline,
                    "priority": priority
                }
            )  #リストの最後に追加
            save_tasks()

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }
        
    sorted_tasks = sorted(
        tasks,
        key=lambda task: (
           task["done"],
            priority_order[task["priority"]]
        )
    )
        
    return render_template(
        "index.html",
        tasks=sorted_tasks,
        today=str(date.today()) # 今日の日付
    )

# タスク削除
@app.route("/delete/<int:task_id>")
def delete(task_id):

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)

            break

    save_tasks()

    return redirect("/")

# タスク完了切り替え
@app.route("/toggle/<int:task_id>")
def toggle(task_id):

    for task in tasks:

        if task["id"] == task_id:

            task["done"] = not task["done"]

            break

    save_tasks()

    return redirect("/")

# Flask起動
if __name__ == "__main__":
    app.run(debug=True)