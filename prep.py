# Functions
# def describe_person(**kwargs):
#     for k, v in kwargs.items():
#         print(f"{k} - {v}")
#
#
# describe_person(age=20, name='Asadbek')

# def calculate_price(price, discount=0, currency="USD"):
#     if discount > 0:
#         discounted = price - discount
#         print(f"Final price: {discounted} {currency}")
#
#     else:
#         print(f"Final price: {price} {currency}")

# def timer(func):
#     def wrapper():
#         print("Starting...")
#         func()
#         print("Done!")
#     return wrapper
#
#
# @timer
# def process_data():
#     print("Processing...")
#
#
# process_data()

# def validate(func):
#     def wrapper(*args, **kwargs):
#         for num in args:
#             if num <= 0:
#                 print("Invalid input!")
#                 return
#         result = func(*args, **kwargs)
#         return result
#     return wrapper
#
#
# @validate
# def multiply(a, b):
#     return a*b
#
#
# multiplication = multiply(-1, 2)
# multiplication

def even_numbers(n):
    for i in range(n+1):
        if i % 2 == 0:
            yield i


nex = even_numbers(11)
print(next(nex))
print(next(nex))
print(next(nex))

