import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    username = 'root',
    password = '123456',
    database = 'ecommerce'
)

cur = db.cursor()

query = """select distinct customer_city from customers"""
cur.execute(query)

data = cur.fetchall()
# print(data)

query2 = """select upper(products.product_category), sum(payments.payment_value) from products
join order_items 
on order_items.product_id = products.product_id
join payments 
on payments.order_id = order_items.order_id
group by 
products.product_category """
cur.execute(query2)

data2 = cur.fetchall()
# print(data2)

df = pd.DataFrame(data2, columns= ['Category', 'Sales'])
# print(df)
top_values = df.nlargest(5, 'Sales')
# print(top_values)

query3 = """ select (sum(case when payment_installments>=1 then 1 else 0 end))/count(*)*100 from payments """
cur.execute(query3)

data3 = cur.fetchall()
# print(data3[0][0])

query4 = """ select customer_state, count(customer_id) from customers group by customer_state  """
cur.execute(query4)

data4 = cur.fetchall()
# print(data4)

df2 = pd.DataFrame(data4, columns=['State','No. of Customer'])
df2= df2.sort_values(by='No. of Customer', ascending= False)
# print(df2)

# plt.bar(df2['State'],df2['No. of Customer'])
# plt.xticks(rotation = 90)
# # plt.show()

# Interidiate Queries

query5 = """ select month(order_purchase_timestamp), count(order_id) from orders
where year(order_purchase_timestamp) = 2018 group by month(order_purchase_timestamp) """
cur.execute(query5)

data5 = cur.fetchall()
df3 = pd.DataFrame(data5, columns= [ 'Month','No. of Orders'])
df3 = df3.sort_values(by='Month', ascending= True)
# print(data5)
# print(df3)

# plt.bar(df3['Month'],df3['No. of Orders'])
# plt.title("Count of Order per Month")
# plt.xlabel('Month')
# plt.ylabel('No. of Orders')
# # plt.show()
 
query6 = """ with count_per_order as 
(select orders.order_id, orders.customer_id, count(order_items.order_item_id) as oc from orders
join order_items on orders.order_id = order_items.order_id group by orders.order_id, orders.customer_id)
select customers.customer_city, round(avg(oc),2) as Average_Orders from customers 
join count_per_order on customers.customer_id = count_per_order.customer_id
group by customers.customer_city order by Average_Orders desc
;  """
cur.execute(query6)
data6 = cur.fetchall()
# print(data6)

df4= pd.DataFrame(data6, columns=['City','Average Orders']).head(10)
# print(df4)

# plt.bar(df4['City'], df4['Average Orders'])
# plt.title("Top Cities with Max Average Orders")
# plt.xlabel('City')
# plt.ylabel('Avg of Orders')
# plt.xticks(rotation = 90)
# plt.show()

query7 =  """select upper(products.product_category), 
round((sum(payments.payment_value)/(select sum(payment_value) from payments)*100),2) as pecentage 
from products
join order_items 
on order_items.product_id = products.product_id
join payments 
on payments.order_id = order_items.order_id
group by 
products.product_category
;"""

cur.execute(query7)
data7 = cur.fetchall()
# print(data7)

df5= pd.DataFrame(data7, columns=['Category','Average Percentage']).head(10)
# print(df5)

sizes = df5['Average Percentage']
labels = df5['Category']

plt.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True)
plt.show()

# print(df5['Average Percentage'])
