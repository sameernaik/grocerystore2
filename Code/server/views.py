from flask import flash,render_template,request,session,redirect,url_for
#from flask_login import logout_user,login_manager, login_required
from models import *
from authentication import createShoppingSessionIfNotExists,CartStatus
from sqlalchemy import func
from histogramGenerator import plotHistogram
from enum import Enum



#Consumer /shop
def computeBuyAgainProductList():
                buyAgainProductList=[]
                userId=session.get('user-id',None)
                #session_id=session.get('shopping-session-id',None)
                if (userId !=None):
                        dbProductIdTupleList=db.session.query(Product.id).filter(Product.id==PurchaseOrderItem.product_id).filter(PurchaseOrder.user_id==userId).filter(PurchaseOrderItem.order_id==PurchaseOrder.id).filter(PurchaseOrder.status==PurchaseOrderStatus.SUCCESS).filter(PurchaseOrder.created_at.between('2023-07-29','2023-12-31')).group_by(PurchaseOrderItem.product_id).order_by(func.sum(PurchaseOrderItem.quantity).desc()).limit(4).all()
                        dbProductIdList=[]
                        for productIdTuple in dbProductIdTupleList:
                                dbProductIdList.append(productIdTuple[0])
                        
                        print("### BuyAgain db Product ID List",dbProductIdList)
                        buyAgainProductList=Product.query.filter(Product.id.in_(dbProductIdList)).all()
                        if (len(buyAgainProductList)>0):
                                print("### BuyAgain Product List",buyAgainProductList)
                        else:
                                print("### Buy Again Product List not found.")
                return buyAgainProductList

def computeCartProductListAndTotal():
                cartProductList=[]
                total = 0
                session_id=session.get('shopping-session-id',None)
                if (session_id !=None):
                        cartItemList=CartItem.query.filter(CartItem.session_id==session_id).all()
                        for cartItem in cartItemList:
                                print('About to display cartItem ',cartItem)
                                product=Product.query.filter(Product.id==cartItem.product_id).first()
                                if (product!=None):
                                        product.quantity=cartItem.quantity
                                        print("adding product to display",product)
                                        cartProductList.append(product)
                                        #total = total + (product.quantity * (product.price - (product.price * product.discount/100)))
                                        total = total + (product.quantity * (product.discounted_price))
                                else:
                                        print('Not Found: Cart Item Product with id ',cartItem.product_id)
                return cartProductList,total

def computeCartProductListAndTotalFromOrder(orderId):
        cartProductList=[]
        total = 0
        
        purchaseOrderItemList=PurchaseOrderItem.query.filter(PurchaseOrderItem.order_id==orderId).all()
        print('#######computeCartProductListAndTotalFromOrder',orderId,purchaseOrderItemList)
        for purchaseOrderItem in purchaseOrderItemList:
                print('About to display purchaseOrderItem ',purchaseOrderItem)
                product=Product.query.filter(Product.id==purchaseOrderItem.product_id).first()
                print('#######computeCartProductListAndTotalFromOrder',product)
                if (product!=None):
                        product.quantity=purchaseOrderItem.quantity
                        print("adding product to display",product)
                        cartProductList.append(product)
                        #total = total + (product.quantity * (product.price - (product.price * product.discount/100)))
                        total = total + (product.quantity * (product.discounted_price))
                else:
                        print('Not Found: Order Item Product with id ',purchaseOrderItem.product_id)
        return cartProductList,total

