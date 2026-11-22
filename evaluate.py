import argparse
import time
import urllib.request

import pandas as pd

from pipeline import Apriori


def get_real_dataset():
    """
    Download and load the T10I4D100K transaction dataset from GitHub.

    Returns:
        A list of transactions, where each transaction is represented
        as a frozenset of items.
    """
    print("Downloading transaction data from github...")
    url = "https://raw.githubusercontent.com/yiweig/Apriori/refs/heads/master/T10I4D100K.dat"

    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")

    transactions = []
    for line in data.strip().split("\n"):
        transactions.append(frozenset(line.split()))
    return transactions


def get_frequent_itemset_and_rules(transactions, s, c):
    """
    Find frequent itemsets and generate association rules using Apriori.

    Args:
        transactions: A collection of transactions.
        s: Minimum support count threshold.
        c: Minimum confidence threshold.

    Returns:
        None. Prints the total number of generated association rules.
    """
    apr = Apriori(s, c)

    print("Start finding frequent itemsets...")
    start_time = time.time()
    frequent_itemsets = apr.find_frequent_itemsets(transactions)
    print(f"number of frequent itemsets = {len(frequent_itemsets)}")
    print("example of frequent itemsets")
    print(frequent_itemsets[:10])
    print(f"finding frequent itemset = {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    print("Start finding association rules...")
    association_rules = apr.mine_association_rules(frequent_itemsets)
    print(f"number of association rules = {len(association_rules)}")
    print(f"finding association rules time = {time.time() - start_time:.2f} seconds")

    for rule in rules[:10]:
        print(f"{rule[0]} -> {rule[1]}, confidence = {rule[2]}")
    return frequent_itemsets, association_rules


def parse_args():
    p = argparse.ArgumentParser(description="Find frequent items and association rules")
    p.add_argument(
        "-s", type=int, default=500, help="minimum support threshold (default: 500)"
    )
    p.add_argument(
        "-c",
        type=float,
        default=0.75,
        help="minimum confidence threshold (default: 0.75)",
    )
    args = p.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    # 1. Download the real dataset
    transactions = get_real_dataset()
    frequent_itemsets, association_rules = get_frequent_itemset_and_rules(
        transactions, 500, 0.75
    )
