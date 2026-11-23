from collections import Counter
from itertools import combinations


class Apriori:
    """Implements the Apriori algorithm to find frequent itemsets and association rules."""

    def __init__(self, s, c):
        """
        Initialize the minimum support threshold and minimum confidence threshold.

        self.support maps every FREQUENT itemset (frozenset) to its support count.
        Infrequent candidates are never stored, which keeps memory usage low.
        """
        self.s = s
        self.c = c
        self.support = {}

    def find_frequent_itemsets(self, transactions):
        """
        Find frequent itemsets from the given transactions.
        Based on pseudocode from https://en.wikipedia.org/wiki/Apriori_algorithm

        Args:
            transactions: A collection of transactions (sets of items).

        Returns:
            A set of frequent itemsets (frozensets).
        """
        L = self.get_pruned_singleton(transactions)
        frequent_itemsets = set(L)
        k = 2

        while L:
            print(f"Finding frequent Itemset with Size = {k}")
            Ck = self.generate_candidates(L, k)
            print(f"Number of candidates with size {k} = {len(Ck)}")
            if not Ck:
                break

            # Optimization: only items that appear in at least one candidate can
            # be part of a frequent k-itemset. Removing all other items from each
            # transaction (and dropping transactions that become shorter than k)
            # shrinks the number of k-combinations that must be enumerated.
            valid_items = set().union(*Ck)
            counter = Counter()

            for transaction in transactions:
                items = transaction & valid_items
                if len(items) < k:
                    continue
                for combi in combinations(items, k):
                    combi_set = frozenset(combi)
                    if combi_set in Ck:
                        counter[combi_set] += 1

            L = self.prune(counter)

            if L:
                frequent_itemsets.update(L)
                # Store the support only for frequent itemsets
                for itemset in L:
                    self.support[itemset] = counter[itemset]
                print(f"Number of frequent item set with size {k} = {len(L)}")
                k += 1
            else:
                print(f"No frequent itemsets with size {k}")
        return frequent_itemsets

    def mine_association_rules(self, frequent_itemsets):
        """
        Generate association rules from all frequent itemsets.

        Args:
            frequent_itemsets: A collection of frequent itemsets.

        Returns:
            A list of association rules (antecedent, consequent, confidence, support),
            sorted by confidence and then support (descending).
        """
        result = []

        for itemset in frequent_itemsets:
            if len(itemset) < 2:
                continue
            result.extend(self.generate_itemset_rule(itemset))

        result.sort(key=lambda r: (r[2], r[3]), reverse=True)
        return result

    def generate_itemset_rule(self, itemset):
        """
        Generate association rules from a single frequent itemset.

        Generates all possible non-empty proper subsets as antecedents
        and uses the remaining items as consequents. Rules are retained
        if their confidence meets the minimum confidence threshold.
        The support of every rule equals the support of the itemset, hence
        it is always >= s.

        Args:
            itemset: A frequent itemset.

        Returns:
            A list of (antecedent, consequent, confidence, support) tuples.
        """
        rules = []
        itemset_support = self.support[itemset]

        for k in range(1, len(itemset)):
            for combi in combinations(itemset, k):
                I = frozenset(combi)
                # Every subset of a frequent itemset is frequent, so it is stored.
                subset_support = self.support.get(I, 0)
                if subset_support == 0:
                    continue

                confidence = itemset_support / subset_support
                if confidence < self.c:
                    continue

                rules.append((set(I), set(itemset - I), confidence, itemset_support))
        return rules

    def prune(self, counter):
        """
        Remove itemsets that do not meet the minimum support threshold.

        Args:
            counter: A Counter containing itemsets and their support counts.

        Returns:
            A set of frequent itemsets.
        """
        return {item for item, count in counter.items() if count >= self.s}

    def get_pruned_singleton(self, transactions):
        """
        Generate frequent singleton itemsets.

        Args:
            transactions: A collection of transactions.

        Returns:
            A set of frequent singleton itemsets.
        """
        counter = Counter()
        print("Finding frequent Itemset with Size = 1")

        for transaction in transactions:
            for item in transaction:
                counter[frozenset([item])] += 1

        itemsets = self.prune(counter)
        for itemset in itemsets:
            self.support[itemset] = counter[itemset]
        print(f"Number of frequent itemsets with size 1 = {len(itemsets)}")
        return itemsets

    def generate_candidates(self, L, k):
        """
        Generate candidate itemsets of size k using frequent itemsets
        from the previous iteration.

        Applies the Apriori pruning property by checking whether all
        subsets of size k-1 are present in L.

        Args:
            L: Frequent itemsets from the previous iteration.
            k: Desired candidate itemset size.

        Returns:
            A set of candidate itemsets represented as frozensets.
        """
        result = set()
        list_L = list(L)
        for i in range(len(list_L)):
            for j in range(i + 1, len(list_L)):
                joined_set = list_L[i] | list_L[j]

                if len(joined_set) != k:
                    continue

                if joined_set in result:
                    continue

                is_candidate = True
                for combi in combinations(joined_set, k - 1):
                    if frozenset(combi) not in L:
                        is_candidate = False
                        break

                if is_candidate:
                    result.add(joined_set)
        return result
