def add_favor(favor_id):
    favor_id = str(favor_id)
    with open('favor_list', 'r') as favor_list:
        if favor_id in favor_list.read():
            return
    with open('favor_list', 'a') as favor_list:
        favor_list.write(f'{favor_id} ')


def show_favor_bd():
    with open('favor_list', 'r') as favor_list:
        favor_ids = favor_list.read()
    favor_ids = [int(favor_id) for favor_id in favor_ids.split()]
    return favor_ids
