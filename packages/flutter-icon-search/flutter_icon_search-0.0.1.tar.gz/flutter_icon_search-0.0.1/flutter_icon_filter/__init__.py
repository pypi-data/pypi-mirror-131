import random

student = ['Icons.people', 'Icons.emoji_events', 'Icons.military_tech']
teacher = ['Icons.groups', 'Icons.person', 'Icons.hive']


def search(reqType):
    if reqType == '1':
        icon = studentIcon()
        return icon
    elif reqType == '0':
        icon = teacherIcon()
        return icon


def studentIcon():
    return random.choice(student)


def teacherIcon():
    return random.choice(teacher)
