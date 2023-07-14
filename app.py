from flask import Flask, request, jsonify
import dialogflow
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillment_text = handle_dialogflow_intent(req)
    response = {'fulfillmentText': fulfillment_text}
    return jsonify(response)

def handle_dialogflow_intent(req):
    action = req.get('queryResult').get('action')
    if action == 'convert_currency':
        # Retrieve source currency, target currency, and amount from the request
        source_currency = req.get('queryResult').get('parameters').get('sourceCurrency')
        target_currency = req.get('queryResult').get('parameters').get('targetCurrency')
        amount = req.get('queryResult').get('parameters').get('amount')

        # Perform the currency conversion using an API or a library
        # Here's an example of using the `forex-python` library
        from forex_python.converter import CurrencyRates
        c = CurrencyRates()
        result = c.convert(source_currency, target_currency, amount)

        # Return the result as a string
        response_text = f"The conversion result from {source_currency} to {target_currency} is {result}."
        return response_text
    else:
        return 'Action not implemented'

if __name__ == '__main__':
    app.run(debug=True)
