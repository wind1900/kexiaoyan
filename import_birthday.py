from info_center.models import Birthday

def im(filename):
    file = open(filename)
    list = []
    for line in file:
        e = line.strip().split(',')
        d = {}
        d['name'] = e[0].decode('gbk').replace(' ', '').replace(u'\u3000', '')
        d['phone'] = e[1]
        d['month'] = e[2]
        d['day'] = e[3]
        d['lunar'] = (e[4] != '0')
        b = Birthday(**d)
        b.save()
