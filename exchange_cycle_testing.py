#!/usr/bin/env python3
"""
Runs stats on hamilton path/cycle generation
"""
import random

from collections import Counter, defaultdict
from copy import deepcopy
from typing import Dict, List


def has_valid_hamiltonian_path(groups: List[List[str]]) -> bool:
      """Determines if a list of groups is capable of generating a hamiltonian path"""
      group_lengths = [len(x) for x in groups]
      two_times_largest_group = 2 * max(group_lengths)
      participant_count = sum(group_lengths)
      # TODO what's the source/explanation for this formula?
      return two_times_largest_group <= participant_count


def find_random_hamiltonian_path(groups: List[List[str]]) -> List[str]:
    """Walks through the participant groups and generates a random path"""
    group_lengths = [len(x) for x in groups]
    participant_count = sum(group_lengths)

    groups_by_size: Dict[int, List[str]] = defaultdict(list)
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

    return path


def is_path_a_circuit(mypath: List[str]) -> bool:
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
    return True


def main():
    """Run several tests and dump the stats"""

    ITERATIONS = 100000

    circuit_count: int = 0
    non_circuit_count: int = 0

    valid_path_count: int = 0
    invalid_path_count: int = 0

    circuits: List[str] = []

    groups = [
        ['A1', 'A2', 'A3', 'A4'],
        ['B1', 'B2', 'B3'],
        ['C1'],
        ['D1', 'D2', 'D3', 'D4'],
        ['E1'],
        ['F1']
    ]

    if has_valid_hamiltonian_path(groups):  
        for i in range(ITERATIONS):
            mygroups = deepcopy(groups)
            path = find_random_hamiltonian_path(mygroups)

            if is_valid_path(path):
                valid_path_count += 1
            else:
                invalid_path_count += 1

            if is_path_a_circuit(path):
                circuit_count += 1
                circuits.append(''.join(path))
                # print(f'circuit: {path}')
            else:
                non_circuit_count += 1
                # print(f'non-circuit: {path}')
    else:
      print("No valid hamiltonian path exists")

    print(f'circuits: {circuit_count}')
    print(f'non-circuits: {non_circuit_count}')
    print(f'valid path count: {valid_path_count}')
    print(f'invalid path count: {invalid_path_count}')

    most_common_circuits = Counter(circuits).most_common(10)
    print(f'most common circuits: {most_common_circuits}')


if __name__ == '__main__':
    main()