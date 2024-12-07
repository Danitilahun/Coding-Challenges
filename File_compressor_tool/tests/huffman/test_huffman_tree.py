import unittest
from hamcrest import assert_that, equal_to
from parameterized import parameterized
from src.huffman.huffman_coding_trees import HuffmanTree
from src.huffman.huffman_node import HuffmanNode

class TestHuffmanTree(unittest.TestCase):
    @parameterized.expand([
        (
            "single_character",
            {"a": 5},
            {"a": "0"},
            "L'a'"
        ),
        (
            "two_characters",
            {"a": 5, "b": 2},
            {"b": "0", "a": "1"},
            "IL'b'L'a'"
        ),
        (
            "three_characters",
            {"a": 5, "b": 2, "c": 1},
            {"c": "00", "b": "01", "a": "1"},
            "IIL'c'L'b'L'a'"
        ),
        (
            "four_characters",
            {"a": 9, "b": 5, "c": 2, "d": 1},
            {"d": "000", "c": "001", "b": "01", "a": "1"},
            "IIIL'd'L'c'L'b'L'a'"
        ),
        (
            "multiple_characters_with_same_frequency",
            {"a": 3, "b": 3, "c": 3},
            {"c": "0", "a": "10", "b": "11"},
            "IL'c'IL'a'L'b'"
        ),
    ])
    def test_build_tree_and_generate_prefix_code_table(self, name, frequencies, expected_code_table, expected_serialized_tree):
        """
        Test Huffman tree construction, prefix code generation, and serialization.
        """
        huffman_tree = HuffmanTree(frequencies)
        huffman_tree.build_tree()
        
        code_table = huffman_tree.generate_prefix_code_table()
        assert_that(code_table, equal_to(expected_code_table))
        
        serialized_tree = huffman_tree.serialize_tree()
        assert_that(serialized_tree, equal_to(expected_serialized_tree))


    def test_build_tree_empty_frequencies(self):
        """
        Test building a Huffman tree with an empty frequency dictionary.
        Expecting root to remain None.
        """
        huffman_tree = HuffmanTree({})
        huffman_tree.build_tree()
        assert_that(huffman_tree.root, equal_to(None))

    @parameterized.expand([
        (
            "invalid_frequency_zero",
            {"a": 0, "b": 2},
            "a"
        ),
        (
            "invalid_frequency_negative",
            {"a": -1, "b": 2},
            "a"
        ),
    ])
    def test_build_tree_with_invalid_frequencies(self, name, frequencies, invalid_char):
        """
        Test building a Huffman tree with invalid frequencies (zero or negative).
        Expecting ValueError to be raised.
        """
        huffman_tree = HuffmanTree(frequencies)
        with self.assertRaises(ValueError) as context:
            huffman_tree.build_tree()
        
        self.assertIn(f"Invalid frequency for character '{invalid_char}'", str(context.exception))

    def test_generate_prefix_code_table_before_building_tree(self):
        """
        Test generating prefix code table before building the tree.
        Expecting an empty code table.
        """
        huffman_tree = HuffmanTree({"a": 5})
        # Intentionally not calling build_tree
        code_table = huffman_tree.generate_prefix_code_table()
        assert_that(code_table, equal_to({}))

    def test_serialize_tree_before_building_tree(self):
        """
        Test serializing the tree before building it.
        Expecting an empty string.
        """
        huffman_tree = HuffmanTree({"a": 5})
        # Intentionally not calling build_tree
        serialized_tree = huffman_tree.serialize_tree()
        assert_that(serialized_tree, equal_to(""))

    def test_huffman_node_is_leaf(self):
        """
        Test the is_leaf method of HuffmanNode.
        """
        leaf_node = HuffmanNode(weight=5, element='a')
        internal_node = HuffmanNode(weight=10, left=leaf_node, right=leaf_node)
        
        assert_that(leaf_node.is_leaf(), equal_to(True))
        assert_that(internal_node.is_leaf(), equal_to(False))

    def test_huffman_node_comparison(self):
        """
        Test the comparison of HuffmanNode instances based on weight and order.
        """
        node1 = HuffmanNode(weight=5, element='a')
        node2 = HuffmanNode(weight=10, element='b')
        node3 = HuffmanNode(weight=5, element='c')  # Same weight as node1
        
        # node1 should be less than node2
        assert_that(node1 < node2, equal_to(True))
        
        # node2 should not be less than node1
        assert_that(node2 < node1, equal_to(False))
        
        # node1 should be less than node3 based on order
        assert_that(node1 < node3, equal_to(True))
        
        # node3 should not be less than node1
        assert_that(node3 < node1, equal_to(False))

    def test_serialize_tree_with_complex_tree(self):
        """
        Test serialization of a complex Huffman tree.
        """
        # Create a more complex Huffman tree
        # Example:
        #        *
        #       / \
        #      *   *
        #     / \ / \
        #    a  b c  d
        node_a = HuffmanNode(weight=4, element='a')
        node_b = HuffmanNode(weight=4, element='b')
        node_c = HuffmanNode(weight=4, element='c')
        node_d = HuffmanNode(weight=4, element='d')
        internal_left = HuffmanNode(weight=8, left=node_a, right=node_b)
        internal_right = HuffmanNode(weight=8, left=node_c, right=node_d)
        root = HuffmanNode(weight=16, left=internal_left, right=internal_right)

        huffman_tree = HuffmanTree({"a":4, "b":4, "c":4, "d":4})
        huffman_tree.root = root  # Manually set the root without calling build_tree

        # Corrected expected serialization: "IIL'a'L'b'IL'c'L'd'"
        expected_serialized_tree = "IIL'a'L'b'IL'c'L'd'"
        serialized_tree = huffman_tree.serialize_tree()
        assert_that(serialized_tree, equal_to(expected_serialized_tree))


        huffman_tree = HuffmanTree({"a":4, "b":4, "c":4, "d":4})
        huffman_tree.root = root  # Manually set the root without calling build_tree

        # Corrected expected serialization: "IIL'a'L'b'IL'c'L'd'"
        expected_serialized_tree = "IIL'a'L'b'IL'c'L'd'"
        serialized_tree = huffman_tree.serialize_tree()
        assert_that(serialized_tree, equal_to(expected_serialized_tree))


    def test_serialize_tree_with_complex_tree(self):
        """
        Test serialization of a complex Huffman tree.
        """
        # Create a more complex Huffman tree
        # Example:
        #        *
        #       / \
        #      *   *
        #     / \ / \
        #    a  b c  d
        node_a = HuffmanNode(weight=4, element='a')
        node_b = HuffmanNode(weight=4, element='b')
        node_c = HuffmanNode(weight=4, element='c')
        node_d = HuffmanNode(weight=4, element='d')
        internal_left = HuffmanNode(weight=8, left=node_a, right=node_b)
        internal_right = HuffmanNode(weight=8, left=node_c, right=node_d)
        root = HuffmanNode(weight=16, left=internal_left, right=internal_right)

        huffman_tree = HuffmanTree({"a":4, "b":4, "c":4, "d":4})
        huffman_tree.root = root  # Manually set the root without calling build_tree

        # Corrected expected serialization: "IIL'a'L'b'IL'c'L'd'"
        expected_serialized_tree = "IIL'a'L'b'IL'c'L'd'"
        serialized_tree = huffman_tree.serialize_tree()
        assert_that(serialized_tree, equal_to(expected_serialized_tree))


    @parameterized.expand([
        (
            "empty_string",
            {},
            {},
            ""
        ),
        (
            "single_character",
            {"a": 1},
            {"a": "0"},
            "L'a'"
        ),
        (
            "two_characters",
            {"a": 2, "b": 1},
            {"b": "0", "a": "1"},
            "IL'b'L'a'"
        ),
    ])
    def test_serialize_tree_various_cases(self, name, frequencies, expected_code_table, expected_serialized_tree):
        """
        Parameterized test for serialize_tree method with various frequency dictionaries.
        """
        huffman_tree = HuffmanTree(frequencies)
        huffman_tree.build_tree()
        serialized_tree = huffman_tree.serialize_tree()
        assert_that(serialized_tree, equal_to(expected_serialized_tree))

    def test_generate_prefix_code_table_multiple_levels(self):
        """
        Test prefix code generation for a tree with multiple levels.
        """
        # Tree structure:
        #        *
        #       / \
        #      *   c
        #     / \
        #    a   b
        node_a = HuffmanNode(weight=3, element='a')
        node_b = HuffmanNode(weight=2, element='b')
        node_c = HuffmanNode(weight=1, element='c')
        internal_node = HuffmanNode(weight=5, left=node_a, right=node_b)
        root = HuffmanNode(weight=6, left=internal_node, right=node_c)
        
        huffman_tree = HuffmanTree({"a":3, "b":2, "c":1})
        huffman_tree.root = root  # Manually set the root without calling build_tree
        
        expected_code_table = {
            "a": "00",
            "b": "01",
            "c": "1"
        }
        
        code_table = huffman_tree.generate_prefix_code_table()
        assert_that(code_table, equal_to(expected_code_table))

    def test_generate_prefix_code_table_with_duplicate_frequencies(self):
        """
        Test prefix code generation when multiple characters have the same frequency.
        """
        frequencies = {"a": 2, "b": 2, "c": 2}
        huffman_tree = HuffmanTree(frequencies)
        huffman_tree.build_tree()
        
        code_table = huffman_tree.generate_prefix_code_table()
        
        # Since frequencies are the same, the exact codes may vary based on insertion order
        # We'll check that all codes are unique and prefix-free
        codes = list(code_table.values())
        self.assertEqual(len(codes), len(set(codes)), "All codes should be unique.")
        
        for i in range(len(codes)):
            for j in range(len(codes)):
                if i != j:
                    self.assertFalse(codes[i].startswith(codes[j]), "Codes should be prefix-free.")

    def test_serialize_tree_empty_tree(self):
        """
        Test serialization of an empty Huffman tree.
        Expecting an empty string.
        """
        huffman_tree = HuffmanTree({})
        huffman_tree.build_tree()
        serialized_tree = huffman_tree.serialize_tree()
        assert_that(serialized_tree, equal_to(""))

    def test_build_tree_with_single_character(self):
        """
        Test building a Huffman tree with a single character.
        """
        frequencies = {"a": 10}
        huffman_tree = HuffmanTree(frequencies)
        huffman_tree.build_tree()
        
        # The root should be a leaf node
        root = huffman_tree.root
        assert_that(root.is_leaf(), equal_to(True))
        assert_that(root.element, equal_to("a"))
        assert_that(root.weight, equal_to(10))
        
        # Prefix code table should have 'a' mapped to '0'
        code_table = huffman_tree.generate_prefix_code_table()
        assert_that(code_table, equal_to({"a": "0"}))
        
        # Serialization should be "L'a'"
        serialized_tree = huffman_tree.serialize_tree()
        assert_that(serialized_tree, equal_to("L'a'"))

    def test_build_tree_with_multiple_characters(self):
        """
        Test building a Huffman tree with multiple characters.
        """
        frequencies = {"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45}
        huffman_tree = HuffmanTree(frequencies)
        huffman_tree.build_tree()
        
        # Generate prefix codes
        code_table = huffman_tree.generate_prefix_code_table()
        
        # Expected prefix codes based on standard Huffman coding
        # Note: Actual codes may vary based on the implementation, but no code should be a prefix of another
        # We'll validate that all codes are prefix-free
        codes = list(code_table.values())
        for i in range(len(codes)):
            for j in range(len(codes)):
                if i != j:
                    assert_that(not codes[i].startswith(codes[j]), "Prefix condition violated")

if __name__ == "__main__":
    unittest.main()
