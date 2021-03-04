from flask import Flask, request
from functions import income_updates_log, process_msg
# from flask import jsonify
# import json

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        income_msg = request.get_json()

        income_updates_log(income_msg)
        process_msg(income_msg)

        # with open('income_request.json', 'a', encoding='utf-8') as f:
        #     json.dump(income_msg, f, indent=2, ensure_ascii=False)
            # return jsonify(income_msg)

    return '<h1>sorry, this url is used for receiving telegram bot webhooks</h1>'


if __name__ == '__main__':
    app.run()
