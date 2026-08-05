import random
import time

#decorator
def pylog(func):
    def wrapper(*args, **kwargs):
        print("\n" + "=" * 40)
        print(f"[CALL]   {func.__name__.upper()}")
        print(f"[ARGS]   {args}")
        print(f"[KWARGS] {kwargs}")

        start = time.perf_counter()
        result = None
        error = None

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error = e
            print(f"[ERROR]  {func.__name__} crashed: {e}")
        finally:
            end = time.perf_counter()
            duration = (end - start) * 1000

            print(f"[TIME]   {duration:.2f} ms")

            if error is None:
                print(f"[RESULT] {result}")

            print("=" * 40)

        return result
    return wrapper



def get_number(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Ungültige Zahl!")
        return None
#funcs

@pylog
def greet(name):
    print(f"Hello {name}")

@pylog
def add(a, b):
    return a + b

@pylog
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Division by zero!")
        return None

@pylog
def random_wait():
    t = random.uniform(0.1, 0.5)
    time.sleep(t)
    return f"Waited {t:.2f} seconds"
#menu
def menu():
    while True:
        print("\nPyLog Demo")
        print("1. Greet")
        print("2. Add")
        print("3. Divide")
        print("4. Random Wait")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            greet(name)

        elif choice == "2":
            a = get_number("Enter a number: ")
            b = get_number("Enter another number: ")
            if a is not None and b is not None:
                add(a, b)

        elif choice == "3":
            a = get_number("Enter a number: ")
            b = get_number("Enter another number: ")
            if a is not None and b is not None:
                divide(a, b)

        elif choice == "4":
            random_wait()

        elif choice == "5":
            print("Bye bye")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()
