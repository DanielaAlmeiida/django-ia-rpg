def full_power_inventory(power):
    if power <= 250:
        power_color = "115, 115, 115,"
        color_back = "#adadad"
    elif power <= 500:
        power_color = "26, 179, 0,"
        color_back = "#0ee700"
    elif power <= 800:
        power_color = "33, 140, 239,"
        color_back = "#60B2FF"
    elif power <= 1300:
        power_color = "239, 33, 222,"
        color_back = " #bf24ff"
    elif power <= 2000:
        power_color = "183, 73, 19,"
        color_back = "#ef5901"
    elif power <= 3000:
        power_color = "183, 19, 19,"
        color_back = "#ff2626"
    else:
        power_color = "218, 165, 32,"
        color_back = "#daa520"

    return power_color, color_back