from flask import Flask, redirect, url_for, render_template, request, flash

import braintree
from gateway import *

import datetime
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('tr_new'))


# Create a new Transaction
@app.route('/tr_new', methods=['GET'])
def tr_new():
    client_token = generate_client_token()
    return render_template('tr_new.html', client_token=client_token)


# The form in tr_new has action="checkouts"
@app.route('/checkouts', methods=['POST'])
def create_checkout():
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        return redirect(url_for('tr_show',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: 
            flash(f'Error: {x.code}: {x.message}')
        return redirect(url_for('tr_new'))


# List all the transactions
@app.route('/tr_list')
def tr_list():
    # All my transactions will be with VISA to semplify the project
    collection = gateway.transaction.search(braintree.TransactionSearch.credit_card_card_type == braintree.CreditCard.CardType.Visa)
    return render_template('tr_list.html', collection=collection)


# Show details of a single transaction
@app.route('/tr_show/<transaction_id>', methods=['GET'])
def tr_show(transaction_id):
    transaction = find_transaction(transaction_id)
    return render_template('tr_show.html', transaction=transaction)


# Refund a transaction
@app.route('/tr_refund/<transaction_id>', methods=['GET'])
def tr_refund(transaction_id):
    # retrieving the transaction
    transaction = gateway.transaction.find(transaction_id)
    
    # if the transaction is on status settled or settling we refund
    if transaction.status == 'settled' or transaction.status == 'settling':
        result = gateway.transaction.refund(transaction_id)
        # Let's keep errors in the Terminal for this project example
        if result.is_success:
            print("Transaction successfully refunded.")
        else:
            print(f"Could not refund, error: {result.errors.deep_errors}")        
    return redirect(url_for('tr_show', transaction_id=transaction_id))


# Void a transaction
@app.route('/tr_void/<transaction_id>', methods=['GET'])
def tr_void(transaction_id):
    # retrieving the transaction
    transaction = gateway.transaction.find(transaction_id)
    
    # if the transaction is on status authorized, submitted for settlement, 
    # or - for PayPal - settlement pending we void the transaction
    if transaction.status == 'authorized' or transaction.status == 'submitted_for_settlement' or transaction.status == ' settlement_pending':
        result = gateway.transaction.void(transaction_id)
        # Let's keep errors in the Terminal for this project example
        if result.is_success:
            print("Transaction successfully voided.")
        else:
            print(f"Could not void the transaction, error: {result.errors.deep_errors}")
    return redirect(url_for('tr_show', transaction_id=transaction_id))





if __name__ =="__main__":
    app.run(host=os.getenv("IP"),
       port=int(os.getenv("PORT")),
       debug=True)