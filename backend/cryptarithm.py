import itertools
import re
import time
import json
from fastapi.responses import JSONResponse

def solve_cryptarithm(inputs, res, op):
    # Extract unique non-digit characters
    equation = op.join(inputs) + "=" + res
    chars = ''.join(set(filter(str.isalpha, ''.join(inputs) + res)))

    # Check if the number of unique characters is more than 10
    if len(chars) > 10:
        return json.dumps({"error": "Too many characters, can't solve with unique digits."})

    # Identify the leading characters (i.e., the first character of each number)
    leading_chars = {term[0] for term in inputs + [res] if term[0].isalpha()}

    # Create character index lookup
    char_indices = {char: index for index, char in enumerate(chars)}

    # Start timer
    start_time = time.time()

    # Check permutations
    for perm in itertools.permutations('0123456789', len(chars)):
        # Ensure no leading character is mapped to zero
        if any(perm[char_indices[ch]] == '0' for ch in leading_chars):
            continue

        table = str.maketrans(chars, ''.join(perm))
        translated_equation = equation.translate(table)

        # Split into left and right parts
        left, right = translated_equation.split('=')

        # Evaluate left side
        terms = re.findall(r'\d+', left)
        if op == '+':
            left_eval = sum(int(term) for term in terms)
        elif op == '-':
            left_eval = int(terms[0])
            for term in terms[1:]:
                left_eval -= int(term)
        elif op == '*':
            left_eval = int(terms[0])
            for term in terms[1:]:
                left_eval *= int(term)
        elif op == '/':
            left_eval = int(terms[0])

            for term in terms[1:]:
                left_eval /= int(term)

        else:
            result = {
                "error": "Invalid operation.",
            }
            print(result)

            headers = {'Content-Type': 'application/json; charset=utf-8'}
            return JSONResponse(content=result, headers=headers, status_code=404)

        if left_eval == int(right):
            result_mapping = {char: int(digit) for char, digit in zip(chars, perm)}

            end_time = time.time()
            result = {
                "left"                  : left.split(op),
                "right"                 : right,
                "operation"             : op,
                "translated_equation"   : translated_equation,
                "mapping"               : dict(sorted(result_mapping.items())),
                "execution_time"        : f"{end_time - start_time:.3f}s"
            }

            headers = {'Content-Type': 'application/json; charset=utf-8'}
            print(result)
            return JSONResponse(content=result, headers=headers, status_code=200)

    # If no solution found
    end_time = time.time()
    result = {
        "error": "No solution found.",
        "execution_time": f"{end_time - start_time:.3f}s"
    }

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    return JSONResponse(content=result, headers=headers, status_code=404)

def filter_input(input_string, select):
    if select == 1:
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,"
    elif select == 2:
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    filtered_string = ''.join(char for char in input_string if char in allowed_chars)
    return filtered_string

def filter_op(input_string):
    allowed_chars = "+-*/"
    filtered_string = ''.join(char for char in input_string if char in allowed_chars)
    if len(filtered_string) == 1:
        return filtered_string[0]
    else:
        return ""

# test backtrack
def solve_cryptarithm2(inputs, res, op):
    # Extract unique non-digit characters
    equation = op.join(inputs) + "=" + res
    chars = ''.join(set(filter(str.isalpha, ''.join(inputs) + res)))

    # Check if the number of unique characters is more than 10
    if len(chars) > 10:
        return json.dumps({"error": "Too many characters, can't solve with unique digits."})

    # Identify the leading characters (i.e., the first character of each number)
    leading_chars = {term[0] for term in inputs + [res] if term[0].isalpha()}

    char_list = list(chars)
    n = len(char_list)

    # Backtracking function
    def backtrack(char_index, digit_used, char_to_digit):
        if char_index == n:
            # All characters have been assigned a digit, evaluate the equation
            table = str.maketrans(char_to_digit)
            translated_equation = equation.translate(table)

            # Split into left and right parts
            left, right = translated_equation.split('=')

            # Evaluate left side
            terms = re.findall(r'\d+', left)
            if op == '+':
                left_eval = sum(int(term) for term in terms)
            elif op == '-':
                left_eval = int(terms[0])
                for term in terms[1:]:
                    left_eval -= int(term)
            elif op == '*':
                left_eval = int(terms[0])
                for term in terms[1:]:
                    left_eval *= int(term)
            elif op == '/':
                left_eval = int(terms[0])
                for term in terms[1:]:
                    left_eval /= int(term)

            if left_eval == int(right):
                return {char: int(char_to_digit[char]) for char in char_to_digit}
            return None

        current_char = char_list[char_index]
        for digit in '0123456789':
            if digit in digit_used:
                continue
            if current_char in leading_chars and digit == '0':
                continue

            char_to_digit[current_char] = digit
            digit_used.add(digit)

            result = backtrack(char_index + 1, digit_used, char_to_digit)
            if result is not None:
                return result

            del char_to_digit[current_char]
            digit_used.remove(digit)

        return None

    # Start timer
    start_time = time.time()

    # Initiate backtracking
    result_mapping = backtrack(0, set(), {})

    # End timer
    end_time = time.time()

    if result_mapping:
        result = {
            "left"                  : inputs,
            "right"                 : res,
            "operation"             : op,
            "mapping"               : dict(sorted(result_mapping.items())),
            "execution_time"        : f"{end_time - start_time:.3f}s"
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        return JSONResponse(content=result, headers=headers, status_code=200)
    else:
        result = {
            "error": "No solution found.",
            "execution_time": f"{end_time - start_time:.3f}s"
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        return JSONResponse(content=result, headers=headers, status_code=200)



def cryptarithm(a, res, op):
    input_raw = re.sub(r'\s+', '', filter_input(a, 1)).split(",")
    inputs = [s.upper() for s in input_raw]
    print(inputs)

    result = solve_cryptarithm(inputs, filter_input(res.upper(), 2), filter_op(op))
    return result



# debug

# input_left = "send, more"
# input_right = "money"
# input_op = "+"

# cryptarithm(input_left, input_right, input_op)
# print('ok')
