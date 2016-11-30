events = []
steps = {}
users = {}

required_points = 24

def register_user_data(user_id, start_time):
    global users
    users[user_id] = {'user_id': user_id, 'start_time':start_time, 'end_time':-1, 'points':0}

def register_event_data(user_id, action, step_id, time):
    global events
    events += [{'user_id':user_id, 'action':action, 'step_id':step_id, 'time':time}]

def register_step_data(step_id, step_cost):
    global steps
    steps[step_id] = {'step_cost': step_cost}

def process_event(event):
    global users
    global required_points
    user_id = event['user_id']
    action = event['action']
    step_id = event['step_id']
    time = event['time']
    if not user_id in users:
        register_user_data(event['user_id'], event['time'])
    if action == 'passed':
        users[user_id]['points'] += steps[step_id]['step_cost']
        if users[user_id]['end_time'] < 0:
            if users[user_id]['points'] >= required_points:
                users[user_id]['end_time'] = time

def get_user_list():
    global users
    user_list = []
    for user in users.values():
        if user['end_time'] >= 0:
            user_list += [user]
    return user_list

with open('course-217-structure.csv') as file_steps:
    for line in file_steps:
        line = line.strip()
        data = line.split(',')
        if data[0] == 'course_id':
            continue
        register_step_data(int(data[5]), int(data[8]))

with open('course-217-events.csv') as file_events:
    for line in file_events:
        line = line.strip()
        data = line.split(',')
        if data[0] == 'user_id':
            continue
        register_event_data(int(data[0]), data[1], int(data[2]), int(data[3]))

events.sort(key=lambda event: event['time'])

for event in events:
    process_event(event)

user_list = get_user_list()

user_list.sort(key=lambda user: user['end_time']-user['start_time'])

for user in user_list[:9]:
    print(user['user_id'], end=',')
print(user_list[9]['user_id'])
