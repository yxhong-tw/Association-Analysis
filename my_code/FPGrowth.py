from my_code.tools import get_all_subsets, get_support
from utils import timer


class FPTreeNode():

    def __init__(self, item: frozenset[str], count: int, parent):
        self.item = item
        self.count = count

        # parent: FPTreeNode; next: FPTreeNode
        self.parent = parent
        self.next = None

        # childs: dict[frozenset[str], FPTreeNode]
        self.childs = {}


class FPTree():

    def __init__(self,
                 sorted_freq_transactions: list[list[frozenset[str]]],
                 header_table: dict[frozenset[str], list[int,
                                                         FPTreeNode]] = None):
        self.root = FPTreeNode(item=None, count=None, parent=None)
        self.header_table = header_table

        for transaction in sorted_freq_transactions:
            self.add_transaction(transaction=transaction)

    def add_transaction(self, transaction: list[frozenset[str]]):
        current_node = self.root

        for item in transaction:
            if item in current_node.childs:
                current_node.childs[item].count += 1
            else:
                new_node = FPTreeNode(item=item, count=1, parent=current_node)
                current_node.childs[item] = new_node

                if self.header_table[item][1] != None:
                    temp_node = self.header_table[item][1]

                    while temp_node.next != None:
                        temp_node = temp_node.next

                    temp_node.next = new_node
                else:
                    self.header_table[item][1] = new_node

            current_node = current_node.childs[item]

    # Just for debugging
    def display_tree(self):
        queue = []

        for child in self.root.childs.values():
            queue.append(child)

        while len(queue) > 0:
            current_node = queue.pop(0)

            for child in current_node.childs.values():
                queue.append(child)

            print(current_node.item, current_node.count)
            print(current_node.parent.item)
            print(current_node.childs.keys())
            print('---')

        for key, value in self.header_table.items():
            print(key)

            temp_node = value[1]
            while temp_node != None:
                print(temp_node.item, temp_node.count, temp_node.parent.item)
                temp_node = temp_node.next

            print('---')


