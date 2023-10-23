from my_code.tools import get_all_subsets, get_support
from utils import timer


class Apriori():

    def __init__(self, transactions: list[list[str]], min_sup: float,
                 min_conf: float):
        self.transactions = transactions
        self.transactions_num = len(transactions)
        self.min_sup = min_sup
        self.min_conf = min_conf

    @timer
    def __call__(self):
        cand_1_itemsets = self.get_cand_1_itemsets()

        freq_itemsets, freq_itemsets_sup_table = self.get_freq_data(
            cand_itemsets=cand_1_itemsets)

        all_freq_itemsets = set()
        for freq_itemset in freq_itemsets:
            all_freq_itemsets.add(freq_itemset)

        k = 2

        while True:
            cand_itemsets = self.get_cand_k_itemsets(
                k=k, freq_itemsets=freq_itemsets)
            freq_itemsets, temp_freq_itemsets_sup_table = self.get_freq_data(
                cand_itemsets=cand_itemsets)

            for freq_itemset in freq_itemsets:
                all_freq_itemsets.add(freq_itemset)
            freq_itemsets_sup_table.update(temp_freq_itemsets_sup_table)
            k += 1

            if len(freq_itemsets) == 0:
                break

        rules = self.get_rules(all_freq_itemsets=all_freq_itemsets)

        return rules

    def get_cand_1_itemsets(self) -> set[frozenset[str]]:
        cand_1_itemsets = set()

        for transaction in self.transactions:
            for item in transaction:
                if not frozenset([item]) in cand_1_itemsets:
                    cand_1_itemsets.add(frozenset([item]))

        return cand_1_itemsets

    def get_freq_data(
        self, cand_itemsets: set[frozenset[str]]
    ) -> (set[frozenset[str]], dict[frozenset[str], int]):
        sup_table = {}

        for cand_itemset in cand_itemsets:
            sup = get_support(itemset=cand_itemset,
                              transactions=self.transactions)

            if sup > 0:
                sup_table[cand_itemset] = sup

        freq_itemsets = set()
        freq_itemsets_sup_table = {}

        for item, sup in sup_table.items():
            if (sup / self.transactions_num) >= self.min_sup:
                freq_itemsets.add(item)
                freq_itemsets_sup_table[item] = sup

        return freq_itemsets, freq_itemsets_sup_table

    def get_cand_k_itemsets(self, k: int, freq_itemsets: set[frozenset[str]]):
        cand_itemsets = set()

        for freq_itemset_i in freq_itemsets:
            for freq_itemset_j in freq_itemsets:
                cand_itemset = frozenset.union(freq_itemset_i, freq_itemset_j)

                if len(cand_itemset) == k:
                    cand_itemsets.add(cand_itemset)

        return cand_itemsets

    def get_rules(self, all_freq_itemsets: set[frozenset[str]]) -> list[tuple]:
        rules = []

        for freq_itemset in all_freq_itemsets:
            subsets = get_all_subsets(itemset=freq_itemset)

            for subset in subsets:
                remain = freq_itemset.difference(subset)

                freq_itemsset_sup = get_support(itemset=freq_itemset,
                                                transactions=self.transactions)
                subset_sup = get_support(itemset=subset,
                                         transactions=self.transactions)
                conf = freq_itemsset_sup / subset_sup

                if conf >= self.min_conf:
                    sup = freq_itemsset_sup / self.transactions_num
                    remain_sup = get_support(
                        itemset=remain,
                        transactions=self.transactions) / self.transactions_num

                    lift = conf / remain_sup
                    rules.append((subset, remain, sup, conf, lift))

        return rules
