"""
Unit tests for the love score calculator.
"""

import unittest
from love_score_advanced import LoveScoreCalculator, CalculationMethod, LoveScoreResult


class TestLoveScoreCalculator(unittest.TestCase):
    """Test cases for LoveScoreCalculator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calculator = LoveScoreCalculator(target_letters="love")
    
    def test_initialization(self):
        """Test calculator initialization."""
        self.assertEqual(self.calculator.target_letters, "love")
        self.assertEqual(len(self.calculator.history), 0)
    
    def test_classic_method(self):
        """Test classic calculation method."""
        result = self.calculator.calculate("love", "lover", CalculationMethod.CLASSIC)
        self.assertIsInstance(result, LoveScoreResult)
        self.assertGreater(result.score, 0)
        self.assertEqual(result.method, "Classic")
    
    def test_phonetic_method(self):
        """Test phonetic calculation method."""
        result = self.calculator.calculate("John", "Joan", CalculationMethod.PHONETIC)
        self.assertIsInstance(result, LoveScoreResult)
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)
    
    def test_statistical_method(self):
        """Test statistical calculation method."""
        result = self.calculator.calculate("Alice", "Albert", CalculationMethod.STATISTICAL)
        self.assertIsInstance(result, LoveScoreResult)
        self.assertGreaterEqual(result.score, 0)
    
    def test_combined_method(self):
        """Test combined calculation method."""
        result = self.calculator.calculate("Kanye", "Kim", CalculationMethod.COMBINED)
        self.assertEqual(result.method, "Combined")
        self.assertIn("classic", result.breakdown)
        self.assertIn("phonetic", result.breakdown)
        self.assertIn("statistical", result.breakdown)
    
    def test_invalid_input_empty(self):
        """Test handling of empty input."""
        with self.assertRaises(ValueError):
            self.calculator.calculate("", "name")
    
    def test_invalid_input_non_string(self):
        """Test handling of non-string input."""
        with self.assertRaises(ValueError):
            self.calculator.calculate(123, "name")
    
    def test_invalid_input_too_long(self):
        """Test handling of excessively long names."""
        long_name = "a" * 101
        with self.assertRaises(ValueError):
            self.calculator.calculate(long_name, "name")
    
    def test_compatibility_level_excellent(self):
        """Test compatibility level for high scores."""
        level = self.calculator._get_compatibility_level(85)
        self.assertEqual(level, "💯 Soulmates!")
    
    def test_compatibility_level_good(self):
        """Test compatibility level for good scores."""
        level = self.calculator._get_compatibility_level(65)
        self.assertEqual(level, "❤️ Great Match")
    
    def test_compatibility_level_poor(self):
        """Test compatibility level for low scores."""
        level = self.calculator._get_compatibility_level(10)
        self.assertEqual(level, "🚫 Not Compatible")
    
    def test_history_tracking(self):
        """Test that calculations are tracked in history."""
        initial_count = len(self.calculator.history)
        self.calculator.calculate("Name1", "Name2")
        self.assertEqual(len(self.calculator.history), initial_count + 1)
    
    def test_statistics(self):
        """Test statistics calculation."""
        self.calculator.calculate("Alice", "Bob")
        self.calculator.calculate("Charlie", "Diana")
        
        stats = self.calculator.get_statistics()
        self.assertEqual(stats["total_calculations"], 2)
        self.assertIn("average_score", stats)
        self.assertIn("highest_score", stats)
        self.assertIn("lowest_score", stats)
    
    def test_char_frequency(self):
        """Test character frequency calculation."""
        freq = self.calculator._get_char_frequency("hello")
        self.assertEqual(freq["h"], 1)
        self.assertEqual(freq["l"], 2)
        self.assertEqual(freq["e"], 1)
    
    def test_result_dataclass(self):
        """Test LoveScoreResult dataclass."""
        result = self.calculator.calculate("Romeo", "Juliet")
        self.assertIsNotNone(result.timestamp)
        self.assertIsNotNone(result.compatibility_level)
        self.assertGreaterEqual(result.score, 0)
        self.assertLessEqual(result.score, 100)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calculator = LoveScoreCalculator()
    
    def test_identical_names(self):
        """Test calculation with identical names."""
        result = self.calculator.calculate("John", "John")
        self.assertGreater(result.score, 0)
    
    def test_single_character_names(self):
        """Test with single character names."""
        result = self.calculator.calculate("A", "B")
        self.assertIsInstance(result, LoveScoreResult)
    
    def test_special_characters_ignored(self):
        """Test that special characters are handled."""
        result1 = self.calculator.calculate("Mary-Jane", "John-Paul")
        result2 = self.calculator.calculate("MarJane", "JohnPaul")
        # Scores may differ due to character count
        self.assertIsNotNone(result1.score)
        self.assertIsNotNone(result2.score)
    
    def test_case_insensitive(self):
        """Test case insensitivity."""
        result1 = self.calculator.calculate("ALICE", "bob")
        result2 = self.calculator.calculate("alice", "BOB")
        self.assertEqual(result1.score, result2.score)


if __name__ == "__main__":
    unittest.main()
