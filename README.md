# CS50 Final Project
## final project
My final project is a website service to sell and buy cars using html, python,flask and sqlite3 for database. I have also used bootstrap and css for styles.

## Login and Register
The first time you try to enter the home page, the website will asked the user to enter username and password. To get a new username and password, you will need to enter register page from the navbar at the top right you will be asked to register a new username and enter the password twice correctly.

After you register a new username and password you can now be able to sign into the website. The first thing you will see is the hompage "index page showing all the cars offered by other users for sale". Each car card should display a picture for the car, car make, model, technical specifications, name of the seller, year of manufacture, milage, the price of the car and at the bottom there is a button for sending request for the seller if you wish to buy the car. 

## Sending a purchase request
You can send a purchase request from (Sending purchase request) button at the bottom of each car card. Once you press the button the button will be deactivated and a request will be send to the seller of the car. the request also will be added in the database until the seller of the car decide to approve or reject his car purchase request. If your request is approved buy the seller a notification will appear at the top of the index page notifying you that your request is approved by the seller and which car is approved.

## Adding a new car Ad
You can add a new car Advirtisement for selling your car by chosing (Sell Car) button at the navbar at the top of the page. Once you click that, you will be transfered to sell car page where you have to enter the make of the car you wish to sell, the model, year of manufacture, milage, the price you asking for the car, you also need to upload one picture of the car and write down some other technical specifications of the car or any other information you wish to add in the text area below.
After you inputted all the information required you can press on Sell Car at the end of the Sell form the car Ad will be posted at the index page with other car Ads.

## Receiving buy requests
When other users send a purchase request for buying your car you will see notifications at the navbar under buy requests. Click that and you will be transfered to a buy requests page where you can see all request for your Ads. You can choose then choose agree or disagree on each car request. Notice that you can only agree at one car buyer for each car once you hit agree at car request, all other requests asking to buy the same car will be deleted immediatly.





