# get 10 number
import math

numbers = []
for i in range(10):
    numbers.append(int(input()))


def get_prime_numbers(inp_number):
    ceil = math.ceil(math.sqrt(inp_number))
    if inp_number == 1:
        return False
    elif inp_number == 2:
        return True

    for num in range(2, ceil + 1):
        if (inp_number % num) == 0:
            return False
    return True


def get_prime_divisors(inp_number):
    prime_divisors = []
    for num in range(2, inp_number + 1):
        if get_prime_numbers(num) and (inp_number % num) == 0:
            prime_divisors.append(num)
    return len(prime_divisors)


final_result = []

for number in numbers:
    final_result.append((number, get_prime_divisors(number)))

# sort the final result first by the number of prime divisors and then by the number itself in descending order
final_result.sort(key=lambda x: (x[1], x[0]), reverse=True)

print(final_result[0][0], final_result[0][1])
