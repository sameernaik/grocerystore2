from flask import Flask,flash,render_template,request,session,redirect,url_for
from models import *
from sqlalchemy import func
from views import computeCartProductListAndTotal
from datetime import datetime

def defineSearchRoutes(app):
    @app.route("/search",methods =['POST'])
    def search():
        productName=request.form.get("search-input").strip()
        categoryId=request.form.get("category-id")
        print("###categoryId",categoryId)
        
        search = "{}%".format(productName)
        print('search',search)
        if int(categoryId)>0:
            dbProductList=Product.query.filter(Product.categoryid==categoryId).filter(Product.name.like(search)).all()
        else:
            
            dbProductList=Product.query.filter(Product.name.like(search)).all()
        #Below 3 lines are for displaying cartin navigation menu
        userId=session.get('user-id',None)
        dbUser=User.query.filter(User.id==userId).first()
        cartProductList,cartTotal=computeCartProductListAndTotal() 
        
        #Category list required to populate the search drop down
        dbCategoryList=Category.query.all()
        
        if len(dbProductList)>0:
            pageheading="Your Search Results"
        else:
            pageheading="No Results Found"
        
        print('productName',productName)
        return render_template('category-product.html',Categories=dbCategoryList,heading=pageheading,Products=dbProductList,user=dbUser,CartItemProducts=cartProductList,CartTotal=cartTotal,searchedProductName=productName, searchedCategoryId=categoryId)
    
    @app.route("/advanced-address-search",methods =['GET','POST'])
    def advancedAddressSearch():
        
        return render_template('advanced-address-search.html')
    
    @app.route("/advanced-search",methods =['GET','POST'])
    def advancedSearch():
        if request.method=="GET":
            dbCategories=Category.query.all()
            userId=session.get('user-id',None)
            print("Got userId",userId)
            dbUser=User.query.filter(User.id==userId).first()
            cartProductList,cartTotal=computeCartProductListAndTotal()  
            return render_template('advanced-search.html',Categories=dbCategories,user=dbUser,CartItemProducts=cartProductList,CartTotal=cartTotal)
        else:
            productName=request.form.get("search-input").strip()
            categoryId=request.form.get("category-id")
            minPrice=request.form.get("min-price").strip()
            maxPrice=request.form.get("max-price").strip()
            
            fromDay=request.form.get("from-day")
            fromMonth=request.form.get("from-month")
            fromYear=request.form.get("from-year")
            toDay=request.form.get("to-day")
            toMonth=request.form.get("to-month")
            toYear=request.form.get("to-year")
            
            fromDayExpiry=request.form.get("from-day-expiry")
            fromMonthExpiry=request.form.get("from-month-expiry")
            fromYearExpiry=request.form.get("from-year-expiry")
            toDayExpiry=request.form.get("to-day-expiry")
            toMonthExpiry=request.form.get("to-month-expiry")
            toYearExpiry=request.form.get("to-year-expiry")
            
            
                
            print("###categoryId",categoryId,'minPrice',minPrice,'maxPrice',maxPrice,'fromDay',fromDay,'toDay',toDay)
            
            search = "{}%".format(productName)
            queryFilter=Product.query.filter(Product.name.like(search))
            print(queryFilter)
            if int(categoryId)>0:
       #                    Product.query.filter(Product.categoryid==categoryId).filter(Product.name.like(search),minPriceFilter).all()
                queryFilter=queryFilter.filter(Product.categoryid==categoryId)
           #else: 
                 #CategoryId=0 i.e. Any Category so do not add Product.categoryid
                 # dbProductList=Product.query.filter(Product.name.like(search)).filter(minPriceFilter).all()
                
            if minPrice!="":
                minPriceFilter=Product.discounted_price>=int(minPrice)
                queryFilter=queryFilter.filter(minPriceFilter)
            if maxPrice!="":
                maxPriceFilter=Product.discounted_price<=int(maxPrice)
                queryFilter=queryFilter.filter(maxPriceFilter)
                
            if fromDay!=None and fromMonth !=None and fromYear !=None:
                date_str=fromYear+'-'+fromMonth+'-'+fromDay
                fromDateObj = datetime.strptime(date_str, '%Y-%m-%d').date()
                fromDateFilter=Product.manufacturingdate >= fromDateObj
                queryFilter=queryFilter.filter(fromDateFilter)
                
                
            if toDay!=None and toMonth!=None and toYear!=None:
                date_str=toYear+'-'+toMonth+'-'+toDay
                toDateObj = datetime.strptime(date_str, '%Y-%m-%d').date()
                toDateFilter=Product.manufacturingdate<=toDateObj
                queryFilter=queryFilter.filter(toDateFilter)
                
            if fromDayExpiry!=None and fromMonthExpiry !=None and fromYearExpiry !=None:
                date_str_expiry=fromYearExpiry+'-'+fromMonthExpiry+'-'+fromDayExpiry
                fromDateObjExpiry = datetime.strptime(date_str_expiry, '%Y-%m-%d').date()
                fromDateFilterExpiry=Product.expirydate >= fromDateObjExpiry
                queryFilter=queryFilter.filter(fromDateFilterExpiry)
                
                
            if toDayExpiry!=None and toMonthExpiry!=None and toYearExpiry!=None:
                date_str_expiry=toYearExpiry+'-'+toMonthExpiry+'-'+toDayExpiry
                toDateObjExpiry = datetime.strptime(date_str_expiry, '%Y-%m-%d').date()
                toDateFilterExpiry=Product.expirydate<=toDateObjExpiry
                queryFilter=queryFilter.filter(toDateFilterExpiry)
           
            print(queryFilter)
            dbProductList=queryFilter.all()
            print('#',len(dbProductList))
            #Below 3 lines are for displaying cartin navigation menu
            userId=session.get('user-id',None)
            dbUser=User.query.filter(User.id==userId).first()
            cartProductList,cartTotal=computeCartProductListAndTotal() 
            dbCategoryList=Category.query.all()
            
            if len(dbProductList)>0:
                pageheading="Your Search Results"
            else:
                pageheading="No Results Found"
            return render_template('category-product.html',Categories=dbCategoryList,heading=pageheading,Products=dbProductList,user=dbUser,CartItemProducts=cartProductList,CartTotal=cartTotal)         