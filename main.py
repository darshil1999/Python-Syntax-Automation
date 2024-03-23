# Required Libraries
from nltk import word_tokenize
from flask import Flask, render_template,json, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import keyword
import re

app = Flask(__name__)

# Confugirations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/users'
app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Home page Api
@app.route("/")
def home():
    return render_template('index.html')

# About page Api
@app.route("/about")
def about():
    return render_template('about.html')

#Contact us class
class Contact(db.Model):
    '''
    Database Generation for contacts:
    Attributes are sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

# Contact page Api
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        return render_template('index')
    else:    
        return render_template('contact.html')

# Login page Class
class Login(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)

# Login page Api
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('psw')
        entry = Login(email=email,password = password,date= datetime.now())
        db.session.add(entry)
        db.session.commit()
        return render_template('codeplaygroud.html')
    else:
        return render_template('login.html')

# Register page Class
class Reg(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    repeat_password = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)

# Register page Api
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('psw')
        repeat_password = request.form.get('psw-repeat')
        entry = Reg(email=email,password = password,repeat_password = repeat_password , date= datetime.now())
        db.session.add(entry)
        db.session.commit()
        return render_template('login.html')
    else:
        return render_template('register.html')

# Code Playground Api
@app.route("/codeplayground",methods=['GET','POST'])
def codeplayground():
    return render_template('code_playground.html')

# validation api
@app.route("/validate",methods=['POST'])
def validate():
    # text input from editor
    text = request.form.to_dict(flat=False)
    print("text>>>", text)

    response_dict = json.dumps(text)
    print(response_dict)

    response = json.loads(response_dict)["\"editor"]
    print("response: ", response)

    editor_value = response[0].replace("\"", "")
    
    # New line starts velidating
    
    if editor_value.find('\n'):

        editor_value = editor_value.split('\n')[-1]
        print("editor_value>>", editor_value)
        
        # keywords for for loop 

        if editor_value == 'f':
            response = {'keywords': 'for | Flase | finally | format(o, format_space) |from | function | float'}
        
        elif editor_value == 'fo':
            response = {'keywords': 'for | format(o, format_space)'}
        
        elif editor_value == 'for':
            response = {'keywords': 'for | format(o, format_space)'}
        
        elif editor_value == 'for ':
            response = {'keywords': 'for '}
        
        # keywords for in 
        
        elif editor_value == 'i':
            response = {'keyword':'import | in |input | is | if '}
        
        elif editor_value == 'in':
            response = {'keyword':'in |input'}
        
        # keywords for input 
        
        elif editor_value == 'inp':
            response = {'keyword':'input'}  

        elif editor_value == 'inpu':
            response = {'keyword':'input'}

        elif editor_value == 'input':
            response = {'keyword':'input'}
        
        # keywords for if 
        
        if editor_value == 'if':
            response = {'keyword':'if'}

        # keywords for else 

        elif editor_value == 'e':
            response = {'keyword':'else | except | elif'}

        elif editor_value == 'el':
            response = {'keyword':'else | elif'}

        elif editor_value == 'els':
            response = {'keyword':'else'}

        elif editor_value == 'else':
            response = {'keyword':'else'}
        
        # keywords for is 
        
        if editor_value == 'is':
            response = {'keyword':'is'}  
  
        # keywords for print 

        if editor_value == 'p':
            response = {'keyword' : 'print | project | pass '}

        elif editor_value == 'pr':
            response = {'keywords': 'print | project'}

        elif editor_value == 'pri':
            response = {'keywords': 'print'}
        
        elif editor_value == 'prin':
            response = {'keyword' : 'print'}

        elif editor_value == 'print':
            response = {'keyword' : 'print'}
        
        # keywords for while 
        
        if editor_value == 'w':
            response = {'keyword':'while | with'}

        elif editor_value == 'wh':
            response = {'keyword':'while'}

        elif editor_value == 'whi':
            response = {'keyword':'while'}

        elif editor_value == 'whil':
            response = {'keyword':'while'}

        elif editor_value == 'while':
            response = {'keyword' : 'while'}
        
        # keywords for Class 
        
        if editor_value == 'c':
            response = {'keyword': 'class | continue'}
        
        elif editor_value == 'cl':
            response = {'keyword' : 'class'}
        
        elif editor_value == 'cla':
            response = {'keyword': 'class'}
        
        elif editor_value == 'clas':
            response = {'keyword': 'class'}
        
        elif editor_value == 'class':
            response = {'keyword': 'class'}
        
        # keywords for Function 
        
        if editor_value == 'd':
            response = {'keyword': 'def | del'}
        
        elif editor_value == 'de':
            response = {'keyword': 'def | del'}
        
        elif editor_value == 'def':
            response = {'keyword': 'def'}
        

        a = word_tokenize(editor_value)[0]
        token = ''

        # token validations

        if keyword.iskeyword(a):
            print(a, "It is a token")
            token = a
        elif a == 'for':
            print(a, "It is a token")
            token = a
        elif a == 'print':
            print(a, "It is a token")
            token = a
        elif a == 'if':
            print(a, "It is a token")
            token = a
        elif a == 'else':
            print(a, "It is a token")
            token = a
        elif a == 'while':
            print(a, "It is a token")
            token = a
        elif a == 'class':
            print(a, "It is a token")
            token = a
        elif a == 'def':
            print(a, "It is a token")
            token = a
        else:
            print(a, "It is a not token")

        print(token)

        # for loop regular expression check

        if token == "for":
            
            # regular expression of for loop

            regex = '^(?:(for)|(?:[\s]{1,4}|[\t]{1})(for))[ ]{1,}[a-z,A-Z,\_,\,\-,0-9]{1,}[ ]{1,}(in)[ ]{1,}(?:[\"][a-z,A-Z,\_,\,\-,0-9]{1,}[\"]|[\'][a-z,A-Z,\_,\,\-,0-9]{1,}[\']|[\'][\'][\'][a-z,A-Z,\_,\,\-,0-9]{1,}[\'][\'][\']|[a-z,A-Z,,\-]{1,}|(range)[(](?:[0-9, ]{1,8}|[0-9, ]{1,7}[-][0-9]|[a-z]{1,3}[(][a-z,A-Z,\_,\,\-,0-9]{1,}[)])[)])[:]$'

            if re.search(regex, editor_value):
                response = {'successMessage': "You entered correct syntax."}
            else:
                response = {'errorMessage': "You entered incorrect syntax."}

        # print statement regular expression check

        elif token == "print":
            
            # regular expression of print statement
            
            regex = '^(print)\(((.)+|([.]+,end=(\"\"))|([+]\w|)+|([.]+,sep=(\"[.]+\")))\)'

            if re.search(regex,editor_value):
                response = {'successMessage': "You entered correct syntax."}
            else:
                response = {'errorMessage': "You entered incorrect syntax."}

        # if regular expression check

        elif token == "if":
            
            # regular expression of if
            
            regex = '^(?:(?:(if)|(?:[\s]{1,4}|[\t]{1})(if))|(?:(elif)|(?:[\s]{1,4}|[\t]{1})(elif)))[ ]{1,}(?:[a-z,A-Z][ ]{1,}(?:[\<,\>,\=,!][=]|[>,<])[ ]{1,}(?:[a-z,A-Z]|[a-z,A-Z][0-9]{1,}|[\"][a-z,A-Z][\"]|[\'][a-z,A-Z][\']|[0-9]{1,})|[a-z,A-Z,][ ]{1,}(?:[\<,\>,\=,!][=]|[>,<])[ ]{1,}(?:[a-z,A-Z]|[a-z,A-Z][0-9]{1,}|[\"][a-z,A-Z][\"]|[\'][a-z,A-Z][\']|[0-9]{1,})[ ]{1,}(?:(and)|(or))[ ]{1,}[a-z,A-Z,][ ]{1,}(?:[\<,\>,\=,!][=]|[>,<])[ ]{1,}(?:[a-z,A-Z]|[a-z,A-Z][0-9]{1,}|[\"][a-z,A-Z][\"]|[\'][a-z,A-Z][\']|[0-9]{1,})|[a-z,A-Z,][ ]{1,}(?:(is)|(in)|(is)[ ]{1,}(not)|(not)[ ]{1,}(in))[ ]{1,}(?:[a-z,A-Z]|[a-z,A-Z][0-9]{1,}|[\"][a-z,A-Z][\"]|[\'][a-z,A-Z][\']|[0-9]{1,})|(True)|(False))[:]$'

            if re.search(regex, editor_value):
                response = {'successMessage': "You entered correct syntax."}
            else:
                response = {'errorMessage':"You entered incorrect syntax."}

        # else regular expression check

        elif token == "else":
            
            # regular expression of else
            
            regex = '(?:(else))[:]$'

            if re.search(regex, editor_value):
                response = {'successMessage': "You entered correct syntax."}
            else:
                response = {'errorMessage':"You entered incorrect syntax."}

        # class regular expression check

        elif token == "class":
            
            # regular expression of class
            
            regex = '^(?:(class)|(?:[\s]{1,4}|[\t]{1})(class))[\s]{1,}[A-Z]{1}[a-z]{1,}[:]$'

            if re.search(regex, editor_value):
                response = {'successMessage': "You entered correct syntax."}
            else:
                response = {'errorMessage' : "You entered incorrect syntax."}

        # function regular expression check

        elif token == "def":
            
            # regular expression of function
            
            regex = '^(?:(def)|(?:[\s]{1,4}|[\t]{1})(def))[\s]{1,}[a-z]{1,}(?:[(][)]|[(][a-z,A-Z,\_,\,\-,0-9]{1,}[)])[:]$'

            if re.search(regex, editor_value):
                response = {'successMessage': "You entered correct syntax."}
            else:
                response = {'errorMessage' : "You entered incorrect syntax."}

        # While regular expression check
            
            # regular expression of while
            
        elif token == "while":

            regex = '^(?:(while)|(?:[\s]{1,4}|[\t]{1})(while))[ ]{1,}(?:[a-z,A-Z,][ ]{1,}(?:[\<,\>,\=,!][=]|[>,<])[ ]{1,}(?:[a-z,A-Z]|[a-z,A-Z][0-9]{1,}|[\"][a-z,A-Z][\"]|[\'][a-z,A-Z][\']|[0-9]{1,})|[a-z,A-Z,][ ]{1,}(?:[\<,\>,\=,!][=]|[>,<])[ ]{1,}(?:[a-z,A-Z]|[a-z,A-Z][0-9]{1,}|[\"][a-z,A-Z][\"]|[\'][a-z,A-Z][\']|[0-9]{1,})[ ]{1,}(?:(and)|(or))[ ]{1,}[a-z,A-Z,][ ]{1,}(?:[\<,\>,\=,!][=]|[>,<])[ ]{1,}(?:[a-z,A-Z]|[a-z,A-Z][0-9]{1,}|[\"][a-z,A-Z][\"]|[\'][a-z,A-Z][\']|[0-9]{1,})|[a-z,A-Z,][ ]{1,}(?:(is)|(in)|(is)[ ]{1,}(not)|(not)[ ]{1,}(in))[ ]{1,}(?:[a-z,A-Z]|[a-z,A-Z][0-9]{1,}|[\"][a-z,A-Z][\"]|[\'][a-z,A-Z][\']|[0-9]{1,})|(True)|(False))[:]$'

            if re.search(regex, editor_value):
                response = {'successMessage': "You entered correct syntax."}

            else:
                response = {'errorMessage': "You entered incorrect syntax."}

    return json.dumps(response)

app.run(debug=True)