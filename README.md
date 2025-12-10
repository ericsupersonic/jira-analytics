# JIRA Analyzer

Инструмент для анализа данных из JIRA и построения аналитических графиков.


## Возможности

Программа автоматически генерирует **6 аналитических графиков**:

1. **Гистограмма времени в открытом состоянии** - распределение задач по времени от создания до закрытия
2. **Распределение времени по статусам** - сколько времени задачи проводят в каждом статусе
3. **Статистика по дням** - количество созданных и закрытых задач по дням с накопительными итогами
4. **Топ-30 пользователей** - рейтинг пользователей по количеству задач (assignee + reporter)
5. **Время в статусе "In Progress"** - распределение времени выполнения задач
6. **Распределение по приоритетам** - количество задач по уровням приоритета

##  Для чего это нужно

- Анализ производительности команды
- Выявление узких мест в процессе разработки
- Оптимизация workflow
- Отчетность для руководства
- Планирование спринтов

##  Быстрый старт

### Установка

```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/jira-analyzer.git
cd jira-analyzer

# Установить зависимости
pip install -r requirements.txt

# Или установить как пакет
pip install -e .
```

### Запуск

```bash
# Базовый запуск (использует config/config.yaml)
python main.py

# С параметрами
python main.py -p KAFKA -n 1000

# Через скрипты
bin/run.bat          # Windows
bash bin/run.sh      # Linux/Mac

# После установки пакета
jira-analyzer
```

### Параметры командной строки

```bash
python main.py [опции]

Опции:
  -p, --project PROJECT        Ключ проекта (например, KAFKA, HDFS)
  -n, --max-results N          Максимальное количество задач для анализа
  -c, --config PATH            Путь к файлу конфигурации
  -h, --help                   Показать справку
```

##  Конфигурация

Создайте файл `config/config.yaml`:

```yaml
jira:
  base_url: "https://issues.apache.org/jira"  # URL вашего JIRA
  email: null                                  # Email для авторизации (опционально)
  api_token: null                              # API токен (опционально)
  auth_required: false                         # Требуется ли авторизация

query:
  project_key: "KAFKA"                         # Ключ проекта
  jql: "project = KAFKA AND created >= -365d"  # JQL запрос
  max_results: 1000                            # Максимум задач (null = все)

output:
  output_dir: "output"                         # Папка для результатов
  top_users: 30                                # Количество пользователей в топе

features:
  fetch_changelog: true                        # Получать историю изменений
```

### Примеры конфигураций

<details>
<summary>Анализ проекта Apache Kafka</summary>

```yaml
jira:
  base_url: "https://issues.apache.org/jira"
  auth_required: false

query:
  project_key: "KAFKA"
  jql: "project = KAFKA AND created >= -365d"
  max_results: 1000

output:
  output_dir: "output/kafka"
  top_users: 30
```
</details>

<details>
<summary>Анализ корпоративного JIRA с авторизацией</summary>

```yaml
jira:
  base_url: "https://your-company.atlassian.net"
  email: "your-email@company.com"
  api_token: "your-api-token-here"
  auth_required: true

query:
  jql: "project = MYPROJECT AND status = Closed AND resolved >= -90d"
  max_results: 500

output:
  output_dir: "output/myproject"
  top_users: 20
```
</details>

##  Примеры выходных графиков

После запуска в папке `output/` будут созданы 6 PNG файлов:

```
output/
├── 1_open_time_histogram.png          # Гистограмма времени в открытом состоянии
├── 2_status_durations.png             # Длительность по статусам
├── 3_daily_stats.png                  # Дневная статистика
├── 4_user_stats.png                   # Топ пользователей
├── 5_time_in_progress_histogram.png   # Время в In Progress
└── 6_priority_distribution.png        # Распределение по приоритетам
```

## Тестирование

### Запуск тестов

```bash
# Все тесты
pytest

# С покрытием
pytest --cov=src --cov-report=html

# Через скрипт
bin/run_tests.bat    # Windows
bash bin/run_tests.sh # Linux/Mac
```

### Тестовое покрытие

- **29 автоматических тестов**
- **73%+ покрытие кода**
- Unit тесты для всех компонентов
- Интеграция с Allure для красивых отчетов

```bash
# Установить Allure (один раз)
scoop install allure  # Windows
brew install allure   # macOS

# Запустить тесты и открыть отчет
pytest --alluredir=allure-results
allure serve allure-results
```

##  Структура проекта

```
jira-analyzer/
├── src/                      # Исходный код
│   ├── data_processor.py    # Обработка данных
│   ├── jira_client.py       # Клиент JIRA API
│   ├── visualizer.py        # Генерация графиков
│   └── cli.py               # CLI интерфейс
│
├── tests/                    # Тесты
│   ├── test_data_processor.py
│   ├── test_jira_client.py
│   └── test_visualizer.py
│
├── bin/                      # Скрипты запуска
│   ├── run.bat              # Windows
│   ├── run.sh               # Linux/Mac
│   ├── run_tests.bat        # Тесты Windows
│   └── run_tests.sh         # Тесты Linux/Mac
│
├── config/                   # Конфигурация
│   └── config.yaml
│
├── output/                   # Результаты (генерируется)
│
├── main.py                   # Точка входа
├── setup.py                  # Установочный скрипт
├── requirements.txt          # Зависимости
├── requirements-dev.txt      # Зависимости для разработки
└── pytest.ini               # Настройки тестов
```

##  Технологии

- **Python 3.7+**
- **requests** - HTTP запросы к JIRA API
- **pandas** - обработка данных
- **matplotlib** - визуализация
- **PyYAML** - конфигурация
- **pytest** - тестирование
- **allure-pytest** - отчеты

##  Использование с разными проектами

### Apache проекты (без авторизации)

```bash
# Kafka
python main.py -p KAFKA -n 1000

# Hadoop HDFS
python main.py -p HDFS -n 500

# Spark
python main.py -p SPARK -n 2000
```




