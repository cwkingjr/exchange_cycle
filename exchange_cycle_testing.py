#!/usr/bin/env python3
"""
Runs stats on hamilton path/cycle generation
"""
import random
import numpy

from collections import Counter, defaultdict
from copy import deepcopy
from typing import Dict, List


def has_valid_hamiltonian_path(groups: List[List[str]]) -> bool:
      """Determines if a list of groups is capable of generating a hamiltonian path"""
      group_lengths = [len(x) for x in groups]
      two_times_largest_group = 2 * max(group_lengths)
      participant_count = sum(group_lengths)
      return two_times_largest_group <= participant_count


def find_random_hamiltonian_path(groups: List[List[str]]) -> List[str]:
    """Walks through the participant groups and generates a random path"""
    group_lengths = [len(x) for x in groups]
    participant_count = sum(group_lengths)

    groups_by_size: Dict[int, List[List[str]]] = defaultdict(list)
    for group in groups:
        groups_by_size[len(group)].append(group)

    path: List[str] = []
    previous_group: List[str] = []

    while (len(path) < participant_count):

        # if the largest group is half (or more) than the total remaining, we have
        # to pick someone from that group. Otherwise, can pick anyone
        remaining_participants = participant_count - len(path)
        group_size = max(groups_by_size.keys())
        if group_size * 2 < remaining_participants:
            group_size = random.choice(list(groups_by_size.keys()))

        # Pick a random group from the groups with the selected size
        # This does mean some participants have a greater chance of getting picked
        current_group = random.choice(groups_by_size[group_size])
        groups_by_size[group_size].remove(current_group)

        if len(groups_by_size[group_size]) == 0:
            del groups_by_size[group_size]

        # pick a random participant from the group and add it to the cycle
        participant = random.choice(current_group)
        current_group.remove(participant)
        path.append(participant)

        # Add the previous group back to the list
        group_size = len(previous_group)
        if group_size:
            groups_by_size[group_size].append(previous_group)

        previous_group = current_group

    return standardize_path_start(path)


def is_path_a_cycle(mypath: List[str]) -> bool:
    """Determines if the head and tail are from the same group"""
    if mypath[0][0] != mypath[-1][0]:
        return True
    return False


def is_valid_path(mypath: List[str]) -> bool:
    """Detemines that there are no adjoinging nodes in the same group"""
    previous_participant = '  '
    for participant in mypath:
        if participant[0] == previous_participant[0]:
            return False
        previous_participant = participant
    return True


# Shift the path so that A1 is in the first position
def standardize_path_start(path: List[str]) -> List[str]:
    a1_index = path.index('A1')
    return list(numpy.roll(path, -1 * a1_index))


def main():
    """Run several tests and dump the stats"""

    ITERATIONS = 100000

    cycle_count: int = 0
    non_cycle_count: int = 0

    cycles: List[str] = []

    groups = [
        ['A1', 'A2', 'A3', 'A4'],
        ['B1', 'B2', 'B3'],
        ['C1'],
        ['D1', 'D2', 'D3', 'D4', 'D5'],
        ['E1'],
        ['F1'],
        ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7'],
    ]

    if has_valid_hamiltonian_path(groups):  
        for i in range(ITERATIONS):

            mygroups = deepcopy(groups)

            path = find_random_hamiltonian_path(mygroups)

            if is_path_a_cycle(path):
                cycle_count += 1
                cycles.append('-'.join(path))
                # print(f'cycle: {path}')
            else:
                non_cycle_count += 1
                # print(f'non-cycle: {path}')
    else:
        print("No valid hamiltonian path exists")

    print(f'cycles: {cycle_count}')
    print(f'non-cycles: {non_cycle_count}')

    most_common_cycles = Counter(cycles).most_common(10)
    print(f'10 most common cycles:')
    for i in most_common_cycles:
        print(i)

    alpha = 'ABCDEFG'
    group_sizes = zip(alpha, [len(x) for x in groups])

    group_info: Dict[str, List[int]] = defaultdict(list)
    for i in group_sizes:
        group_info[i[0]].append(i[1])

    starters = [x[0] for x in cycles]
    starter_count = Counter(starters)
    # counter does not return zero counts
    for key in alpha:
        group_info[key].append(starter_count[key] or 0)

    print('group group-size group-starts')
    for i in group_info:
        print(f'{i:5} {group_info[i][0]:5} {group_info[i][1]:10}')

if __name__ == '__main__':
    main()
