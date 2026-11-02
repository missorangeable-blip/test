from flask import Flask, render_template, request
                                           #requestはフォームに入力されたデータを受け取るための部品
app = Flask(__name__)

tasks = [
    "買い物",
    "レポート提出"
]

@app.route("/", methods=["GET", "POST"])  #GET..普通にページを開く　POST..フォーム送信
def home():

    if request.method == "POST":  #追加ボタンが押された？

        task = request.form["task"]  #HTMLの name="task" に入っていた文字を取得

        if task:
            tasks.append(task)  #リストの最後に追加

    return render_template(
        "index.html",
        tasks=tasks
    )

if __name__ == "__main__":
    app.run(debug=True)