class FPGrowth():

    def __init__(self, transactions: list[list[str]], min_sup: float,
                 min_conf: float) -> None:
        self.transactions = transactions
        self.transactions_num = len(transactions)
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.items_order = []
        self.freq_itemsets = set()

    @timer
    def __call__(self):
        header_table, sorted_freq_transactions = self.scanDB()
        fp_tree = FPTree(sorted_freq_transactions=sorted_freq_transactions,
                         header_table=header_table)
        self.get_all_freq_itemsets(header_table=header_table,
                                   freq_itemset=set())
        rules = self.get_rules()

        return rules

    def scanDB(self):
        header_table = {}
        sorted_freq_transactions = []

        # Calculate support for each item
        for transaction in self.transactions:
            for item in transaction:
                if item in header_table:
                    header_table[item] += 1
                else:
                    header_table[item] = 1

        # Sort items with letter and remove items that is smaller than min_sup
        header_table = {
            item: sup
            for item, sup in sorted(
                header_table.items(), key=lambda kv: kv[0], reverse=False)
            if (sup / self.transactions_num) >= self.min_sup
        }

        # Sort items with sup
        header_table = {
            item: sup
            for item, sup in sorted(
                header_table.items(), key=lambda kv: kv[1], reverse=True)
        }

        # Change the format of the header table = {item: [sup, firstNode]}
        header_table = {
            frozenset([item]): [sup, None]
            for item, sup in header_table.items()
        }

        for item in header_table.keys():
            self.items_order.append(item)

        # Get frequent items in each transaction and sort them
        for transaction in self.transactions:
            if len(transaction) > 0:
                # Sort items with letter
                sorted_freq_transaction = sorted([
                    item for item in transaction
                    if frozenset([item]) in header_table
                ])

                # Change the format from str to frozenset
                sorted_freq_transaction = [
                    frozenset([item]) for item in sorted_freq_transaction
                ]

                sorted_freq_transaction.sort(
                    key=lambda item: header_table[item][0], reverse=True)
                sorted_freq_transactions.append(sorted_freq_transaction)

        return header_table, sorted_freq_transactions

    # Return header_table: dict[frozenset[str], list[int, FPTreeNode]]
    # Return sorted_freq_cond_pattern_bases: list[list[frozenset[str]]]
    def scanCPB(self, cond_pattern_bases: dict[frozenset[str], int]):
        cond_pattern_bases_num = len(cond_pattern_bases)
        header_table = {}
        sorted_freq_cond_pattern_bases = []

        # Calculate support for each item
        for cond_pattern_base, count in cond_pattern_bases.items():
            for item in cond_pattern_base:
                if item in header_table:
                    header_table[item] += count
                else:
                    header_table[item] = count

        # Sort items with letter and remove items that is smaller than min_sup
        header_table = {
            item: count
            for item, count in sorted(
                header_table.items(),
                key=lambda kv: self.items_order.index(frozenset([kv[0]])),
                reverse=False) if count >= self.min_sup * self.transactions_num
        }

        # Sort items with count
        header_table = {
            item: count
            for item, count in sorted(
                header_table.items(), key=lambda kv: kv[1], reverse=True)
        }

        # Change the format of the header table = {item: [count, firstNode]}
        header_table = {
            frozenset([item]): [count, None]
            for item, count in header_table.items()
        }

        # Get frequent items in each cond_frequent_base and sort them
        for cond_pattern_base, count in cond_pattern_bases.items():
            if len(cond_pattern_base) > 0:
                # Sort items with letter
                sorted_freq_cond_pattern_base = sorted(
                    [
                        item for item in cond_pattern_base
                        if frozenset([item]) in header_table
                    ],
                    key=lambda item: self.items_order.index(frozenset([item])),
                    reverse=False)

                # Change the format from str to frozenset
                sorted_freq_cond_pattern_base = [
                    frozenset([item]) for item in sorted_freq_cond_pattern_base
                ]

                sorted_freq_cond_pattern_base.sort(
                    key=lambda item: header_table[item][0], reverse=True)

                if len(sorted_freq_cond_pattern_base) > 0:
                    for _ in range(count):
                        sorted_freq_cond_pattern_bases.append(
                            sorted_freq_cond_pattern_base)

        return header_table, sorted_freq_cond_pattern_bases

    def get_cond_pattern_bases(self, node) -> dict[frozenset[str], int]:
        cond_pattern_bases = {}

        while node != None:
            temp_node = node.parent
            cond_pattern_base = []

            while temp_node.parent != None:
                cond_pattern_base.append(next(iter(temp_node.item)))
                temp_node = temp_node.parent

            if len(cond_pattern_base) > 0:
                cond_pattern_bases[frozenset(cond_pattern_base)] = node.count

            node = node.next

        return cond_pattern_bases

    def get_all_freq_itemsets(self, header_table: dict[frozenset[str],
                                                       list[int, FPTreeNode]],
                              freq_itemset: set):
        if len(header_table) == 0:
            return

        for key, value in header_table.items():
            newfreq_itemset = freq_itemset.copy()
            newfreq_itemset.add(next(iter(key)))
            self.freq_itemsets.add(frozenset(newfreq_itemset))

            node = value[1]
            cond_pattern_bases = self.get_cond_pattern_bases(node=node)

            cpb_header_table, sorted_freq_cond_pattern_bases = self.scanCPB(
                cond_pattern_bases=cond_pattern_bases)

            sub_fp_tree = FPTree(
                sorted_freq_transactions=sorted_freq_cond_pattern_bases,
                header_table=cpb_header_table)

            self.get_all_freq_itemsets(header_table=cpb_header_table,
                                       freq_itemset=newfreq_itemset)

    def get_rules(self) -> list[tuple]:
        rules = []

        for freq_itemset in self.freq_itemsets:
            subsets = get_all_subsets(itemset=freq_itemset)

            for subset in subsets:
                remain = freq_itemset.difference(subset)

                freq_itemsset_sup = get_support(itemsset=freq_itemset,
                                                transactions=self.transactions)
                subset_sup = get_support(itemsset=subset,
                                         transactions=self.transactions)
                conf = freq_itemsset_sup / subset_sup

                if conf >= self.min_conf:
                    sup = freq_itemsset_sup / self.transactions_num
                    remain_sup = get_support(
                        itemsset=remain,
                        transactions=self.transactions) / self.transactions_num

                    lift = conf / remain_sup
                    rules.append((subset, remain, sup, conf, lift))

        return rules
