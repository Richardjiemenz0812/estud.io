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
    user=request.cookies.get("user")
    if user != None:
        return redirect("/profile")
    else:
        return render_template("/login.html")

@app.route("/profile")
def profile():
    user=request.cookies.get("user")
    if user != None:
        name=r.hget(user,"name")
        name=str(name).replace("b'","").replace("'","")
        pwd=r.hget(user,"pwd")
        pwd=str(pwd).replace("b'","").replace("'","")
        pts=r.hget(user,"pts")
        pts=str(pts).replace("b'","").replace("'","")
        return render_template("/profile.html",name=name,pwd=pwd,pts=pts)
    else:
        return redirect("/login")

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
    by=r.lrange(q,3,3)
    by=str(by).replace("[b'","").replace("']","").split(":")
    print(by)
    try:
        img = r.lrange(q,0,0)
        img=str(img).replace("[b'","").replace("']","")
    except expression as identifier:
        pass
    print()
    return render_template('search.html',title=q,post=con,img=img,by=by[1])
    
@app.route('/add')
def add():
    user=request.cookies.get("user")
    if user != None:
        return render_template("add.html")
    else:
        return render_template('/login.html',msg="before write a post you must login")

@app.route('/addf', methods=['POST'])
def addf():
    user=str(request.cookies.get("user"))
    print(user)
    title=request.form.get('title')
    post=request.form.get('post')
    r.lpush(title,user,title,post)
    try:
        fname=str(random.random()) + ".jpg"
        f = request.files['file']
        f.save(os.path.join("static/imgs",fname))
        r.lpush(title,fname)
    except expression as identifier:
        pass
    return redirect('/')

@app.route("/like")
def like():
    user=request.cookies.get("user")
    q=request.args.get("q")
    p=request.args.get("by")
    userp="user:"+ p
    print(userp)
    pts=0
    if user != None:
        if q == "1":
            pts=r.hget(userp,"pts")
            print(pts)
            pts=int(pts)+1
            print(int(pts))
            r.hset(userp,"pts",pts)
            return redirect('/')
    else:
        return redirect("/add")

app.run(debug=True,host="0.0.0.0")