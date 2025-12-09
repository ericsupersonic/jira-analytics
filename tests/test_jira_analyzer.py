import unittest
from unittest.mock import Mock, patch
from datetime import datetime
import os
import sys
import shutil

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jira_analyzer import DataProcessor, JiraClient, Visualizer


class TestDataProcessor(unittest.TestCase):
    """Тесты для DataProcessor"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_issue_resolved = {
            'fields': {
                'created': '2024-01-01T10:00:00.000+0000',
                'resolutiondate': '2024-01-11T10:00:00.000+0000',
                'status': {'name': 'Done'},
                'priority': {'name': 'High'},
                'assignee': {'displayName': 'John Doe'},
                'reporter': {'displayName': 'Jane Smith'}
            },
            'changelog': {
                'histories': []
            }
        }
        
        self.test_issue_open = {
            'fields': {
                'created': '2024-01-01T10:00:00.000+0000',
                'resolutiondate': None,
                'status': {'name': 'Open'},
                'priority': {'name': 'Low'},
                'assignee': None,
                'reporter': {'displayName': 'Jane Smith'}
            }
        }
    
    def test_calculate_open_time(self):
        """Тест 1: Расчет времени в открытом состоянии"""
        issues = [self.test_issue_resolved]
        result = DataProcessor.calculate_open_time(issues)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 10)  # 10 дней
    
    def test_calculate_open_time_no_resolution(self):
        """Тест 2: Расчет времени для незакрытых задач"""
        issues = [self.test_issue_open]
        result = DataProcessor.calculate_open_time(issues)
        
        self.assertEqual(len(result), 0)  # Незакрытые задачи не учитываются
    
    def test_get_priority_distribution(self):
        """Тест 3: Распределение по приоритетам"""
        issues = [self.test_issue_resolved, self.test_issue_open]
        result = DataProcessor.get_priority_distribution(issues)
        
        self.assertIn('High', result)
        self.assertIn('Low', result)
        self.assertEqual(result['High'], 1)
        self.assertEqual(result['Low'], 1)
    
    def test_get_user_stats(self):
        """Тест 4: Статистика по пользователям"""
        issues = [self.test_issue_resolved, self.test_issue_open]
        result = DataProcessor.get_user_stats(issues, top_n=10)
        
        self.assertGreater(len(result), 0)
        self.assertIn('user', result.columns)
        self.assertIn('count', result.columns)
        # Jane Smith упоминается 2 раза (reporter), John Doe - 1 раз (assignee)
        self.assertEqual(len(result), 2)
    
    def test_get_daily_stats(self):
        """Тест 5: Статистика по дням"""
        issues = [self.test_issue_resolved]
        result = DataProcessor.get_daily_stats(issues)
        
        self.assertIn('date', result.columns)
        self.assertIn('created', result.columns)
        self.assertIn('closed', result.columns)
        self.assertIn('created_cumsum', result.columns)
        self.assertIn('closed_cumsum', result.columns)
        self.assertGreater(len(result), 0)


class TestJiraClient(unittest.TestCase):
    """Тесты для JiraClient"""
    
    @patch('requests.get')
    def test_fetch_issues_success(self, mock_get):
        """Тест 6: Успешное получение задач"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'issues': [{'key': 'TEST-1'}],
            'total': 1
        }
        mock_get.return_value = mock_response
        
        client = JiraClient('https://test.atlassian.net', 'user@test.com', 'token')
        issues = client.fetch_issues('project = TEST', max_results=10)
        
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['key'], 'TEST-1')
    
    @patch('requests.get')
    def test_fetch_issues_error(self, mock_get):
        """Тест 7: Обработка ошибки при получении задач"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Unauthorized'
        mock_get.return_value = mock_response
        
        client = JiraClient('https://test.atlassian.net', 'user@test.com', 'token')
        
        with self.assertRaises(Exception):
            client.fetch_issues('project = TEST')


class TestVisualizer(unittest.TestCase):
    """Тесты для Visualizer"""
    
    def setUp(self):
        """Создание тестовой директории"""
        self.test_dir = 'test_output'
        self.visualizer = Visualizer(output_dir=self.test_dir)
    
    def tearDown(self):
        """Удаление тестовой директории"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_output_directory_creation(self):
        """Тест 8: Создание директории для графиков"""
        self.assertTrue(os.path.exists(self.test_dir))
    
    def test_plot_open_time_histogram(self):
        """Тест 9: Создание гистограммы времени в открытом состоянии"""
        open_times = [1, 2, 3, 5, 8, 13, 21]
        self.visualizer.plot_open_time_histogram(open_times)
        
        output_file = f'{self.test_dir}/1_open_time_histogram.png'
        self.assertTrue(os.path.exists(output_file))
    
    def test_plot_priority_distribution(self):
        """Тест 10: Создание графика распределения по приоритетам"""
        priority_counts = {'High': 10, 'Medium': 20, 'Low': 5}
        self.visualizer.plot_priority_distribution(priority_counts)
        
        output_file = f'{self.test_dir}/6_priority_distribution.png'
        self.assertTrue(os.path.exists(output_file))


if __name__ == '__main__':
    # Запуск всех тестов
    unittest.main(verbosity=2)
