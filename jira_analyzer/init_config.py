def main():
    config_content = """jira:
  base_url: "https://issues.apache.org/jira"
  auth_required: false

query:
  project_key: "KAFKA"
  jql: "project = KAFKA AND created >= -365d"
  max_results: 100

output:
  output_dir: "output"
  top_users: 30

features:
  fetch_changelog: true
"""
    
    with open('config.yaml', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✅ config.yaml created!")
    print("Edit it and run: jira-analyzer")


if __name__ == '__main__':
    main()
