"""
Advanced Love Score Calculator
Provides multiple algorithms and comprehensive features for calculating compatibility scores.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
import hashlib


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('love_score.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CalculationMethod(Enum):
    """Available calculation methods for love score."""
    CLASSIC = "classic"
    PHONETIC = "phonetic"
    STATISTICAL = "statistical"
    COMBINED = "combined"


@dataclass
class LoveScoreResult:
    """Data class for love score results."""
    name1: str
    name2: str
    score: float
    method: str
    breakdown: Dict[str, float]
    timestamp: str
    compatibility_level: str


class LoveScoreCalculator:
    """
    Advanced love score calculator with multiple algorithms.
    """
    
    def __init__(self, target_letters: str = "love"):
        """
        Initialize the calculator.
        
        Args:
            target_letters: Letters to search for in names
        """
        self.target_letters = target_letters.lower()
        self.history: list[LoveScoreResult] = []
        logger.info(f"Calculator initialized with target letters: {self.target_letters}")
    
    def _validate_input(self, name1: str, name2: str) -> None:
        """
        Validate input names.
        
        Args:
            name1: First name
            name2: Second name
            
        Raises:
            ValueError: If names are invalid
        """
        if not isinstance(name1, str) or not isinstance(name2, str):
            raise ValueError("Names must be strings")
        if not name1.strip() or not name2.strip():
            raise ValueError("Names cannot be empty")
        if len(name1) > 100 or len(name2) > 100:
            raise ValueError("Names must be less than 100 characters")
        logger.debug(f"Input validation passed for: {name1}, {name2}")
    
    def _classic_method(self, name1: str, name2: str) -> Tuple[float, Dict]:
        """
        Classic method: Count target letters in both names.
        
        Args:
            name1: First name
            name2: Second name
            
        Returns:
            Tuple of (score, breakdown dict)
        """
        combined = (name1 + name2).lower()
        total_letters = len(combined)
        
        if total_letters == 0:
            return 0.0, {"matching_letters": 0, "total_letters": 0}
        
        matching_count = sum(1 for letter in combined if letter in self.target_letters)
        score = (matching_count / total_letters) * 100
        
        return score, {
            "matching_letters": matching_count,
            "total_letters": total_letters,
            "percentage": score
        }
    
    def _phonetic_method(self, name1: str, name2: str) -> Tuple[float, Dict]:
        """
        Phonetic method: Analyze phonetic similarity using name length ratio.
        
        Args:
            name1: First name
            name2: Second name
            
        Returns:
            Tuple of (score, breakdown dict)
        """
        len1 = len(name1)
        len2 = len(name2)
        max_len = max(len1, len2)
        
        if max_len == 0:
            return 0.0, {"length_similarity": 0}
        
        # Calculate length-based similarity
        length_similarity = min(len1, len2) / max_len * 100
        
        # Count vowels for additional phonetic analysis
        vowels = "aeiouAEIOU"
        vowel_count1 = sum(1 for c in name1 if c in vowels)
        vowel_count2 = sum(1 for c in name2 if c in vowels)
        vowel_ratio = (min(vowel_count1, vowel_count2) / max(1, max(vowel_count1, vowel_count2))) * 100
        
        score = (length_similarity + vowel_ratio) / 2
        
        return score, {
            "length_similarity": length_similarity,
            "vowel_similarity": vowel_ratio,
            "combined": score
        }
    
    def _statistical_method(self, name1: str, name2: str) -> Tuple[float, Dict]:
        """
        Statistical method: Advanced character frequency analysis.
        
        Args:
            name1: First name
            name2: Second name
            
        Returns:
            Tuple of (score, breakdown dict)
        """
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        # Get character frequencies
        freq1 = self._get_char_frequency(name1_lower)
        freq2 = self._get_char_frequency(name2_lower)
        
        # Calculate similarity using intersection
        common_chars = set(freq1.keys()) & set(freq2.keys())
        
        if not common_chars:
            return 0.0, {"common_characters": 0, "similarity": 0}
        
        similarity = len(common_chars) / max(len(freq1), len(freq2)) * 100
        
        return similarity, {
            "common_characters": len(common_chars),
            "name1_unique_chars": len(freq1),
            "name2_unique_chars": len(freq2),
            "similarity": similarity
        }
    
    def _get_char_frequency(self, text: str) -> Dict[str, int]:
        """
        Calculate character frequency in text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of character frequencies
        """
        frequency = {}
        for char in text:
            if char.isalpha():
                frequency[char] = frequency.get(char, 0) + 1
        return frequency
    
    def _get_compatibility_level(self, score: float) -> str:
        """
        Convert score to compatibility level.
        
        Args:
            score: Score between 0-100
            
        Returns:
            Compatibility level string
        """
        if score >= 80:
            return "💯 Soulmates!"
        elif score >= 60:
            return "❤️ Great Match"
        elif score >= 40:
            return "💕 Good Potential"
        elif score >= 20:
            return "💘 Keep Trying"
        else:
            return "🚫 Not Compatible"
    
    def calculate(self, name1: str, name2: str, method: CalculationMethod = CalculationMethod.COMBINED) -> LoveScoreResult:
        """
        Calculate love score using specified method.
        
        Args:
            name1: First name
            name2: Second name
            method: Calculation method to use
            
        Returns:
            LoveScoreResult object
            
        Raises:
            ValueError: If input is invalid
        """
        try:
            self._validate_input(name1, name2)
            
            if method == CalculationMethod.CLASSIC:
                score, breakdown = self._classic_method(name1, name2)
                method_name = "Classic"
            elif method == CalculationMethod.PHONETIC:
                score, breakdown = self._phonetic_method(name1, name2)
                method_name = "Phonetic"
            elif method == CalculationMethod.STATISTICAL:
                score, breakdown = self._statistical_method(name1, name2)
                method_name = "Statistical"
            elif method == CalculationMethod.COMBINED:
                # Average all methods
                classic, classic_bd = self._classic_method(name1, name2)
                phonetic, phonetic_bd = self._phonetic_method(name1, name2)
                statistical, stat_bd = self._statistical_method(name1, name2)
                score = (classic + phonetic + statistical) / 3
                method_name = "Combined"
                breakdown = {
                    "classic": classic,
                    "phonetic": phonetic,
                    "statistical": statistical,
                    "average": score
                }
            else:
                raise ValueError(f"Unknown method: {method}")
            
            result = LoveScoreResult(
                name1=name1,
                name2=name2,
                score=round(score, 2),
                method=method_name,
                breakdown=breakdown,
                timestamp=datetime.now().isoformat(),
                compatibility_level=self._get_compatibility_level(score)
            )
            
            self.history.append(result)
            logger.info(f"Calculated score for {name1} & {name2}: {score:.2f}% ({method_name})")
            
            return result
        
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    def save_history(self, filename: str = "love_scores_history.json") -> None:
        """
        Save calculation history to JSON file.
        
        Args:
            filename: Output filename
        """
        try:
            data = [
                {
                    "name1": r.name1,
                    "name2": r.name2,
                    "score": r.score,
                    "method": r.method,
                    "breakdown": r.breakdown,
                    "timestamp": r.timestamp,
                    "compatibility": r.compatibility_level
                }
                for r in self.history
            ]
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"History saved to {filename}")
        
        except IOError as e:
            logger.error(f"Error saving history: {e}")
            raise
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about all calculations.
        
        Returns:
            Dictionary with statistics
        """
        if not self.history:
            return {"total_calculations": 0, "average_score": 0}
        
        scores = [r.score for r in self.history]
        
        return {
            "total_calculations": len(self.history),
            "average_score": round(sum(scores) / len(scores), 2),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "recent_calculations": len(self.history)
        }


def main():
    """Main function with example usage."""
    calculator = LoveScoreCalculator(target_letters="love")
    
    # Test with different methods
    couples = [
        ("Kanye West", "Kim Kardashian"),
        ("Romeo", "Juliet"),
        ("Harry", "Meghan")
    ]
    
    for name1, name2 in couples:
        print(f"\n--- Calculating for {name1} & {name2} ---")
        
        # Try combined method
        result = calculator.calculate(name1, name2, CalculationMethod.COMBINED)
        
        print(f"Score: {result.score}%")
        print(f"Level: {result.compatibility_level}")
        print(f"Breakdown: {result.breakdown}")
    
    # Display statistics
    print(f"\n--- Statistics ---")
    stats = calculator.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Save history
    calculator.save_history()
    print("\nHistory saved!")


if __name__ == "__main__":
    main()
