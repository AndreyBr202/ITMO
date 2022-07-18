import random
your_try = 0
right_number = random.randint(1, 100)
your_number = 0
enter_try = int(input("Enter your try: "))

while your_try < enter_try:
    your_number = int(input("Enter your number: "))
    your_try += 1
    if your_number > right_number:
        print("Failure. Try again. Your number must be smaller.")
    elif your_number < right_number:
        print("Failure. Try again. Your number must be larger.")
    else:
        print("Congratulations!!!")
        print(f"You spent {your_try} tries")    
        break
else:
    print(f"Tries ended. Right number {right_number} ")

