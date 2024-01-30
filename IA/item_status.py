from IA.status_generator import status_generator

listOfRarity = ["Bronze", "Silver", "Gold", "Emerald", "Diamond", "Ruby", "Obsidian", "Opal"]


def item_status():
    stat = status_generator()

    if stat <= 80:
        rarity = listOfRarity[0]
    elif stat <= 130:
        rarity = listOfRarity[1]
    elif stat <= 180:
        rarity = listOfRarity[2]
    elif stat <= 220:
        rarity = listOfRarity[3]
    elif stat <= 260:
        rarity = listOfRarity[4]
    elif stat <= 300:
        rarity = listOfRarity[5]
    elif stat <= 350:
        rarity = listOfRarity[6]
    else:
        rarity = listOfRarity[7]

    return rarity, stat
