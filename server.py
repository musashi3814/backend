from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


# Flaskの設定
# app = Flask(__name__, static_folder="../frontend/build/static", template_folder="../frontend/build")
app = Flask(__name__)
CORS(app)  # buildの場合不要

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'  # SQLiteを使用しますが、他のデータベースも選択可能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  
db = SQLAlchemy(app)

# Todoモデルの定義
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)


# アプリケーションコンテキストを手動で設定
app.app_context().push()

# データベースの初期化
db.drop_all()
db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_todo', methods=['GET'])
def api0():
    todos = Todo.query.all()
    todo_list = [{"id": todo.id, "title": todo.title, "done": todo.done} for todo in todos]
    return jsonify(todo_list) 

@app.route('/api/add_todo', methods=['GET','POST'])
def api1():
    data = request.get_json()
    new_todo = Todo(id=data["id"], title=data["title"], done=data["done"])
    db.session.add(new_todo)
    db.session.commit()
    return f"get {new_todo}!"

@app.route('/api/delete_todo/<int:id>', methods=['DELETE'])
def api2(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return f"delete id: {id}!"

@app.route('/api/update_done/<int:id>', methods=['PUT'])
def api3(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return f"update done: {todo.done}!"

@app.route('/api/update_title/<int:id>', methods=['PUT'])
def api4(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    todo.title = data["title"]
    db.session.commit()
    return f"update title: {todo.title}!"

if __name__ == '__main__':
    app.debug = True
    app.run("127.0.0.1",port=8000)

