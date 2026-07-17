print("1. addition")
print("2. subtraction")
print("3. multiplication")
print("4. division")

choice = input("Enter choice(1/2/3/4): ")
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
if choice == '1':
    print(num1, "+", num2, "=", num1 + num2)
elif choice == '2':
    print(num1, "-", num2, "=", num1 - num2)
elif choice == '3':
    print(num1, "*", num2, "=", num1 * num2)        
elif choice == '4':
    if num2 != 0:
        print(num1, "/", num2, "=", num1 / num2)
    else:
        print("Error: Division by zero is not allowed.")
        