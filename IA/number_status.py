from IA.item_status import item_status
import random as rd


def number_status():
    rarity_card, status = item_status()

    rarity_status = []
    value_status = []
    status_list = ['STR', 'INT', 'VIT', 'AGI', 'RES', 'LUC']

    if rarity_card == "Bronze":
        i = 1
        for number in range(0, i):
            card_rarity, stats = item_status()
            value_status.append(stats)
            type_status = rd.choice(status_list)
            status_list.remove(type_status)
            card_info = {'rarity': card_rarity, 'status': stats, 'type': type_status}
            rarity_status.append(card_info)
    elif rarity_card == "Silver":
        i = 2
        for number in range(0, i):
            card_rarity, stats = item_status()
            value_status.append(stats)
            type_status = rd.choice(status_list)
            status_list.remove(type_status)
            card_info = {'rarity': card_rarity, 'status': stats, 'type': type_status}
            rarity_status.append(card_info)
    elif rarity_card == "Gold":
        i = 3
        for number in range(0, i):
            card_rarity, stats = item_status()
            value_status.append(stats)
            type_status = rd.choice(status_list)
            status_list.remove(type_status)
            card_info = {'rarity': card_rarity, 'status': stats, 'type': type_status}
            rarity_status.append(card_info)
    elif rarity_card == "Emerald":
        i = 4
        for number in range(0, i):
            card_rarity, stats = item_status()
            value_status.append(stats)
            type_status = rd.choice(status_list)
            status_list.remove(type_status)
            card_info = {'rarity': card_rarity, 'status': stats, 'type': type_status}
            rarity_status.append(card_info)
    elif rarity_card == "Diamond":
        i = 5
        for number in range(0, i):
            card_rarity, stats = item_status()
            value_status.append(stats)
            type_status = rd.choice(status_list)
            status_list.remove(type_status)
            card_info = {'rarity': card_rarity, 'status': stats, 'type': type_status}
            rarity_status.append(card_info)
    elif rarity_card == "Ruby":
        i = 6
        for number in range(0, i):
            card_rarity, stats = item_status()
            value_status.append(stats)
            type_status = rd.choice(status_list)
            status_list.remove(type_status)
            card_info = {'rarity': card_rarity, 'status': stats, 'type': type_status}
            rarity_status.append(card_info)
    elif rarity_card == "Obsidian":
        i = 6
        for number in range(0, i):
            card_rarity, stats = item_status()
            value_status.append(stats)
            type_status = rd.choice(status_list)
            status_list.remove(type_status)
            card_info = {'rarity': card_rarity, 'status': stats, 'type': type_status}
            rarity_status.append(card_info)
    else:
        i = 6
        for number in range(0, i):
            card_rarity, stats = item_status()
            value_status.append(stats)
            type_status = rd.choice(status_list)
            status_list.remove(type_status)
            card_info = {'rarity': card_rarity, 'status': stats, 'type': type_status}
            rarity_status.append(card_info)

    return rarity_card, status, rarity_status, value_status
