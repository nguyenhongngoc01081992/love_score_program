# Love Score Program 💕

An advanced love compatibility calculator with multiple algorithms and comprehensive features.

## Features

- **Multiple Calculation Methods**:
  - 🔤 **Classic**: Count target letters in names
  - 🎵 **Phonetic**: Analyze phonetic similarity and vowel patterns
  - 📊 **Statistical**: Advanced character frequency analysis
  - 🔄 **Combined**: Average of all three methods for balanced results

- **Input Validation**: Robust error handling and validation
- **Result Tracking**: Save and track calculation history
- **Statistics**: Generate statistics from all calculations
- **Logging**: Comprehensive logging for debugging
- **Type Hints**: Full type annotations for better code clarity
- **Unit Tests**: Comprehensive test coverage

## Installation

```bash
# Clone the repository
git clone https://github.com/nguyenhongngoc01081992/love_score_program.git
cd love_score_program

# No external dependencies required - uses only Python standard library
```

## Quick Start

```python
from love_score_advanced import LoveScoreCalculator, CalculationMethod

# Create calculator instance
calculator = LoveScoreCalculator(target_letters="love")

# Calculate love score using combined method
result = calculator.calculate("Romeo", "Juliet", CalculationMethod.COMBINED)

# Display results
print(f"Score: {result.score}%")
print(f"Compatibility: {result.compatibility_level}")
print(f"Details: {result.breakdown}")

# Save history
calculator.save_history()
```

## Usage Examples

### Using Different Methods

```python
# Classic method
result_classic = calculator.calculate("Alice", "Bob", CalculationMethod.CLASSIC)

# Phonetic method
result_phonetic = calculator.calculate("Alice", "Bob", CalculationMethod.PHONETIC)

# Statistical method
result_stat = calculator.calculate("Alice", "Bob", CalculationMethod.STATISTICAL)

# Combined (default)
result_combined = calculator.calculate("Alice", "Bob", CalculationMethod.COMBINED)
```

### Getting Statistics

```python
stats = calculator.get_statistics()
print(f"Total calculations: {stats['total_calculations']}")
print(f"Average score: {stats['average_score']}")
print(f"Highest score: {stats['highest_score']}")
print(f"Lowest score: {stats['lowest_score']}")
```

### Running Tests

```bash
python -m pytest test_love_score.py -v
# or
python -m unittest test_love_score.py
```

## Compatibility Levels

The calculator returns compatibility levels based on the score:

| Score Range | Level | Emoji |
|-------------|-------|-------|
| 80-100      | Soulmates! | 💯 |
| 60-79       | Great Match | ❤️ |
| 40-59       | Good Potential | 💕 |
| 20-39       | Keep Trying | 💘 |
| 0-19        | Not Compatible | 🚫 |

## Algorithm Details

### Classic Method
Counts how many times letters from the target word ("love") appear in the combined names, then calculates the percentage.

### Phonetic Method
Analyzes:
- Length similarity between names
- Vowel pattern similarity
- Combines both factors for overall score

### Statistical Method
Analyzes:
- Unique character intersection
- Character frequency patterns
- Provides detailed breakdown of common characters

## Output Format

Each calculation returns a `LoveScoreResult` object with:
- `name1`: First name
- `name2`: Second name
- `score`: Compatibility score (0-100)
- `method`: Calculation method used
- `breakdown`: Detailed breakdown of calculation
- `timestamp`: When calculation was performed
- `compatibility_level`: Human-readable compatibility level

## Logging

All activities are logged to:
- **Console**: Real-time output
- **File**: `love_score.log` for persistence

Enable debug logging for more details:

```python
import logging
logging.getLogger("love_score_advanced").setLevel(logging.DEBUG)
```

## Project Structure

```
love_score_program/
├── love_score                    # Original simple implementation
├── love_score_advanced.py        # Advanced calculator with all features
├── test_love_score.py            # Comprehensive test suite
├── README.md                     # This file
└── love_scores_history.json      # Generated history file
```

## Original Implementation

The original `love_score` file contains the basic implementation for reference.

## Contributing

Feel free to fork, modify, and improve this project!

## License

Open source - use freely

## Future Enhancements

- [ ] Web UI interface
- [ ] API endpoint
- [ ] Database persistence
- [ ] Batch processing
- [ ] Custom algorithm creation
- [ ] Advanced statistics and visualizations
- [ ] ML-based compatibility prediction

---

**Created with ❤️ by nguyenhongngoc01081992**
