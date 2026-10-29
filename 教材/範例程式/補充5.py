def classify(index_up, middle_up, ring_up, little_up):
    if not any((index_up, middle_up, ring_up, little_up)):
        return 'rock'
    if index_up and middle_up and not ring_up and not little_up:
        return 'scissors'
    if all((index_up, middle_up, ring_up, little_up)):
        return 'paper'
    return 'unknown'

print('rock test', classify(False, False, False, False))
print('scissors test', classify(True, True, False, False))
print('paper test', classify(True, True, True, True))
