from pprint import pprint

x = [(f'{m} * {n}', m * n) for m in range(1, 13) for n in range(1, 13)]
# x = [x * 3 for x in range(1, 13) if x % 2 == 0]
print(x)
print('Hello', 'World')




# x = [f'{str(m).rjust(2)} * {str(n).rjust(2)} = {str(m * n).rjust(3)}' for m in range(1, 13) for n in range(1, 13)]
# pprint(x)
#
#
# def do_it():
#     for m in range(1, 13):
#         print(m, end=' ')
#
#
# do_it()
