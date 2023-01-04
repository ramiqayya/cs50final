# CS50 Final Project
## final project
My final project is a website service to sell and buy cars using html, python,flask and sqlite3 for database. I have also used bootstrap and css for styles.

## Login and Register
The first time a user tries to enter the home page, the website will asked him to enter username and password. For making a new username and password, he will need to enter register page from the navbar at the top right. Then he will be asked to register a new unique username and password then confirm the password again.

After the user registers a new username and password he can now be able to sign into the website. The first thing he will see is the hompage "**index page showing all the cars offered by other users for sale**". Each car card should display *a picture for the car, car make, model, technical specifications, name of the seller, year of manufacture, milage, the price of the car*. At the bottom there is a button for sending request for the seller if a user wants to buy the car. 

## Sending a purchase request
You can send a purchase request from *Sending purchase request button* at the bottom of each car card. Once you press the buttonm it will be deactivated and a request will be sent to the seller of the car. The request also will be added in the database until the seller of the car decide to approve or reject his car purchase request. If your request is approved by the seller, a notification will appear at the top of the index page notifying that your request is approved by the seller and which car is approved.

## Adding a new car Ad
You can add a new car advertisement for selling your car by chosing *Sell Car button* at the navbar at the top of the page. Once you click **Sell Car**, you will be transfered to sell car page where you have to enter the *make of the car you wish to sell, the model, year of manufacture, milage, the price* you asking for the car, you also need to upload one *picture* of the car and write down some other *technical specifications* of the car or any other information you wish to add in the text area below.
After you inputted all the information required you can press on Sell Car at the end of the Sell form the car Ad will be posted at the index page with other car Ads.

## Receiving buy requests
When other users send a purchase request for buying one of your cars, a notifications will appear at the navbar under buy requests button, with the number of requests you have. Click that and you will be transfered to a buy requests page, where you can see all requests for buying your car/s. You can click agree or reject on each car request. You can only agree at one request for each car, once you hit agree at car request, all other requests asking to buy the same car will be deleted immediatly.

## Notification for approved request
As soon as your request for buying a car is approved buy the seller a notification will appear in the hompage informing you that the seller has approved on your request.

## Database tables
Below is the list of tables used in the sqlite3 database **projectv2.db**
### users table
This table stores user ID with username and a hash for the password.
### cars table
This table stores each car ID, make, model, year, milage, price, seller user id and technical specification for each car which has been entered by the seller from sell car form.
### images table
This table stores images for each car as a blob. Each image is linked to a car id.
### requests table 
When a buyer sends a request for buying a car, the request button will be deactivated, and a request will be sent to the seller user, this request is going to be saved also in the database under table caller requests. and the request will be saved there until the seller take a decision for approving or rejecting your or other user request for buying the same car. That time it will be deleted from the requests table in the database.
### approved table
When the seller approved for a car buy request it will be saved under table called approved. That table stores the approved request ID, the buyer ID, the car make, the car model, and the name of the seller.
all these informations will be deleted once the buyer see the message and dismiss it.





