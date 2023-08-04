import requests
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

class CongressDotGov(ExperimentalBaseConnection):

    BASE_URL = "https://api.congress.gov/v3/"

    def _connect(self, **kwargs) -> requests.Session:
        session = requests.Session()

        kw = kwargs.copy()
        if 'api_key' in kw and len(kw['api_key'])>0:
            print(kw['api_key'])
            api_key = kw['api_key']
            print(kw['api_key'])
        else:
            api_key = self._secrets['API_KEY_CONGRESS']

        session.params = {'api_key': api_key}
        return session
    
    def cursor(self) -> requests.Session:
        return self._instance
    
    def _make_request(self, endpoint, params=None):
        session = self.cursor()
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = session.get(url, params=params)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            print(f"Error response: {response.text}")
            return {response.text}
        
    def get_committee_meetings(self, params=None):
        endpoint = "committee-meeting"
        return self._make_request(endpoint, params=params)
    
    def get_committee_meetings_by_congress(self, congress, ttl: int = 3600):
        @cache_data(ttl=ttl)
        def _get_committee_meetings_by_congress(congress):
            endpoint = f"committee-meeting/{congress}"
            return self._make_request(endpoint)
        return _get_committee_meetings_by_congress(congress)
    
    def get_committee_meetings_by_congress_chamber(self, congress, chamber, ttl: int = 3600):
        @cache_data(ttl=ttl)
        def _get_committee_meetings_by_congress_chamber(congress, chamber):
            endpoint = f"committee-meeting/{congress}/{chamber}"
            return self._make_request(endpoint)
        return _get_committee_meetings_by_congress_chamber(congress, chamber)
    
    def get_committee_meetings_by_congress_chamber_event(self, congress, chamber, eventID, ttl: int = 3600):
        @cache_data(ttl=ttl)
        def _get_committee_meetings_by_congress_chamber_event(congress, chamber, eventID):
            endpoint = f"committee-meeting/{congress}/{chamber}/{eventID}"
            return self._make_request(endpoint)
        
        return _get_committee_meetings_by_congress_chamber_event(congress, chamber, eventID)