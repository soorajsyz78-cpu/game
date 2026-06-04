import click
from joke_generator import JokeGenerator
from datetime import datetime


@click.group()
def cli():
    """Joke Generator CLI - Get random jokes from various APIs"""
    pass


@cli.command()
@click.option('--api', type=click.Choice(['jokeapi', 'official', 'random']), 
              default='jokeapi', help='Which API to use')
@click.option('--category', type=str, default='Any', 
              help='Joke category (for JokeAPI: Programming, General, Knock-Knock, Any)')
@click.option('--count', type=int, default=1, 
              help='Number of jokes to fetch')
@click.option('--safe', is_flag=True, default=True, 
              help='Get safe jokes only (for JokeAPI)')
def joke(api, category, count, safe):
    """Get random jokes"""
    try:
        generator = JokeGenerator(default_api=api)
        
        click.echo(click.style("\n🎭 Joke Generator", fg='cyan', bold=True))
        click.echo(click.style(f"API: {api.upper()}", fg='yellow'))
        click.echo(click.style(f"Count: {count}", fg='yellow'))
        click.echo(click.style(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", fg='gray'))
        click.echo("\n" + "="*50 + "\n")
        
        # Get jokes
        if count == 1:
            jokes = [generator.get_joke(category=category) if api == 'jokeapi' else generator.get_joke()]
        else:
            jokes = generator.get_multiple_jokes(count=count, category=category if api == 'jokeapi' else None)
        
        # Display jokes
        for i, joke_data in enumerate(jokes, 1):
            if joke_data:
                click.echo(click.style(f"Joke #{i}:", fg='green', bold=True))
                
                # Display based on joke format
                if 'joke' in joke_data:
                    click.echo(f"  {joke_data['joke']}")
                elif 'setup' in joke_data and 'punchline' in joke_data:
                    click.echo(f"  Setup: {joke_data['setup']}")
                    click.echo(f"  Punchline: {joke_data['punchline']}")
                
                # Display metadata
                if 'source' in joke_data:
                    click.echo(click.style(f"  Source: {joke_data['source']}", fg='blue', dim=True))
                
                click.echo()
            else:
                click.echo(click.style(f"❌ Failed to fetch joke #{i}", fg='red'))
        
        click.echo("="*50 + "\n")
    
    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'), err=True)


@cli.command()
def compare():
    """Compare jokes from all available APIs"""
    try:
        generator = JokeGenerator()
        
        click.echo(click.style("\n🎭 Comparing All APIs", fg='cyan', bold=True))
        click.echo("="*60 + "\n")
        
        results = generator.get_joke_from_all_apis()
        
        for api_name, joke_data in results.items():
            click.echo(click.style(f"\n{api_name.upper()}", fg='green', bold=True))
            click.echo("-" * 40)
            
            if joke_data:
                if 'joke' in joke_data:
                    click.echo(f"  {joke_data['joke']}")
                elif 'setup' in joke_data and 'punchline' in joke_data:
                    click.echo(f"  Setup: {joke_data['setup']}")
                    click.echo(f"  Punchline: {joke_data['punchline']}")
                click.echo()
            else:
                click.echo(click.style("  ❌ Failed to fetch", fg='red'))
        
        click.echo("\n" + "="*60 + "\n")
    
    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'), err=True)


@cli.command()
def list_apis():
    """List all available APIs"""
    generator = JokeGenerator()
    apis = generator.get_available_apis()
    
    click.echo(click.style("\n📡 Available APIs:", fg='cyan', bold=True))
    click.echo()
    
    api_info = {
        'jokeapi': 'JokeAPI - Programming and general jokes',
        'official': 'Official Joke API - Classic joke format',
        'random': 'Random.D API - Various random jokes'
    }
    
    for api in apis:
        click.echo(click.style(f"  ✓ {api}", fg='green'))
        click.echo(f"    {api_info.get(api, 'No description')}")
        click.echo()


@cli.command()
@click.option('--format', type=click.Choice(['table', 'json']), 
              default='table', help='Output format')
def categories(format):
    """List available joke categories for JokeAPI"""
    categories_list = [
        ('Programming', 'Programming and developer jokes'),
        ('Knock-Knock', 'Classic knock-knock jokes'),
        ('General', 'General humor'),
        ('Any', 'Mix of all categories')
    ]
    
    click.echo(click.style("\n📂 JokeAPI Categories:", fg='cyan', bold=True))
    click.echo()
    
    if format == 'table':
        for cat, desc in categories_list:
            click.echo(click.style(f"  • {cat}", fg='green'))
            click.echo(f"    {desc}")
    else:
        import json
        data = [{'category': cat, 'description': desc} for cat, desc in categories_list]
        click.echo(json.dumps(data, indent=2))
    
    click.echo()


@cli.command()
def version():
    """Show version information"""
    click.echo(click.style("\n🎭 Joke Generator v1.0.0", fg='cyan', bold=True))
    click.echo("A random joke generator using external APIs")
    click.echo()
    click.echo(click.style("Available APIs:", fg='yellow'))
    click.echo("  • JokeAPI (https://jokeapi.dev)")
    click.echo("  • Official Joke API (https://official-joke-api.appspot.com)")
    click.echo("  • Random.D API (https://random.d-apis.com)")
    click.echo()


if __name__ == '__main__':
    cli()
