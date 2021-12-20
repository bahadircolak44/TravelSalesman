import json
import pprint
import time
import traceback

from rest_api.utils.pub_sub import PubSub

example_problem = {
    "max_travel_distance": 3000,
    "num_vehicles": 3,
    "depot": 0,
    "locations": [
        [288, 149], [288, 129], [270, 133], [256, 141], [256, 157], [246, 157],
        [236, 169], [228, 169], [228, 161], [220, 169], [212, 169], [204, 169],
        [104, 161], [104, 169], [90, 165], [80, 157], [64, 157], [64, 165],
        [56, 169], [56, 161], [56, 153], [56, 145], [56, 137], [56, 129],
        [16, 97], [16, 109], [8, 109], [8, 97], [8, 89], [8, 81],
        [8, 73], [8, 65], [8, 57], [16, 57], [8, 49], [8, 41],
        [56, 81], [48, 83], [56, 89], [56, 97], [104, 97], [104, 105],
        [104, 113], [104, 121], [104, 129], [104, 137], [104, 145]
    ]
}

print('-*-*--*-*--*-*--*-*--*-*--*-*---*-*---*-*---*-*-')
print("PROBLEM SENDING...")
pprint.pprint(example_problem)
print('-*-*--*-*--*-*--*-*--*-*--*-*---*-*---*-*---*-*-')
max_try = 80
try_count = 0
try:
    while try_count < max_try:
        try:
            solution = PubSub().emit(json.dumps(example_problem).encode())
            print("SOLUTION RECEIVED...")
            print('-*-*--*-*--*-*--*-*--*-*--*-*---*-*---*-*---*-*-')
            pprint.pprint(solution)
            break
        except Exception as ex:
            print("UNEXPEDTED ERROR...")
            print(ex)
            print('-*-*--*-*--*-*--*-*--*-*--*-*---*-*---*-*---*-*-')
            print(f"TRYING AGAIN --> MAX_TRY_COUNT: {max_try} CURRENT_TRY_COUNT: {try_count}")
            print(ex)
            print('-*-*--*-*--*-*--*-*--*-*--*-*---*-*---*-*---*-*-')
            try_count += 1
            time.sleep(0.3)
            continue
except Exception as ex:
    print(traceback.format_exc())
