list_depot = []
list_customer = []
for val in graph.nodes():
    if val[0] == 'D':
        list_depot.append(val)
    else:
        list_customer.append(val)
