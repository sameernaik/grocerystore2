from flask import (
    Flask,
    flash,
    render_template,
    request,
    session,
    redirect,
    url_for,
    send_from_directory,
)
from models import *
import datetime as datetime
from sqlalchemy import func
from histogramGenerator import plotHistogram
from viewsDashboard import getEmployeeName

from config import GRAPH_FOLDER


def defineSummaryRoutes(app):
    def Convert(tup, di):
        for a, b in tup:
            print("Value of a", a, "Value of b", b)
            di[a] = b
        return di

    def generateTopNProductsGraph(topTenProductQuantityImage, numberOfProducts):
        today = datetime.date.today() + timedelta(days=1)
        week_ago = today - datetime.timedelta(days=7)
        print("Computing graph from today:", today, "to weekago:", week_ago)
        topTenProducts = (
            db.session.query(Product.name, func.sum(PurchaseOrderItem.quantity))
            .filter(Product.id == PurchaseOrderItem.product_id)
            .filter(PurchaseOrderItem.order_id == PurchaseOrder.id)
            .filter(PurchaseOrder.status == PurchaseOrderStatus.SUCCESS)
            # .filter(PurchaseOrder.created_at.between(week_ago, today))
            .group_by(PurchaseOrderItem.product_id)
            .order_by(func.sum(PurchaseOrderItem.quantity).desc())
            .limit(numberOfProducts)
            .all()
        )
        productQuantityDict = {}
        Convert(topTenProducts, productQuantityDict)
        plotHistogram(
            productQuantityDict,
            topTenProductQuantityImage,
            "Top 10 Selling Products",
            "Products",
            "Units",
        )
        return topTenProducts

    def generateTopNCategorywiseProductsGraph(
        topTenProductQuantityImage, numberOfProducts
    ):
        today = datetime.date.today() + timedelta(days=1)
        week_ago = today - datetime.timedelta(days=7)
        print("Computing graph from today:", today, "to weekago:", week_ago)

        topTenProducts = (
            db.session.query(Category.name, func.sum(PurchaseOrderItem.quantity))
            .filter(Category.id == Product.categoryid)
            .filter(Product.id == PurchaseOrderItem.product_id)
            .filter(PurchaseOrderItem.order_id == PurchaseOrder.id)
            .filter(PurchaseOrder.status == PurchaseOrderStatus.SUCCESS)
            .filter(PurchaseOrder.created_at.between(week_ago, today))
            .group_by(Category.id)
            .order_by(func.sum(PurchaseOrderItem.quantity).desc())
            .limit(numberOfProducts)
            .all()
        )
        productQuantityDict = {}
        Convert(topTenProducts, productQuantityDict)

        plotHistogram(
            productQuantityDict,
            topTenProductQuantityImage,
            "Top 10 Selling Categories",
            "Categories",
            "Units",
        )
        return topTenProducts

    def generateDayOfWeekVsOrdersGraph(topTenProductQuantityImage):
        weekQuantityList = (
            db.session.query(
                func.strftime("%w", PurchaseOrder.created_at),
                func.count(PurchaseOrder.id),
            )
            .filter(PurchaseOrder.status == PurchaseOrderStatus.SUCCESS)
            .filter(PurchaseOrder.created_at.between("2023-07-29", "2023-12-31"))
            .group_by(func.strftime("%w", PurchaseOrder.created_at))
            .order_by(func.strftime("%w", PurchaseOrder.created_at))
            .limit(7)
            .all()
        )
        weekQuantityIntDict = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
        Convert(weekQuantityList, weekQuantityIntDict)
        weekQuantityStringDict = {}
        weekQuantityStringDict["Sunday"] = weekQuantityIntDict["0"]
        weekQuantityStringDict["Monday"] = weekQuantityIntDict["1"]
        weekQuantityStringDict["Tuesday"] = weekQuantityIntDict["2"]
        weekQuantityStringDict["Wednesday"] = weekQuantityIntDict["3"]
        weekQuantityStringDict["Thursday"] = weekQuantityIntDict["4"]
        weekQuantityStringDict["Friday"] = weekQuantityIntDict["5"]
        weekQuantityStringDict["Saturday"] = weekQuantityIntDict["6"]

        plotHistogram(
            weekQuantityStringDict,
            topTenProductQuantityImage,
            "Weekday wise Orders",
            "Day of Week",
            "# of Orders",
        )
        return weekQuantityStringDict

    def generateModeOfPaymentTrendGraph(modeOfPaymentTrendImage):
        paymentModeTrendList = (
            db.session.query(PaymentMode.mode, func.count(PaymentDetails.payment_mode))
            .filter(PaymentMode.id == PaymentDetails.payment_mode)
            .group_by(PaymentDetails.payment_mode)
            .all()
        )
        paymentModeTrendDict = {}
        Convert(paymentModeTrendList, paymentModeTrendDict)
        plotHistogram(
            paymentModeTrendDict,
            modeOfPaymentTrendImage,
            "Payment Mode Trend",
            "Payment Mode",
            "# of Orders",
        )
        print("paymentModeTrend", paymentModeTrendList)

    app.generateTopNProductsGraph = generateTopNProductsGraph
    app.generateTopNCategorywiseProductsGraph = generateTopNCategorywiseProductsGraph
    app.generateDayOfWeekVsOrdersGraph = generateDayOfWeekVsOrdersGraph
    app.generateModeOfPaymentTrendGraph = generateModeOfPaymentTrendGraph

    @app.route("/summary")
    def summary_page():
        # db.session.query(func.count(Table.column1),Table.column1, Table.column2).group_by(Table.column1, Table.column2).all()
        # SELECT sum(quantity),count(*),product_id FROM "purchase_order_item" group by product_id;
        # output=db.session.query(PurchaseOrderItem.product_id,func.sum(PurchaseOrderItem.quantity)).filter(PurchaseOrderItem.order_id==PurchaseOrder.id).filter(PurchaseOrder.status==1).filter(PurchaseOrder.created_at.between('2023-07-30','2023-07-31')).group_by(PurchaseOrderItem.product_id).all()
        # output=db.session.query(Product.name,func.sum(PurchaseOrderItem.quantity)).filter(Product.id==PurchaseOrderItem.product_id).filter(PurchaseOrderItem.order_id==PurchaseOrder.id).filter(PurchaseOrder.status==1).filter(PurchaseOrder.created_at.between('2023-07-30','2023-07-31')).group_by(PurchaseOrderItem.product_id).all()
        topTenProductQuantityImage = "top_10_product_quantity.png"
        topTenProducts = generateTopNProductsGraph(topTenProductQuantityImage, 10)

        topNCategorywiseProductImage = "top_10_categorywise_product.png"
        topNCategorywiseProducts = generateTopNCategorywiseProductsGraph(
            topNCategorywiseProductImage, 10
        )

        dayOfWeekWiseOrdersImage = "dayOfWeekWiseOrders.png"
        dayOfWeekWiseOrders = generateDayOfWeekVsOrdersGraph(dayOfWeekWiseOrdersImage)
        print("### Day of Week Wise Orders ", dayOfWeekWiseOrders)

        paymentModeTrendImage = "paymentModeTrend.png"
        generateModeOfPaymentTrendGraph(paymentModeTrendImage)
        return render_template(
            "summary.html",
            employee_name=getEmployeeName(),
            TopTenProduct=topTenProducts,
            topTenProductQuantityImageName=topTenProductQuantityImage,
            TopNCategorywiseProducts=topNCategorywiseProducts,
            topNCategorywiseProductImageName=topNCategorywiseProductImage,
            dayOfWeekWiseOrdersImageName=dayOfWeekWiseOrdersImage,
            paymentModeTrendImageName=paymentModeTrendImage,
            pageTitle="Summary",
        )

    @app.route("/graph/<path:filename>")
    def display_graph_file(filename):
        print("display_graph_file for filename:", filename)
        return send_from_directory(GRAPH_FOLDER, filename)
