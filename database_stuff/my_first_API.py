#!flask/bin/python
from flask import Flask, jsonify, abort

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'flowering 12/12',
        'description': u'lights on for 12 hours, and off for 12',
        'logfile' : u'/home/pi/usbdrv/growberry_testlog/grow1_log.txt',
        'pic_dir' : u'/home/pi/usbdrv/growberry_testlog/flowering_pictures/',
        'measurement_interval' : 10,
        'toggle_camera' : True,
        'fan_temp' : 22.5,
        'lights_on_time' : 1100,
        'daylength' : 12,
        'watertimes' : [0600,1100,1600,2100],
        'pumptime' : 4


    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False,
        'watertimes' : ['fake',1100,1600,2100]
    }
]


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'parameters': task[0]})


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)