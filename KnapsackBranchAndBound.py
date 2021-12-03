import timeit
from queue import Queue
from collections import namedtuple
import FileHandler


class Node:
    def __init__(self):
        self.level = None
        self.value = None
        self.bound = None
        self.weight = None


def bound(node, n, w, items):
    # if nodes weight is greater than given weight then return 0 
    if node.weight >= w:
        return 0

    bound_value = int(node.value)
    level = node.level + 1
    weight = int(node.weight)

    while (level < n) and (weight + items[level].weight) <= w:
        weight += items[level].weight
        bound_value += items[level].value
        level += 1

    if level < n:
        bound_value += (w - weight) * items[level].value / float(items[level].weight)

    return bound_value


def branch_and_bound(capacity_weight, items, n_items):

    # Sort items in decreasing order of value/weight ratio
    items = sorted(items, key=lambda x: x.value / float(x.weight), reverse=True)
    curr = Node()
    curr.level, curr.value, curr.weight = -1, 0, 0
    # creating a queue
    que = Queue()
    que.put(curr)

    # first max value is 0
    max_profit = 0

    while not que.empty():
        # getting start queue
        curr = que.get()
        temp = Node()  # Added line
        # if it is the start node, change level to 0
        if curr.level == -1:
            temp.level = 0

        if curr.level == n_items - 1:
            continue

        # if the node is not the last node, increase level by 1 of the start node
        temp.level = curr.level + 1
        # Adding current level’s weight and value (temp) to start node weight and value (curr)
        temp.weight = curr.weight + items[temp.level].weight
        temp.value = curr.value + items[temp.level].value

        if temp.weight <= capacity_weight and temp.value > max_profit:
            max_profit = temp.value

        # if current nodes bound (temp.bound) is greater than max profit, insert current to queue
        temp.bound = bound(temp, n_items, capacity_weight, items)
        if temp.bound > max_profit:
            que.put(temp)

        # If not considering Current node as a part of the solution, adding a new node to queue
        new_temp = Node()
        new_temp.level = curr.level + 1
        new_temp.weight = curr.weight
        new_temp.value = curr.value
        new_temp.bound = bound(new_temp, n_items, capacity_weight, items)

        # If current bound is greater than max_profit insert current node to queue
        if new_temp.bound > max_profit:
            que.put(new_temp)

    return max_profit


def main():
    # Get the problem set
    number = input("Please enter a problem number, it should be between 1 to 8: ")
    values, weights, knapsack_max_capacity, num_of_items = FileHandler.read_files(number)

    Item = namedtuple("Item", ['index', 'value', 'weight'])
    items = []
    for i in range(0, num_of_items):
        items.append(Item(i - 1, int(values[i]), float(weights[i])))

    print("Data loaded. Number of items in the dataset: ", num_of_items)

    # Branch and Bound
    print()
    print("Running Branch and Bound Approach")
    start = timeit.default_timer()
    bb = branch_and_bound(knapsack_max_capacity, items, num_of_items)
    stop = timeit.default_timer()
    #print("Time taken for branch & bound = ", (stop - start))
    print("Optimal Profit in the knapsack =", bb)


if __name__ == "__main__":
    main()
