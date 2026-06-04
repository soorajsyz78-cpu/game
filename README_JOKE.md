# Joke Generator

A simple joke generator application that fetches random jokes from external APIs and displays them with a clean interface.

## Features

- 🎭 **Random Joke Generator** - Fetch jokes from multiple sources
- 📱 **Multiple APIs** - Support for different joke APIs
- 🎨 **Clean Interface** - Simple and user-friendly CLI and web interface
- ⚡ **Fast & Responsive** - Quick joke retrieval
- 🔄 **Caching** - Optional caching to reduce API calls
- 📊 **Joke Categories** - Support for different joke types
- 🌐 **Web Interface** - Flask-based web UI

## Supported APIs

1. **JokeAPI** (https://jokeapi.dev) - Programming and general jokes
2. **Official Joke API** (https://official-joke-api.appspot.com) - Classic joke format
3. **Random.D** (https://random.d-apis.com) - Random jokes

## Requirements

- Python 3.7+
- requests
- flask (for web interface)
- python-dotenv (for environment variables)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/soorajsyz78-cpu/joke-generator.git
   cd joke-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface (CLI)

```bash
python cli.py
```

Options:
```bash
python cli.py --api jokeapi           # Use JokeAPI
python cli.py --api official          # Use Official Joke API
python cli.py --category programming  # Get programming jokes
python cli.py --count 5               # Get 5 jokes
python cli.py --format long           # Get longer jokes
```

### Web Interface

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

### Python Module

```python
from joke_generator import JokeGenerator

generator = JokeGenerator()

# Get a random joke
joke = generator.get_joke()
print(joke)

# Get multiple jokes
jokes = generator.get_multiple_jokes(count=3)
for joke in jokes:
    print(joke)

# Get jokes by category
programming_joke = generator.get_joke(category='programming')
print(programming_joke)
```

## Project Structure

```
.
├── joke_generator.py      # Main joke generator class
├── cli.py                 # Command line interface
├── app.py                 # Flask web application
├── utils.py               # Utility functions
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── templates/
│   ├── base.html         # Base HTML template
│   ├── index.html        # Home page
│   └── joke.html         # Joke display
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── script.js     # Client-side logic
└── README.md             # This file
```

## Configuration

Create a `.env` file based on `.env.example`:

```env
# Default API to use
DEFAULT_API=jokeapi

# API Keys (if required)
JOKEAPI_KEY=your_key_here

# Cache settings
ENABLE_CACHE=true
CACHE_DURATION=3600

# Web app settings
FLASK_ENV=development
FLASK_DEBUG=true
```

## API Endpoints

### Web Interface

- `GET /` - Home page
- `GET /api/joke` - Get a random joke (JSON)
- `GET /api/joke?count=5` - Get multiple jokes
- `GET /api/joke?category=programming` - Get jokes by category
- `GET /api/categories` - Get available categories

## Examples

### Get a Programming Joke
```bash
python cli.py --category programming
```

### Get 3 Random Jokes
```bash
python cli.py --count 3
```

### Get Long Format Jokes
```bash
python cli.py --format long
```

### Get Dark Humor Jokes
```bash
python cli.py --category dark
```

## Joke Formats

### Single Line Format
```json
{
  "joke": "Why do programmers prefer dark mode? Because light attracts bugs!"
}
```

### Two-Part Format
```json
{
  "setup": "Why do programmers prefer dark mode?",
  "punchline": "Because light attracts bugs!"
}
```

## Error Handling

The application gracefully handles:
- Network errors
- API timeouts
- Invalid API responses
- Rate limiting
- Missing dependencies

## Caching

Optional caching to reduce API calls:
- Cache jokes for configurable duration
- Clear cache on demand
- Cache statistics

## Future Enhancements

- [ ] User authentication and preferences
- [ ] Save favorite jokes
- [ ] Share jokes on social media
- [ ] Mobile app
- [ ] Offline mode with local jokes
- [ ] Joke rating system
- [ ] Multi-language support
- [ ] Custom joke submission
- [ ] Advanced filtering options
- [ ] Webhook support for scheduled jokes

## Troubleshooting

**"Connection Error"**
- Check your internet connection
- Verify the API is online

**"Rate Limited"**
- Wait a few seconds before requesting again
- Enable caching to reduce API calls

**"Module Not Found"**
- Run: `pip install -r requirements.txt`

## License

Free to use and modify

## Author

Developed by soorajsyz78-cpu

## Contributing

Feel free to submit issues and pull requests to improve the joke generator!

## Acknowledgments

- JokeAPI for providing a free joke API
- Official Joke API for their joke database
- Flask community for the web framework
