"""Tests for DataProcessor module"""
import pytest
import allure
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from data_processor import DataProcessor


@allure.feature('Data Processing')
@allure.story('Open Time Calculation')
class TestOpenTimeCalculation:
    
    @allure.title("Test 1: Calculate open time for resolved issue")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_calculate_open_time_resolved(self, sample_issue_resolved):
        """Расчет времени в открытом состоянии для закрытой задачи"""
        result = DataProcessor.calculate_open_time([sample_issue_resolved])
        assert len(result) == 1, "Should return one result"
        assert result[0] == 10, "Should be 10 days"
    
    @allure.title("Test 2: Ignore unresolved issues")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_calculate_open_time_ignores_open(self, sample_issue_open):
        """Незакрытые задачи не учитываются"""
        result = DataProcessor.calculate_open_time([sample_issue_open])
        assert len(result) == 0, "Open issues should be ignored"
    
    @allure.title("Test 3: Multiple issues")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_calculate_open_time_multiple(self, sample_issues_list):
        """Обработка нескольких задач"""
        result = DataProcessor.calculate_open_time(sample_issues_list)
        assert len(result) == 2, "Should return 2 resolved issues"
        assert all(isinstance(x, int) for x in result), "All should be integers"
        assert all(x > 0 for x in result), "All should be positive"


@allure.feature('Data Processing')
@allure.story('Status Duration')
class TestStatusDurations:
    
    @allure.title("Test 4: Status durations with changelog")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_status_durations_with_changelog(self, sample_issue_resolved):
        """Расчет времени в статусах при наличии changelog"""
        result = DataProcessor.get_status_durations([sample_issue_resolved])
        assert isinstance(result, dict), "Should return dict"
        assert 'Open' in result, "Should contain 'Open' status"
    
    @allure.title("Test 5: Status durations without changelog")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_status_durations_no_changelog(self, sample_issue_no_changelog):
        """Обработка задач без changelog"""
        result = DataProcessor.get_status_durations([sample_issue_no_changelog])
        assert isinstance(result, dict), "Should return dict"
        assert len(result) > 0, "Should have at least one status"
    
    @allure.title("Test 6: Status durations non-negative")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_status_durations_non_negative(self, sample_issues_list):
        """Все длительности неотрицательные"""
        result = DataProcessor.get_status_durations(sample_issues_list)
        for status, durations in result.items():
            assert all(d >= 0 for d in durations), f"{status} has negative durations"


@allure.feature('Data Processing')
@allure.story('Daily Statistics')
class TestDailyStats:
    
    @allure.title("Test 7: Daily stats structure")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_daily_stats_structure(self, sample_issues_list):
        """Проверка структуры дневной статистики"""
        result = DataProcessor.get_daily_stats(sample_issues_list)
        assert 'date' in result.columns
        assert 'created' in result.columns
        assert 'closed' in result.columns
        assert 'created_cumsum' in result.columns
        assert 'closed_cumsum' in result.columns
    
    @allure.title("Test 8: Cumulative values increase")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_daily_stats_cumsum_increases(self, sample_issues_list):
        """Накопительные значения растут"""
        result = DataProcessor.get_daily_stats(sample_issues_list)
        assert result['created_cumsum'].is_monotonic_increasing
        assert result['closed_cumsum'].is_monotonic_increasing
    
    @allure.title("Test 9: Non-negative counts")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_daily_stats_non_negative(self, sample_issues_list):
        """Все счетчики неотрицательные"""
        result = DataProcessor.get_daily_stats(sample_issues_list)
        assert (result['created'] >= 0).all()
        assert (result['closed'] >= 0).all()


@allure.feature('Data Processing')
@allure.story('User Statistics')
class TestUserStats:
    
    @allure.title("Test 10: User statistics")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_user_stats_basic(self, sample_issues_list):
        """Базовая статистика по пользователям"""
        result = DataProcessor.get_user_stats(sample_issues_list, top_n=10)
        assert 'user' in result.columns
        assert 'count' in result.columns
        assert len(result) > 0
    
    @allure.title("Test 11: Top N limit")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_user_stats_top_n_limit(self, sample_issues_list):
        """Ограничение количества пользователей"""
        result = DataProcessor.get_user_stats(sample_issues_list, top_n=2)
        assert len(result) <= 2
    
    @allure.title("Test 12: Sorted descending")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_user_stats_sorted(self, sample_issues_list):
        """Пользователи отсортированы по убыванию"""
        result = DataProcessor.get_user_stats(sample_issues_list, top_n=10)
        counts = result['count'].tolist()
        assert counts == sorted(counts, reverse=True)


@allure.feature('Data Processing')
@allure.story('Priority Distribution')
class TestPriorityDistribution:
    
    @allure.title("Test 13: Priority distribution")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_priority_distribution_basic(self, sample_issues_list):
        """Базовое распределение по приоритетам"""
        result = DataProcessor.get_priority_distribution(sample_issues_list)
        assert isinstance(result, dict)
        assert len(result) > 0
        assert all(isinstance(v, int) for v in result.values())
    
    @allure.title("Test 14: Priority counts positive")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_priority_counts_positive(self, sample_issues_list):
        """Все счетчики положительные"""
        result = DataProcessor.get_priority_distribution(sample_issues_list)
        assert all(v > 0 for v in result.values())


@allure.feature('Data Processing')
@allure.story('Time in Progress')
class TestTimeInProgress:
    
    @allure.title("Test 15: Time in progress")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_time_in_progress_basic(self, sample_issue_resolved):
        """Расчет времени в In Progress"""
        result = DataProcessor.get_time_in_progress_distribution([sample_issue_resolved])
        assert isinstance(result, list)
        if len(result) > 0:
            assert all(isinstance(x, (int, float)) for x in result)
            assert all(x >= 0 for x in result)