def defineRoutes(app):
        #required in 
        #order and order-detail-modal to convert Enum to String
        #your-order to convert Enum to String
        @app.template_filter()
        def to_string(obj):
                if isinstance(obj, Enum):
                        return obj.value
                # For all other types, let Jinja use default behavior
                return obj
        
        @app.route("/")
        def home_page():
                return redirect('/shop')
        
        #Consumer search, advanced search
        @app.route("/category-product/<categoryId>")
        def category_product_page(categoryId):
                dbCategory=Category.query.filter(Category.id==categoryId).first()
                dbProductList=Product.query.filter(Product.categoryid==categoryId).all()
                #Below 3 lines are for displaying cartin navigation menu
                userId=session.get('user-id',None)
                dbUser=User.query.filter(User.id==userId).first()
                cartProductList,cartTotal=computeCartProductListAndTotal()
                dbCategoryList=Category.query.all()
                return render_template('category-product.html',heading=dbCategory.name,Categories=dbCategoryList,Products=dbProductList,user=dbUser,CartItemProducts=cartProductList,CartTotal=cartTotal)
       
        @app.route("/shop",methods =['GET'])
        def shop_page():
                dbCategoryList=Category.query.all()
                categoryProductDict={}
                for category in dbCategoryList:
                        print(category.id)
                        dbProductList=Product.query.filter(Product.categoryid==category.id).all()
                        categoryProductDict[category.id]=dbProductList
                        #for product in dbProductList:
                        #print(product.name,product.categoryid)
                print('categories list',len(dbCategoryList))
                print('categoriesProduct dict',categoryProductDict)
                # We use session.get('user-id',None) to avoid KeyError which we get in
                # userId=session['user-id'] because 'user-id' was never 
                # added when /shop page was directly accessed without logging in.
                
                #Below 3 lines are for displaying cart in navigation menu
                userId=session.get('user-id',None)
                print("Got userId",userId)
                dbUser=User.query.filter(User.id==userId).first()
                cartProductList,cartTotal=computeCartProductListAndTotal()
                
                #Display top 4 products brought by user in the past.
                buyAgainProductList=computeBuyAgainProductList()              
                
                return render_template('shop.html',Categories=dbCategoryList,CategoriesProductDict=categoryProductDict,user=dbUser,CartItemProducts=cartProductList,CartTotal=cartTotal,BuyAgainProductList=buyAgainProductList)
                 
        @app.route("/product-detail/<productId>",methods =['GET','POST'])
        def product_detail_add_to_cart(productId):
                if createShoppingSessionIfNotExists()==False:
                        return redirect('/login-user')
                if request.method=="GET":
                        product=Product.query.filter(Product.id==productId).first()
                        print("session ",session)
                        session_id=session.get('shopping-session-id',None)
                        cartItem=CartItem.query.filter(CartItem.session_id==session_id,CartItem.product_id==productId).first()
                        if(cartItem!=None):
                                product.quantity=cartItem.quantity
                        else :
                                #Default quantity is 1 when add product is opened first time
                                #and was not previously selected
                               print('Do nothing' )
                               product.quantity=1
                        
                        #Fetching related products
                        relatedProducts=Product.query.filter(Product.categoryid==product.categoryid).filter(Product.id != product.id).all()
                        
                        #Below 3 lines are for displaying cart in navigation menu
                        userId=session.get('user-id',None)
                        dbUser=User.query.filter(User.id==userId).first()
                        cartProductList,cartTotal=computeCartProductListAndTotal() 
                        dbCategoryList=Category.query.all()
                        return render_template('product-detail.html',Product=product,Categories=dbCategoryList,showAddToCart="true",RelatedProducts=relatedProducts,user=dbUser,CartItemProducts=cartProductList,CartTotal=cartTotal)
                else:   #Handle POST method
                        #Handle Add to Cart
                        #session['shopping-session-id']=shoppingSession.id
                        itemQuantity=int(request.form.get('quantity'))
                        #itemQuantity will always be greater than 0 because user selects it from drop down options.
                        cartItem=CartItem.query.filter(CartItem.session_id==session['shopping-session-id'],CartItem.product_id==request.form.get('productId')).first()
                        if(cartItem==None):
                                cartItem=CartItem(session_id=session['shopping-session-id'],product_id=request.form.get('productId'),quantity=itemQuantity)
                        else:
                                cartItem.quantity=itemQuantity
                        db.session.add(cartItem)
                        db.session.commit()
                        print("Product Id ",request.form.get('productId'))
                        print("Quantity ",itemQuantity)
                        print("I am a good Software Developer")
                        return redirect("/cart")
                        
        
        @app.route("/cart",methods=['GET','POST'])
        def cart_page():
                if request.method=="GET":
                        cartProductList,cartTotal=computeCartProductListAndTotal()
                        userId=session.get('user-id',None)
                        dbUser=User.query.filter(User.id==userId).first()
                        dbCategoryList=Category.query.all()
                        session_id=session.get('shopping-session-id',None)
                        cart=Cart.query.filter(Cart.user_id==userId,Cart.id==session_id).first()
                        if len(cartProductList) > 0:
                                return render_template('cart.html',user=dbUser,Categories=dbCategoryList,CartItemProducts=cartProductList,CartTotal=cartTotal,applyPromoCode=cart.apply_promo_code)
                        else:
                                #redirecting to shop because cart is empty
                                return redirect('/shop')
                else:
                        print('checking out with checkout.html')
                        return redirect('/checkout') 
        
        #Route to remove item from cart.
        @app.route("/cart-item/<productId>/delete",methods=['GET'])
        def cart_item(productId):
                print("cart-item/<productId>/delete for ",productId)
                session_id=session.get('shopping-session-id',None)
                print("cart-item session_id=",session_id)
                if (session_id !=None):
                        CartItem.query.filter(CartItem.session_id==session_id).filter(CartItem.product_id==productId).delete()
                        db.session.commit()
                        print("delete cart-item db session commited for ",productId)
                return redirect("/cart")
                                
        #contact_person_name, contact_person_number, housename, line_address,town_city, state, landmark, pincode
        #Consumer: /checkout
        def getDeliveryAddressListForUser():
                userId=session.get('user-id',None)
                dbAddressList=Address.query.filter(Address.user_id==userId).all()
                addressDict={}
                defaultAddressId=None
                if len(dbAddressList)>0:
                        defaultAddressId=dbAddressList[0].id
                for dbAddress in dbAddressList :
                        if dbAddress.defaultAddress==1:
                                defaultAddressId=dbAddress.id
                        dbState=State.query.filter(State.id==dbAddress.state).first()
                        stringAddress=dbAddress.contact_person_name +", "+dbAddress.housename+", "+dbAddress.line_address+", "+dbAddress.landmark+", "+dbState.name+", "+dbAddress.town_city+", "+ str(dbAddress.pincode) +", Ph No: "+str(dbAddress.contact_person_number)
                        #print('####### ',stringAddress)
                        addressDict[dbAddress.id]=stringAddress
                #print('defaultAddressId',defaultAddressId,',addressDict',addressDict)        
                return addressDict,defaultAddressId
        
        def getDeliveryAddressForUser(addressId):
                userId=session.get('user-id',None)
                print('userId',userId)
                dbAddress=Address.query.filter(Address.user_id==userId,Address.id==addressId).first()
                dbState=State.query.filter(State.id==dbAddress.state).first()
                stringAddress=dbAddress.contact_person_name +", "+dbAddress.housename+", "+dbAddress.line_address+", "+dbAddress.landmark+", "+dbState.name+", "+dbAddress.town_city+", "+ str(dbAddress.pincode) +", Ph No: "+str(dbAddress.contact_person_number)
                print('####### ',stringAddress)
                return stringAddress
        
        @app.route("/checkout", methods =['GET','POST'])
        def checkout_page():
                if request.method=="GET":
                        #Below 3 lines are for displaying cartin navigation menu
                        userId=session.get('user-id',None)
                        dbUser=User.query.filter(User.id==userId).first()
                        cartProductList,cartTotal=computeCartProductListAndTotal() 
                        deliveryAddressList,defaultAddressId=getDeliveryAddressListForUser()
                        
                        #All Categories are required by top search bar
                        dbCategoryList=Category.query.all()
                        return render_template('checkout.html',user=dbUser,Categories=dbCategoryList,CartItemProducts=cartProductList,CartTotal=cartTotal,DeliveryAddressDict=deliveryAddressList,DefaultAddressId=defaultAddressId)
                else:
                        delivery_address=request.form.get("delivery-address")
                        if delivery_address == None:
                                flash('Please enter delivery address')
                                return redirect("/checkout")
                        else:
                                user_id=session.get('user-id',None)
                                session_id=session.get('shopping-session-id',None)
                                shipping_charges=request.form.get("shipping-charges")
                                total=request.form.get("order-total")
                                payment_mode=request.form.get("payment-mode")
                                productList,cartTotal=computeCartProductListAndTotal()
                                
                                if payment_mode=="1":
                                        information='Successful Payment'
                                        status=PurchaseOrderStatus.SUCCESS
                                        payment_status=1
                                        #Emptying the cart Start
                                        cart=Cart.query.filter(Cart.id==session_id).first()
                                        cart.status=CartStatus.SUCCESS
                                        db.session.add(cart)
                                        #Emptying the cart End
                                        #Managing the Inventory Start
                                        for product in productList:
                                                dbProduct=Product.query.filter(Product.id==product.id).first()
                                                dbProduct.stock_quantity=int(dbProduct.stock_quantity)-(int(product.quantity)*int(product.sell_quantity))
                                                if dbProduct.stock_quantity<1:
                                                        # Send Major message manager that stock quantity is going low
                                                        dbCategory=Category.query.filter(Category.id==dbProduct.categoryid).first()
                                                        addToDBMessage=Message(message='Product: '+dbProduct.name+' stock quantity is 0 '+dbProduct.stock_unit +'.', severity='MAJOR', owner=dbCategory.owner)
                                                        db.session.add(addToDBMessage)
                                                
                                                elif dbProduct.stock_quantity<100:
                                                        # Warn manager that stock quantity is going low
                                                        dbCategory=Category.query.filter(Category.id==dbProduct.categoryid).first()
                                                        addToDBMessage=Message(message='Product: '+dbProduct.name+' stock quantity below 100 '+dbProduct.stock_unit +' .Current Stock '+ str(dbProduct.stock_quantity)+' '+dbProduct.stock_unit+'.', severity='WARN', owner=dbCategory.owner)
                                                        db.session.add(addToDBMessage)
                                                db.session.add(dbProduct) 
                                        #Managing the Inventory End
                                
                                else:
                                        information='Failed Payment'
                                        status=PurchaseOrderStatus.PAYMENTFAILED
                                        payment_status=2
                                
                                #promo_code=
                                
                                print("#######delivery_address",delivery_address)
                                purchaseorder=PurchaseOrder(user_id=user_id,session_id=session_id,shipping_charges=shipping_charges,total=total,status=status,delivery_address=delivery_address)
                                #check if in-stock
                                #update stock
                                db.session.add(purchaseorder)
                                db.session.commit() 
                                print('checking out with checkout.html',purchaseorder.id,user_id,session_id,shipping_charges,total,payment_mode,delivery_address)
                                
                                
                                for product in productList:
                                        purchaseorderitem=PurchaseOrderItem(order_id=purchaseorder.id,product_id=product.id,quantity=product.quantity,price=float(product.discounted_price),discount=product.discount)
                                        db.session.add(purchaseorderitem) 
                                
                                paymentdetails=PaymentDetails(user_id=user_id,order_id=purchaseorder.id,payment_mode=payment_mode,information=information,status=payment_status)
                                db.session.add(paymentdetails)
                                
                                db.session.commit()
                                if payment_mode=="1":
                                        
                                        # Be careful. We have removed the shopping-session-id because it is SUCCESS and now new session is required.
                                        # removing the session because payment was successful. 
                                        # New shopping session will be created when user clicks 
                                        # Add To Cart by calling createShoppingSessionIfNotExists()
                                        session.pop('shopping-session-id')  

                                return redirect(url_for('orderConfirmation',orderId=purchaseorder.id))
        
        @app.route("/order-confirmation/<orderId>")
        def orderConfirmation(orderId):
                if request.method=="GET":
                        deliveryAddress=getDeliveryAddressForUser(PurchaseOrder.query.filter(PurchaseOrder.id==orderId).first().delivery_address)
                        dbPurchaseOrderStatus=PurchaseOrder.query.filter(PurchaseOrder.id==orderId).first().status
                        
                        productList,computedCartTotal=computeCartProductListAndTotalFromOrder(orderId)
                        userId=session.get('user-id',None)
                        dbUser=User.query.filter(User.id==userId).first()
                        dbCategoryList=Category.query.all()

                        if dbPurchaseOrderStatus==PurchaseOrderStatus.SUCCESS:
                                return render_template('order-confirmation.html',user=dbUser,Categories=dbCategoryList,Products=productList,cartTotal=computedCartTotal,CartTotal=0,DeliveryAddress=deliveryAddress,orderStatus=dbPurchaseOrderStatus)
                        else:
                                return render_template('order-confirmation.html',user=dbUser,Categories=dbCategoryList,Products=productList,CartItemProducts=productList,cartTotal=computedCartTotal,CartTotal=computedCartTotal,DeliveryAddress=deliveryAddress,orderStatus=dbPurchaseOrderStatus)         
                else:
                        print('checking out with checkout.html')
                        return redirect('/')        
       
        #Historic orders for user
        @app.route("/your-orders")
        def your_orders():
                userId=session.get('user-id',None)
                dbUser=User.query.filter(User.id==userId).first()
                cartProductList,cartTotal=computeCartProductListAndTotal()
                dbCategoryList=Category.query.all() 
                
                dbPastOrders=PurchaseOrder.query.filter(PurchaseOrder.user_id==userId).order_by(PurchaseOrder.id.desc()).all()
                print('dbPastOrders ',dbPastOrders)
                return render_template('your-orders.html',user=dbUser,CartItemProducts=cartProductList,CartTotal=cartTotal,pastOrders=dbPastOrders,Categories=dbCategoryList)
        
        @app.route("/your-order/<orderId>",methods =['GET'])
        def your_order_details_page(orderId):
               if request.method=="GET":
                        dbPurchaseOrder=db.session.query(PurchaseOrder.id,User.username,PurchaseOrder.total,PurchaseOrder.created_at,PurchaseOrder.status).filter(PurchaseOrder.id==orderId).filter(User.id==PurchaseOrder.user_id).first()
                        #deliveryAddress=getDeliveryAddressForUser(PurchaseOrder.query.filter(PurchaseOrder.id==orderId).first().delivery_address)
                        productList,cartTotal=computeCartProductListAndTotalFromOrder(orderId)
                        #return render_template('order-Confirmation.html',Products=productList,CartTotal=cartTotal,DeliveryAddress=deliveryAddress)
                        return render_template('your-order-detail-modal.html',Order=dbPurchaseOrder,Products=productList,CartTotal=cartTotal,pageTitle="Order Details",modal=True)
        
        @app.route("/newDeliveryAddressModal",methods=['GET','POST'])
        def newDeliveryAddressModal():
                if request.method=="GET":
                        dbStatesList=State.query.all()
                        return render_template('address-modal.html',States=dbStatesList)
                else :
                       #contact_person_name, contact_person_number, housename, town_city, state, landmark, pincode
                        userId=session.get('user-id',None)
                        defaultAddressFlag=request.form.get("defaultAddressFlag")
                        print('#######Default Address Flag ',defaultAddressFlag)
                        hasPreviousDefaultAddress=Address.query.filter(Address.user_id==userId,Address.defaultAddress==1).first()
                        
                        if defaultAddressFlag == "1":
                                print('###defaultAddressFlag ',defaultAddressFlag)
                                if hasPreviousDefaultAddress != None:
                                        #reset pervious default address because we have new default address.
                                        print('###Resetting previous Address for ',userId)
                                        hasPreviousDefaultAddress.defaultAddress=0
                                        db.session.add(hasPreviousDefaultAddress)
                                        db.session.commit()
                        else:
                                if hasPreviousDefaultAddress==None:
                                        #Marking current address as default address 
                                        # because there is No Default Address set previously
                                        defaultAddressFlag=1
                                else:
                                        defaultAddressFlag=0 
                                
                        print('#######Storing in DB Default Address Flag ',defaultAddressFlag)
                        address=Address(user_id=userId,
                                                contact_person_name=request.form.get("contact_person_name"),
                                                contact_person_number=request.form.get("contact_person_number"),
                                                housename=request.form.get("housename"),
                                                line_address=request.form.get("line_address"),
                                                town_city=request.form.get("town_city"),
                                                state=request.form.get("state"),
                                                landmark=request.form.get("landmark"),
                                                pincode=request.form.get("pincode"),
                                                defaultAddress=defaultAddressFlag
                                                )
                        print(address,'address is being added to database')
                        db.session.add(address)
                        db.session.commit()
                        return redirect("/checkout")
        
      
        '''@app.route('/logout')

        @login_required
        def logout():
                #logout_user()
                if session.get('was_once_logged_in'):
                        # prevent flashing automatically logged out message
                        del session['was_once_logged_in']
                flash('You have successfully logged yourself out.')
                return redirect('/login-user')
        
        @app.route('/login-user', methods=['GET', 'POST'])
                def login():
                if app.current_user.is_authenticated:  # already logged in
                        return redirect('/home')
                if request.method == 'POST':
                        user = SessionUser.find_by_session_id(request.data['user_id'])
                        if user:
                        login_user(user)
                        session['was_once_logged_in'] = True
                        return redirect('/home')
                        flash('That user was not found in the database.')
                if session.get('was_once_logged_in'):
                        flash('You have been automatically logged out.')
                        del session['was_once_logged_in']
                return render_template('/login.html')



        @app.route('/home')
        @login_required
                def home():
                return 'You are logged in as {0}.'.format(app.current_user.id)
                
        https://stackoverflow.com/questions/47670382/how-to-logout-a-user-from-the-database-with-flask-login
        https://stackoverflow.com/questions/37227780/flask-session-persisting-after-close-browser
        https://www.roseindia.net/answers/viewqa/pythonquestions/102444-ModuleNotFoundError-No-module-named-Flask-Login.html
                '''