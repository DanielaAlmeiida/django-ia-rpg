from IA.number_status import number_status


def full_power():
    rarity_card, status, rarity_status, value_status = number_status()

    final_status = status + sum(value_status)

    if final_status <= 250:
        power_color = "115, 115, 115,"
        color_back = "#adadad"
    elif final_status <= 500:
        power_color = "26, 179, 0,"
        color_back = "#0ee700"
    elif final_status <= 800:
        power_color = "33, 140, 239,"
        color_back = "#60B2FF"
    elif final_status <= 1300:
        power_color = "239, 33, 222,"
        color_back = " #bf24ff"
    elif final_status <= 2000:
        power_color = "183, 73, 19,"
        color_back = "#ef5901"
    elif final_status <= 3000:
        power_color = "183, 19, 19,"
        color_back = "#ff2626"
    else:
        power_color = "218, 165, 32,"
        color_back = "#daa520"

    return power_color, final_status, color_back, rarity_card, status, rarity_status
