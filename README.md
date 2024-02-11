# Amazon-Price-Tracker
Input your phone number and the links to items on your Amazon wishlist, and you will get a text alert if a price drops over 10%!

Enter_Links.py - When you want to add links to track, run this program. Many different users can enter items and it will store their phone numbers so they can receive a text when necessary.

Price_Tracker.py - Compares the current prices of all the items entered in the tracker with the prices when the alert was set up, and if they dropped over 10%, a text will be sent to the users phone number through Twilio.

Check_Every_Hour.py - Runs the Price_Tracker every hour, so when the price is updated the user can be alerted.

master_data.csv - this file will be created when Enter_Links.py is ran and it will store the users phone number, the Amazon product name and link, and the price of the product. This doscument will be updated any time a user adds an item.
