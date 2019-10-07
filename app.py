import datetime, re, os, random, json, urllib.parse, urllib.request
from flask import Flask, render_template, request, jsonify, session, abort, redirect, url_for, Response
import pymysql

app = Flask(__name__)
db = pymysql.connect(host="47.102.223.204", user="wml", password="123456", database="easy_watch", charset="utf8")
app.secret_key = b'\xa3P\x05\x1a\xf8\xc6\xff\xa4!\xd2\xb5\n\x96\x05\xed\xc3\xc90=\x07\x8d>\x8e\xeb'


@app.route("/")
def home():
    return("登录试试看！")
@app.route("/reg", methods=["GET", "POST"])
def reg_handle():
    if request.method == "GET":
        return render_template("reg.html")
    elif request.method == "POST":
        
        uname = request.form.get("uname")
        upass = request.form.get("upass")
        upass2 = request.form.get("upass2")
        phone = request.form.get("phone")
        verify_code = request.form.get("verify_code")
        email = request.form.get("email")

        if not (uname and uname.strip() and upass and upass2 and phone and verify_code and email):
            return render_template("404.html")

        # if re.search(r"[\u4E00-\u9FFF]", uname):
        #     abort(Response("用户名含有中文汉字！"))

        if not re.fullmatch("[a-zA-Z0-9_]{4,20}", uname):
            abort(Response("用户名不合法！"))
        
        cur = db.cursor()
        cur.execute("SELECT uid FROM ez_user WHERE uname=%s", (uname))
        res = cur.rowcount
        cur.close()      
        if res != 0:
            abort(Response("用户名已被注册！"))

        # 密码长度介于6-15
        if not (len(upass) >= 6 and len(upass) <= 15 and upass == upass2):
            abort(Response("密码错误！再试一次吧！"))

        if not re.fullmatch(r"[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+", email):
            abort(Response("邮箱格式错误！"))

        try:
            cur = db.cursor()
            cur.execute("INSERT INTO ez_user VALUES (default, %s, md5(%s), %s, %s, sysdate(), sysdate(), '1', '1')", (uname, uname + upass, phone, email))
            cur.close()
            db.commit()
        except:
            abort(Response("用户注册失败！"))

        # 注册成功就跳转到登录页面
        return "注册成功啦"

@app.route("/login", methods=["GET", "POST"])
def login_handle():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        uname = request.form.get("uname")
        upass = request.form.get("upass")
        print(uname, upass)

        if not (uname and uname.strip() and upass and upass.strip()):
            abort(Response("登录失败！"))

        if not re.fullmatch("[a-zA-Z0-9_]{4,20}", uname):
            abort(Response("用户名不合法！"))

        # 密码长度介于6-15
        if not (len(upass) >= 6 and len(upass) <= 15):
            abort(Response("密码不合法！"))    
        
        cur = db.cursor()
        cur.execute("SELECT * FROM ez_user WHERE uname=%s AND upass=MD5(%s)", (uname, uname + upass))
        res = cur.fetchone()
        cur.close()
              
        if res:
            # 登录成功就跳转到用户个人中心
            cur_login_time = datetime.datetime.now()

            session["user_info"] = {
                "uid": res[0],
                "uname": res[1],
                "upass": res[2],
                "phone": res[3],
                "email": res[4],
                "reg_time": res[5],
                "last_login_time": res[6],
                "priv": res[7],
                "state": res[8],
                "cur_login_time": cur_login_time
            }

            try:
                cur = db.cursor()
                cur.execute("UPDATE ez_user SET last_login_time=%s WHERE uid=%s", (cur_login_time, res[0]))
                cur.close()
                db.commit()
            except Exception as e:
                print(e)
            
            print("登录成功！", session)
            return redirect(url_for("user_center"))
        else:
            # 登录失败
            print("登录失败！")
            return render_template("login.html", login_fail=1)

@app.route("/user_center")
def user_center():
    if session:
        print(session)
        return render_template("user_center.html")
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(port=80, debug=True)