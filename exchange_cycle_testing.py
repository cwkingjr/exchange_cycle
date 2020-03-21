import random

def has_valid_hamiltonian_cycle(groups):
  lens = list(map(len, groups))
  return (2 * max(lens)) <= sum(lens)

def find_random_hamiltonian_cycle(groups):
  lens = list(map(len, groups))
  tot = sum(lens)

  groups_by_size = {k:[] for k in lens}
  for group in groups:
    groups_by_size[len(group)].append(group)

  cycle = []
  prev_group = []

  # TODO: have to make sure the last element isn't from the same group as the first
  while (len(cycle) < tot):

    # if the largest group is half (or more) than the total remaining, we have
    # to pick someone from that group. Otherwise, can pick anyone
    num = max(groups_by_size.keys())
    if (num * 2 < tot - len(cycle)):
      num = random.choice(list(groups_by_size.keys()))

    # Pick a random group from the groups with the selected size
    # This does mean some participants have a greater chance of getting
    # picked.
    curr_group = random.choice(groups_by_size[num])
    groups_by_size[num].remove(curr_group)

    if len(groups_by_size[num]) == 0:
      del groups_by_size[num]

    # pick a random participant from the group and add it to the cycle
    p = random.choice(curr_group)
    curr_group.remove(p)
    cycle.append(p)

    # Add the previous group back to the list
    num = len(prev_group)
    if num > 0:
      if not (num in groups_by_size):
        groups_by_size[num] = []
      groups_by_size[num].append(prev_group)

    prev_group = curr_group

  return cycle

groups = [
  ['A1', 'A2', 'A3', 'A4'],
  ['B1', 'B2', 'B3'],
  ['C1'],
  ['D1', 'D2', 'D3', 'D4'],
  ['E1'],
  ['F1']
]

if (has_valid_hamiltonian_cycle(groups)):
  cycle = find_random_hamiltonian_cycle(groups)
  print(cycle)
else:
  print("No valid hamiltonian cycle exists")
