class SparseMatrix:
    def __init__(self, file_path=None):
        """
        Initialize a sparse matrix from an input file or as an empty matrix.
        """
        self.data = {}  # Store non-zero elements
        self.dimensions = (0, 0)

        if file_path:
            try:
                self._load_from_file(file_path)
                print(f"Matrix loaded successfully from '{file_path}' with dimensions {self.dimensions}.")
            except (FileNotFoundError, ValueError) as e:
                raise RuntimeError(f"Error initializing matrix: {e}")

    def _load_from_file(self, file_path):
        """
        Load matrix dimensions and non-zero values from an input file.
        """
        with open(file_path, 'r') as file:
            rows = cols = 0
            for line in file:
                line = line.strip()

                if line.startswith('rows='):
                    rows = int(line.split('=')[1])
                elif line.startswith('cols='):
                    cols = int(line.split('=')[1])
                elif line and '=' not in line and not line.startswith('#'):
                    try:
                        row, col, value = map(int, line.strip('()').split(','))
                        self.data[(row, col)] = value
                    except ValueError:
                        raise ValueError("Invalid matrix data format.")

            if rows == 0 or cols == 0:
                raise ValueError("Matrix dimensions must be specified.")

            self.dimensions = (rows, cols)

    def get_dimensions(self):
        """
        Return matrix dimensions as rows and cols.
        """
        return self.dimensions

    def _validate_operation(self, other_matrix, operation):
        """
        Validate matrix dimensions for the given operation.
        """
        if operation in ['add', 'subtract'] and self.dimensions != other_matrix.dimensions:
            raise ValueError("Matrices must be compatible (have matching dimensions) for addition or subtraction.")
        elif operation == 'multiply' and self.dimensions[1] != other_matrix.dimensions[0]:
            raise ValueError("Matrix multiplication requires compatible (matching) dimensions.")

    def _combine_matrices(self, other_matrix, operator):
        """
        Combine two matrices using the specified operation ('add' or 'subtract').
        """
        result = SparseMatrix()
        result.dimensions = self.dimensions

        for position, value in self.data.items():
            result.data[position] = value

        for position, value in other_matrix.data.items():
            if operator == 'add':
                result.data[position] = result.data.get(position, 0) + value
            elif operator == 'subtract':
                result.data[position] = result.data.get(position, 0) - value

        return result

    def add(self, other_matrix):
        """
        Add to another matrix and return the result.
        """
        self._validate_operation(other_matrix, 'add')
        return self._combine_matrices(other_matrix, 'add')

    def subtract(self, other_matrix):
        """
        Subtract from another matrix and return the result.
        """
        self._validate_operation(other_matrix, 'subtract')
        return self._combine_matrices(other_matrix, 'subtract')

    def multiply(self, other_matrix):
        """
        Multiply with another matrix and return the result.
        """
        self._validate_operation(other_matrix, 'multiply')

        result = SparseMatrix()
        result.dimensions = (self.dimensions[0], other_matrix.dimensions[1])

        for (i, k), value_a in self.data.items():
            for (j, l), value_b in other_matrix.data.items():
                if k == j:
                    result.data[(i, l)] = result.data.get((i, l), 0) + value_a * value_b

        return result

    def display(self):
        """
        Display the matrix in proper (row, col, value) format.
        """
        print(f"rows={self.dimensions[0]}")
        print(f"cols={self.dimensions[1]}")
        for (row, col), value in sorted(self.data.items()):
            print(f"({row}, {col}, {value})")
