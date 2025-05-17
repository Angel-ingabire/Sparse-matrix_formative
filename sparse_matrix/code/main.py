from sparse_matrix import SparseMatrix
import os
import sys

def perform_sparse_matrix_operations():
    input_directory = 'sample_input'

    if not os.path.exists(input_directory):
        raise RuntimeError(f"Path not found: {os.path.abspath(input_directory)}")

    # Grab all the matrix .txt files 
    matrix_files = [file for file in os.listdir(input_directory) if file.endswith('.txt')]

    # make sure users select at least TWO files
    if len(matrix_files) < 2:
        print("Error: At least two matrix files must be present.")
        sys.exit(1)

    # Load dimensions of all matrices to help users identify compatible matrices
    matrix_dimensions = {}
    for file in matrix_files:
        try:
            matrix = SparseMatrix(file_path=os.path.join(input_directory, file))
            matrix_dimensions[file] = matrix.get_dimensions()
        except (ValueError, RuntimeError, FileNotFoundError) as error:
            print(f"Error: {error}")
            sys.exit(1)

    # show off all the available matrix files with dimensions
    print("\nAvailable Matrix Files:")
    for idx, filename in enumerate(matrix_files, 1):
        dimensions = matrix_dimensions[filename]
        print(f"{idx}. {filename} (Dimensions: {dimensions})")

    # ask the user to pick two matrices 
    try:
        first_choice = int(input("\nSelect the first matrix (enter number): "))
        second_choice = int(input("Select the second matrix (enter number): "))

        # Make sure the user isnt fooling around
        if not (1 <= first_choice <= len(matrix_files)) or not (1 <= second_choice <= len(matrix_files)):
            raise ValueError("Invalid selection. Please select valid matrix numbers.")

    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)

    # Getting the full paths of the chosen files 
    matrix_path_1 = os.path.join(input_directory, matrix_files[first_choice - 1])
    matrix_path_2 = os.path.join(input_directory, matrix_files[second_choice - 1])

    # Ask what mathematical operation the user wants to perform
    operation = input("\nChoose an operation (Add, Subtract, Multiply): ").strip().lower()

    # Load up the matrices 
    try:
        print("\nLoading selected matrices...")
        matrix_1 = SparseMatrix(file_path=matrix_path_1)
        matrix_2 = SparseMatrix(file_path=matrix_path_2)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"Unexpected error: {error}")
        sys.exit(1)

    # matrix dimensions
    print(f"\nMatrix 1 Dimensions: {matrix_1.get_dimensions()}")
    print(f"Matrix 2 Dimensions: {matrix_2.get_dimensions()}")

    # Quick check: Are these matrices even compatible for the operation?
    dims_1, dims_2 = matrix_1.get_dimensions(), matrix_2.get_dimensions()

    if operation in ['add', 'subtract'] and dims_1 != dims_2:
        print("Error: Matrices must share dimensions for addition or subtraction.")
        sys.exit(1)

    if operation == 'multiply' and dims_1[1] != dims_2[0]:
        print("Error: Matrix multiplication requires matching inner dimensions.")
        sys.exit(1)

    # Time to do the math
    try:
        if operation == 'add':
            result = matrix_1.add(matrix_2)
        elif operation == 'subtract':
            result = matrix_1.subtract(matrix_2)
        elif operation == 'multiply':
            result = matrix_1.multiply(matrix_2)
        else:
            print("Error: Unsupported operation.")
            sys.exit(1)

        # Here's your matrix, Thank you :)
        print("\nResulting Matrix:")
        result.display()

    except Exception as error:
        print(f"Error during matrix operation: {error}")
        sys.exit(1)

if __name__ == '__main__':
    perform_sparse_matrix_operations()