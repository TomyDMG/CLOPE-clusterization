#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from Transaction import Transaction
from Cluster import Cluster


def erase_blank_transactions(clusters):
    for cluster in clusters:
        cluster.transactions = filter(None, cluster.transactions)
    return clusters


def erase_blank_clusters(clusters):
    return filter(lambda c: len(c.transactions) > 0, clusters)


def clusterizzze(filename, repulsion=2.5):
    clusters = []
    transactions = []
    with open(filename, "r") as ins:
        for idx, line in enumerate(ins):

            transaction = Transaction(line)
            transactions.append(transaction)
        for i, transaction in enumerate(transactions):
            clusters = add_instance_to_best_cluster(
                clusters, transaction, repulsion
            )

        while True:
            moved = False
            for i, transaction in enumerate(transactions):
                original_cluster_id = transaction.cluster_id
                clusters[original_cluster_id].remove_transaction(transaction)
                clusters = add_instance_to_best_cluster(
                clusters, transaction, repulsion
                )
                if transaction.cluster_id != original_cluster_id:
                    moved = True


            if not moved:
                    break

    return erase_blank_clusters(erase_blank_transactions(clusters))


def add_instance_to_best_cluster(clusters, transaction, repulsion):
    best_cluster = None
    items = transaction.items
    temp_s = len(items)
    temp_w = temp_s

    max_delta = temp_s / (temp_w ** repulsion)
    best_delta = 0
    for i, cluster in enumerate(clusters):
        delta = cluster.get_delta(items, repulsion)
        if delta > best_delta:
            if delta > max_delta:
                cluster.add_transaction(transaction)
                return clusters
            else:
                best_delta = delta
                best_cluster = cluster

    clusters.append(Cluster(len(clusters), transaction))
    return clusters




def main():
    filename = sys.argv[1]
    repulsion = float(sys.argv[2])
    e = 0
    p = 0
    result = clusterizzze(filename, repulsion)
    for i, cluster in enumerate(result):
        print cluster.id
        ei = 0
        pi = 0
        for i, transactions in enumerate(cluster.transactions):
            if transactions.items[0] == 'e':
                e = e + 1
                ei = ei + 1
            else:
                p += 1
                pi += 1
        print '{}'.format(ei.__abs__())
        print pi
    print 'Построено {} кластеров'.format(len(result))
    print e
    print p

if __name__ == "__main__":
    main()
