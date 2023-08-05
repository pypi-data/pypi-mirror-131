def is_pal(str):
    if (len(str) <= 1):
        return False
    str = str.lower().replace(' ', '')
    return str == str[::-1]

