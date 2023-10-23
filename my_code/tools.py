from utils import timer


def get_all_subsets(itemset: frozenset[str]):
    ret_subsets = set()
    itemlist = list(itemset)
    num_items = len(itemlist)

    for i in range(1, 2**num_items - 1):
        subset = frozenset(itemlist[j] for j in range(num_items)
                           if (i >> j) & 1)
        ret_subsets.add(subset)

    return ret_subsets


@timer
def get_rules(freq_itemsets: set[frozenset[str]],
              transactions: list[list[str]], min_conf: float) -> list[tuple]:
    transactions_num = len(transactions)
    rules = []

    for freq_itemset in freq_itemsets:
        subsets = get_all_subsets(itemset=freq_itemset)

        freq_itemsset_sup = get_support(itemset=freq_itemset,
                                        transactions=transactions)

        for subset in subsets:
            if len(subset) == 0 or len(subset) == len(freq_itemset):
                continue

            subset_sup = get_support(itemset=subset, transactions=transactions)
            conf = freq_itemsset_sup / subset_sup

            if conf >= min_conf:
                sup = freq_itemsset_sup / transactions_num
                remain = freq_itemset.difference(subset)
                remain_sup = get_support(
                    itemset=remain,
                    transactions=transactions) / transactions_num
                lift = conf / remain_sup

                rules.append((subset, remain, sup, conf, lift))

    return rules


def get_support(itemset: frozenset[str], transactions: list[list[str]]) -> int:
    support = 0

    for transaction in transactions:
        if itemset.issubset(frozenset(transaction)):
            support += 1

    return support
