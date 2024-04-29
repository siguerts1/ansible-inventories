import requests

def fetch_inventory(api_url):
    """
    Fetches inventory data from the given API URL and prints it.

    :param api_url: URL to the API endpoint that returns inventory data
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises a HTTPError for bad responses
        # Print formatted JSON data
        print(response.json())
    except requests.RequestException as e:
        print(f"Error fetching inventory: {e}")

def main():
    # URL to your Flask API endpoint
    api_url = "http://10.0.0.131:5001/multipass_inventory"
    fetch_inventory(api_url)

if __name__ == '__main__':
    main()
