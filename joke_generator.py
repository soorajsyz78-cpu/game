import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class JokeAPI:
    """Base class for joke API implementations"""
    
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.base_url = ""
        self.cache = {}
        self.cache_expiry = {}
    
    def get_joke(self, **kwargs) -> Optional[Dict]:
        """Get a single joke"""
        raise NotImplementedError
    
    def get_multiple_jokes(self, count: int = 1, **kwargs) -> List[Dict]:
        """Get multiple jokes"""
        jokes = []
        for _ in range(count):
            joke = self.get_joke(**kwargs)
            if joke:
                jokes.append(joke)
        return jokes
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Make HTTP request to API"""
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Error: Request timeout ({self.timeout}s)")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Connection failed. Check your internet connection.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP {e.response.status_code}")
            return None
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def _is_cache_valid(self, key: str, duration: int = 3600) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        if key not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[key]
    
    def _cache_data(self, key: str, data: Dict, duration: int = 3600):
        """Cache data with expiry"""
        self.cache[key] = data
        self.cache_expiry[key] = datetime.now() + timedelta(seconds=duration)


class JokeAPIProvider(JokeAPI):
    """JokeAPI.dev provider - Programming and general jokes"""
    
    def __init__(self, timeout=5):
        super().__init__(timeout)
        self.base_url = "https://v2.jokeapi.dev/joke"
    
    def get_joke(self, category: str = "Any", safe: bool = True, **kwargs) -> Optional[Dict]:
        """
        Get a joke from JokeAPI
        Categories: Programming, Knock-Knock, General, Any
        """
        # Validate category
        valid_categories = ["Programming", "Knock-Knock", "General", "Any"]
        if category not in valid_categories:
            category = "Any"
        
        cache_key = f"jokeapi_{category}_{safe}"
        
        # Check cache
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        params = {
            "type": "single" if category == "Knock-Knock" else "single,twopart",
            "safe-mode": "true" if safe else "false"
        }
        
        url = f"{self.base_url}/{category}"
        data = self._make_request(url, params)
        
        if data and data.get("error") is False:
            joke = self._format_joke(data)
            self._cache_data(cache_key, joke)
            return joke
        
        return None
    
    def _format_joke(self, data: Dict) -> Dict:
        """Format JokeAPI response"""
        if data.get("type") == "single":
            return {
                "joke": data.get("joke"),
                "source": "JokeAPI",
                "category": data.get("category"),
                "timestamp": datetime.now().isoformat()
            }
        else:  # two-part
            return {
                "setup": data.get("setup"),
                "punchline": data.get("delivery"),
                "source": "JokeAPI",
                "category": data.get("category"),
                "timestamp": datetime.now().isoformat()
            }


class OfficialJokeAPI(JokeAPI):
    """Official Joke API provider - Classic joke format"""
    
    def __init__(self, timeout=5):
        super().__init__(timeout)
        self.base_url = "https://official-joke-api.appspot.com"
    
    def get_joke(self, joke_type: str = "random", **kwargs) -> Optional[Dict]:
        """
        Get a joke from Official Joke API
        Types: random, random_ten
        """
        cache_key = f"official_joke_{joke_type}"
        
        # Check cache
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        url = f"{self.base_url}/random_joke"
        data = self._make_request(url)
        
        if data:
            joke = self._format_joke(data)
            self._cache_data(cache_key, joke)
            return joke
        
        return None
    
    def _format_joke(self, data: Dict) -> Dict:
        """Format Official Joke API response"""
        return {
            "setup": data.get("setup"),
            "punchline": data.get("punchline"),
            "source": "Official Joke API",
            "type": data.get("type"),
            "id": data.get("id"),
            "timestamp": datetime.now().isoformat()
        }


class RandomAPIProvider(JokeAPI):
    """Random.D API provider - Various random jokes"""
    
    def __init__(self, timeout=5):
        super().__init__(timeout)
        self.base_url = "https://random.d-apis.com/api/joke"
    
    def get_joke(self, **kwargs) -> Optional[Dict]:
        """Get a random joke from Random.D API"""
        cache_key = "random_d_joke"
        
        # Check cache
        if self._is_cache_valid(cache_key):
            return self.cache[cache_key]
        
        data = self._make_request(self.base_url)
        
        if data:
            joke = self._format_joke(data)
            self._cache_data(cache_key, joke)
            return joke
        
        return None
    
    def _format_joke(self, data: Dict) -> Dict:
        """Format Random.D API response"""
        return {
            "joke": data.get("body"),
            "source": "Random.D API",
            "timestamp": datetime.now().isoformat()
        }


class JokeGenerator:
    """Main joke generator that manages multiple API providers"""
    
    def __init__(self, default_api: str = "jokeapi"):
        self.providers = {
            "jokeapi": JokeAPIProvider(),
            "official": OfficialJokeAPI(),
            "random": RandomAPIProvider()
        }
        self.default_api = default_api if default_api in self.providers else "jokeapi"
        self.current_provider = self.providers[self.default_api]
    
    def set_provider(self, api_name: str) -> bool:
        """Switch to a different API provider"""
        if api_name in self.providers:
            self.current_provider = self.providers[api_name]
            self.default_api = api_name
            return True
        return False
    
    def get_joke(self, api: str = None, **kwargs) -> Optional[Dict]:
        """Get a single joke"""
        if api and api != self.default_api:
            self.set_provider(api)
        
        return self.current_provider.get_joke(**kwargs)
    
    def get_multiple_jokes(self, count: int = 1, api: str = None, **kwargs) -> List[Dict]:
        """Get multiple jokes"""
        if api and api != self.default_api:
            self.set_provider(api)
        
        return self.current_provider.get_multiple_jokes(count, **kwargs)
    
    def get_joke_from_all_apis(self) -> Dict[str, Optional[Dict]]:
        """Get a joke from each available API"""
        results = {}
        for api_name in self.providers.keys():
            self.set_provider(api_name)
            results[api_name] = self.current_provider.get_joke()
        return results
    
    def clear_cache(self):
        """Clear cache from all providers"""
        for provider in self.providers.values():
            provider.cache.clear()
            provider.cache_expiry.clear()
    
    def get_available_apis(self) -> List[str]:
        """Get list of available API providers"""
        return list(self.providers.keys())
