from models import db, PurchaseOrder, User, PurchaseOrderItem, Product


class OrderService:
    @staticmethod
    def getOrderInfo(orderId):
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
        # Convert datetime to string

        if dbPurchaseOrder:
            # Assuming the order is (id, username, total, created_at, status)
            order_id, username, total, created_at, status = dbPurchaseOrder

            # Convert datetime to string
            created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S")
            status = status.name
            # Create a new tuple with the converted datetime
            updated_dbPurchaseOrder = {
                "order_id": order_id,
                "username": username,
                "total": total,
                "created_at_str": created_at_str,
                "status": status,
            }

            return updated_dbPurchaseOrder
        else:
            return None

    @staticmethod
    def getOrderProductsInfo(orderId):
        cartProductList = []
        # total = 0

        purchaseOrderItemList = PurchaseOrderItem.query.filter(
            PurchaseOrderItem.order_id == orderId
        ).all()
        print(
            "#######computeCartProductListAndTotalFromOrder",
            orderId,
            purchaseOrderItemList,
        )
        for purchaseOrderItem in purchaseOrderItemList:
            print("About to display purchaseOrderItem ", purchaseOrderItem)
            product = Product.query.filter(
                Product.id == purchaseOrderItem.product_id
            ).first()
            print("#######computeCartProductListAndTotalFromOrder", product)
            if product != None:
                product_data = product.to_dict()
                product_data["quantity"] = purchaseOrderItem.quantity

                print("adding product to display", product_data)
                cartProductList.append(product_data)
                # total = total + (product.quantity * (product.price - (product.price * product.discount/100)))
                # total = total + (product.quantity * (product.discounted_price))
            else:
                print(
                    "Not Found: Order Item Product with id ",
                    purchaseOrderItem.product_id,
                )
        print("returning cartProductList")
        return cartProductList
