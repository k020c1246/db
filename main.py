#from flask import Flask, render_template # これだけだったけど
from flask import Flask, render_template, request, redirect # 追加で2つimportする
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

#DBのテーブルの設定をする。
#Postはテーブル名。
class Post(db.Model):
    # IDは整数。主キー。
    id = db.Column(db.Integer, primary_key=True)
    # titleはToDoListの内容。文字列。空っぽは禁止。
    title = db.Column(db.String(50), nullable=False)

#DBのテーブルを作る。
#db.create_all()

#Topページ
#@app.route('/') # 元々はこれだったけど
@app.route('/', methods=['GET', 'POST']) # こちらに変更
def index():
    #GETメソッドで受け取れば（POSTメソッドではないとき）
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)
    #POSTメソッドで受け取れば（ToDoリストの項目を追加するとき）
    else:
        #POSTメソッドのtitle、idの値を取得する。
        title = request.form.get('title')
        
        #Postテーブルの項目titleに変数titleの行を作成する
        new_post = Post(title=title)
        
        #SQLのCREATE文にあたるもの。行の追加。
        db.session.add(new_post)
        
        #SQLのCOMMIT文（上書き）にあたるもの
        db.session.commit()

        #トップページに飛ぶ
        return redirect('/')

#項目の追加ページ
@app.route('/create')
def create():
    return render_template('create.html')

#項目の削除
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    
    #SQLのDELETE文にあたるもの。行の削除。
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

app.run(host='0.0.0.0')