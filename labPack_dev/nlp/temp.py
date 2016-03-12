__author__ = 'rcj1492'
__created__ = '2015.11'

'''
pip install twilio
pip install textblob
pip install scapy

ngrok for pushing localhost to live
OpenFace (facial recognition api)
'''

from flask import Flask, request
from twilio import twiml
from textblob import TextBlob

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
    response = twiml.Response()
    body = request.form['Body']

    blob = TextBlob(body)

    verbs = []
    proper_nouns = []
    for tag in blob.tags:
        if 'V' in tag[1]:
            verbs.append(tag[0])
        elif 'NNP' in tag [1]:
            proper_nouns.append(tag[0])

    if verbs:
        for verb in verbs:
            if 'buy' in verb.lemma:
                response.message("Connecting you to seller...")
            if 'sell' in verb.lemma:
                response.message("Connecting you to buyer...")

    sentiment = blob.sentiment

    if sentiment.subjectivity > 0.25:
        attitude = 'Positive'
    elif sentiment.subjectivity < -0.25:
        attitude = 'Negative'
    else:
        attitude = 'Indifferent'

    app.logger.info('Received: {0}\n\nSentiment: {1}\n\nSent: {2}'.format(body, attitude, response.verbs[0].verbs[0].body))

    return str(response)

if __name__ == '__main__':
    app.debug()
    app.run(host='0.0.0.0', port=5000)

