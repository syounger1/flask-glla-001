from datetime import datetime
from flask import render_template
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

# chenjun
from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
# chenjun




# chenjun
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        token = 'your_token'  # 替换为自己在公众号设置中的Token
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        list = [token, timestamp, nonce]
        list.sort()
        s = ''.join(list).encode('utf-8')
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
        else:
            return 'Invalid Signature'
    else:
        xml_data = request.stream.read()
        xml_tree = ET.fromstring(xml_data)
        msg_type = xml_tree.find('MsgType').text
        if msg_type == 'text':
            content = xml_tree.find('Content').text
            response_content = chat_with_gpt(content)
            response = generate_text_response(xml_tree, response_content)
            return make_response(response)
        else:
            response_content = '暂不支持该类型消息的回复。'
            response = generate_text_response(xml_tree, response_content)
            return make_response(response)

def chat_with_gpt(text):
   prompt = f'User: {text}\nAI:'
   model_id = 'gpt-3.5-turbo'  # 替换为自己的模型ID
   api_key = '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'  # 替换为自己的API密钥
   headers = {'Authorization': f'Bearer {api_key}'}
   data = {
        'model': model_id,
        'prompt': prompt,
        'temperature': 0.5,
        'max_tokens': 1024,
        'stop': '\n'
    }
   response = request.post('https://api.openai.com/v1/completions', headers=headers, json=data)
   if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
   else:
        return '对话出现错误，请稍后再试。'

def generate_text_response(xml_tree, content):
    # 根据对话结果生成XML格式的回复消息
    pass
# chenjun 1

