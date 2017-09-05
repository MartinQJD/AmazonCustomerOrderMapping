# AmazonCustomerOrderMapping
------------------------------------------------------------------
Build mappings beween customer-id and order-id for amazon orders
------------------------------------------------------------------

On the amazon marketplace, sometimes, your customer left a review on your listing, and you hope know which order that your customer placed, and then send message by the order to your customer to actively help resolve customer's problem. However, you will find that seems impossible, because you cannot directly relate reviews to orders at all. 

But today, I'll tell you an approach to do this.

Firstly, you need to get the customer Id of the review. To do this, you need to know how to spy the source code of the web page,because the customer id hides in the source code of the web page. In fact, if you know how to use the built-in debug plugin of web brower,it's so easy.<br/>
I'll illustrate the approach with Chrome browser as below:
1) Move your mouse cursor over the reviewer's name.<br/>
2) Right click the mouse, and you will see a popup menu.<br/>
3) Click the "Inspect" item.<br/>
4) Browser will open a new window at the right side. And in the selected text block, you can see a string like 'href="/gp/pdp/profile/XXXXXXXX/',"XXXXXXX" is just the customer id. Of course, here is an example, different customer name has different customer id.<br/>

Next, you hope know which order(s) the customer id placed. If you know that,you can send message to your customer by the order.<br/><br/> 
It is the problem that the project will resolve.But before introduce the project,I need to tell you a backgound. <br/><br/>
When you search orders in your seller central, the search result is a list of order infos. Seemingly, the order info include order id and customer name, but not customer id. In fact, customer id also has been included, but hides in the source code of the web page. If you know how to spy the source code, you will find out it.<br/><br/>
It's exciting. But even if you know how to find out the customer id for an order, it still is the nightmare when you need to find out all of cutomer id for all orders, maybe 10,100,1000 or more orders.<br/><br/>
um......Don't worry,this project is subject to wake you up from the nightmare.

<b>[Debriefing]</b><br/>
This project is a program coded with python.<br/>
This project uses selenium to load and parse web page.<br/>
The program needs to run in command mode.<br/>
The program is used to download customer orders, and save the mappings between customer id and order id into files. In future, you can seek them when you need.

<b>[Prerequisite]</b><br/>
To let the program work you need to:
1) Install python enviroment and selenium on your computer managing your seller central.
2) Modify the script to specify the SKU and marketplace that you want to download.

