"""
Validation tests - проверка корректности данных и расчетов
Эти тесты доказывают, что мы берем правильные данные и корректно их обрабатываем
"""
import pytest
import allure
import sys
import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from data_processor import DataProcessor


@allure.feature('Data Validation')
@allure.story('Input Data Validation')
class TestInputDataValidation:
    
    @allure.title("Test 30: Validate issue has required fields")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.unit
    def test_issue_has_required_fields(self, sample_issue_resolved):
        """Валидация: задача содержит все обязательные поля"""
        assert 'key' in sample_issue_resolved
        assert 'fields' in sample_issue_resolved
        assert 'created' in sample_issue_resolved['fields']
        assert 'status' in sample_issue_resolved['fields']
        assert 'priority' in sample_issue_resolved['fields']
    
    @allure.title("Test 31: Validate date format")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_date_format_validation(self, sample_issue_resolved):
        """Валидация: даты в правильном формате JIRA"""
        created = sample_issue_resolved['fields']['created']
        
        # Проверяем что дата парсится
        try:
            parsed_date = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f%z')
            assert parsed_date is not None
        except ValueError:
            pytest.fail("Invalid date format")
    
    @allure.title("Test 32: Validate resolution date after creation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_resolution_after_creation(self, sample_issue_resolved):
        """Валидация: дата закрытия после даты создания"""
        created = datetime.strptime(
            sample_issue_resolved['fields']['created'],
            '%Y-%m-%dT%H:%M:%S.%f%z'
        )
        resolved = datetime.strptime(
            sample_issue_resolved['fields']['resolutiondate'],
            '%Y-%m-%dT%H:%M:%S.%f%z'
        )
        
        assert resolved > created, "Resolution date must be after creation date"


@allure.feature('Data Validation')
@allure.story('Calculation Validation')
class TestCalculationValidation:
    
    @allure.title("Test 33: Validate open time calculation accuracy")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_open_time_calculation_accuracy(self, sample_issue_resolved):
        """Валидация: точность расчета времени в открытом состоянии"""
        # Вручную вычисляем ожидаемое значение
        created = datetime.strptime(
            sample_issue_resolved['fields']['created'],
            '%Y-%m-%dT%H:%M:%S.%f%z'
        )
        resolved = datetime.strptime(
            sample_issue_resolved['fields']['resolutiondate'],
            '%Y-%m-%dT%H:%M:%S.%f%z'
        )
        expected_days = (resolved - created).days
        
        # Вычисляем через наш метод
        result = DataProcessor.calculate_open_time([sample_issue_resolved])
        
        assert len(result) == 1
        assert result[0] == expected_days, f"Expected {expected_days} days, got {result[0]}"
    
    @allure.title("Test 34: Validate cumulative sum consistency")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_cumulative_sum_consistency(self, sample_issues_list):
        """Валидация: накопительные суммы соответствуют обычным"""
        df = DataProcessor.get_daily_stats(sample_issues_list)
        
        # Проверяем что cumsum равен сумме всех предыдущих значений
        manual_cumsum_created = df['created'].cumsum()
        manual_cumsum_closed = df['closed'].cumsum()
        
        assert (df['created_cumsum'] == manual_cumsum_created).all()
        assert (df['closed_cumsum'] == manual_cumsum_closed).all()
    
    @allure.title("Test 35: Validate user count accuracy")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_user_count_accuracy(self, sample_issues_list):
        """Валидация: точность подсчета задач пользователей"""
        # Вручную считаем упоминания
        manual_counts = {}
        for issue in sample_issues_list:
            assignee = issue['fields'].get('assignee')
            reporter = issue['fields'].get('reporter')
            if assignee:
                name = assignee['displayName']
                manual_counts[name] = manual_counts.get(name, 0) + 1
            if reporter:
                name = reporter['displayName']
                manual_counts[name] = manual_counts.get(name, 0) + 1
        
        # Получаем через наш метод
        result = DataProcessor.get_user_stats(sample_issues_list, top_n=100)
        
        # Проверяем каждого пользователя
        for _, row in result.iterrows():
            user = row['user']
            count = row['count']
            assert count == manual_counts[user], f"Count mismatch for {user}"
    
    @allure.title("Test 36: Validate priority distribution total")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_priority_distribution_total(self, sample_issues_list):
        """Валидация: сумма по приоритетам равна общему количеству задач"""
        result = DataProcessor.get_priority_distribution(sample_issues_list)
        
        total_from_distribution = sum(result.values())
        total_issues_with_priority = len([
            i for i in sample_issues_list 
            if i['fields'].get('priority')
        ])
        
        assert total_from_distribution == total_issues_with_priority


@allure.feature('Data Validation')
@allure.story('Output Validation')
class TestOutputValidation:
    
    @allure.title("Test 37: Validate no data loss in processing")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_no_data_loss(self, sample_issues_list):
        """Валидация: не теряем данные при обработке"""
        input_count = len(sample_issues_list)
        
        # Обрабатываем разными методами
        daily_stats = DataProcessor.get_daily_stats(sample_issues_list)
        
        # Проверяем что в daily_stats учтены все задачи
        total_created = daily_stats['created'].sum()
        assert total_created == input_count, "Lost issues in daily stats processing"
    
    @allure.title("Test 38: Validate data types consistency")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_data_types_consistency(self, sample_issues_list):
        """Валидация: типы данных остаются консистентными"""
        open_times = DataProcessor.calculate_open_time(sample_issues_list)
        
        # Все значения должны быть целыми числами (дни)
        assert all(isinstance(x, int) for x in open_times)
        
        # Время в progress должно быть float (часы)
        time_in_progress = DataProcessor.get_time_in_progress_distribution(sample_issues_list)
        if time_in_progress:
            assert all(isinstance(x, (int, float)) for x in time_in_progress)
    
    @allure.title("Test 39: Validate changelog parsing correctness")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_changelog_parsing_correctness(self, sample_issue_resolved):
        """Валидация: корректность парсинга changelog"""
        status_durations = DataProcessor.get_status_durations([sample_issue_resolved])
        
        # В нашем тестовом issue есть переходы Open -> In Progress -> Done
        assert 'Open' in status_durations, "Should parse 'Open' status from changelog"
        assert 'In Progress' in status_durations, "Should parse 'In Progress' status"
        
        # Проверяем что длительности положительные
        for status, durations in status_durations.items():
            assert all(d >= 0 for d in durations), f"Negative duration in {status}"


@allure.feature('Data Validation')
@allure.story('Edge Cases Validation')
class TestEdgeCasesValidation:
    
    @allure.title("Test 40: Handle missing optional fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_missing_optional_fields(self):
        """Валидация: обработка отсутствующих опциональных полей"""
        issue_minimal = {
            'key': 'TEST-1',
            'fields': {
                'created': '2024-01-01T10:00:00.000+0000',
                'resolutiondate': None,
                'status': {'name': 'Open'},
                'priority': None,  # Нет приоритета
                'assignee': None,  # Нет assignee
                'reporter': None   # Нет reporter
            }
        }
        
        # Не должно падать
        priority_dist = DataProcessor.get_priority_distribution([issue_minimal])
        user_stats = DataProcessor.get_user_stats([issue_minimal])
        
        assert isinstance(priority_dist, dict)
        assert len(user_stats) == 0  # Нет пользователей
    
    @allure.title("Test 41: Handle zero duration edge case")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_zero_duration_edge_case(self):
        """Валидация: обработка задач с нулевой длительностью"""
        issue_zero = {
            'key': 'TEST-1',
            'fields': {
                'created': '2024-01-01T10:00:00.000+0000',
                'resolutiondate': '2024-01-01T10:00:00.000+0000',  # Создана и закрыта в одно время
                'status': {'name': 'Closed'},
                'priority': {'name': 'High'},
                'assignee': {'displayName': 'User'},
                'reporter': {'displayName': 'User'}
            }
        }
        
        result = DataProcessor.calculate_open_time([issue_zero])
        assert len(result) == 1
        assert result[0] == 0, "Should handle zero duration correctly"