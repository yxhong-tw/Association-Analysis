class Apriori():

    def __init__(self, transactions: set[frozenset[str]], min_sup: float,
                 min_conf: float):
        self.transactions = transactions
        self.min_sup = min_sup
        self.min_conf = min_conf

    def __call__(self):
        cand_1_itemssets = self.get_cand_1_itemssets(
            transactions=self.transactions)

        freq_itemssets, freq_itemssets_sup_table = self.get_freq_data(
            cand_itemssets=cand_1_itemssets,
            min_sup=self.min_sup,
            transactions=self.transactions)
        all_freq_itemssets = [freq_itemssets]
        k = 2

        while True:
            cand_itemssets = self.get_cand_k_itemssets(
                k=k, freq_itemssets=freq_itemssets)
            freq_itemssets, temp_freq_itemssets_sup_table = self.get_freq_data(
                cand_itemssets=cand_itemssets,
                min_sup=self.min_sup,
                transactions=self.transactions)

            print("---")
            print(f'k: {k}')
            print(len(cand_itemssets))
            print(len(freq_itemssets))

            all_freq_itemssets.append(freq_itemssets)
            freq_itemssets_sup_table.update(temp_freq_itemssets_sup_table)
            k += 1

            if len(freq_itemssets) == 0:
                break

        print("---")

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
        freq_itemssets = set()
        freq_itemssets_sup_table = {}

        for cand_itemsset in cand_itemssets:
            for transaction in transactions:
                if cand_itemsset.issubset(transaction):
                    if not cand_itemsset in sup_table.keys():
                        sup_table[cand_itemsset] = 1
                    else:
                        sup_table[cand_itemsset] += 1

        transactions_num = len(transactions)

        for item, sup in sup_table.items():
            if (sup / transactions_num) > min_sup:
                freq_itemssets.add(item)
                freq_itemssets_sup_table[item] = sup

        return freq_itemssets, freq_itemssets_sup_table

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
