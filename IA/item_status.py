from IA.status_generator import status_generator

listOfRarity = ["Bronze", "Silver", "Gold", "Emerald", "Diamond", "Ruby", "Obsidian", "Opal"]

def item_status():

    stat = status_generator()

    if stat <= 80:
        rarity = listOfRarity[0]
        stt = stat
    elif stat <= 130:
        rarity = listOfRarity[1]
        stt = stat
    elif stat <= 180:
        rarity = listOfRarity[2]
        stt = stat
    elif stat <= 220:
        rarity = listOfRarity[3]
        stt = stat
    elif stat <= 260:
        rarity = listOfRarity[4]
        stt = stat
    elif stat <= 300:
        rarity = listOfRarity[5]
        stt = stat
    elif stat <= 350:
        rarity = listOfRarity[6]
        stt = stat
    else:
        rarity = listOfRarity[7]
        stt = stat

    return rarity, stt