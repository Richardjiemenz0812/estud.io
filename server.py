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
    pl=""
    for i in list:
        print(i)
        print(r.type(i))
        print("---------------------")
        if i != "":
            type=r.type(i)
            type=str(type)
            if type == "b'list'":
                print("es una lista!")
                pl=str(pl) + i + ","
    print(pl)
    pl=pl.split(",")
    return render_template("index.html",list=pl)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def loginp():
    user=request.form.get('user')
    pwd=request.form.get('pwd')
    print("--------------------------------")
    print(user)
    print(pwd)
    print("--------------------------------")
    rd=r.scan()
    list=str(rd).replace("(0, [b","").replace("])","").replace(", b","").replace("","").replace("(0, [","").split("'")
    print(list)
    pl=""
    for i in list:
        print(i)
        print(r.type(i))
        print("---------------------")
        if i != "":
            type=r.type(i)
            type=str(type)
            if type == "b'hash'":
                print("es un hash!")
                user="user:"+user
                if user in list:
                    print("yessssssssssssssssssss")
                    print(user)
                    print(r.hget(user,"pwd"))
                    p=str(r.hget(user,"pwd")).replace("b'","").replace("'","")
                    if p == pwd:
                        print("access")
                        res=make_response(redirect("/"))
                        res.set_cookie("user",user)
                        return res
    return redirect('/login')

@app.route("/test")
def test():
    p=request.cookies.get("user")
    return p

@app.route('/search')
def search():
    q=request.args.get('q')
    con=r.lrange(q,1,1)
    con=str(con).replace("[b'","").replace("']","").replace("\\r\\n","<br>").replace('[b"',"").replace('"]',"")
    try:
        img = r.lrange(q,0,0)
        img=str(img).replace("[b'","").replace("']","")
    except expression as identifier:
        pass
    print()
    return render_template('search.html',title=q,post=con,img=img)
    
@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/addf', methods=['POST'])
def addf():
    user=request.cookies.get("user")
    print(user)
    if user != None:
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
    return redirect('/login')


app.run(debug=True,host="0.0.0.0")