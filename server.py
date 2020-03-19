from flask import *
from flask_redis import FlaskRedis
import random
import os

app = Flask(__name__)
r=FlaskRedis(app)

path_folder='static/imgs'

@app.route('/')
def index():
    rd=r.scan()
    list=str(rd).replace("(0, [b","").replace("])","").replace(", b","").replace("","").replace("(0, [","").split("'")
    print(list)
    return render_template("index.html",list=list)

@app.route('/search')
def search():
    req=request.args.get('q')
    pos=r.lrange(req,0,-1)
    list=str(pos).replace("(0, [b","").replace("])","").replace(", b",""
    ).replace("","").replace("(0, [","").replace("[b","").replace("]","").split("'")
    print(list)
    title=list[5]
    post=list[3]
    img=list[1]
    post=str(post).replace("[b'","").replace("']","").replace("\\r\\n","<br>")
    print(title)
    return render_template("/search.html",title=title,post=post,img=img)

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/addf', methods=['POST'])
def addf():
    title=request.form.get('title')
    post=request.form.get('post')
    r.lpush(title,title,post)
    try:
        fname=str(random.random()) + ".jpg"
        f = request.files['file']
        f.save(os.path.join("static/imgs",fname))
        r.lpush(title,fname)
    except expression as identifier:
        pass
    return redirect('/')


app.run(debug=True,host="0.0.0.0")