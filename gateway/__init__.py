import os
import braintree


# Configuring the environment and API credentials
# Source: https://developer.paypal.com/braintree/docs/start/hello-server/python
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=BT_MERCHANT_ID,
        public_key=BT_PUBLIC_KEY,
        private_key=BT_PRIVATE_KEY
    )
)

# pass client_token to your front-end
def generate_client_token():
    return gateway.client_token.generate()

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)