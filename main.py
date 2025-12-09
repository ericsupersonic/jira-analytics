import os
import sys
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jira_analyzer import JiraClient, DataProcessor, Visualizer


def load_config(config_path=None):
    if config_path is None:
        for path in ['config.yaml', 'config.yml', 'config.ini']:
            if os.path.exists(path):
                config_path = path
                break
        else:
            raise FileNotFoundError("Config file not found")
    
    print(f"   Config: {config_path}")
    
    if config_path.endswith(('.yaml', '.yml')):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        import configparser
        cfg = configparser.ConfigParser()
        cfg.read(config_path, encoding='utf-8')
        return {
            'jira': {
                'base_url': cfg.get('JIRA', 'url'),
                'email': cfg.get('JIRA', 'email', fallback=None),
                'api_token': cfg.get('JIRA', 'api_token', fallback=None),
                'auth_required': True
            },
            'query': {
                'jql': cfg.get('QUERY', 'jql'),
                'max_results': cfg.getint('QUERY', 'max_results')
            },
            'output': {
                'output_dir': cfg.get('OUTPUT', 'output_dir'),
                'top_users': cfg.getint('OUTPUT', 'top_users')
            },
            'features': {
                'fetch_changelog': cfg.getboolean('FEATURES', 'fetch_changelog', fallback=True)
            }
        }


def main():
    print("=" * 60)
    print("JIRA ANALYZER")
    print("=" * 60)
    print()
    
    try:
        print("📋 Loading config...")
        config = load_config()
        
        jira_cfg = config['jira']
        query_cfg = config['query']
        output_cfg = config['output']
        features_cfg = config.get('features', {})
        
        jql = query_cfg.get('jql') or f"project = {query_cfg.get('project_key')} AND created >= -365d"
        max_results = query_cfg.get('max_results', 1000) or None
        output_dir = output_cfg.get('output_dir', 'output')
        top_users = output_cfg.get('top_users', 30)
        fetch_changelog = features_cfg.get('fetch_changelog', True)
        
        print(f"   URL: {jira_cfg['base_url']}")
        print(f"   JQL: {jql}")
        print()
        
        print("🔌 Connecting...")
        client = JiraClient(
            jira_cfg['base_url'],
            jira_cfg.get('email'),
            jira_cfg.get('api_token')
        )
        print("   ✓ Connected")
        print()
        
        print("📥 Fetching issues...")
        issues = client.fetch_issues(jql, max_results, 'changelog' if fetch_changelog else None)
        print()
        
        if not issues:
            print("⚠️  No issues found")
            return 1
        
        print("⚙️  Processing...")
        open_times = DataProcessor.calculate_open_time(issues)
        status_durations = DataProcessor.get_status_durations(issues)
        daily_stats = DataProcessor.get_daily_stats(issues)
        user_stats = DataProcessor.get_user_stats(issues, top_users)
        time_in_progress = DataProcessor.get_time_in_progress_distribution(issues)
        priority_dist = DataProcessor.get_priority_distribution(issues)
        print()
        
        print("📊 Creating charts...")
        viz = Visualizer(output_dir)
        viz.plot_open_time_histogram(open_times)
        viz.plot_status_durations(status_durations)
        viz.plot_daily_stats(daily_stats)
        viz.plot_user_stats(user_stats)
        viz.plot_time_in_progress_histogram(time_in_progress)
        viz.plot_priority_distribution(priority_dist)
        print()
        
        print("=" * 60)
        print("✅ DONE")
        print("=" * 60)
        print(f"📁 Results: {output_dir}/")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
