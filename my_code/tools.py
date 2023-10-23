def get_all_subsets(itemset: frozenset[str]):
    subsets = [[]]

    for item in itemset:
        new_subsets = []

        for subset in subsets:
            new_subsets.append(subset + [item])

        subsets.extend(new_subsets)

    ret_subsets = set()

    for subset in subsets:
        if len(subset) == 0 or len(subset) == len(itemset):
            continue

        ret_subsets.add(frozenset(subset))

    return ret_subsets


# transactions: set[frozenset[str]] or list[list[str]]
def get_rules(freq_itemsets: set[frozenset[str]], transactions,
              min_conf: float) -> list[tuple]:
    print(freq_itemsets)
    print(transactions)
    input()
    transactions_num = len(transactions)
    rules = []

    for freq_itemset in freq_itemsets:
        subsets = get_all_subsets(itemset=freq_itemset)

        for subset in subsets:
            remain = freq_itemset.difference(subset)

            freq_itemsset_sup = get_support(itemset=freq_itemset,
                                            transactions=transactions)
            subset_sup = get_support(itemset=subset, transactions=transactions)
            conf = freq_itemsset_sup / subset_sup

            if conf >= min_conf:
                sup = freq_itemsset_sup / transactions_num
                remain_sup = get_support(
                    itemset=remain,
                    transactions=transactions) / transactions_num

                lift = conf / remain_sup

                rules.append((subset, remain, sup, conf, lift))

    return rules


# transactions: set[frozenset[str]] or list[list[str]]
def get_support(itemset: frozenset[str], transactions) -> int:
    support = 0

    for transaction in transactions:
        if isinstance(transaction, list) == True:
            temp_transaction = frozenset(transaction)
        # isinstance(transaction, frozenset) == True
        else:
            temp_transaction = transaction

        if itemset.issubset(temp_transaction):
            support += 1

    return support
