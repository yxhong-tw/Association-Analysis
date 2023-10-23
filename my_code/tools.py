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


def get_support(itemsset: frozenset[str], transactions: set) -> int:
    support = 0

    for transaction in transactions:
        if isinstance(transaction, list) == True:
            temp_transaction = frozenset(transaction)

        if itemsset.issubset(temp_transaction):
            support += 1

    return support
