from collections import Counter
from itertools import combinations


class Apriori:
    """Implements the Apriori algorithm to find frequent itemsets."""

    def __init__(self, s, c):
        """Initialize the minimum support threshold, minimum confidence threshold, and support counters."""
        self.s = s
        self.c = c
        self.counter = Counter()

    def find_frequent_itemsets(self, transactions):
        """
        Find frequent itemsets from the given transactions.

        Args:
            transactions: A collection of transactions.

        Returns:
            A set of frequent itemsets
        """
        L = self.get_pruned_singleton(transactions)
        frequent_itemsets = L
        k = 2

        while L:
            print(f"Finding frequent Itemset with Size = {k}")
            Ck = self.generate_candidates(L, k)
            print(f"Number of candidates with size {k} = {len(Ck)}")
            if not Ck:
                break

            counter = Counter()

            for transaction in transactions:
                for combi in combinations(transaction, k):
                    combi_set = frozenset(sorted(combi))
                    if combi_set in Ck:
                        counter[combi_set] += 1

            L = self.prune(counter)

            if L:
                frequent_itemsets.update(L)
                print(f"Number of frequent item set with size {k} = {len(L)}")
                k += 1
                self.counter += counter
            else:
                print(f"No frequent itemsets with size {k}")
        return frequent_itemsets

    def mine_association_rules(self, frequent_itemsets):
        """
        Generate association rules from all frequent itemsets.

        Args:
            frequent_itemsets: A list of frequent itemsets.

        Returns:
            A list of association rules, where each rule contains
            an antecedent, consequent, and confidence value.
        """
        result = []

        for itemset in frequent_itemsets:
            if len(itemset) < 2:
                continue

            rules = self.generate_itemset_rule(itemset)
            result.extend(rules)

        return result

    def generate_itemset_rule(self, itemset):
        """
        Generate association rules from a single frequent itemset.

        Generates all possible non-empty proper subsets as antecedents
        and uses the remaining items as consequents. Rules are retained
        if their confidence meets the minimum confidence threshold.

        Args:
            itemset: A frequent itemset.

        Returns:
            A list of association rules represented as
            (antecedent, consequent, confidence) tuples.
        """
        rules = []
        itemset_support = self.counter[frozenset(itemset)]

        for k in range(1, len(itemset)):
            for combi in combinations(itemset, k):
                I = frozenset(combi)
                subset_support = self.counter[I]
                if subset_support == 0:
                    continue

                confidence = itemset_support / subset_support

                if confidence < self.c:
                    continue
                j = itemset - I

                rules.append((set(I), set(j), confidence))
        return rules

    def prune(self, counter):
        """
        Remove itemsets that do not meet the minimum support threshold.

        Args:
            counter: A Counter containing itemsets and their support counts.

        Returns:
            A set of frequent itemsets.
        """
        filtered_items = {
            item: count for item, count in counter.items() if count >= self.s
        }
        return set(filtered_items.keys())

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

        candidates = self.prune(counter)
        self.counter += counter
        print(f"Number of frequent itemsets with size 1 = {len(candidates)}")
        return candidates

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
                joined_set = list_L[i].union(list_L[j])

                if len(joined_set) != k:
                    continue

                if joined_set in result:
                    continue

                is_candidate = True
                for combi in combinations(joined_set, k - 1):
                    combi_set = frozenset(combi)

                    if combi_set not in L:
                        is_candidate = False
                        break

                if is_candidate:
                    result.add(joined_set)
        return result
