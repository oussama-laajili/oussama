# test_main_c_module.py

import sys
import os

print("--- Testing main_c_module import and functionality ---")

# Add the current directory to sys.path to ensure the module can be found
# This is usually not necessary if the .so file is in the same directory as the script,
# but it's good practice for clarity or if running from a different location.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    import main_c_module
    print("\nSUCCESS: 'main_c_module' imported successfully!")

    print("\n--- Listing available attributes/functions in main_c_module ---")
    # dir() will show all attributes, including functions, exposed by the module
    available_items = [item for item in dir(main_c_module) if not item.startswith('__')]
    if available_items:
        print("The C module exposes the following (non-special) items:")
        for item in available_items:
            print(f" - {item}")
    else:
        print("The C module appears to expose no public functions/attributes.")
        print("This might mean main.c was not fully set up for Python interaction,")
        print("or it only exposes internal C structures.")


    print("\n--- Attempting to call placeholder functions ---")

    # Placeholder 1: A simple "hello world" or greeting function
    if hasattr(main_c_module, 'greet'):
        try:
            print("Trying to call main_c_module.greet('Ahmed')...")
            result = main_c_module.greet("Ahmed")
            print(f"  Result: {result}")
        except TypeError as e:
            print(f"  Error calling 'greet': Likely wrong arguments or signature. Error: {e}")
        except Exception as e:
            print(f"  An unexpected error occurred calling 'greet': {e}")
    else:
        print("Function 'greet' not found in main_c_module.")

    # Placeholder 2: A function that takes two numbers and returns a sum/product
    if hasattr(main_c_module, 'calculate_sum'): # Or 'add', 'multiply', etc.
        try:
            print("Trying to call main_c_module.calculate_sum(5, 7)...")
            result = main_c_module.calculate_sum(5, 7)
            print(f"  Result: {result}")
        except TypeError as e:
            print(f"  Error calling 'calculate_sum': Likely wrong arguments or signature. Error: {e}")
        except Exception as e:
            print(f"  An unexpected error occurred calling 'calculate_sum': {e}")
    else:
        print("Function 'calculate_sum' not found in main_c_module.")

    # Placeholder 3: A function that might run a more complex operation, like simulation
    if hasattr(main_c_module, 'run_simulation'):
        try:
            print("Trying to call main_c_module.run_simulation(100)...")
            # Assuming 'run_simulation' takes an integer argument, e.g., number of steps
            result = main_c_module.run_simulation(100)
            print(f"  Simulation result (if any): {result}")
        except TypeError as e:
            print(f"  Error calling 'run_simulation': Likely wrong arguments or signature. Error: {e}")
        except Exception as e:
            print(f"  An unexpected error occurred calling 'run_simulation': {e}")
    else:
        print("Function 'run_simulation' not found in main_c_module.")


    print("\n--- Test complete ---")

except ImportError as e:
    print(f"\nERROR: Could not import 'main_c_module'. This means:")
    print(f"1. The .so file ('main_c_module.cpython-312-x86_64-linux-gnu.so') might not be in the current directory.")
    print(f"2. The C code in 'main.c' was not correctly structured using the Python C API.")
    print(f"3. There might be missing C dependencies (shared libraries) that the .so file needs.")
    print(f"  Details: {e}")
except Exception as e:
    print(f"\nAn unexpected error occurred during module import: {e}")