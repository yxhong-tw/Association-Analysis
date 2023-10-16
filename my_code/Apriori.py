class Apriori():

    def __init__(self, transactions: set[frozenset[str]], min_sup: float,
                 min_conf: float):
        self.transactions = transactions
        self.transactions_num = len(transactions)
        self.min_sup = min_sup
        self.min_conf = min_conf

    def __call__(self):
        cand_1_itemssets = self.get_cand_1_itemssets(
            transactions=self.transactions)

        freq_itemssets, freq_itemssets_sup_table = self.get_freq_data(
            cand_itemssets=cand_1_itemssets,
            min_sup=self.min_sup,
            transactions=self.transactions)

        all_freq_itemssets = set()
        for freq_itemsset in freq_itemssets:
            all_freq_itemssets.add(freq_itemsset)

        k = 2

        while True:
            cand_itemssets = self.get_cand_k_itemssets(
                k=k, freq_itemssets=freq_itemssets)
            freq_itemssets, temp_freq_itemssets_sup_table = self.get_freq_data(
                cand_itemssets=cand_itemssets,
                min_sup=self.min_sup,
                transactions=self.transactions)

            for freq_itemsset in freq_itemssets:
                all_freq_itemssets.add(freq_itemsset)
            freq_itemssets_sup_table.update(temp_freq_itemssets_sup_table)
            k += 1

            if len(freq_itemssets) == 0:
                break

        rules = self.get_rules(all_freq_itemssets=all_freq_itemssets)

        return rules

    def get_cand_1_itemssets(
            self, transactions: set[frozenset[str]]) -> set[frozenset[str]]:
        cand_1_itemssets = set()

        for transaction in transactions:
            for item in transaction:
                if not frozenset([item]) in cand_1_itemssets:
                    cand_1_itemssets.add(frozenset([item]))

        return cand_1_itemssets

    def get_freq_data(
        self, cand_itemssets: set[frozenset[str]], min_sup: float,
        transactions: set[frozenset[str]]
    ) -> (set[frozenset[str]], dict[frozenset[str], int]):
        sup_table = {}

        for cand_itemsset in cand_itemssets:
            sup = self.get_support(itemsset=cand_itemsset,
                                   transactions=transactions)

            if sup > 0:
                sup_table[cand_itemsset] = sup

        freq_itemssets = set()
        freq_itemssets_sup_table = {}

        for item, sup in sup_table.items():
            if (sup / self.transactions_num) >= min_sup:
                freq_itemssets.add(item)
                freq_itemssets_sup_table[item] = sup

        return freq_itemssets, freq_itemssets_sup_table

    def get_support(self, itemsset: frozenset[str],
                    transactions: set[frozenset[str]]) -> int:
        support = 0

        for transaction in transactions:
            if itemsset.issubset(transaction):
                support += 1

        return support

    def get_cand_k_itemssets(self, k: int,
                             freq_itemssets: set[frozenset[str]]):
        cand_itemssets = set()

        for freq_itemssets_i in freq_itemssets:
            for freq_itemssets_j in freq_itemssets:
                cand_itemsset = frozenset.union(freq_itemssets_i,
                                                freq_itemssets_j)

                if len(cand_itemsset) == k:
                    cand_itemssets.add(cand_itemsset)

        return cand_itemssets

    def get_rules(self,
                  all_freq_itemssets: set[frozenset[str]]) -> list[tuple]:
        rules = []

        for freq_itemsset in all_freq_itemssets:
            subsets = self.get_all_subsets(itemsset=freq_itemsset)

            for subset in subsets:
                remain = freq_itemsset.difference(subset)

                freq_itemsset_sup = self.get_support(
                    itemsset=freq_itemsset, transactions=self.transactions)
                subset_sup = self.get_support(itemsset=subset,
                                              transactions=self.transactions)
                conf = freq_itemsset_sup / subset_sup

                if conf >= self.min_conf:
                    sup = freq_itemsset_sup / self.transactions_num
                    remain_sup = self.get_support(
                        itemsset=remain,
                        transactions=self.transactions) / self.transactions_num

                    lift = conf / remain_sup

                    rules.append((subset, remain, sup, conf, lift))

        return rules

    def get_all_subsets(self, itemsset: frozenset[str]):
        subsets = [[]]

        for item in itemsset:
            new_subsets = []

            for subset in subsets:
                new_subsets.append(subset + [item])

            subsets.extend(new_subsets)

        ret_subsets = set()

        for subset in subsets:
            if len(subset) == 0 or len(subset) == len(itemsset):
                continue

            ret_subsets.add(frozenset(subset))

        return ret_subsets
