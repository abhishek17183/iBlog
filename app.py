from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import math
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME ='abhishekbiranje1718@gmail.com',
    MAIL_PASSWORD = 'abhishekbiranje1718@abhiismyprod@'

)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/iblog'
db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50),nullable=False)
    phone_no = db.Column(db.String(15),nullable=False)
    date = db.Column(db.String(12), nullable=True)
    msg = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.name

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(30),nullable=True)
    content = db.Column(db.String(100),nullable=False)
    date = db.Column(db.String(12), nullable=True)

    def __repr__(self):
        return self.title

@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    llast = math.cei(len(posts)/3)
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*3:(page-1) * 3 + 3]
    if page==1:
        prev = "#"
        next = "/?page="+ str(page+1)
    elif page==last:
        prev = "/?page="+ str(page-1)
        next = "#"
    else:
        prev = "/?page="+ str(page-1)
        next = "/?page="+ str(page+1)
    print(f"Page Is {page}")
    return render_template('index.html',posts=posts, prev=prev, next=next)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/post/<string:post_slug>")
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',post=post)

@app.route("/contact",methods =['GET','POST'])
def contact():
    if(request.method == 'POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        msg=request.form.get('msg')

        entry= Contact(name=name,email=email,phone_no=phone,date=datetime.now(),msg=msg)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name,sender=email,recipients = ['abhishekbiranje1718@gmail.com'],body = 'From ' + email  + "\n" + "Phone No." + phone + "\n" + "Message: " + msg )
        return render_template('contact.html',success=True)

    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)