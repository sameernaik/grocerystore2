from flask import Flask,flash,render_template,request,session,redirect,url_for
from models import *
from email_validator import validate_email, EmailNotValidError

from sqlalchemy import func

class CartStatus:
        ACTIVE=1
        SUCCESS=2

'''class ApplyPromoCode:
        FALSE=0
        TRUE=1

def applyFirstTransactionPromoCode(user_id):
        purchaseOrder= PurchaseOrder.query.filter(PurchaseOrder.user_id==user_id,PurchaseOrder.status=='SUCCESS').first()
        if purchaseOrder:
                print('First Time User Transaction Promo Code not applicable')
                return ApplyPromoCode.FALSE
        else:
                print('First Time User Transaction Promo Code applicable')
                return ApplyPromoCode.TRUE'''
        
def createShoppingSessionIfNotExists():
                if session.get('user-id',None) !=None:
                        shoppingSession=Cart.query.filter(Cart.user_id==session['user-id'],Cart.status==CartStatus.ACTIVE).first()
                        if(shoppingSession==None):
                                #promo_code_apply=applyFirstTransactionPromoCode(session['user-id'])
                                #shoppingSession=Cart(user_id= session['user-id'],total=0,status=CartStatus.ACTIVE,apply_promo_code=promo_code_apply)
                                shoppingSession=Cart(user_id= session['user-id'],total=0,status=CartStatus.ACTIVE)
                                db.session.add(shoppingSession)
                                db.session.commit()
                        print("shopping_session.id=",shoppingSession.id)
                        session['shopping-session-id']=shoppingSession.id
                        return True
                else :
                        flash('Please Login to continue Shopping')
                        return False   
                
def defineAuthenticationRoutes(app):
    @app.route("/login-user",methods =['GET','POST'])
    def login_page():
        if request.method=="GET":
            return render_template('login.html',loginType="User")
        elif request.method=="POST":
                tryLogUserName=request.form.get("username")
                tryPassword=request.form.get("password")
                try:
                        emailinfo = validate_email(tryLogUserName, check_deliverability=False)
                        if emailinfo:
                                #print(tryLogUserName,tryPassword)
                                dbUser=User.query.filter(User.username==tryLogUserName, User.password==tryPassword).first()
                                print('Database Users',dbUser)
                                if (dbUser != None):
                                        session['user-id'] = dbUser.id
                                        print(tryLogUserName," is valid User",dbUser.id)
                                        createShoppingSessionIfNotExists()
                                        print('Added shopping session and user-id in session object',session['shopping-session-id'],session['user-id'],session)
                                        return redirect('/shop')
                                else:
                                        flash('Invalid username/password')
                                        return redirect('/login-user',)
                        else:
                                flash('Username is not a valid email address')
                                return redirect('/login-user')
                except EmailNotValidError as e:
                        flash("Username is not a valid email address",category='error')
                        return redirect('/login-user')
                        
    #https://stackoverflow.com/questions/42013067/how-to-access-session-variables-in-jinja-2-flask
    @app.route("/login-admin",methods =['GET','POST'])
    def login_manager():
            if request.method=="GET":
                return render_template('login.html',loginType="Manager")
            elif request.method=="POST":
                #print('Hello ',request.form.get("username"),request.form.get("password"))
                tryLogManagerName=request.form.get("username")
                tryPassword=request.form.get("password")
                try:
                        emailinfo = validate_email(tryLogManagerName, check_deliverability=False)
                        if emailinfo:
                                #print(tryLogManagerName,tryPassword)
                                dbManager=Manager.query.filter(Manager.username==tryLogManagerName, Manager.password==tryPassword).first()
                                print('Database Users',dbManager)
                                if (dbManager!=None):
                                        print(tryLogManagerName," is valid Manager User")
                                        session['role'] = 'manager'
                                        session['manager-id']=dbManager.id
                                        session['employee-name']=dbManager.firstname
                                        print("Manager id is ",dbManager.id)
                                        return redirect('/summary')
                                else:
                                        flash('Invalid username/password')
                                        return redirect('/login-admin')
                        else:
                                flash('Username is not a valid email address')
                except EmailNotValidError as e:
                        flash("Username is not a valid email address",category='error')
                        return redirect('/login-admin')
                
    @app.route("/register-admin", methods=['GET','POST'])
    def register_manager():
            if request.method=="GET": 
                    return render_template('register.html',registrationType="Manager")
            elif request.method=="POST":
                newLogUserName=request.form.get("username")
                newPassword=request.form.get("password")
                repeatPassword=request.form.get("repeatpassword")
                
                if newPassword == repeatPassword:
                        try:
                                emailinfo = validate_email(newLogUserName, check_deliverability=False)
                                if emailinfo:
                                        if len(newPassword) < 7:
                                                flash("Password must be atleast of 7 characters",category='error')
                                                return redirect('/register-admin')

                                        emailExists = Manager.query.filter(Manager.username==newLogUserName).first() 

                                        if not emailExists: 
                                                firstname=request.form.get("firstname")
                                                lastname=request.form.get("lastname")
                                                newUser = Manager(firstname=firstname,lastname=lastname,username=newLogUserName,password=newPassword)
                                                
                                                try:
                                                        db.session.add(newUser) 
                                                        db.session.commit() 
                                                        flash("User created successfully.",category='info')
                                                        print('User ',newLogUserName,'created successfully')
                                                        return redirect("/login-admin")

                                                except:
                                                        flash("Error occurred while creating your account",category='error')
                                                        return redirect('/register-admin') 

                                        else:
                                                flash("This email already exists, Please signup with other username",category='error')
                                                return redirect('/register-admin')

                        except EmailNotValidError as e:
                                flash("Username is not a valid email address",category='error')
                                return redirect('/register-admin')
                                
                
                else:
                        flash("Both the passwords don't match",category='error')
                        return redirect('/register-admin')
           
    @app.route("/register", methods =['GET','POST'])
    def register_user():
            if request.method=="GET":
                return render_template('register.html',registrationType="User")
            elif request.method=="POST":
                newLogUserName=request.form.get("username")
                newPassword=request.form.get("password")
                repeatPassword=request.form.get("repeatpassword")
                   
                if newPassword == repeatPassword:
                        
                        try:
                                emailinfo = validate_email(newLogUserName, check_deliverability=False)
                                if emailinfo:
                                        if len(newPassword) < 7:
                                                flash("Password must be atleast of 7 characters",category='error')
                                                return redirect('/register') 

                                        emailExists = User.query.filter(User.username==newLogUserName).first() 

                                        if not emailExists: 
                                                firstname=request.form.get("firstname")
                                                lastname=request.form.get("lastname")
                                                newUser = User(firstname=firstname,lastname=lastname,username=newLogUserName,password=newPassword)
                                                
                                                try:
                                                        db.session.add(newUser) 
                                                        db.session.commit() 
                                                        flash("User created successfully.",category='info')
                                                        print('User ',newLogUserName,'created successfully')
                                                        return redirect("/login-user")

                                                except Exception as e:
                                                        print(e)
                                                        flash("Error occurred while creating your account",category='error')
                                                        return redirect('/register') 

                                        else:
                                                flash("This email already exists, Please signup with other username",category='error')
                                                return redirect('/register') 

                        except EmailNotValidError as e:
                                flash("The given email isn't valid",category='error')
                                return redirect('/register')
                                
                
                else:
                        flash("Both the passwords don't match",category='error')
                        return redirect('/register')

               
            

    @app.route("/forgotPassword")
    def forgotPassword_page():
            return render_template('forgotPassword.html')