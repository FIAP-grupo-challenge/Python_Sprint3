def processar_status(status):
    dict_status = {}
    index = 0
    status = str(status)
    status = status.replace("/", "").replace(":", "").split()
    while index < 7:
        dict_status[status[index]] = status[index + 1]
        index += 2
    return dict_status
