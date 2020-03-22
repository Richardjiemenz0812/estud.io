from flask import *
from flask_redis import FlaskRedis
import random
import os

app = Flask(__name__)
r=FlaskRedis(app)
app.secret_key = "key"

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
    if "user" in session:
        user=session["user"]
        if user != None:
            return redirect("/profile")
    else:
        return render_template("/login.html")


@app.route("/profile")
def profile():
    if "user" in session:
        user=session["user"]
        if user != None:
            name=r.hget(user,"name")
            name=str(name).replace("b'","").replace("'","")
            pwd=r.hget(user,"pwd")
            pwd=str(pwd).replace("b'","").replace("'","")
            pts=r.hget(user,"pts")
            pts=str(pts).replace("b'","").replace("'","")
            rd=r.scan()
            list=str(rd).replace("(0, [b","").replace("])","").replace(", b","").replace("","").replace("(0, [","").split("'")
            print(list)
            pl=""
            list2=""
            for i in list:
                print(i)
                print(r.type(i))
                print("---------------------")
                if i != "":
                    type=r.type(i)
                    type=str(type)
                    if type == "b'list'":
                        print("es una lista!")
                        print("########################################")
                        pl=str(pl) + i + ","
                        print(pl)
                        print("##################################")
                        ub=pl.split(",")
                        print(ub)
                        list2=""
                        for u in ub:
                            if u != "":
                                print(u)
                                ulist=r.lrange(u,3,3)
                                print(ulist)
                                print("-------------------------------")
                                print(user)
                                print("-------------------------------")
                                ulist=str(ulist)
                                print("#"+ulist)
                                ulist=ulist.replace("[b'","").replace("']","")
                                print("="+ulist)
                                if user == ulist:
                                    print("exito!!!!!!!!!!!!!!!!!!!!!!!!")
                                    list2=list2+u+","
                                print(list2)
                                
                        
            y=list2.split(",")
            n=len(y)
            n=n-1           
            return render_template("/profile.html",name=name,pwd=pwd,pts=pts,posts=y,n=n)
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
                        session["user"]= user
                        return redirect("/login")
    return redirect('/login')

@app.route("/test")
def test():
    
    return session["user"]

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
    except:
        pass
    print()
    return render_template('search.html',title=q,post=con,img=img,by=by[1])
    
@app.route('/add')
def add():
    if "user" in session:
        user=session["user"]
        if user != None:
            return render_template("add.html")
    else:
        return render_template('/login.html',msg="before write a post or give feedback you must login")

@app.route('/addf', methods=['POST'])
def addf():
    user=str(session["user"])
    print(user)
    title=request.form.get('title')
    post=request.form.get('post')
    r.lpush(title,user,title,post)
    try:
        fname=str(random.random()) + ".jpg"
        f = request.files['file']
        f.save(os.path.join("static/imgs",fname))
        r.lpush(title,fname)
    except:
        pass
    return redirect('/')

@app.route("/like")
def like():
    if "user" in session:
        user=session['user']
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

@app.route("/chpwd", methods=["POST"])
def chpwd():
    user=session['user']
    pwd=request.form.get("pwd")
    r.hset(user,"pwd",pwd)
    return redirect("/")

@app.route("/sw.js")
def sw():
    return app.send_static_file("/static/js/sw.js")

@app.route("/logout")
def logout():
    user=session['user']
    res=make_response(redirect("/"))
    res.set_cookie("session",user,0)
    return res

@app.route("/user")
def user():
    user=request.args.get("q")
    user="user:"+user
    user_name=str(r.hget(user,"name")).replace("b'","").replace("'","")
    user_pts=str(r.hget(user,"pts")).replace("b'","").replace("'","")
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
                print("########################################")
                pl=str(pl) + i + ","
                print(pl)
                print("##################################")
                ub=pl.split(",")
                print(ub)
                list2=""
                for u in ub:
                    if u != "":
                        print(u)
                        ulist=r.lrange(u,3,3)
                        print(ulist)
                        print("-------------------------------")
                        print(user)
                        print("-------------------------------")
                        ulist=str(ulist)
                        print("#"+ulist)
                        ulist=ulist.replace("[b'","").replace("']","")
                        print("="+ulist)
                        if user == ulist:
                            print("exito!!!!!!!!!!!!!!!!!!!!!!!!")
                            list2=list2+u+","
                        print(list2)
                        
                
    y=list2.split(",")
    n=len(y)
    n=n-1          
    return render_template("/view_profile.html",name=user_name,pts=user_pts,posts=y,n=n)

@app.route("/del_post")
def del_post():
    if "user" in session:
        user=session["user"]
        if user != None:
            name=r.hget(user,"name")
            name=str(name).replace("b'","").replace("'","")
            pwd=r.hget(user,"pwd")
            pwd=str(pwd).replace("b'","").replace("'","")
            pts=r.hget(user,"pts")
            pts=str(pts).replace("b'","").replace("'","")
            rd=r.scan()
            list=str(rd).replace("(0, [b","").replace("])","").replace(", b","").replace("","").replace("(0, [","").split("'")
            print(list)
            pl=""
            list2=""
            ulist=""
            for i in list:
                print(i)
                print(r.type(i))
                print("---------------------")
                if i != "":
                    type=r.type(i)
                    type=str(type)
                    if type == "b'list'":
                        print("es una lista!")
                        print("########################################")
                        pl=str(pl) + i + ","
                        print(pl)
                        print("##################################")
                        ub=pl.split(",")
                        print(ub)
                        list2=""
                        for u in ub:
                            if u != "":
                                print(u)
                                ulist=r.lrange(u,3,3)
                                print(ulist)
                                print("-------------------------------")
                                print(user)
                                print("-------------------------------")
                                ulist=str(ulist)
                                print("#"+ulist)
                                ulist=ulist.replace("[b'","").replace("']","")
                                print("="+ulist)
                                if user == ulist:
                                    print("exito!!!!!!!!!!!!!!!!!!!!!!!!")
                                    list2=list2+u+","
                                print(list2)
                                
                        
            y=list2.split(",")
            n=len(y)
            n=n-1
            user=ulist           
            return render_template("/profile_del.html",name=name,pwd=pwd,pts=pts,posts=y,n=n,user=ulist)
    else:
        return redirect("/login")

@app.route("/del")
def dell():
    if "user" in session:
        user=session["user"]
        q=request.args.get("q")
        u=request.args.get("user")
        if u == user:
            r.delete(q)
            return redirect("/profile")
        else:
            return "este post no es tuyo"
    else:
        return redirect("/login")


app.run(debug=True,host="0.0.0.0")