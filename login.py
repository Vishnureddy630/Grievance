from flask import Flask, render_template, request
import mysql.connector
import e_mail as ea
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html', error_message=None)

@app.route('/login', methods=['POST'])
def login():
    got_username = request.form['username']
    got_password = request.form['password']
    type_user=request.form['user']
    global student 
    global user_info
    global elements
    global branch
    global cell
    
    if type_user=="admin":
        try:
            my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
            # my=mysql.connector.connect(host="vishnu1215.mysql.pythonanywhere-services.com",user='vishnu1215',password='vishnu@1234',database='vishnu1215$cb')
            cursor=my.cursor()
            cursor.execute(f"select * from cridentialsadmin where username='{got_username}' and password='{got_password}'")
            recods=cursor.fetchall()
            for row in recods:
                admin_user_name=row[0]
                name=row[2]
                branch=row[3]
                id=row[4]
                cell=row[5]
            # print(student,name,rollno,branch,cell)
            print(cell)
            user_info = {'User_type': admin_user_name,'Name': name,'Roll_no': id,'Branch': branch}            
            if cell=='Facalty Cell':
                cursor.execute(f"select status from complent where cell='{cell}' and branch='{branch}'")
                recods=cursor.fetchall()
                temp={}
                for row in recods:
                    key=row[0]
                    value=1
                    if key in temp:
                        temp[key]=value+temp[key]
                    else:
                        temp[key]=value        
            else:
                cursor.execute(f"select status from complent where cell='{cell}'")
                recods=cursor.fetchall()
                temp={}
                for row in recods:
                    key=row[0]
                    value=1
                    if key in temp:
                        temp[key]=value+temp[key]
                    else:
                        temp[key]=value                      
            return render_template('admin5.html',user_info=user_info,temp=temp)
            

        except:
            error_message = 'Incorrect username or password. Please try again.'
            return render_template('login.html', error_message=error_message)
    else:       
        try:
            my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
            # my=mysql.connector.connect(host="vishnu1215.mysql.pythonanywhere-services.com",user='vishnu1215',password='vishnu@1234',database='vishnu1215$cb')
            cursor=my.cursor()
            cursor.execute(f"select * from cridentials where username='{got_username}' and password='{got_password}'")
            recods=cursor.fetchall()
            for row in recods: 
                student=row[0]
                name=row[1]
                rollno=row[2]
                branch=row[3]
            user_info = {'User_type': type_user,'Name': name,'Roll_no': rollno,'Branch': branch}
            return render_template('oncomplents.html')
            # return render_template('main_page.html',user_info=user_info)

        except:
            error_message = 'Incorrect username or password. Please try again.'
            return render_template('login.html', error_message=error_message)

@app.route('/option', methods=['POST'])
def option():  
    global button_clicked
    button_clicked = ''
    if request.method == 'POST':
        if 'Examintaion Cell' in request.form:
            button_clicked = 'Examintaion Cell'
        elif 'Facalty Cell' in request.form:
            button_clicked = 'Facalty Cell'
            user_info['Name']="unknown person"
            user_info['Roll_no']="Unknown"
        elif 'Maintaince cell' in request.form:
            button_clicked = 'Maintaince cell'
    return render_template('main_page2.html',user_info=user_info,button_clicked=button_clicked)

@app.route('/send', methods=['POST'])
def send():
    try:
        mess = request.form['complaint-description']
        subject = request.form['subject']
        my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
        cursor=my.cursor()
        status='Unsolved'
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d')
        print(current_date)        
        cursor.execute("INSERT INTO complent  VALUES (%s, %s,%s,%s,%s,%s,%s)", ( student,button_clicked,branch,subject, mess,current_date,status))
        my.commit()
        cursor.close()
        my.close()
        # ea.mail(mess, subject,button_clicked,branch)
        response = "Thank you for your complaint. We will look into it and get back to you as soon as possible."
        return render_template('pop_up_interface.html', response=response)
    except Exception as e:
        print(e)
        response= "An error occurred while processing your request."+str(e)
        return render_template('pop_up_interface.html', response=response)

