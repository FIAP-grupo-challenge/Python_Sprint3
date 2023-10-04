def processar_status(status):
    dict_status = {}
    index = 0
    status = str(status)
    status = status.replace("/", "").replace(":", "").split()
    while index < 7:
        dict_status[status[index]] = status[index + 1]
        index += 2
    return dict_status

def processar_string_compra(compra):
    compra = str(compra)
    dict_compra = {}
    compras = compra.replace("/", " ").split()
    print(compras)
    for c in compras:
        if c in dict_compra.keys():
            dict_compra[c] += 1
        else:
            dict_compra[c] = 1
    return dict_compra


