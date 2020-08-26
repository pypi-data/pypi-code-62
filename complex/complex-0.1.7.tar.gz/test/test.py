import unittest
from complex.complex import Complex

class TestComplex(unittest.TestCase):
	def complex(self):
		x, y = Complex(2, 1), Complex(5, 6)
		su, sub, mul, div, mod_x, mod_y = x+y, x-y, x*y, x/y, x.mod(), y.mod()
		self.assertEqual(su, '7.00+7.00i')
		self.assertEqual(sub, '-3.00-5.00i')
		self.assertEqual(mul, '4.00+17.00i')
		self.assertEqual(div, '0.26-0.11i')
		self.assertEqual(mod_x, '2.24+0.00i')
		self.assertEqual(mod_y, '7.81+0.00i')


if __name__ == '__main__':
	unittest.main()








