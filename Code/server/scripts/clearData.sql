-- database: /Users/nasameer/research/iit/ModernAppDev2/Project/GroceryStore/Code/server/instance/grocerystore.database.sqlite3

-- Use the ▷ button in the top right corner to run the entire file.

delete from purchase_order_item;
delete from purchase_order;
delete from cart_item;
delete from cart;
delete from product where id>24;
delete from category where id>7;
delete from approvals;
delete from payment_details;
delete from manager where id>2;
delete from user where id>4;
