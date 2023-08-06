import numpy as np

class Matrix:
    """ 
    Matrix class for calculating matrix operations
    
    Attributes:
        columns (integer) represnting the number of the columns of the matrix
        rows (integer) represnting the number of the rows of the matrix
        m_values (Array) represnting an array containg the matrix's values at each position
    """
    def __init__(self, cols, rows):
        self.columns = cols
        self.rows = rows
        self.m_values = np.array([[0 for i in range(cols)] for j in range(rows)])
        
    def multiplication(self, other):
        """
        Function to calculate the multiplication of the matrices
        
        Args:
            other (Matrix): the second matrix to be multiplied with the matrix
            
        Returns:
            Matrix: the new matrix 
        
        """
        new_matrix = Matrix(other.columns, self.rows)
        new_matrix.m_values = np.dot(self.m_values,other.m_values)
        return new_matrix
    
    def __add__(self, other):
        """
        Function to add together two matrices
		
		Args:
			other (Matrix): Matrix instance
			
		Returns:
			Matrix: Matrix instance
			
		"""
        if self.columns != other.columns or self.rows != other.rows:
            print('Columns or rows of the two matrices does not match!')
            return
        new_matrix = Matrix(self.columns, self.rows)
        new_matrix.m_values = np.add(self.m_values, other.m_values)
        
        return new_matrix
        
    def __sub__(self, other):
        """
        Function to subtract two matrices
		
		Args:
			other (Matrix): Matrix instance
			
		Returns:
			Matrix: Matrix instance
			
		"""
        if self.columns != other.columns or self.rows != other.rows:
            print('Columns or rows of the two matrices does not match!')
            return
        new_matrix = Matrix(self.columns, self.rows)
        new_matrix.m_values = np.subtract(self.m_values, other.m_values)
        
        return new_matrix    
    
    def calculate_determinant(self):
        """
        Function to calculate the determinant of a matrix
		
		Args:
			none
			
		Returns:
			Integer: The determinant 
			
		"""
        if self.columns != self.rows:
            return
        else:
            if self.columns == 2:
                return self.m_values[0][0]*self.m_values[1][1] - self.m_values[0][1] * self.m_values[1][0]
            elif self.columns == 3:
                a_one = self.m_values[1][1]*self.m_values[2][2] - self.m_values[1][2] * self.m_values[2][1]
                a_two = self.m_values[1][0]*self.m_values[2][2] - self.m_values[1][2] * self.m_values[2][0]
                a_three = self.m_values[1][0]*self.m_values[2][1] - self.m_values[1][1] * self.m_values[2][0]

                det = self.m_values[0][0]*a_one - self.m_values[0][1]*a_two + self.m_values[0][2]*a_three
                return det
            else:
                return np.linalg.det(self.m_values)
            
    def get_inverse(self):
        """
        Function to get the inverse of a matrix
		
		Args:
			none
			
		Returns:
			Matrix: Matrix instance
			
		"""
        if self.columns != self.rows:
            print('The matrix is not a square matrix, so it\'s not invertible')
            return
        elif self.calculate_determinant() == 0:
            print('The determinant of th matrix is equal to zero, so it\'s not invertible')
            return
        else:
            new_matrix = Matrix(self.columns, self.rows)
            new_matrix.m_values = np.linalg.inv(self.m_values)
            return new_matrix
    def __repr__(self):
        """
        Function to output the characteristics of the Matrix instance
		
		Args:
			none
			
		Returns:
			string: characteristics of the Matrix
			
		"""  
        return "{} a {}x{} matrix with a determinant of {}".format(self.m_values, self.rows, self.columns, self.calculate_determinant())

                
                
            
        
        
    