from flask import Flask, render_template, jsonify, request
from joke_generator import JokeGenerator
from datetime import datetime
import os

app = Flask(__name__, 
            template_folder='templates_jokes',
            static_folder='static_jokes')

# Initialize joke generator
generator = JokeGenerator()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', apis=generator.get_available_apis())


@app.route('/api/joke')
def get_joke():
    """Get a random joke"""
    try:
        api = request.args.get('api', 'jokeapi')
        category = request.args.get('category', 'Any')
        count = int(request.args.get('count', '1'))
        
        # Validate count
        count = min(max(count, 1), 10)  # Between 1 and 10
        
        # Get jokes
        if count == 1:
            if api == 'jokeapi':
                joke = generator.get_joke(api=api, category=category)
            else:
                joke = generator.get_joke(api=api)
            
            return jsonify({
                'success': joke is not None,
                'data': joke,
                'count': 1,
                'timestamp': datetime.now().isoformat()
            })
        else:
            jokes = generator.get_multiple_jokes(count=count, api=api, category=category if api == 'jokeapi' else None)
            
            return jsonify({
                'success': len(jokes) > 0,
                'data': jokes,
                'count': len(jokes),
                'timestamp': datetime.now().isoformat()
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/apis')
def get_apis():
    """Get list of available APIs"""
    apis = generator.get_available_apis()
    api_details = {
        'jokeapi': {
            'name': 'JokeAPI',
            'url': 'https://jokeapi.dev',
            'description': 'Programming and general jokes',
            'categories': ['Programming', 'Knock-Knock', 'General', 'Any']
        },
        'official': {
            'name': 'Official Joke API',
            'url': 'https://official-joke-api.appspot.com',
            'description': 'Classic joke format with setup and punchline'
        },
        'random': {
            'name': 'Random.D API',
            'url': 'https://random.d-apis.com',
            'description': 'Various random jokes'
        }
    }
    
    return jsonify({
        'success': True,
        'apis': [api_details.get(api, {'name': api}) for api in apis]
    })


@app.route('/api/categories')
def get_categories():
    """Get available categories for JokeAPI"""
    categories = [
        {'name': 'Programming', 'description': 'Programming and developer jokes'},
        {'name': 'Knock-Knock', 'description': 'Classic knock-knock jokes'},
        {'name': 'General', 'description': 'General humor'},
        {'name': 'Any', 'description': 'Mix of all categories'}
    ]
    
    return jsonify({
        'success': True,
        'categories': categories
    })


@app.route('/api/clear-cache', methods=['POST'])
def clear_cache():
    """Clear the joke cache"""
    try:
        generator.clear_cache()
        return jsonify({
            'success': True,
            'message': 'Cache cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Create template directory if it doesn't exist
    os.makedirs('templates_jokes', exist_ok=True)
    os.makedirs('static_jokes/css', exist_ok=True)
    os.makedirs('static_jokes/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
