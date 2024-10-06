from flask import (
    flash,
    render_template,
    request,
    session,
    redirect,
    url_for,
    send_from_directory,
)
from models import *
from views import computeCartProductListAndTotalFromOrder
from datetime import datetime
import os
from config import REPORT_FOLDER


def getEmployeeName():
    employee_name = session.get("employee-name", None)
    return employee_name


def defineDashboardRoutes(app):
    @app.route("/category", methods=["GET"])
    def category_page():
        _method = request.form.get("_method")
        print("Hidden value is ", _method)
        if request.method == "GET":
            dbCategoryList = Category.query.filter(
                Category.owner == session["manager-id"]
            ).all()
            print("categories list", len(dbCategoryList))
            return render_template(
                "category.html",
                Categories=dbCategoryList,
                pageTitle="Category",
                employee_name=getEmployeeName(),
            )

    @app.route("/category/add", methods=["GET", "POST"])
    def categoryModalAdd():
        if request.method == "GET":
            return render_template(
                "category-modal-add.html",
                modal=True,
                pageTitle="Add Category",
                employee_name=getEmployeeName(),
            )
        elif request.method == "POST":
            newCategoryName = request.form.get("category-name")
            print(newCategoryName)
            dbCategory = Category.query.filter(Category.name == newCategoryName).all()
            print("Database Category", dbCategory)
            if len(dbCategory) > 0:
                print(
                    newCategoryName, " category already exits.Please use different name"
                )
                flash(
                    'Category "'
                    + newCategoryName
                    + '" already exits.Please use different name'
                )
                return redirect("/category/add")
            else:
                category = Category(name=newCategoryName, owner=session["manager-id"])
                db.session.add(category)
                db.session.commit()
                print(newCategoryName, " category created successfully")

                return redirect("/category")

    @app.route("/category/<id>/edit", methods=["GET", "POST"])
    def categoryModalEdit(id):
        _method = request.form.get("_method")
        print(
            "Category Edit Page:Request method",
            request.method,
            "Hidden value is ",
            _method,
            "Category id to be modified",
            id,
        )
        dbCategory = Category.query.filter(
            Category.id == id, Category.owner == session["manager-id"]
        ).first()
        print("db category", dbCategory)
        if request.method == "GET":
            return render_template(
                "category-modal-edit.html",
                id=id,
                Category=dbCategory,
                modal=True,
                pageTitle="Edit Category",
                employee_name=getEmployeeName(),
            )
        elif request.method == "POST" and _method == "PUT":
            # we have used POST method to tunnel PUT method because HTML
            # only supports GET and POST in form
            # More info : https://stackoverflow.com/questions/8054165/using-put-method-in-html-form
            if dbCategory != None:
                category = dbCategory
                category.name = request.form.get("changed-category-name")
                db.session.add(category)
                db.session.commit()
                # Category edit done. Let's display the category page with edited category now.
                return redirect("/category")
        else:
            return render_template(
                "category-modal-edit.html",
                id=id,
                Category=dbCategory,
                modal=True,
                pageTitle="Edit Category",
                employee_name=getEmployeeName(),
            )

    @app.route("/category/<id>/delete", methods=["GET", "POST"])
    def categoryModalDelete(id):
        if request.method == "GET":
            dbCategory = Category.query.filter(
                Category.id == id, Category.owner == session["manager-id"]
            ).first()
            return render_template(
                "category-modal-delete.html",
                Category=dbCategory,
                modal=True,
                pageTitle="Delete Category",
            )
        elif request.method == "POST":
            Product.query.filter(Product.categoryid == id).delete()
            Category.query.filter(
                Category.id == id, Category.owner == session["manager-id"]
            ).delete()
            db.session.commit()
            return redirect("/category")

    @app.route("/product", methods=["GET"])
    def product_page():
        if request.method == "GET":
            dbCategoryList = Category.query.filter(
                Category.owner == session["manager-id"]
            ).all()
            dbCategoryIdList = []
            dbCategoriesDict = {}
            for category in dbCategoryList:
                dbCategoryIdList.append(category.id)
                dbCategoriesDict[category.id] = category.name
            print("dbCategoryIdList ", dbCategoryIdList)
            dbProductList = Product.query.filter(
                Product.categoryid.in_(dbCategoryIdList)
            ).all()
            # dbProductList=Product.query.all()
            print("###products list", len(dbProductList))
            return render_template(
                "product.html",
                Products=dbProductList,
                Categories=dbCategoriesDict,
                pageTitle="Product",
                employee_name=getEmployeeName(),
            )

    @app.route("/product/category/<category_id>", methods=["GET"])
    def categorywiseProductManagementPage(category_id):
        if request.method == "GET":
            category = (
                Category.query.filter(Category.owner == session["manager-id"])
                .filter(Category.id == category_id)
                .first()
            )
            dbCategoriesDict = {}
            dbCategoriesDict[category.id] = category.name
            # print("dbCategoryIdList ",dbCategoryIdList)
            dbProductList = Product.query.filter(
                Product.categoryid == category_id
            ).all()
            # dbProductList=Product.query.all()
            print("###products list", len(dbProductList))
            print("###return path", "/product/category/" + category_id)
            return render_template(
                "product.html",
                Products=dbProductList,
                Categories=dbCategoriesDict,
                pageTitle="Product",
                employee_name=getEmployeeName(),
            )

    @app.route("/product/add", methods=["GET", "POST"])
    def productModalAdd():
        if request.method == "GET":
            dbCategoryList = Category.query.filter(
                Category.owner == session["manager-id"]
            ).all()
            dbCategoriesDict = {}
            for category in dbCategoryList:
                dbCategoriesDict[category.id] = category.name
            print("Add product modal", dbCategoryList)

            return render_template(
                "product-modal-add.html",
                modal=True,
                pageTitle="Add Product",
                Categories=dbCategoriesDict,
                employee_name=getEmployeeName(),
            )
        else:
            newProductName = request.form.get("product-name")
            print(newProductName)
            dbProduct = Product.query.filter(Product.name == newProductName).first()
            print("Database Product", dbProduct)
            if dbProduct != None:
                print(
                    newProductName, " product already exits.Please use different name"
                )
                flash(
                    'Product "'
                    + newProductName
                    + '" already exits.Please use different name'
                )
                return redirect("/product/add")
            else:
                product = Product(
                    name=newProductName,
                    description=request.form.get("product-description"),
                    imagename=request.form.get("product-imagename"),
                    stock_quantity=request.form.get("product-stock-quantity"),
                    stock_unit=request.form.get("product-stock-unit"),
                    sell_quantity=request.form.get("product-sell-quantity"),
                    sell_unit=request.form.get("product-sell-unit"),
                    price=request.form.get("product-price"),
                    discount=request.form.get("product-discount"),
                    categoryid=request.form.get("product-categoryid"),
                    available=request.form.get("product-available"),
                )
                manufacturingDateStr = request.form.get(
                    "product-manufacturingdate"
                ).strip()
                expiryDateStr = request.form.get("product-expirydate").strip()
                if manufacturingDateStr != "":
                    manufacturingDateObj = datetime.strptime(
                        manufacturingDateStr, "%Y-%m-%d"
                    )
                    product.manufacturingdate = manufacturingDateObj
                if expiryDateStr != "":
                    expiryDateObj = datetime.strptime(expiryDateStr, "%Y-%m-%d")
                    product.expirydate = expiryDateObj

                print(product, " product is being added to database")
                db.session.add(product)
                db.session.commit()
                print(newProductName, " product created successfully")
                return redirect("/product")

    @app.route("/product/<id>/edit", methods=["GET", "POST"])
    def productModalEdit(id):
        print("product edit page method ", request.method)
        _method = request.form.get("_method")
        print("Hidden value is ", _method)
        print("Product id to be modified", id)

        dbProduct = Product.query.filter(Product.id == id).first()
        dbCategory = Category.query.filter(
            Category.id == dbProduct.categoryid, Category.owner == session["manager-id"]
        ).first()
        if dbCategory != None:
            print("db product", dbProduct)
            if request.method == "GET":
                categories = Category.query.filter(
                    Category.owner == session["manager-id"]
                ).all()
                return render_template(
                    "product-modal-edit.html",
                    id=id,
                    Product=dbProduct,
                    Categories=categories,
                    modal=True,
                    pageTitle="Edit Product",
                    employee_name=getEmployeeName(),
                )
            elif request.method == "POST" and _method == "PUT":
                if dbProduct != None:
                    product = dbProduct
                    product.name = request.form.get("product-name")
                    product.description = request.form.get("product-description")
                    product.imagename = request.form.get("product-imagename")
                    product.stock_quantity = request.form.get("product-stock-quantity")
                    # print('request form stock quantity ',request.form.get("product-stock-quantity"))
                    product.stock_unit = request.form.get("product-stock-unit")
                    product.sell_quantity = request.form.get("product-sell-quantity")
                    product.sell_unit = request.form.get("product-sell-unit")
                    product.price = request.form.get("product-price")
                    product.discount = request.form.get("product-discount")
                    product.categoryid = request.form.get("product-categoryid")

                    manufacturingDateStr = request.form.get(
                        "product-manufacturingdate"
                    ).strip()
                    if manufacturingDateStr != "None":
                        manufacturingDateObj = datetime.strptime(
                            manufacturingDateStr, "%Y-%m-%d"
                        )
                        product.manufacturingdate = manufacturingDateObj

                    expiryDateStr = request.form.get("product-expirydate").strip()
                    if expiryDateStr != "None":
                        expiryDateObj = datetime.strptime(expiryDateStr, "%Y-%m-%d")
                        product.expirydate = expiryDateObj

                    product.available = request.form.get("product-available")
                    print("Adding to DB for update", product)
                    db.session.add(product)
                    db.session.commit()
                    # Product edit done. Let's display the product page with edited product now.
                    return redirect("/product")
            else:
                return render_template(
                    "product-modal-edit.html",
                    id=id,
                    Product=dbProduct,
                    pageTitle="Edit Product",
                    employee_name=getEmployeeName(),
                )
        else:
            print(
                "Manager with id ",
                session["manager-id"],
                " does not own the product with id ",
                id,
                " and hence cannot view or edit the product",
            )

    @app.route("/product/<id>/delete", methods=["GET", "POST"])
    def productModalDelete(id):
        if request.method == "GET":
            dbProduct = (
                Product.query.filter(Product.id == id)
                .filter(Category.id == Product.categoryid)
                .filter(Category.owner == session["manager-id"])
                .first()
            )
            return render_template(
                "product-modal-delete.html",
                Product=dbProduct,
                modal=True,
                pageTitle="Delete Product",
                employee_name=getEmployeeName(),
            )
        elif request.method == "POST":
            Product.query.filter(Product.id == id).delete()
            db.session.commit()
            return redirect("/product")

    @app.route("/order/<orderId>", methods=["GET"])
    def order_details_page(orderId):
        if request.method == "GET":
            dbPurchaseOrder = (
                db.session.query(
                    PurchaseOrder.id,
                    User.username,
                    PurchaseOrder.total,
                    PurchaseOrder.created_at,
                    PurchaseOrder.status,
                )
                .filter(PurchaseOrder.id == orderId)
                .filter(User.id == PurchaseOrder.user_id)
                .first()
            )
            productList, cartTotal = computeCartProductListAndTotalFromOrder(orderId)
            return render_template(
                "order-detail-modal.html",
                Order=dbPurchaseOrder,
                Products=productList,
                CartTotal=cartTotal,
                pageTitle="Order Details",
                modal=True,
                employee_name=getEmployeeName(),
            )

    @app.route("/order", methods=["GET"])
    def order_page():
        if request.method == "GET":
            dbPurchaseOrderList = (
                db.session.query(
                    PurchaseOrder.id,
                    User.username,
                    PurchaseOrder.total,
                    PurchaseOrder.created_at,
                    PurchaseOrder.status,
                )
                .filter(User.id == PurchaseOrder.user_id)
                .all()
            )
            return render_template(
                "order.html",
                Orders=dbPurchaseOrderList,
                pageTitle="Orders",
                employee_name=getEmployeeName(),
            )

    @app.route("/order/download", methods=["GET"])
    def order_download():
        print("app.root.path", app.root_path)
        full_path = os.path.join(app.root_path, REPORT_FOLDER)
        print("full path", full_path)
        dbPurchaseOrderList = (
            db.session.query(
                PurchaseOrder.id,
                User.username,
                PurchaseOrder.total,
                PurchaseOrder.created_at,
                PurchaseOrder.status,
            )
            .filter(User.id == PurchaseOrder.user_id)
            .all()
        )
        reportGenerationDateTimeFile = datetime.now().strftime("%d-%m-%Y-%H_%M_%S")
        reportDate = datetime.now().strftime("%d-%m-%Y")
        reportTime = datetime.now().strftime("%H:%M:%S")
        filecontent = render_template(
            "order-report.html",
            Orders=dbPurchaseOrderList,
            pageTitle="Order Report",
            displayReportDate=reportDate,
            displayReportTime=reportTime,
            employee_name=getEmployeeName(),
        )
        filename = "order-report-" + reportGenerationDateTimeFile + ".html"
        file1 = open(os.path.join(full_path, filename), "w")
        file1.write(filecontent)
        file1.close()
        return send_from_directory(full_path, filename, as_attachment=True)

    @app.route("/messages")
    def message_page():
        if request.method == "GET":
            dbMessageList = (
                db.session.query(Message.created_at, Message.message, Message.severity)
                .filter(Message.owner == session["manager-id"])
                .all()
            )
            return render_template(
                "messages.html",
                pageTitle="Messages",
                Messages=dbMessageList,
                employee_name=getEmployeeName(),
            )
