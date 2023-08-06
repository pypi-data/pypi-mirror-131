#module to calculate task stats for the todoapp
import json

def extract_task_status(data):
    open_tasks = len([ task.id for task in data if task.status=='Open'])
    inprogress_tasks = len([ task.id for task in data if task.status=='In Progress'])
    closed_tasks = len([task.id for task in data if task.status=='Close'])

    return json.dumps([open_tasks, closed_tasks, inprogress_tasks])


def extract_task_category(data):
    category_work = len([task.id for task in data if task.category=='Work'])
    category_leisure = len([task.id for task in data if task.category=='Leisure'])
    category_travel = len([task.id for task in data if task.category=='Travel'])
    category_shopping = len([task.id for task in data if task.category=='Shopping'])

    return json.dumps([category_leisure, category_shopping, category_travel, category_work])

def extract_task_labels(data):
    return json.dumps(['Leisure', 'Shopping', 'Travel', 'Work'])