@app.route('/close', methods=['POST'])
def close():
    return render_template('login.html', error_message=None)

@app.route('/capture')
def capture():
    button_value = request.args.get('button')
    print(f'Button clicked: {button_value}')
    my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
    cursor=my.cursor()
    if cell=='Facalty Cell':
        cursor.execute("select subject from complent where cell=%s and status=%s and branch=%s ",(cell,button_value,branch))
        recods=cursor.fetchall()
        elements = []
        for row in recods:
            elements.append(row[0])
    else:
        cursor.execute("select subject from complent where cell=%s and status=%s ",(cell,button_value))
        recods=cursor.fetchall()
        elements = []
        for row in recods:
            elements.append(row[0])
    return render_template('files.html',elements=elements)

@app.route('/clicked', methods=['POST'])
def clicked():
    global clicked_element
    clicked_element=""
    if request.method == 'POST':
        clicked_element = request.form['element']
        print(clicked_element)
        my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
        cursor=my.cursor()
        # Insert data into database
        cursor.execute("SELECT subject,complent,date,username FROM complent WHERE cell=%s AND  subject=%s", ( cell ,clicked_element ))
        recods=cursor.fetchall()
        for row in recods: 
                subj=row[0]
                com=row[1]
                date=row[2]
                username=row[3]
        letter={'subject':subj,'content':com,'date':date,'cell':cell,'username':username}
        return render_template('letter.html', letter=letter)

@app.route('/lettercapture')
def lettercapture():
    button = request.args.get('button')
    print(f'Button clicked: {button}')
    my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
    cursor=my.cursor()       
    cursor.execute("UPDATE complent SET status=%s WHERE subject=%s", ( button, clicked_element))
    my.commit()
    cursor.close()
    my.close()
    my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
    cursor=my.cursor() 
    cursor.execute(f"select status from complent where cell='{cell}'")
    recods=cursor.fetchall()
    print("hai")
    temp={}
    for row in recods:
        key=row[0]
        value=1
        if key in temp:
            temp[key]=value+temp[key]
        else:
            temp[key]=value
    return render_template('admin5.html',user_info=user_info,temp=temp)
    
@app.route('/adminsidebar')
def sidebar():
    button_value = request.args.get('choice')
    print(f'side bar Button clicked: {button_value}')
    return render_template('add_admin.html')

@app.route('/addadmin_verification', methods=['POST'])
def addadmin():
    global email
    email = request.form['email']
    print(email)
    ea.otp(email)
    error_message=""
    return render_template('otp.html',error_message=error_message)
       
@app.route('/otp', methods=['POST'])
def otp():
    otp = request.form['otp']
    print("came to otp",otp)
    my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
    cursor=my.cursor() 
    print(type(email))
    cursor.execute("select otp from otp where email=%s",(email,))
    recods=cursor.fetchall()
    for row in recods:
        fetchotp=row[0]
    if fetchotp==otp:
        error_message=""
        return render_template('cridentials.html',email=email,error_message=error_message)
    else:
        error_message="Sorry, the OTP you entered is incorrect. Please try again or request a new OTP if you haven't received it."
    print(email)
    return render_template('otp.html',error_message=error_message)

@app.route('/cridentials', methods=['POST'])
def cridentials():
    newusername = request.form['newusername']
    newbranch = request.form['newbranch']
    newpassword = request.form['newpassword']
    id = request.form['id']
    usercell = request.form['usercell']
    print(newusername,newbranch,newpassword,id,usercell)
    my=mysql.connector.connect(host="localhost",user='root',password='vishnu@123',database='cb')
    cursor = my.cursor()
    cursor.execute("insert into cridentialsadmin values(%s,%s,%s,%s,%s,%s)",(email,newpassword,newusername,newbranch,id,usercell))
    my.commit()
    cursor.close()
    my.close()
    response=f"New admin is added details are email:{email}\n username:{newusername}\n newbranch:{newbranch} \n newpassword:{newpassword}\nid:{id}\nusercell:{usercell} "
    # print(response)
    return render_template('pop_up_interface.html',response=response)

if __name__ == '__main__':
    # webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
    