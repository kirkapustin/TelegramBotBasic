from requests import get
from datetime import datetime
import os
import text

token = os.getenv('TELEGRAM_BOT_TOKEN')


def send_request(method, headers=None, params=None):
    """общий метод отправки запроса к TELEGRAM BOT API"""
    url = 'https://api.telegram.org/bot' + token + '/' + method
    """Telegram supports GET and POST HTTP methods
    In this project we use GET method in all cases"""
    request = get(url, headers=headers, params=params)

    if request.status_code != 200:
        bad_outcome_request_log(request)


def bad_outcome_request_log(data):
    """логируем ошибки при отправке запросов"""
    error = f"{datetime.now()} - " \
            f"code: {data.status_code}; error_text: <{data.text}>"
    with open('bad_outcome_request.log', 'a', encoding='utf-8') as file:
        file.write(error + '\n')


def income_updates_log(data):
    """логируем входящие сообщения"""
    if 'text' in data['message']:
        content = data['message']['text']
    else:
        content = 'не текстовое сообщение'

    new_line = f"{datetime.now()} - " \
               f"chat_id: {data['message']['chat']['id']}; " \
               f"msg_id: {data['message']['message_id']}; " \
               f"user_name: {data['message']['from']['username']}; " \
               f"content: <{content}>"
    with open('income_updates.log', 'a', encoding='utf-8') as file:
        file.write(new_line + '\n')


def send_message(chat_id, msg_text, reply_to_msg_id=None):
    msg_params = {
        'chat_id': chat_id,
        'text': msg_text
    }
    if reply_to_msg_id:
        msg_params['reply_to_message_id'] = reply_to_msg_id

    send_request('sendMessage', params=msg_params)


def process_msg(data):
    """обработка входящего сообщения"""
    msg_text = ''
    not_text_content = False

    chat_id = data['message']['chat']['id']
    # msg_id = data['message']['message_id']

    if 'text' in data['message']:
        msg_text = data['message']['text']
    else:
        not_text_content = True

    if not_text_content:
        send_message(chat_id, text.not_text_reply)

    elif msg_text == '/start':
        send_message(chat_id, text.welcome_msg)

    elif msg_text == '/help':
        send_message(chat_id, text.help_msg)

    elif msg_text[0] == '/':
        send_message(chat_id, text.unknown_command_msg)

    else:
        send_message(chat_id, text.simple_reply)
