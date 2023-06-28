
def find_duplicates_in_list(iteration: list, key):
    unique_list = []
    duplicates = []
    for item in iteration:
        item_id = item[key]
        if item_id not in unique_list:
            unique_list.append(item_id)
        else:
            duplicates.append(item_id)
    return duplicates

