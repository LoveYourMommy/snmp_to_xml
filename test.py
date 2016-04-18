input = input("Filter items: ") or 'default'
input_list = input.split(' ')
numbers = [x.strip() for x in input_list]
print(numbers)