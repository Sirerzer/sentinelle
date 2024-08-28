import requests
from ..config import pterodactyl , api_key , api_url

def get_server_id_from_uuid(uuid, api_url=api_url, api_key=api_key):
    if pterodactyl:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        page = 1
        while True:
            servers_url = f"{api_url}/api/application/servers?page={page}"
            try:
                response = requests.get(servers_url, headers=headers)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to retrieve servers: {e}")
                return None

            data = response.json()
            servers = data.get('data', [])

            if not servers:
                print("No server found with the specified UUID.")
                return None

            for server in servers:
                if server['attributes'].get('uuid') == uuid:
                    return server['attributes'].get('id')

            page += 1
            if page > data.get('meta', {}).get('pagination', {}).get('total_pages', 1):
                print("No server found with the specified UUID.")
                return None

def suspend_pterodactyl_server(uuid, api_url=api_url, api_key=api_key):
    if pterodactyl:
        server_id = suspend_pterodactyl_server(uuid=uuid , api_url=api_url, api_key=api_key)
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        suspend_url = f"{api_url}/api/application/servers/{server_id}/suspend"
        response = requests.post(suspend_url, headers=headers)
        return response.status_code == 204 