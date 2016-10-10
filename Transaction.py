class Transaction(object):
    __dict__ = ['items', 'cluster_id', 'cluster_pos']

    def __init__(self, items):
        self.cluster_pos = 0
        self.cluster_id = 0
        self.items = items
        if items:
            self.items = items.strip().split(',')
