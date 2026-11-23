import argparse
import time
import urllib.request

from pipeline import Apriori

URL = (
    "https://raw.githubusercontent.com/yiweig/Apriori/refs/heads/master/T10I4D100K.dat"
)


def get_real_dataset(path=None):
    """
    Load the T10I4D100K transaction dataset.

    If a local path is given the file is read from disk, otherwise the
    dataset is downloaded from GitHub.

    Returns:
        A list of transactions, each represented as a frozenset of items.
    """
    if path:
        print(f"Reading transaction data from {path}...")
        with open(path, "r") as f:
            data = f.read()
    else:
        print("Downloading transaction data from github...")
        with urllib.request.urlopen(URL) as response:
            data = response.read().decode("utf-8")

    return [
        frozenset(line.split()) for line in data.strip().split("\n") if line.strip()
    ]


def get_frequent_itemset_and_rules(transactions, s, confidences):
    """
    Find frequent itemsets once, then mine association rules for every
    confidence threshold in `confidences`.

    Args:
        transactions: A collection of transactions.
        s: Minimum support count threshold.
        confidences: List of minimum confidence thresholds.

    Returns:
        (frequent_itemsets, rules of the first confidence, list of result rows)
    """
    print(f"Running with minimum support threshold s = {s}")
    apr = Apriori(s, confidences[0])

    print("Start finding frequent itemsets...")
    start_time = time.time()
    frequent_itemsets = apr.find_frequent_itemsets(transactions)
    itemsets_time = time.time() - start_time
    max_size = max(len(i) for i in frequent_itemsets) if frequent_itemsets else 0
    print(
        f"Number of frequent itemsets = {len(frequent_itemsets)} (max size = {max_size})"
    )
    print("Example of frequent itemsets")
    print(list(frequent_itemsets)[:10])
    print(f"Finding frequent itemset time = {itemsets_time:.2f} seconds")

    rows = []
    first_rules = None
    for c in confidences:
        apr.c = c
        t0 = time.time()
        print(f"\nStart finding association rules with c = {c}...")
        rules = apr.mine_association_rules(frequent_itemsets)
        rules_time = time.time() - t0
        print(f"Number of association rules = {len(rules)}")
        print(f"Finding association rules time = {rules_time:.2f} seconds")
        for A, B, conf, supp in rules[:10]:
            print(f"{set(A)} -> {set(B)}, support = {supp}, confidence = {conf:.2f}")
        print(f"Total time = {itemsets_time + rules_time:.2f}")
        rows.append(
            (
                s,
                c,
                len(frequent_itemsets),
                max_size,
                len(rules),
                itemsets_time,
                rules_time,
            )
        )
        if first_rules is None:
            first_rules = rules
    return frequent_itemsets, first_rules, rows


def parse_args():
    p = argparse.ArgumentParser(description="Find frequent items and association rules")
    p.add_argument(
        "-s",
        type=int,
        default=1000,
        help="minimum support threshold, absolute count (default: 1000)",
    )
    p.add_argument(
        "-c",
        type=float,
        nargs="+",
        default=[0.75],
        help="minimum confidence threshold(s) in [0,1] (default: 0.75). "
        "Several values can be given: itemsets are mined only once.",
    )
    p.add_argument(
        "-d",
        "--dataset",
        default=None,
        help="optional local path of T10I4D100K.dat (default: download it)",
    )
    p.add_argument(
        "--csv",
        default=None,
        help="optional CSV file where one summary row per (s, c) is appended",
    )
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()

    transactions = get_real_dataset(args.dataset)
    _, _, rows = get_frequent_itemset_and_rules(transactions, args.s, args.c)

    if args.csv:
        import os

        new = not os.path.exists(args.csv)
        with open(args.csv, "a") as f:
            if new:
                f.write("s,c,n_itemsets,max_size,n_rules,itemsets_time,rules_time\n")
            for r in rows:
                f.write("{},{},{},{},{},{:.2f},{:.2f}\n".format(*r))
