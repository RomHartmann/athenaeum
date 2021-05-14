"""
Search algorithm that finds the position of a target value within a sorted array.
Binary search compares the target value to the middle element of the array.
  If they are not equal, the half in which the target cannot lie is eliminated and the search continues on the remaining half,
  again taking the middle element to compare to the target value, and repeating this until the target value is found.

If the search ends with the remaining half being empty, the target is not in the array.
"""


def binary_search(arr, val):
    """Return the index at which the value lies in the array.

    :param arr: A sorted array
    :type arr: list of int
    :param val: Value to find in the array
    :type val: int
    :return:
    :rtype:
    """
    mid_ind = len(arr)//2  # integer division
    mid_val = arr[mid_ind]
    # print("    ", mid_ind, mid_val, arr, val)
    if val == mid_val:
        return mid_ind

    if len(arr) == 1 and val != mid_val:
        return None
    if val < mid_val:
        ret = binary_search(arr[:mid_ind], val)
    else:
        ret = binary_search(arr[mid_ind:], val)
        ret = None if ret is None else ret + mid_ind

    return ret


if __name__ == '__main__':
    li = [3, 4, 5, 8, 10, 12, 13, 19]
    # print(binary_search(li, 8))
    for n in range(20):
        idx = binary_search(li, n)
        print(n, idx)
