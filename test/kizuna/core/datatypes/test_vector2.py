import unittest

from kizuna.core.datatypes import Vector2


class Vector2Tests(unittest.TestCase):

    def test_vector2_constructor_converts_to_float(self):
        # Act
        v = Vector2(1, 2.5)

        # Assert
        self.assertIsInstance(v.x, float)
        self.assertIsInstance(v.y, float)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.5)

    def test_vector2_as_tuple(self):
        # Arrange
        v = Vector2(1, 2.5)

        # Act
        v_tuple = tuple(v)

        # Assert
        self.assertIsInstance(v_tuple[0], float)
        self.assertIsInstance(v_tuple[1], float)
        self.assertEqual(v_tuple, (1.0, 2.5))

    def test_vector2_eq_with_vectors(self):
        # Arrange
        v = Vector2(2, 3.5)
        u = Vector2(2, 3.5)
        w = Vector2(5, -2)

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

    def test_vector2_eq_with_tuples(self):
        # Arrange
        v = Vector2(2, 3.5)
        u = (2, 3.5)
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

    def test_vector2_eq_with_lists(self):
        # Arrange
        v = Vector2(2, 3.5)
        u = [2, 3.5]
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

    def test_vector2_add_vector2(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = Vector2(4, -2)

        # Act
        result_a = v + u
        result_b = u + v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(5, 0.5))
        self.assertEqual(result_b, Vector2(5, 0.5))

    def test_vector2_add_tuple(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = (4, -2)

        # Act
        result_a = v + u
        result_b = u + v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(5, 0.5))
        self.assertEqual(result_b, Vector2(5, 0.5))

    def test_vector2_add_list(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = [4, -2]

        # Act
        result_a = v + u
        result_b = u + v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(5, 0.5))
        self.assertEqual(result_b, Vector2(5, 0.5))

    def test_vector2_sub_vector2(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = Vector2(4, -2)

        # Act
        result_a = v - u
        result_b = u - v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(-3, 4.5))
        self.assertEqual(result_b, Vector2(3, -4.5))

    def test_vector2_sub_tuple(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = (4, -2)

        # Act
        result_a = v - u
        result_b = u - v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(-3, 4.5))
        self.assertEqual(result_b, Vector2(3, -4.5))

    def test_vector2_sub_list(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = [4, -2]

        # Act
        result_a = v - u
        result_b = u - v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(-3, 4.5))
        self.assertEqual(result_b, Vector2(3, -4.5))

    def test_vector2_neg(self):
        # Arrange
        v = Vector2(1, 2.5)

        # Act
        result = -v

        # Assert
        self.assertIsInstance(result, Vector2)
        self.assertEqual(result, Vector2(-1, -2.5))

    def test_vector2_mul_by_scalar(self):
        # Arrange
        v = Vector2(1, 2.5)
        k = 3

        # Act
        result_a = v * k
        result_b = k * v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(3, 7.5))
        self.assertEqual(result_b, Vector2(3, 7.5))

    def test_vector2_mul_vector2(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = Vector2(4, -2)

        # Act
        result_a = v * u
        result_b = u * v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(4, -5))
        self.assertEqual(result_b, Vector2(4, -5))

    def test_vector2_mul_tuple(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = (4, -2)

        # Act
        result_a = v * u
        result_b = u * v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(4, -5))
        self.assertEqual(result_b, Vector2(4, -5))

    def test_vector2_mul_list(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = [4, -2]

        # Act
        result_a = v * u
        result_b = u * v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(4, -5))
        self.assertEqual(result_b, Vector2(4, -5))

    def test_vector2_div_by_scalar(self):
        # Arrange
        v = Vector2(6, -6)
        k = 3

        # Act
        result_a = v / k
        result_b = k / v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(2, -2))
        self.assertEqual(result_b, Vector2(1 / 2, -1 / 2))

    def test_vector2_div_vector2(self):
        # Arrange
        v = Vector2(12, 6)
        u = Vector2(4, -2)

        # Act
        result_a = v / u
        result_b = u / v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(3, -3))
        self.assertEqual(result_b, Vector2(1 / 3, -1 / 3))

    def test_vector2_div_tuple(self):
        # Arrange
        v = Vector2(12, 6)
        u = (4, -2)

        # Act
        result_a = v / u
        result_b = u / v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(3, -3))
        self.assertEqual(result_b, Vector2(1 / 3, -1 / 3))

    def test_vector2_div_list(self):
        # Arrange
        v = Vector2(12, 6)
        u = [4, -2]

        # Act
        result_a = v / u
        result_b = u / v

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(3, -3))
        self.assertEqual(result_b, Vector2(1 / 3, -1 / 3))
