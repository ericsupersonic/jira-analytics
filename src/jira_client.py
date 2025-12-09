import requests
import time
from typing import List, Dict, Optional


class JiraClient:
    def __init__(self, base_url: str, email: Optional[str] = None, api_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.auth = (email, api_token) if email and api_token else None
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.api_version = self._detect_api_version()
    
    def _detect_api_version(self) -> str:
        for version in ["2", "3"]:
            try:
                url = f"{self.base_url}/rest/api/{version}/serverInfo"
                if requests.get(url, auth=self.auth, headers=self.headers, timeout=5).status_code == 200:
                    return version
            except:
                continue
        return "2"
    
    def fetch_issues(self, jql_query: str, max_results: Optional[int] = None, expand: Optional[str] = None) -> List[Dict]:
        all_issues = []
        start_at = 0
        batch_size = 50
        
        print(f"   JQL: {jql_query}")
        print(f"   API: v{self.api_version}")
        
        while True:
            url = f"{self.base_url}/rest/api/{self.api_version}/search"
            params = {
                'jql': jql_query,
                'startAt': start_at,
                'maxResults': batch_size,
                'fields': '*all'
            }
            if expand:
                params['expand'] = expand
            
            try:
                response = requests.get(url, auth=self.auth, headers=self.headers, params=params, timeout=30)
                
                if response.status_code != 200:
                    raise Exception(f"JIRA API error {response.status_code}: {response.text[:200]}")
                
                data = response.json()
                issues = data.get('issues', [])
                total = data.get('total', 0)
                
                if not issues:
                    break
                
                all_issues.extend(issues)
                print(f"   → {len(all_issues)}/{total}", end='\r')
                
                if max_results and len(all_issues) >= max_results:
                    all_issues = all_issues[:max_results]
                    break
                
                if len(all_issues) >= total:
                    break
                
                start_at += batch_size
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                raise Exception(f"Network error: {e}")
        
        print(f"   ✓ Loaded {len(all_issues)} issues")
        return all_issues
    
    def test_connection(self) -> bool:
        try:
            url = f"{self.base_url}/rest/api/{self.api_version}/serverInfo"
            return requests.get(url, auth=self.auth, headers=self.headers, timeout=10).status_code == 200
        except:
            return False
