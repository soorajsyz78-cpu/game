#!/usr/bin/env python
"""
Quick start script for the Joke Generator application.
Provides options to run CLI, Web Server, or get a single joke.
"""

import sys
import argparse
from joke_generator import JokeGenerator
from datetime import datetime


def print_joke(joke_data, joke_number=1):
    """Pretty print a joke"""
    if not joke_data:
        print("\n❌ Failed to fetch joke")
        return
    
    print(f"\n{'='*50}")
    print(f"Joke #{joke_number}")
    print(f"{'='*50}")
    
    if 'joke' in joke_data:
        print(f"\n{joke_data['joke']}\n")
    elif 'setup' in joke_data and 'punchline' in joke_data:
        print(f"\nSetup: {joke_data['setup']}")
        print(f"Punchline: {joke_data['punchline']}\n")
    
    if 'source' in joke_data:
        print(f"Source: {joke_data['source']}")
    if 'category' in joke_data:
        print(f"Category: {joke_data['category']}")


def main():
    parser = argparse.ArgumentParser(
        description='Joke Generator - Get random jokes from external APIs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python quick_start.py --joke                          # Get a single joke
  python quick_start.py --joke --api jokeapi --category programming
  python quick_start.py --joke --count 3               # Get 3 jokes
  python quick_start.py --cli                           # Start CLI
  python quick_start.py --web                           # Start web server
        """
    )
    
    parser.add_argument('--joke', action='store_true', help='Get a random joke')
    parser.add_argument('--cli', action='store_true', help='Start CLI mode')
    parser.add_argument('--web', action='store_true', help='Start web server')
    parser.add_argument('--api', default='jokeapi', 
                       choices=['jokeapi', 'official', 'random'],
                       help='API to use (default: jokeapi)')
    parser.add_argument('--category', default='Any',
                       choices=['Programming', 'General', 'Knock-Knock', 'Any'],
                       help='Joke category for JokeAPI (default: Any)')
    parser.add_argument('--count', type=int, default=1,
                       help='Number of jokes to fetch (default: 1)')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not (args.joke or args.cli or args.web):
        parser.print_help()
        return
    
    # Get jokes
    if args.joke:
        print("\n🎭 Joke Generator")
        print(f"API: {args.api.upper()}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        generator = JokeGenerator(default_api=args.api)
        
        if args.count == 1:
            if args.api == 'jokeapi':
                joke = generator.get_joke(api=args.api, category=args.category)
            else:
                joke = generator.get_joke(api=args.api)
            print_joke(joke)
        else:
            jokes = generator.get_multiple_jokes(
                count=args.count, 
                api=args.api, 
                category=args.category if args.api == 'jokeapi' else None
            )
            for i, joke in enumerate(jokes, 1):
                print_joke(joke, i)
        
        print(f"\n{'='*50}\n")
    
    # CLI mode
    elif args.cli:
        print("\n🎭 Joke Generator CLI")
        print("Type 'help' for commands or 'quit' to exit\n")
        import cli_jokes
        # The CLI is implemented with Click
        # You would run: python cli_jokes.py
        print("To use CLI mode, run: python cli_jokes.py")
    
    # Web mode
    elif args.web:
        print("\n🌐 Starting Joke Generator Web Server...")
        print("Open http://localhost:5000 in your browser\n")
        import app_jokes
        app_jokes.app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
