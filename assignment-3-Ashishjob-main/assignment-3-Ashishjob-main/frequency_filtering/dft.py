# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries
from dip import *
import math


class Dft:
    def __init__(self):
        pass

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""

        r, c = matrix.shape

        fourier_transform = zeros((r, c), dtype=complex)

        for row in range(r):
            for col in range(c):
                complex_sum = 0
                for i in range(r):
                    for j in range(c):
                        complex_sum += matrix[i, j] * complex(
                            math.cos(2 * math.pi * (row * i / r + col * j / c)),
                            -math.sin(2 * math.pi * (row * i / r + col * j / c))
                        )
                fourier_transform[row, col] = complex_sum

        return fourier_transform

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse fourier transform"""

        r, c = matrix.shape

        inverse_result = zeros((r, c), dtype=complex)

        for row in range(r):
            for col in range(c):
                complex_sum = 0
                for i in range(r):
                    for j in range(c):
                        complex_sum += matrix[i, j] * complex(
                            math.cos(2 * math.pi * (i * row / r + j * col / c)),
                            math.sin(2 * math.pi * (i * row / r + j * col / c))
                        )
                inverse_result[row, col] = complex_sum / (r * c)

        return inverse_result

    def magnitude(self, matrix):
        """Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the complex matrix"""

        r, c = matrix.shape

        magnitude_matrix = zeros((r, c), dtype=uint8)

        for i in range(r):
            for j in range(c):
                magnitude_matrix[i, j] = round(
                    math.sqrt(matrix[i, j].real ** 2 + matrix[i, j].imag ** 2)
                )

        return magnitude_matrix