import unittest

from kizuna.core.datatypes import IVector2


class IVector2Tests(unittest.TestCase):

    def test_ivector2_constructor_converts_to_int(self):
        # Act
        v = IVector2(1, 3)

        # Assert
        self.assertIsInstance(v.x, int)
        self.assertIsInstance(v.y, int)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 3)

    def test_ivector2_as_tuple(self):
        # Arrange
        v = IVector2(1, 3)

        # Act
        v_tuple = tuple(v)

        # Assert
        self.assertIsInstance(v_tuple[0], int)
        self.assertIsInstance(v_tuple[1], int)
        self.assertEqual((1, 3), v_tuple)

    def test_ivector2_eq_with_vectors(self):
        # Arrange
        v = IVector2(2, 3)
        u = IVector2(2, 3)
        w = IVector2(5, -2)

        # Act
        u_equals_v = u == v
        v_equals_u = v == u
        w_equals_u = w == u
        u_equals_w = u == w

        # Assert
        self.assertTrue(u_equals_v)
        self.assertTrue(v_equals_u)
        self.assertFalse(w_equals_u)
        self.assertFalse(u_equals_w)

    def test_ivector2_eq_with_tuples(self):
        # Arrange
        v = IVector2(2, 3)
        u = (2, 3)
        w = (5, -2)

        # Act
        u_equals_v = u == v
        v_equals_u = v == u
        w_equals_u = w == u
        u_equals_w = u == w

        # Assert
        self.assertTrue(u_equals_v)
        self.assertTrue(v_equals_u)
        self.assertFalse(w_equals_u)
        self.assertFalse(u_equals_w)

    def test_ivector2_eq_with_lists(self):
        # Arrange
        v = IVector2(2, 3)
        u = [2, 3]
        w = [5, -2]

        # Act
        u_equals_v = u == v
        v_equals_u = v == u
        w_equals_u = w == u
        u_equals_w = u == w

        # Assert
        self.assertTrue(u_equals_v)
        self.assertTrue(v_equals_u)
        self.assertFalse(w_equals_u)
        self.assertFalse(u_equals_w)

    def test_ivector2_add_ivector2(self):
        # Arrange
        v = IVector2(1, 2)
        u = IVector2(4, -2)

        # Act
        result_a = v + u
        result_b = u + v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(5, 0), result_a)
        self.assertEqual(IVector2(5, 0), result_b)

    def test_ivector2_add_tuple(self):
        # Arrange
        v = IVector2(1, 2)
        u = (4, -2)

        # Act
        result_a = v + u
        result_b = u + v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(5, 0), result_a)
        self.assertEqual(IVector2(5, 0), result_b)

    def test_ivector2_add_list(self):
        # Arrange
        v = IVector2(1, 2)
        u = [4, -2]

        # Act
        result_a = v + u
        result_b = u + v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(5, 0), result_a)
        self.assertEqual(IVector2(5, 0), result_b)

    def test_ivector2_pos(self):
        # Arrange
        v = IVector2(1, 2)

        # Act
        result = +v

        # Assert
        self.assertIsInstance(result, IVector2)
        self.assertEqual(IVector2(1, 2), result)

    def test_ivector2_sub_ivector2(self):
        # Arrange
        v = IVector2(1, 2)
        u = IVector2(4, -2)

        # Act
        result_a = v - u
        result_b = u - v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(-3, 4), result_a)
        self.assertEqual(IVector2(3, -4), result_b)

    def test_ivector2_sub_tuple(self):
        # Arrange
        v = IVector2(1, 2)
        u = (4, -2)

        # Act
        result_a = v - u
        result_b = u - v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(-3, 4), result_a)
        self.assertEqual(IVector2(3, -4), result_b)

    def test_ivector2_sub_list(self):
        # Arrange
        v = IVector2(1, 2)
        u = [4, -2]

        # Act
        result_a = v - u
        result_b = u - v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(-3, 4), result_a)
        self.assertEqual(IVector2(3, -4), result_b)

    def test_ivector2_neg(self):
        # Arrange
        v = IVector2(1, 2)

        # Act
        result = -v

        # Assert
        self.assertIsInstance(result, IVector2)
        self.assertEqual(IVector2(-1, -2), result)

    def test_ivector2_mul_by_scalar(self):
        # Arrange
        v = IVector2(1, 2)
        k = 3

        # Act
        result_a = v * k
        result_b = k * v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(3, 6), result_a)
        self.assertEqual(IVector2(3, 6), result_b)

    def test_ivector2_mul_ivector2(self):
        # Arrange
        v = IVector2(1, 2)
        u = IVector2(4, -2)

        # Act
        result_a = v * u
        result_b = u * v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(4, -4), result_a)
        self.assertEqual(IVector2(4, -4), result_b)

    def test_ivector2_mul_tuple(self):
        # Arrange
        v = IVector2(1, 2)
        u = (4, -2)

        # Act
        result_a = v * u
        result_b = u * v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(4, -4), result_a)
        self.assertEqual(IVector2(4, -4), result_b)

    def test_ivector2_mul_list(self):
        # Arrange
        v = IVector2(1, 2)
        u = [4, -2]

        # Act
        result_a = v * u
        result_b = u * v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(4, -4), result_a)
        self.assertEqual(IVector2(4, -4), result_b)

    def test_ivector2_div_by_scalar(self):
        # Arrange
        v = IVector2(6, -6)
        k = 3

        # Act
        result_a = v // k
        result_b = k // v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(2, -2), result_a)
        self.assertEqual(IVector2(3 // 6, 3 // (-6)), result_b)

    def test_ivector2_div_ivector2(self):
        # Arrange
        v = IVector2(12, 6)
        u = IVector2(4, -2)

        # Act
        result_a = v // u
        result_b = u // v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(3, -3), result_a)
        self.assertEqual(IVector2(3 // 6, 3 // (-6)), result_b)

    def test_ivector2_div_tuple(self):
        # Arrange
        v = IVector2(12, 6)
        u = (4, -2)

        # Act
        result_a = v // u
        result_b = u // v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(3, -3), result_a)
        self.assertEqual(IVector2(3 // 6, 3 // (-6)), result_b)

    def test_ivector2_div_list(self):
        # Arrange
        v = IVector2(12, 6)
        u = [4, -2]

        # Act
        result_a = v // u
        result_b = u // v

        # Assert
        self.assertIsInstance(result_a, IVector2)
        self.assertIsInstance(result_b, IVector2)
        self.assertEqual(IVector2(3, -3), result_a)
        self.assertEqual(IVector2(3 // 6, 3 // (-6)), result_b)
