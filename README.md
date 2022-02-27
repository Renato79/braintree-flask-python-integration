# PayPal BrainTree Integration with Flask/Python

Live demo on Heroku: [Click here](https://braintree-flask-integration.herokuapp.com/).

Official documentation: [Click here](https://developer.paypal.com/braintree/docs/start/overview).

What this project includes:

- Sandbox and Braintree Python SDK

- Enter a new transaction (Process a sandbox payment)

- Show the transaction details

- List all the transactions

- Void a transaction

- Refund a transaction

- Void a refund


You will need your own Merchant ID, Public Key, Private Key to interact with your Sandbox BrainTree account. Go to [Sandbox](https://sandbox.braintreegateway.com/), click on Settings at the top right (the gear icon), click on API, your account's details are right there. Replace these details in gateway/__ __init____.py and .env. 


Install the requirements:
```
pip3 install -r requirements.txt
```

In my case, I run a virtual environment that I created with the project, the venv is included here in Github with the code. You can choose either to install the requirements and run the server or use the venv included:
```
source "/MY_FlaskProjectFolder_PATH/"
```
Run Flask Server:
```
flask run
```