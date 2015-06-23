"""
arry = []
odds_dict = get_page(xeid, xhash, odd_type)
if odds_dict:
    for key, val in odds_dict.iteritems():
        hcap_value = float(val["handicapValue"])
        odds_dict = val['odds']
        odds_arry = [odds_dict[item] for item in odds_dict]
        if hcap_value % 1 != 0:
            data = map_close(odds_arry)

            if data:
                arry.append((
                    data['length'],
                    (float(hcap_value), -1 * float(hcap_value)),
                    (data['home'], data['away']),
                    data['delta']
                ))
    sort_arry = sorted(arry, key=lambda k: k[3], reverse=False)
    return sort_arry[0] if sort_arry[0][0] > 10 else sort_arry[1]
"""
# values, keys, items
odds = {
    '378': [1.9, 1.9],
    '424': [1.87, 1.95],
    '161': [1.87, 1.95],
    '15': [1.87, 1.95],
    '46': [1.84, 1.84],
    '78': [1.88, 2.03],
    '16': [1.83, 2],
    '379': [1.72, 2],
    '140': [1.85, 1.95]
}

for val in odds:
    print(val)
