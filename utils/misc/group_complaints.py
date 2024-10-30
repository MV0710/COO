corpus_dict = {
    '/b1': 'Бутлерова 1',
    '/b3': 'Бутлерова 3',
    '/b5': 'Бутлерова 5',
    '/v1': 'Академика Волгина 2/1',
    '/v2': 'Академика Волгина 2/2'
}


def grouping(data):
    groups = dict()

    for complaint in data:

        if complaint.block == 'Этаж':
            if not groups.get(complaint.block + ' ' + complaint.floor):
                groups[complaint.block + ' ' + complaint.floor] = [complaint]
            else:
                group = groups.get(complaint.block + ' ' + complaint.floor)
                group.append(complaint)
                groups[complaint.block + ' ' + complaint.floor] = group.copy()

        else:
            if not groups.get(complaint.block):
                groups[complaint.block] = [complaint]
            else:
                group = groups.get(complaint.block)
                group.append(complaint)
                groups[complaint.block] = group.copy()

    return groups