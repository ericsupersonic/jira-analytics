"""Tests for Visualizer module"""
import pytest
import allure
import sys
import os
import shutil
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from visualizer import Visualizer
from data_processor import DataProcessor


@allure.feature('Visualization')
@allure.story('Chart Generation')
class TestVisualizerCharts:
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and cleanup"""
        self.test_dir = 'test_output_temp'
        self.visualizer = Visualizer(output_dir=self.test_dir)
        yield
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @allure.title("Test 23: Create output directory")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_output_directory_creation(self):
        """Создание директории для графиков"""
        assert os.path.exists(self.test_dir)
    
    @allure.title("Test 24: Open time histogram")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_plot_open_time_histogram(self):
        """Генерация гистограммы времени"""
        open_times = [1, 2, 3, 5, 8, 13, 21, 34]
        self.visualizer.plot_open_time_histogram(open_times)
        
        output_file = os.path.join(self.test_dir, '1_open_time_histogram.png')
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    @allure.title("Test 25: Priority distribution chart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_plot_priority_distribution(self):
        """Генерация графика приоритетов"""
        priority_counts = {'High': 10, 'Medium': 25, 'Low': 15}
        self.visualizer.plot_priority_distribution(priority_counts)
        
        output_file = os.path.join(self.test_dir, '6_priority_distribution.png')
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
    
    @allure.title("Test 26: Daily stats chart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_plot_daily_stats(self):
        """Генерация графика дневной статистики"""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'created': [5, 3, 7, 2, 8, 4, 6, 3, 5, 7],
            'closed': [2, 4, 3, 5, 2, 6, 4, 5, 3, 6],
            'created_cumsum': [5, 8, 15, 17, 25, 29, 35, 38, 43, 50],
            'closed_cumsum': [2, 6, 9, 14, 16, 22, 26, 31, 34, 40]
        })
        self.visualizer.plot_daily_stats(df)
        
        output_file = os.path.join(self.test_dir, '3_daily_stats.png')
        assert os.path.exists(output_file)
    
    @allure.title("Test 27: User stats chart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_plot_user_stats(self):
        """Генерация графика по пользователям"""
        df = pd.DataFrame({
            'user': ['Alice', 'Bob', 'Charlie', 'David'],
            'count': [25, 20, 15, 10]
        })
        self.visualizer.plot_user_stats(df)
        
        output_file = os.path.join(self.test_dir, '4_user_stats.png')
        assert os.path.exists(output_file)
    
    @allure.title("Test 28: Handle empty data")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_plot_with_empty_data(self):
        """Обработка пустых данных"""
        self.visualizer.plot_time_in_progress_histogram([])
        
        output_file = os.path.join(self.test_dir, '5_time_in_progress_histogram.png')
        assert os.path.exists(output_file)
    
    @allure.title("Test 29: All 6 charts generated")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_all_charts_generated(self, sample_issues_list):
        """Проверка генерации всех графиков"""
        open_times = DataProcessor.calculate_open_time(sample_issues_list)
        status_durations = DataProcessor.get_status_durations(sample_issues_list)
        daily_stats = DataProcessor.get_daily_stats(sample_issues_list)
        user_stats = DataProcessor.get_user_stats(sample_issues_list)
        time_in_progress = DataProcessor.get_time_in_progress_distribution(sample_issues_list)
        priority_dist = DataProcessor.get_priority_distribution(sample_issues_list)
        
        self.visualizer.plot_open_time_histogram(open_times)
        self.visualizer.plot_status_durations(status_durations)
        self.visualizer.plot_daily_stats(daily_stats)
        self.visualizer.plot_user_stats(user_stats)
        self.visualizer.plot_time_in_progress_histogram(time_in_progress)
        self.visualizer.plot_priority_distribution(priority_dist)
        
        expected_files = [
            '1_open_time_histogram.png',
            '2_status_durations.png',
            '3_daily_stats.png',
            '4_user_stats.png',
            '5_time_in_progress_histogram.png',
            '6_priority_distribution.png'
        ]
        for filename in expected_files:
            filepath = os.path.join(self.test_dir, filename)
            assert os.path.exists(filepath), f"{filename} should exist"
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup: create test directory, Teardown: cleanup"""
        self.test_dir = 'test_output_temp'
        self.visualizer = Visualizer(output_dir=self.test_dir)
        yield
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @allure.title("Test 23: Create output directory")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_output_directory_creation(self):
        """Создание директории для графиков"""
        with allure.step("Verify directory exists"):
            assert os.path.exists(self.test_dir), "Output directory should be created"
            allure.attach(self.test_dir, name="Output directory", attachment_type=allure.attachment_type.TEXT)
    
    @allure.title("Test 24: Generate open time histogram")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_plot_open_time_histogram(self):
        """Генерация гистограммы времени в открытом состоянии"""
        open_times = [1, 2, 3, 5, 8, 13, 21, 34]
        
        with allure.step("Generate histogram"):
            self.visualizer.plot_open_time_histogram(open_times)
        
        with allure.step("Verify output file"):
            output_file = os.path.join(self.test_dir, '1_open_time_histogram.png')
            assert os.path.exists(output_file), "Histogram file should be created"
            assert os.path.getsize(output_file) > 0, "File should not be empty"
    
    @allure.title("Test 25: Generate priority distribution chart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_plot_priority_distribution(self):
        """Генерация графика распределения по приоритетам"""
        priority_counts = {'High': 10, 'Medium': 25, 'Low': 15}
        
        with allure.step("Generate priority chart"):
            self.visualizer.plot_priority_distribution(priority_counts)
        
        with allure.step("Verify output file"):
            output_file = os.path.join(self.test_dir, '6_priority_distribution.png')
            assert os.path.exists(output_file), "Priority chart should be created"
            assert os.path.getsize(output_file) > 0, "File should not be empty"
    
    @allure.title("Test 26: Generate daily stats chart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_plot_daily_stats(self):
        """Генерация графика дневной статистики"""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'created': [5, 3, 7, 2, 8, 4, 6, 3, 5, 7],
            'closed': [2, 4, 3, 5, 2, 6, 4, 5, 3, 6],
            'created_cumsum': [5, 8, 15, 17, 25, 29, 35, 38, 43, 50],
            'closed_cumsum': [2, 6, 9, 14, 16, 22, 26, 31, 34, 40]
        })
        
        with allure.step("Generate daily stats chart"):
            self.visualizer.plot_daily_stats(df)
        
        with allure.step("Verify output file"):
            output_file = os.path.join(self.test_dir, '3_daily_stats.png')
            assert os.path.exists(output_file), "Daily stats chart should be created"
            assert os.path.getsize(output_file) > 0, "File should not be empty"
    
    @allure.title("Test 27: Generate user stats chart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_plot_user_stats(self):
        """Генерация графика статистики по пользователям"""
        df = pd.DataFrame({
            'user': ['Alice', 'Bob', 'Charlie', 'David'],
            'count': [25, 20, 15, 10]
        })
        
        with allure.step("Generate user stats chart"):
            self.visualizer.plot_user_stats(df)
        
        with allure.step("Verify output file"):
            output_file = os.path.join(self.test_dir, '4_user_stats.png')
            assert os.path.exists(output_file), "User stats chart should be created"
            assert os.path.getsize(output_file) > 0, "File should not be empty"
    
    @allure.title("Test 28: Handle empty data gracefully")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.unit
    def test_plot_with_empty_data(self):
        """Обработка пустых данных"""
        with allure.step("Generate chart with empty data"):
            self.visualizer.plot_time_in_progress_histogram([])
        
        with allure.step("Verify placeholder created"):
            output_file = os.path.join(self.test_dir, '5_time_in_progress_histogram.png')
            assert os.path.exists(output_file), "Should create placeholder file"
    
    @allure.title("Test 29: All chart files generated")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.unit
    def test_all_charts_generated(self, sample_issues_list):
        """Проверка генерации всех графиков"""
        from data_processor import DataProcessor
        
        with allure.step("Process data"):
            open_times = DataProcessor.calculate_open_time(sample_issues_list)
            status_durations = DataProcessor.get_status_durations(sample_issues_list)
            daily_stats = DataProcessor.get_daily_stats(sample_issues_list)
            user_stats = DataProcessor.get_user_stats(sample_issues_list)
            time_in_progress = DataProcessor.get_time_in_progress_distribution(sample_issues_list)
            priority_dist = DataProcessor.get_priority_distribution(sample_issues_list)
        
        with allure.step("Generate all charts"):
            self.visualizer.plot_open_time_histogram(open_times)
            self.visualizer.plot_status_durations(status_durations)
            self.visualizer.plot_daily_stats(daily_stats)
            self.visualizer.plot_user_stats(user_stats)
            self.visualizer.plot_time_in_progress_histogram(time_in_progress)
            self.visualizer.plot_priority_distribution(priority_dist)
        
        with allure.step("Verify all 6 charts exist"):
            expected_files = [
                '1_open_time_histogram.png',
                '2_status_durations.png',
                '3_daily_stats.png',
                '4_user_stats.png',
                '5_time_in_progress_histogram.png',
                '6_priority_distribution.png'
            ]
            for filename in expected_files:
                filepath = os.path.join(self.test_dir, filename)
                assert os.path.exists(filepath), f"{filename} should exist"
                allure.attach(filename, name="Generated chart", attachment_type=allure.attachment_type.TEXT)