from flask import Flask,render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import base64
import psycopg2
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = '12345678'

db_params = {
    'dbname' : 'palm_data',
    'user' : 'wongsatorn',
    'password' : '12345678',
    'host' : 'localhost',
    'port' : '5432'
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods= ['GET','POST'])
def register():
    if request.method == 'POST':
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        fName = request.form['firstname']
        lName = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hash_pass = bcrypt.generate_password_hash(password)
        conPassword = request.form['conPassword']
        hash_conPass = bcrypt.generate_password_hash(conPassword)
        print(fName,lName,username,email,password,conPassword)
        print(hash_pass)
        print(hash_conPass)

        checkExistedPrompt = """
            SELECT * FROM users WHERE username = %s
        """
        cursor.execute(checkExistedPrompt, (username, ))
        account = cursor.fetchone()
        print(account)

        if account:
            print("already existed!")
            flash('Account already existed!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            print("Username must char num")
            flash('Username must contain only characters and nunmbers')
        elif password != conPassword:
            print("Password don't match")
            flash("Password doesn't match")
        else:
            user_data = (username, email, hash_pass, fName, lName)
            registerPrompt = """
                INSERT INTO users (username, email, user_password, firstname, lastname, date_created, last_login)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """
            cursor.execute(registerPrompt, user_data)
            conn.commit()
            flash('You have successfully registered!')

    return render_template('register.html')

@app.route('/collect')
def collect():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    query = """
        SELECT 
            p.id,
            p.img,
            p.img_Name,
            r.ripeness_level,
            p.oil_content,
            p.time_captured,
            p.last_edit
        FROM
            palm p
        JOIN
            ripeness r ON p.ripeness_id = r.id
    """
    ripenessLevelQuery = """
        SELECT * FROM ripeness;
    """
    count = """
        SELECT COUNT(*) FROM palm;
    """
    cursor.execute(query)
    data0 = cursor.fetchall()
    data1 = [
        {
            'id' : data[0],
            'img' : base64.b64encode(data[1]).decode('utf-8'),
            'img_name' : data[2],
            'ripeness_level' : data[3],
            'oil_content' : data[4],
            'time_captured' : data[5],
            'last_edit' : data[6]
        }
        for data in data0
    ]
    cursor.execute(ripenessLevelQuery)
    data2 = cursor.fetchall()
    cursor.execute(count)
    data3 = cursor.fetchall()

    
    
    context = [data1, data2]
    cursor.close()
    conn.close()
    return render_template('collect.html', data = context)

@app.route("/edit/<int:palm_id>", methods = ["GET","POST"])
def edit(palm_id):
    whatEdit = palm_id
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    query = """
        SELECT * FROM palm WHERE id = %s;
    """

    ripenessLevelQuery = """
        SELECT * FROM ripeness;
    """
    cursor.execute(query,(whatEdit,))
    data1 = cursor.fetchone()
    cursor.execute(ripenessLevelQuery)
    ripeness = cursor.fetchall()
    context = [data1, ripeness]

    if request.method == "POST":
        new_name = request.form.get("name")    
        new_ripeness = request.form.get("ripeness")
        new_oilContent = request.form.get("oilContent")
        print(new_name,new_ripeness,new_oilContent)
        whatUpdate = (new_name, new_ripeness, new_oilContent, whatEdit)
        updatePrompt = """
            UPDATE palm SET
                img_name = %s,
                ripeness_id = %s,
                oil_content = %s,
                last_edit = CURRENT_TIMESTAMP
            WHERE
                id = %s
        """
        cursor.execute(updatePrompt, whatUpdate)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("collect"))
    else:
        return render_template("edit.html", data = context)
    
@app.route("/delete/<int:palm_id>")
def delete(palm_id):
    whatDel = palm_id
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    delPrompt = """
        DELETE FROM palm WHERE id = %s
    """
    cursor.execute(delPrompt, (whatDel,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('collect'))


@app.route("/add", methods = ["POST"])
def add():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    image = request.files['image']
    image_data = image.read()

    name = request.form.get("name")
    ripeness = request.form.get("ripeness")
    oilContent = request.form.get("oilContent")
    newPalm = (name, ripeness, oilContent, image_data)
    addPrompt = """
        INSERT INTO palm (img_name,ripeness_id,oil_content, time_captured, last_edit, img)
        VALUES (%s,%s,%s, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,%s);
    """

    addPrompt2 = """
        INSERT INTO palm(img_name, ripeness_id, oil_content, img, time_captured, last_edit, captured_by, edited_by)
        VALUES ('palm_001',2,40.5,'',current_timestamp, current_timestamp, 1,1);
    """

    cur.execute(addPrompt, newPalm)

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("collect"))

@app.route('/report' , methods = ['GET','POST'])
def report():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    query = """
        SELECT 
            p.id,
            p.img,
            p.img_Name,
            r.ripeness_level,
            p.oil_content,
            p.time_captured,
            p.last_edit
        FROM
            palm p
        JOIN
            ripeness r ON p.ripeness_id = r.id
    """
    ripeQuery = """
        SELECT * FROM ripeness;
    """
    cursor.execute(query)
    data0 = cursor.fetchall()
    data1 = [
        {
            'id' : data[0],
            'img' : base64.b64encode(data[1]).decode('utf-8'),
            'img_name' : data[2],
            'ripeness_level' : data[3],
            'oil_content' : data[4],
            'time_captured' : data[5],
            'last_edit' : data[6]
        }
        for data in data0
    ]
    cursor.execute(ripeQuery)
    data2 = cursor.fetchall()
    context = [data1, data2]
    if request.method == "POST":
        date_from = request.form['date_from'] + ' 00:00:00'
        date_to = request.form['date_to'] + ' 23:59:59'
        print(date_from,date_to)
        dateQuery = """
            SELECT 
                p.id,
                p.img,
                p.img_Name,
                r.ripeness_level,
                p.oil_content,
                p.time_captured,
                p.last_edit
            FROM
                palm p
            JOIN
                ripeness r ON p.ripeness_id = r.id
            WHERE
                p.time_captured BETWEEN %s AND %s
        """
        cursor.execute(dateQuery,(date_from,date_to))
        data3 = cursor.fetchall()
        data3IMG = [
            {
                'id' : data[0],
                'img' : base64.b64encode(data[1]).decode('utf-8'),
                'img_name' : data[2],
                'ripeness_level' : data[3],
                'oil_content' : data[4],
                'time_captured' : data[5],
                'last_edit' : data[6]
            }
            for data in data3
        ]
        context = [data3IMG, data2]
        cursor.close()
        conn.close()
        return render_template('report.html', data = context)
    return render_template('report.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')





if __name__ == '__main__':
    app.run(debug=True)