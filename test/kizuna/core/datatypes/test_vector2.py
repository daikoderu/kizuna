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
        v_tuple = v.as_tuple

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

    def test_vector2_add_tuple(self):
        # Arrange
        v = Vector2(1, 2.5)
        u = Vector2(4, -2)

        # Act
        result_a = v + u
        result_b = v + u

        # Assert
        self.assertIsInstance(result_a, Vector2)
        self.assertIsInstance(result_b, Vector2)
        self.assertEqual(result_a, Vector2(5, 0.5))
        self.assertEqual(result_b, Vector2(5, 0.5))

