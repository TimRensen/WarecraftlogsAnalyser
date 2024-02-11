import os
import time
import requests
import json

from config import WCL

def _obtain_access_token() -> bool:
    if _read_token():
        return True

    data = {
        'grant_type': 'client_credentials',
    }
    auth = (WCL.clientID, WCL.clientSecret)

    with requests.Session() as session:
        response = session.post(
            WCL.tokenURL,
            auth = auth,
            data = data,
        )
        response.raise_for_status
    
    if response.status_code == 200:
        _safe_token(response)
        return True

    return False

def _safe_token(response : str = '') -> None:
    try:
        with open('.token.json', mode = 'w+', encoding = 'utf-8') as f:
            json.dump(response.json(), f)
    except OSError as e:
        print(e)
        return None
    
def _read_token() -> str | None:
    try:
        with open('.token.json', mode = 'r+', encoding = 'utf-8') as f:
            response = json.load(f)

            if os.path.getctime('.token.json') + response.get('expires_in') <= time.time():
                if not _obtain_access_token:
                    raise Exception('A valid token couldn''t be acquired')
            
            return response.get('access_token')
    except OSError as e:
        print(e)
        return None

def _get_headers() -> dict[str, str]:
    return {
        "Authorization": f'Bearer {_read_token()}'
    }

def _fetch_data(query:str, **kwargs):
    data = {"query": query, "variables": kwargs}
    with requests.Session() as session:
        session.headers = _get_headers()
        response = session.get(WCL.publicURL, json = data)
        response.raise_for_status

    return response

def main():
    graphql_query = """
        query($id:Int){
            characterData{
                character(id: $id){
                    id
                    name
                    zoneRankings
                }
            }
        }
    """

    response = _fetch_data(graphql_query, id = 54822614)

    print(response.json())

    return

if __name__ == '__main__':
    main()