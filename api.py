import os
from flask import Flask, request, jsonify
from cloudflare import Report

app = Flask(__name__)

C = {
    'submitter': {
        'name': os.environ['CFAPI_SUBMITTER'],
        'email': os.environ['CFAPI_SUBMITTER_EMAIL'],
        'company': os.environ['CFAPI_SUBMITTER_COMPANY'],
    },
    'password': os.environ['CFAPI_PASSWORD']
}
@app.route('/report', methods=['POST'])
def report():
    assert len(request.form['url']) > 5
    assert len(request.form['justification']) > 5
    if request.form.get('password') != C['password']:
        return ':('
    R = Report(request.form['url'], C['submitter'], request.form['justification'])
    r = R.report()
    print('steamphishingreporting', request.form['url'])
    print(r)
    print(r.text)

    return jsonify(r.json())



def main():
    app.run(host='0.0.0.0', port=int(os.getenv('CFAPI_PORT', '80')))
if __name__ == '__main__':
    main()
