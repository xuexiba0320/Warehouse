data = [n.replace('\n', '').replace('\t', '').strip() for n in data.split(';')]
cookies = {n.split('=')[0]: n.split('=')[1] for n in data}