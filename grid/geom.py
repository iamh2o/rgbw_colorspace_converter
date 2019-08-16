from typing import NamedTuple


class Geometry(NamedTuple):
    """
    Geometry represents the dimensions of a panel or side of the car.
    """

    rows: int

    def row_length(self, n: int) -> int:
        if n < 0 or n >= self.rows:
            raise IndexError(f'row {n} out of range ({self.rows} rows total)')

        return (n + 1) * 2 - 1

    def midpoint(self, row: int) -> int:
        length = self.row_length(row)
        return int(length - (length / 2))

    @property
    def cell_count(self) -> int:
        return sum(self.row_length(i) for i in range(self.rows))

    @staticmethod
    def triangular_number(n: int) -> int:
        """Returns the number of elements in an equilateral triangle of n rows."""
        # Typically the triangle number is (n(n+1))/2 but our triangle has rows of 1, 3, 5...
        return n ** 2
