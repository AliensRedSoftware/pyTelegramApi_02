#!/usr/bin/env python3

def order(dict1, reverse=False):
    sorted_values = sorted(dict1.values(), reverse=reverse) # Sort the values
    sorted_dict = {}
    for i in sorted_values:
        for k in dict1.keys():
            if dict1[k] == i:
                sorted_dict[k] = dict1[k]
                break
    return sorted_dict
