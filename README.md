# RSQ Utils

A comprehensive Python utility library providing common functionality for data manipulation, environment management, memory tracking, text processing, time operations, and URL handling.

## Installation

```bash
pip install rsq-utils
```

For development installation:

```bash
git clone https://github.com/rsq230798/rsq-utils.git
cd rsq-utils
pip install -e ".[dev]"  # Installs with development dependencies
```

## Features

### Data Transformation (`data_transformation`)

```python
from rsq_utils.data_transformation import list_batch_split

# Split a list into batches
data = list(range(100))
batches = list_batch_split(data, batch_size=10)
```

### Environment Variables (`env`)

```python
from rsq_utils.env import load_dotenv

# Load environment variables from .env file
load_dotenv()  # Default .env file
load_dotenv("custom.env")  # Custom path
```

### Memory Management (`memory`)

```python
from rsq_utils.memory import Memory

# Track memory usage
memory = Memory()
memory.get_current_memory()  # Get current memory stats
memory.append_memory_history()  # Add to memory history
```

### Text Processing (`text`)

```python
from rsq_utils.text import camel_to_snake, convert_keys_to_snake_case

# Convert camelCase to snake_case
snake = camel_to_snake("camelCase")  # "camel_case"

# Convert dictionary keys
data = {"firstName": "John", "lastName": "Doe"}
snake_keys = convert_keys_to_snake_case(data)
# {"first_name": "John", "last_name": "Doe"}
```

### Time Utilities (`time`)

```python
from rsq_utils.time import Timer, DateRange, HistoricalDates

# Use Timer
timer = Timer()
timer.start()
# ... your code ...
timer.stop()
print(f"Time elapsed: {timer.time_elapsed} seconds")

# Generate date ranges
date_range = DateRange("2024-01-01", "2024-01-31")
dates = date_range.date_range
date_pairs = date_range.pair_dates()

# Get historical dates
historical = HistoricalDates()
last_30_days = historical.generate_historic_dates(30)
```

### URL Utilities (`url`)

```python
from rsq_utils.url import url_encode, generate_parameter_combos

# Encode URL parameters
url = url_encode("https://api.example.com", {"key": "value"})

# Generate parameter combinations
params = {
    "type": ["A", "B"],
    "status": [1, 2]
}
combinations = generate_parameter_combos(params)
```

### Variable Management (`variables`)

```python
from rsq_utils.variables import Variables

# Create variable container
vars = Variables({
    "data": [1, 2, 3],
    "config": {"setting": True}
})

# Get variable summaries
summary = vars.get_summary()
```

## Development

### Running Tests

```bash
pytest  # Run all tests
pytest -v  # Verbose output
pytest --cov=rsq_utils  # With coverage report
```

### Type Checking

```bash
mypy src/  # Check types
```

### Linting

```bash
pylint src/  # Lint source code
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
