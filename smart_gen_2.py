import pandas as pd
import re
import random


class SmartBot:
    def __init__(self, region, acc, number):
        self.region = region
        self.acc = acc
        self.number = number

    def proxy_gen(self):
        file = pd.read_csv('smart_sticky.csv')
        quantity_all = []
        quantity_range = []
        for country in self.region:
            condition = file['Proxy address'] == f'{country}.smartproxy.com'
            m = re.compile(r'([\d.]+) - ([\d.]+)').search(str(file[condition]['Port']))
            quantity_range.append([int(m.groups()[0]), int(m.groups()[1])])
            quantity = int(m.groups()[1]) - int(m.groups()[0])
            quantity_all.append(quantity)

        quantity_sum = sum(quantity_all)
        i = 0
        random_proxy = []
        for country in self.region:
            number_proxy = int(quantity_all[i] / quantity_sum * self.number)
            for n in range(number_proxy):
                random_port = f'{country}.smartproxy.com:' \
                              + '{}'.format(random.choice(range(quantity_range[i][0], quantity_range[i][1]))) \
                              + ':' + self.acc
                random_proxy.append(random_port + '\n')
            i += 1

        with open(r'./proxy.txt', 'w') as f:
            f.write(''.join(random.sample(random_proxy, len(random_proxy))))
