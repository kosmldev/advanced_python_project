from src.game.command_center import CommandCenter
from flask import Flask, request, render_template

command_center = CommandCenter()

app = Flask(__name__, static_folder='static', template_folder="src/frontend")


@app.route('/')
def hello_world():
    return render_template('template.html')


@app.route('/game_api', methods=['POST'])
def api():
    input_value = request.data.decode('utf-8')

    if request.method == 'POST':
        output = command_center.parse_log(input_value)
        return output
    else:
        return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
