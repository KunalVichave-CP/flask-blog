from flask import Flask, render_template, request, Response
from werkzeug.utils import secure_filename
import sqlite3

# from flask_mail import Mail
app = Flask(__name__)


# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='465',
#     MAIL_USE_SSL='True',
#     MAIL_USER='kunalvichavealt@gmail.com',
#     MAIL_PASSWORD='lanukvichave'
# )
# mail = Mail(app);
@app.route("/dash", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        subh = request.form['subhead']
        content = request.form['content']

        destination_path = ""
        fileobj = request.files['pic']
        mimetype=fileobj.mimetype
        file_extensions = ["JPG", "JPEG", "PNG", "GIF"]
        uploaded_file_extension = fileobj.filename.split(".")[1]
        # validating file extension
        if (uploaded_file_extension.upper() in file_extensions):
            destination_path = f"static/uploads/{fileobj.filename}"
            fileobj.save(destination_path)

            connection = sqlite3.connect("indimonk.db")
            cursor = connection.cursor()
            query1 = "INSERT INTO posts(title,content,subh,pic,mimetype) VALUES('{title}','{content}','{subh}','{pic}'," \
                     "'{mimetype}')".format(title=title, content=content, subh=subh, pic=destination_path,mimetype=mimetype)
            cursor.execute(query1)
            connection.commit()
            # mail.send_message('New msg from ',
            #                   sender=email,
            #                   recipients=['kunalvichavealt@gmail.com'],
            #                   body=message + "\n" + phone)
            cursor.close()
    return render_template('dashboard.html', title="Dashboard")


# @app.route("/<int:id>")



def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


@app.route("/")
def home():
    name = "kunal"
    return render_template('index.html', title="Home")


@app.route("/post/<string:sr>", methods=['GET'])
def post(sr):
    # p_slug=request.args.get("post")
    conn = sqlite3.connect('indimonk.db')
    cursor = conn.cursor()
    query2 = "SELECT * FROM posts WHERE id={sr}".format(sr=sr)
    cursor.execute(query2)
    result = cursor.fetchone()

    # title = result[0]

    # print(res)

    conn.commit()
    conn.close()
    content = '' + result[2]
    print(content)

    return render_template('posts.html', content=content, title=result[1])


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        connection = sqlite3.connect("indimonk.db")
        cursor = connection.cursor()
        query1 = "INSERT INTO contact(name,email,phone,message) VALUES('{name}','{email}','{phone}','{message}')".format(
            name=name, phone=phone,
            email=email,
            message=message)
        cursor.execute(query1)
        connection.commit()
        # mail.send_message('New msg from ',
        #                   sender=email,
        #                   recipients=['kunalvichavealt@gmail.com'],
        #                   body=message + "\n" + phone)
        cursor.close()

    return render_template('contact.html', title="Contact")


@app.route('/facts/')
def fact():
    conn = sqlite3.connect('indimonk.db')
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('facts.html', posts=posts, title="Facts")


app.run(debug=True)
