import pytest
import sys
import os

# Добавляем src в path (абсолютный путь)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))


@pytest.fixture
def sample_issue_resolved():
    return {
        'key': 'TEST-1',  # ← Добавлено
        'fields': {
            'created': '2024-01-01T00:00:00.000000+0000',
            'resolutiondate': '2024-01-11T00:00:00.000000+0000',
            'status': {'name': 'Open'},
            'assignee': {'displayName': 'Alice'},
            'reporter': {'displayName': 'Bob'},
            'priority': {'name': 'High'},
        },
        'changelog': {
            'histories': [
                {
                    'created': '2024-01-03T00:00:00.000000+0000',
                    'items': [
                        {'field': 'status', 'fromString': 'Open', 'toString': 'In Progress'}
                    ]
                },
                {
                    'created': '2024-01-08T00:00:00.000000+0000',
                    'items': [
                        {'field': 'status', 'fromString': 'In Progress', 'toString': 'Resolved'}
                    ]
                }
            ]
        }
    }


@pytest.fixture
def sample_issue_open():
    return {
        'key': 'TEST-2',  # ← Добавлено
        'fields': {
            'created': '2024-01-01T00:00:00.000000+0000',
            'resolutiondate': None,  # ← Добавлено для открытых задач
            'status': {'name': 'Open'},
            'assignee': {'displayName': 'Charlie'},
            'reporter': {'displayName': 'Dana'},
            'priority': {'name': 'Low'},
        },
        'changelog': {'histories': []}
    }


@pytest.fixture
def sample_issue_no_changelog():
    return {
        'key': 'TEST-3',  # ← Добавлено
        'fields': {
            'created': '2024-01-05T00:00:00.000000+0000',
            'resolutiondate': '2024-01-10T00:00:00.000000+0000',
            'status': {'name': 'Closed'},
            'assignee': {'displayName': 'Eve'},
            'reporter': {'displayName': 'Frank'},
            'priority': {'name': 'Medium'},
        }
    }


@pytest.fixture
def sample_issues_list():
    issue1 = {
        'key': 'TEST-1',  # ← Добавлено
        'fields': {
            'created': '2024-01-01T00:00:00.000000+0000',
            'resolutiondate': '2024-01-11T00:00:00.000000+0000',
            'status': {'name': 'Open'},
            'assignee': {'displayName': 'Alice'},
            'reporter': {'displayName': 'Bob'},
            'priority': {'name': 'High'},
        },
        'changelog': {
            'histories': [
                {
                    'created': '2024-01-03T00:00:00.000000+0000',
                    'items': [
                        {'field': 'status', 'fromString': 'Open', 'toString': 'In Progress'}
                    ]
                },
                {
                    'created': '2024-01-08T00:00:00.000000+0000',
                    'items': [
                        {'field': 'status', 'fromString': 'In Progress', 'toString': 'Resolved'}
                    ]
                }
            ]
        }
    }

    issue2 = {
        'key': 'TEST-2',  # ← Добавлено
        'fields': {
            'created': '2024-01-02T00:00:00.000000+0000',
            'resolutiondate': '2024-01-07T00:00:00.000000+0000',
            'status': {'name': 'Open'},
            'assignee': {'displayName': 'George'},
            'reporter': {'displayName': 'Helen'},
            'priority': {'name': 'Medium'},
        },
        'changelog': {
            'histories': [
                {
                    'created': '2024-01-04T00:00:00.000000+0000',
                    'items': [
                        {'field': 'status', 'fromString': 'Open', 'toString': 'In Progress'}
                    ]
                },
                {
                    'created': '2024-01-06T00:00:00.000000+0000',
                    'items': [
                        {'field': 'status', 'fromString': 'In Progress', 'toString': 'Resolved'}
                    ]
                }
            ]
        }
    }

    return [issue1, issue2]