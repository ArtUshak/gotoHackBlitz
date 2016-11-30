import time

events = []
steps = []

def register_event_data(user_id, action, step_id, time):
    global events
    events += [{'user_id':user_id, 'action':action, 'step_id':step_id, 'time':time}]

def register_step_data(step_id, module_position, lesson_position, step_position):
    global steps
    steps += [{'step_id':step_id, 'module_position':module_position, 'lesson_position':lesson_position, 'step_position':step_position, 'visitors':{}, 'revisitors':[]}]

def get_step_pos(step_id):
    for i in range(len(steps)):
        if steps[i]['step_id'] == step_id:
            return i

def process_event(event):
    user_id = event['user_id']
    action = event['action']
    step_id = event['step_id']
    time = event['time']
    step_pos = get_step_pos(step_id)
    if not user_id in steps[step_pos]['visitors']:
        steps[step_pos]['visitors'][user_id] = {'user_id':user_id, 'first_time':time, 'last_time':time}
    else:
        if step_pos+1 < len(steps):
            if not user_id in steps[step_pos]['revisitors']:
                if user_id in steps[step_pos+1]['visitors']:
                    if steps[step_pos]['visitors'][user_id]['first_time'] < steps[step_pos+1]['visitors'][user_id]['last_time']:
                        steps[step_pos]['revisitors'] += [user_id]
    steps[step_pos]['visitors'][user_id]['last_time'] = time

t1 = time.perf_counter()

with open('course-217-structure.csv') as file_steps:
    for line in file_steps:
        line = line.strip()
        data = line.split(',')
        if data[0] == 'course_id':
            continue
        register_step_data(int(data[5]), int(data[2]), int(data[4]), int(data[6]))

t2 = time.perf_counter()

with open('course-217-events.csv') as file_events:
    for line in file_events:
        line = line.strip()
        data = line.split(',')
        if data[0] == 'user_id':
            continue
        register_event_data(int(data[0]), data[1], int(data[2]), int(data[3]))

t3 = time.perf_counter()

steps.sort(key=lambda step: [step['module_position'], step['lesson_position'], step['step_position']])

events.sort(key=lambda event: event['time'])

t4 = time.perf_counter()

for event in events:
    process_event(event)

t5 = time.perf_counter()

for step in steps:
    step['revisit_k'] = len(step['revisitors']) / len(step['visitors'])

result_steps = sorted(steps, key=lambda step: step['revisit_k'])[::-1]

t6 = time.perf_counter()

print(t2 - t1)
print(t3 - t2)
print(t4 - t3)
print(t5 - t4)
print(t6 - t5)

for result_step in result_steps[0:9]:
    print(result_step['step_id'], end=',')
print(result_steps[9]['step_id'])
