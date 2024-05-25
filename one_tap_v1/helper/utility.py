def modify_key_name(key):
    key = key.lower()
    key = "_".join(key.split(" "))
    return key