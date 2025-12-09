"""Tests for JiraClient module"""
import pytest
import allure
import sys
import os
from unittest.mock import Mock, patch

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from jira_client import JiraClient


@allure.feature('JIRA Client')
@allure.story('Connection and Authentication')
class TestJiraClientConnection:
    
    @allure.title("Test 16: Initialize JIRA client")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_jira_client_initialization(self):
        """Инициализация клиента JIRA"""
        client = JiraClient(
            'https://test.atlassian.net',
            'user@test.com',
            'token123'
        )
        assert client.base_url == 'https://test.atlassian.net'
        assert client.auth == ('user@test.com', 'token123')
    
    @allure.title("Test 17: JIRA client without auth")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_jira_client_no_auth(self):
        """Клиент без аутентификации"""
        client = JiraClient('https://issues.apache.org/jira')
        assert client.auth is None
    
    @allure.title("Test 18: Base URL normalization")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.unit
    def test_base_url_normalization(self):
        """URL без trailing slash"""
        client = JiraClient('https://test.atlassian.net/')
        assert client.base_url == 'https://test.atlassian.net'
        assert not client.base_url.endswith('/')


@allure.feature('JIRA Client')
@allure.story('Fetching Issues')
class TestJiraClientFetch:
    
    @allure.title("Test 19: Fetch issues successfully")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.unit
    @patch('jira_client.requests.get')
    def test_fetch_issues_success(self, mock_get):
        """Успешное получение задач"""
        # API version check
        mock_version = Mock()
        mock_version.status_code = 200
        
        # Actual fetch
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'issues': [{'key': 'KAFKA-1', 'fields': {}}],
            'total': 1
        }
        mock_get.side_effect = [mock_version, mock_response]
        
        client = JiraClient('https://test.atlassian.net', 'user@test.com', 'token')
        issues = client.fetch_issues('project = TEST', max_results=10)
        
        assert len(issues) == 1
        assert issues[0]['key'] == 'KAFKA-1'
    
    @allure.title("Test 20: Handle API errors")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    @patch('jira_client.requests.get')
    def test_fetch_issues_api_error(self, mock_get):
        """Обработка ошибок API"""
        # API version check
        mock_version = Mock()
        mock_version.status_code = 200
        
        # Error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Unauthorized'
        mock_get.side_effect = [mock_version, mock_response]
        
        client = JiraClient('https://test.atlassian.net', 'user@test.com', 'wrong_token')
        
        with pytest.raises(Exception) as exc_info:
            client.fetch_issues('project = TEST')
        
        assert '401' in str(exc_info.value)
    
    @allure.title("Test 21: Empty results handling")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    @patch('jira_client.requests.get')
    def test_fetch_issues_empty(self, mock_get):
        """Обработка пустых результатов"""
        # API version check
        mock_version = Mock()
        mock_version.status_code = 200
        
        # Empty result
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'issues': [],
            'total': 0
        }
        mock_get.side_effect = [mock_version, mock_response]
        
        client = JiraClient('https://test.atlassian.net')
        issues = client.fetch_issues('project = NONEXISTENT')
        
        assert len(issues) == 0


@allure.feature('JIRA Client')
@allure.story('API Version Detection')
class TestJiraClientAPIVersion:
    
    @allure.title("Test 22: Detect API version")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    @patch('jira_client.requests.get')
    def test_api_version_detection(self, mock_get):
        """Определение версии JIRA API"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = JiraClient('https://test.atlassian.net')
        assert client.api_version in ['2', '3']