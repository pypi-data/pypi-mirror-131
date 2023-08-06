# %%
import random
from random import shuffle
from RDSQueryHelper import RDSQueryHelper
import os
from pprint import pprint

helper = RDSQueryHelper()

people = helper.single_table_select_all(
    'ranked()', 'TRUE'
)
# pprint(people)


def group(people):

    group_size = 3

    groups = []
    idx = 0
    while idx < len(people):
        group = people[idx: idx + group_size]
        groups.append(group)
        idx += group_size
    else:
        final_group = people[idx:]
        # print('final group', final_group)
        if len(final_group) > 0:
            people.append(final_group)

    def map_student(student):
        return {
            'name': student['first_name'] + ' ' + student['last_name'],
            'lesson': student['lesson_name'],
            'start_date': student['start_date']
        }

    def map_group(group):
        return list(map(map_student, group))

    groups = list(map(map_group, groups))
    return groups


# def group(people, group_size=4):
#     shuffle(people)
#     groups = []
#     idx = 0
#     while idx < len(people):
#         groups.append(people[idx:idx + group_size])
#         idx += group_size
#     return groups

def print_agenda():

    todays_demos = [
        {
            'host': 'Ivan',
            'name': 'Web scraping on EC2',
            'difficulty': 'Intermediate',
            'starts': '1930',
            'ends': '2000'
        },
        {
            'host': 'Harry',
            'name': 'How to use VIM',
            'difficulty': 'Intermediate',
            'starts': '2100',
            'ends': '2130'
        }
    ]

    default_agenda = [
        {
            'name': 'Do your thing',
            'starts': '1830',
            'ends': '1930'
        },
        {
            'name': 'Work together on practicals',
            'starts': '1930',
            'ends': '2100'
        },
        {
            'name': 'Smash that quiz',
            'starts': '2100',
            'ends': '2130'
        }
    ]

    agenda = ''

    greeting = random.choice([
        'Hi team',
        'Hi all',
        'Hello everyone',
        "What's up team?",
        "Hi squad",
        "Hello squad"
    ])
    greeting += '\n\n'
    agenda += greeting

    agenda_intro = random.choice([
        "Here's the agenda for today:",
        "Here's the schedule for today:",
        "Here's what's happening today:",
        "Here's what we should all be doing today:",
        "Here's what we're doing today:",
        "Here's the plan for today:"
    ])
    agenda_intro += '\n'
    agenda += agenda_intro

    all_agenda_items = [
        *default_agenda,
        *[
            {**i, 'name': f"Demo hosted by {i['host']}: {i['name']}. Difficulty: {i['difficulty']}"} for i in
            todays_demos
        ]
    ]
    all_agenda_items.sort(key=lambda i: i['starts'])

    for agenda_item in all_agenda_items:
        agenda += f"- {agenda_item['starts']}-{agenda_item['ends']}: {agenda_item['name']}\n"

    agenda += '\n'
    # print(agenda)

    return agenda


def print_groups(groups, instructor=False, start_room_idx=2):
    text = ''

    text += print_agenda()

    groups_intro = random.choice([
        'Here are the groups for today:',
        "Here's the groups:",
        "Here's the rooms:",
        "Here's the groups for today:",
        "Here's where we recommend you to be:",
    ])
    groups_intro += '\n'
    text += groups_intro

    room_idx = start_room_idx
    for group_idx, group in enumerate(groups):
        print(group)
        text += f'- Room {room_idx}\n'
        room_idx += 1
        # print(f'- Room {room_idx}')
        for student in group:
            if instructor:
                text += f'\t- {student["name"]}. Lesson: {student["lesson"]}\n'
                # print(f'\t- {student["name"]}. Lesson: {student["lesson"]}')
            else:
                text += f'\t- {student["name"]}\n'
                # print(f'\t- {student["name"]}')

        print('final room idx for this group:', room_idx)
    return text, room_idx


unique_start_dates = {p['start_date'] for p in people}
print(unique_start_dates)


def get_group_names(unique_start_dates):
    group_names = [
        get_group_name_from_start_date(date)
        for date in unique_start_dates
        if date != 'None'
    ]
    return group_names


def get_group_name_from_start_date(start_date):
    start_date_to_group_name = {
        'August 21': 'Theta',
        'July 21': 'Eta',
        'June 21': 'Zeta'
    }
    if start_date in start_date_to_group_name:
        return start_date_to_group_name[start_date]
    else:
        return start_date


group_names = get_group_names(unique_start_dates)

people = [
    {**p, 'group_name': get_group_name_from_start_date(p['start_date'])} for p in people]


def filter_by_cohort(people, group_name):
    return [p for p in people if p['group_name'] == group_name]


room_idx = 2
for group_name in group_names:

    print()
    print(group_name)
    cohort = filter_by_cohort(people, group_name)
    groups = group(cohort)
    print_agenda()

    # CREATE MESSAGES FOR ENGINEERS
    text, new_room_idx = print_groups(
        groups,
        instructor=False,
        start_room_idx=room_idx,
    )
    with open(f'messages_to_send_to_groups/{group_name}.txt', 'w') as f:
        f.write(text)

    # SAVE INFO FOR AICORE TEAM
    text, _ = print_groups(
        groups,
        instructor=True,
        start_room_idx=room_idx,
    )
    with open(f'info_for_team/{group_name}.txt', 'w') as f:
        f.write(text)

    # INCREMENT ROOM IDX
    room_idx = new_room_idx


# pprint(groups)


# %%
# pprint(people)
# %%
