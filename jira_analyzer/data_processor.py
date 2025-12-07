from datetime import datetime
from typing import List, Dict
import pandas as pd
from collections import defaultdict


class DataProcessor:
    
    @staticmethod
    def calculate_open_time(issues: List[Dict]) -> List[int]:
        open_times = []
        for issue in issues:
            created = issue['fields']['created']
            resolved = issue['fields'].get('resolutiondate')
            if resolved:
                created_dt = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f%z')
                resolved_dt = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f%z')
                open_times.append((resolved_dt - created_dt).days)
        return open_times
    
    @staticmethod
    def get_status_durations(issues: List[Dict]) -> Dict[str, List[int]]:
        status_durations = defaultdict(list)
        
        for issue in issues:
            changelog = issue.get('changelog', {})
            histories = changelog.get('histories', [])
            
            if not histories:
                status = issue['fields']['status']['name']
                created = issue['fields']['created']
                resolved = issue['fields'].get('resolutiondate')
                if resolved:
                    created_dt = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f%z')
                    resolved_dt = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f%z')
                    status_durations[status].append((resolved_dt - created_dt).days)
                continue
            
            status_timeline = []
            created = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
            
            first_status = None
            for history in histories:
                for item in history.get('items', []):
                    if item['field'] == 'status':
                        first_status = item.get('fromString', 'Open')
                        break
                if first_status:
                    break
            
            if first_status:
                status_timeline.append({'status': first_status, 'date': created})
            
            for history in histories:
                changed_date = datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                for item in history.get('items', []):
                    if item['field'] == 'status':
                        status_timeline.append({'status': item['toString'], 'date': changed_date})
            
            for i in range(len(status_timeline) - 1):
                status = status_timeline[i]['status']
                days = (status_timeline[i + 1]['date'] - status_timeline[i]['date']).days
                if days >= 0:
                    status_durations[status].append(days)
            
            if status_timeline:
                last_status = status_timeline[-1]['status']
                last_date = status_timeline[-1]['date']
                resolved = issue['fields'].get('resolutiondate')
                if resolved:
                    resolved_dt = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f%z')
                    days = (resolved_dt - last_date).days
                    if days >= 0:
                        status_durations[last_status].append(days)
        
        return dict(status_durations)
    
    @staticmethod
    def get_daily_stats(issues: List[Dict]) -> pd.DataFrame:
        daily_data = defaultdict(lambda: {'created': 0, 'closed': 0})
        
        for issue in issues:
            created = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
            daily_data[created]['created'] += 1
            
            resolved = issue['fields'].get('resolutiondate')
            if resolved:
                resolved_date = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f%z').date()
                daily_data[resolved_date]['closed'] += 1
        
        df = pd.DataFrame([
            {'date': date, 'created': stats['created'], 'closed': stats['closed']}
            for date, stats in sorted(daily_data.items())
        ])
        
        df['created_cumsum'] = df['created'].cumsum()
        df['closed_cumsum'] = df['closed'].cumsum()
        return df
    
    @staticmethod
    def get_user_stats(issues: List[Dict], top_n: int = 30) -> pd.DataFrame:
        user_counts = defaultdict(int)
        
        for issue in issues:
            assignee = issue['fields'].get('assignee')
            reporter = issue['fields'].get('reporter')
            if assignee:
                user_counts[assignee['displayName']] += 1
            if reporter:
                user_counts[reporter['displayName']] += 1
        
        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return pd.DataFrame(sorted_users, columns=['user', 'count'])
    
    @staticmethod
    def get_time_in_progress_distribution(issues: List[Dict]) -> List[float]:
        time_in_progress = []
        
        for issue in issues:
            if not issue['fields'].get('resolutiondate'):
                continue
            
            changelog = issue.get('changelog', {})
            histories = changelog.get('histories', [])
            if not histories:
                continue
            
            status_times = {}
            current_status = None
            status_start = None
            created = datetime.strptime(issue['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
            
            for history in histories:
                for item in history.get('items', []):
                    if item['field'] == 'status':
                        current_status = item.get('fromString')
                        status_start = created
                        break
                if current_status:
                    break
            
            for history in histories:
                changed_date = datetime.strptime(history['created'], '%Y-%m-%dT%H:%M:%S.%f%z')
                for item in history.get('items', []):
                    if item['field'] == 'status':
                        if current_status and status_start:
                            duration_hours = (changed_date - status_start).total_seconds() / 3600
                            status_times[current_status] = status_times.get(current_status, 0) + duration_hours
                        current_status = item['toString']
                        status_start = changed_date
            
            if current_status and status_start:
                resolved = datetime.strptime(issue['fields']['resolutiondate'], '%Y-%m-%dT%H:%M:%S.%f%z')
                duration_hours = (resolved - status_start).total_seconds() / 3600
                status_times[current_status] = status_times.get(current_status, 0) + duration_hours
            
            for status, hours in status_times.items():
                if 'progress' in status.lower():
                    time_in_progress.append(hours)
                    break
        
        return time_in_progress
    
    @staticmethod
    def get_priority_distribution(issues: List[Dict]) -> Dict[str, int]:
        priority_counts = defaultdict(int)
        for issue in issues:
            priority = issue['fields'].get('priority')
            if priority:
                priority_counts[priority['name']] += 1
        return dict(priority_counts)
