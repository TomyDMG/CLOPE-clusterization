class Cluster(object):

    __dict__ = [
        'id', 'occ', 'transactions', 'add_item', 'delete_item', 'n', 'w', 's', 'delta_add', 'add_instance', 'delete_instance'
    ]

    def __init__(self, cluster_id, transaction):
        self.id = cluster_id
        self.n = 1
        self.s = self.w = len(transaction.items)
        self.occ = {item: 1 for item in transaction.items}
        self.transactions = [transaction]
        transaction.cluster_id = cluster_id

    def add_item(self, item):
        if item in self.occ:
            self.occ[item] += 1
        else:
            self.occ[item] = 1

    def delete_item(self, item):
        if self.occ[item] == 1:
            del self.occ[item]
        else:
            self.occ[item] -= 1

    def get_delta(self, items, r):
        s_new = self.s + len(items)
        w_new = self.w

        for item in items:
            if item not in self.occ:
                w_new += 1

        if self.n == 0:
            delta_profit = s_new / (w_new ** r)
        else:
            profit = self.s * self.n / (self.w ** r)
            profit_new = s_new * (self.n + 1) /(w_new **r)
            delta_profit = profit_new - profit

        return delta_profit

    def add_transaction(self, transaction):
        for item in transaction.items:
            self.add_item(item)
        transaction.cluster_id = self.id
        transaction.cluster_pos = len(self.transactions)
        self.transactions.append(transaction)
        self.s += len(transaction.items)
        self.w = len(self.occ)
        self.n += 1

    def remove_transaction(self, transaction):
        for item in transaction.items:
            self.delete_item(item)

        self.transactions[transaction.cluster_pos] = None
        transaction.cluster_id = None
        self.s -= len(transaction.items)
        self.w = len(self.occ)
        self.n -= 1
