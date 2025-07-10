# llm_life-simulation

# Полная архитектура системы текстовой эмуляции мира

## 1. КОНЦЕПТУАЛЬНАЯ ОСНОВА И ЦЕЛИ

### Ключевые принципы
- **Иерархическая детализация**: важные локации обрабатываются подробнее
- **Эмерджентность**: сложное поведение из простых правил
- **Консистентность**: все события согласованы во времени и пространстве
- **Экономичность**: минимум токенов LLM для максимум результата

### Масштабы обработки
- **Уровень 1 (Критический)**: Детальная симуляция с индивидуальными историями
- **Уровень 2 (Важный)**: Социальные процессы и групповые события  
- **Уровень 3 (Фоновый)**: Упрощенная обработка ключевых изменений

## 2. ФАЙЛОВАЯ АРХИТЕКТУРА

### Общая структура проекта
```
/LLM_LIFE-SIMULATION
├── /engine                          # 🚀 Движок симуляции (общий для всех миров)
│   ├── world_engine.py              # Основной цикл симуляции
│   ├── llm_manager.py               # Управление LLM запросами
│   ├── event_processor.py           # Обработка событий
│   ├── chronicle_generator.py       # Генерация хроник
│   ├── consistency_checker.py       # Проверка противоречий
│   └── /prompts                     # Библиотека промптов
│       ├── location_events.j2
│       ├── character_update.j2
│       └── chronicle_generation.j2
├── /tools                           # 🛠️ Утилиты (общие для всех миров)
│   ├── init_world.py                # Создание нового мира
│   ├── cli.py                       # Командная строка
│   ├── export_chronicles.py         # Экспорт результатов
│   └── world_manager.py             # Управление мирами
├── /world_1                         # 🌍 Первый мир
│   ├── config.yaml                  # Настройки мира
│   ├── people_params.json           # Параметры персонажей
│   ├── location_params.json         # Параметры локаций
│   ├── continents.json              # Континенты и их описания
│   ├── professions.json             # Профессии и их характеристики
│   ├── creatures.json               # Существа, животные, расы
│   ├── world_description.md         # Описание мира и сеттинга
│   ├── world_rules.json             # Основные правила мира (~10)
│   ├── /data
│   │   ├── /continents
│   │   │   └── /aethermoor          # Пример континента
│   │   │       ├── meta.yaml        # Климат, культура, особенности
│   │   │       └── /regions
│   │   │           ├── /northern_reaches
│   │   │           │   ├── meta.yaml
│   │   │           │   └── /locations
│   │   │           │       ├── /irongate_city
│   │   │           │       │   ├── state.yaml      # Текущее состояние
│   │   │           │       │   ├── people.json     # Персонажи локации
│   │   │           │       │   ├── events_queue.json # События к обработке
│   │   │           │       │   ├── relationships.json # Связи между NPC
│   │   │           │       │   └── /logs
│   │   │           │       │       └── day_0432.md
│   │   │           │       └── /mistwood_village
│   │   │           └── /southern_plains
│   │   ├── /chronicles              # Хроники мира
│   │   │   ├── global_timeline.md   # Главная хроника
│   │   │   ├── /by_year
│   │   │   └── /by_region
│   │   ├── /templates               # Шаблоны для генерации
│   │   └── /cache                   # Кэш для embeddings и промптов
│   └── /exports                     # Экспортированные данные
├── /world_2                         # 🌍 Второй мир (пример)
│   ├── config.yaml                  # Свои настройки
│   ├── people_params.json           # Свои параметры персонажей
│   ├── location_params.json         # Свои параметры локаций
│   ├── continents.json              # Свои континенты
│   ├── professions.json             # Свои профессии
│   ├── creatures.json               # Свои существа
│   ├── world_description.md         # Свое описание мира
│   ├── world_rules.json             # Свои правила
│   └── /data
│       └── ...                      # Аналогичная структура
└── requirements.txt                 # Зависимости Python
```

### Работа с разными мирами
```bash
# Создание нового мира
python tools/init_world.py --world world_3 --name "Sci-Fi Universe"

# Запуск симуляции конкретного мира
python engine/world_engine.py --world world_1 --days 30

# Экспорт хроник мира
python tools/export_chronicles.py --world world_1 --format markdown
```

## 3. СХЕМЫ ДАННЫХ

### config.yaml - Глобальные настройки мира
```yaml
world:
  name: "Aethermoor Chronicles"
  start_day: 1
  current_day: 432
  time_scale: "1_day"  # 1 тик = 1 день
  tick_frequency: 1    # Частота тиков (каждые N дней)
  
simulation:
  max_events_per_location_per_day: 3
  population_event_multiplier: 0.001  # вероятность события на душу населения
  inter_location_delay: 1  # дни для путешествий между локациями
  
  # 🎯 МАСШТАБИРУЕМОСТЬ (10-1000 существ)
  character_limits:
    max_active_characters: 100      # Максимум активных персонажей
    max_background_characters: 500  # Максимум фоновых персонажей
    max_dormant_characters: 1000    # Максимум спящих персонажей
  
  batch_processing:
    background_update_frequency: 7   # Обновлять фоновых персонажей раз в N дней
    dormant_update_frequency: 30     # Обновлять спящих персонажей раз в N дней
    batch_size: 50                   # Размер batch для групповых операций
  
  demographics:
    average_lifespan_years: 70       # Средняя продолжительность жизни
    birth_rate_per_1000: 25          # Рождаемость на 1000 жителей в год
    death_rate_per_1000: 15          # Смертность на 1000 жителей в год
    marriage_age_min: 18             # Минимальный возраст для брака
    marriage_age_max: 35             # Максимальный возраст для брака
  
llm:
  provider: "openai"  # openai, anthropic, deepseek, local
  model: "gpt-4o-mini"
  max_tokens: 1000
  temperature: 0.7
  
  # 💰 ОПТИМИЗАЦИЯ ЗАТРАТ
  tiered_models:
    critical_tasks: "gpt-4o"         # Дорогая модель для критических задач
    standard_tasks: "gpt-4o-mini"    # Дешевая модель для обычных задач
    simple_tasks: "local"            # Локальная модель для простых задач
  
processing:
  detail_levels:
    critical: 1.0    # Полная обработка
    important: 0.7   # Большинство событий
    background: 0.3  # Только ключевые изменения
  
  # 🚀 ПРОИЗВОДИТЕЛЬНОСТЬ
  performance:
    lazy_loading: true               # Ленивая загрузка персонажей
    cache_character_summaries: true  # Кэшировать краткие описания
    parallel_location_processing: true # Параллельная обработка локаций
```

### people_params.json - Настройки доступных параметров 
```json
{
    "value": "0=lowest, 1=highest; fractional values allowed",
    "vital_stats": [
        {
            "name": "health",
            "desc": "Character’s health. 0 – dead, 1 – fully healthy"
        },
        {
            "name": "moral",
            "desc": "Character’s morale. 0 – despair, 1 – happiness"
        },
        {
            "name": "wealth",
            "desc": "Character’s wealth. 0 – poor, 1 – wealthy"
        },
        {
            "name": "reputation",
            "desc": "Character’s reputation. 0 – bad, 1 – good"
        }
    ],
    "traits": [
        {
            "name": "brave",
            "desc": "Willing to face danger or pain without fear"
        },
        {
            "name": "greedy",
            "desc": "Has an excessive desire for wealth or possessions"
        },
        {
            "name": "social",
            "desc": "Enjoys interacting with others and building relationships"
        },
        {
            "name": "ambitious",
            "desc": "Driven by a strong desire to achieve success or power"
        },
        {
            "name": "kidness",
            "desc": "Shows a caring and generous nature toward others"
        }
    ],
    "type_relationship": [
        {
            "name": "spouse",
            "desc": "A partner joined by marriage or committed relationship"
        },
        {
            "name": "rival",
            "desc": "Someone competing for the same goal or position"
        },
        {
            "name": "friend",
            "desc": "A person with whom one shares mutual affection and trust"
        },
        {
            "name": "enemy",
            "desc": "Someone who is actively hostile or opposed"
        },
        {
            "name": "relative",
            "desc": "A person connected by blood or familial ties"
        },
        {
            "name": "parent",
            "desc": "An individual who has begotten or raised a child"
        },
        {
            "name": "child",
            "desc": "A young person born to or raised by a parent"
        },
        {
            "name": "subordinate",
            "desc": "An individual working under the authority of another"
        },
        {
            "name": "boss",
            "desc": "A person with authority to oversee and direct others"
        }
    ]
}
```
### location_params.json - Параметры локаций
```json
{
    "value": "0=lowest, 1=highest; fractional values allowed",
    "resources": [
        {"name": "food", "desc": "Food availability and agricultural capacity"},
        {"name": "materials", "desc": "Raw materials and construction resources"},
        {"name": "wealth", "desc": "Economic prosperity and trade capacity"},
        {"name": "knowledge", "desc": "Education, libraries, and scholarly activity"},
        {"name": "population", "desc": "Number of inhabitants"}
    ],
    "conditions": [
        {"name": "weather", "desc": "Current weather and seasonal patterns"},
        {"name": "mood", "desc": "General mood and satisfaction of population"},
        {"name": "stability", "desc": "Political and social stability"},
        {"name": "health", "desc": "Disease prevention and medical care quality"}
    ],
    "economy": [
        {"name": "primary_trade", "desc": "Main economic activities and specializations"},
        {"name": "trade_routes", "desc": "Connections to other locations for commerce"},
        {"name": "market_conditions", "desc": "Current state of local economy"}
    ],
    "politics": [
        {"name": "ruler", "desc": "Current leader or governing body"},
        {"name": "government_type", "desc": "System of governance"},
        {"name": "current_issues", "desc": "Active political problems or conflicts"}
    ],
    "culture": [
        {"name": "primary_values", "desc": "Core cultural values and beliefs"},
        {"name": "current_trends", "desc": "Popular activities and social movements"},
        {"name": "traditions", "desc": "Long-standing customs and practices"}
    ]
}
```

### continents.json - Континенты мира
```json
{
    "continents": [
        {
            "id": "aethermoor",
            "name": "Aethermoor",
            "description": "A mystical continent shrouded in ancient magic and dotted with floating islands",
            "climate": "temperate with magical phenomena",
            "culture_traits": ["mystical", "scholarly", "traditional"],
            "dominant_races": ["humans", "elves", "wizards"],
            "regions": ["northern_reaches", "southern_plains", "central_highlands"]
        },
        {
            "id": "ironlands",
            "name": "Ironlands", 
            "description": "A harsh mountainous continent rich in minerals and forges",
            "climate": "cold and dry",
            "culture_traits": ["industrious", "militant", "honor-bound"],
            "dominant_races": ["dwarves", "humans", "orcs"],
            "regions": ["mountain_kingdoms", "steel_valleys"]
        }
    ]
}
```

### professions.json - Профессии в мире
```json
{
    "professions": [
        {
            "id": "blacksmith",
            "name": "Blacksmith",
            "description": "Crafts weapons, tools, and metal goods",
            "typical_traits": {"brave": 0.6, "social": 0.4, "ambitious": 0.5},
            "typical_wealth": 0.6,
            "location_types": ["city", "town", "village"],
            "required_resources": ["materials"],
            "profession_category": "crafter"
        },
        {
            "id": "farmer",
            "name": "Farmer",
            "description": "Grows crops and raises livestock",
            "typical_traits": {"brave": 0.4, "social": 0.6, "ambitious": 0.3},
            "typical_wealth": 0.3,
            "location_types": ["village", "town"],
            "required_resources": ["food"],
            "profession_category": "producer"
        },
        {
            "id": "merchant",
            "name": "Merchant",
            "description": "Trades goods between locations",
            "typical_traits": {"brave": 0.5, "social": 0.8, "ambitious": 0.7},
            "typical_wealth": 0.7,
            "location_types": ["city", "town"],
            "required_resources": ["wealth"],
            "profession_category": "trader"
        },
        {
            "id": "guard",
            "name": "Guard",
            "description": "Protects locations and maintains order",
            "typical_traits": {"brave": 0.8, "social": 0.5, "ambitious": 0.4},
            "typical_wealth": 0.4,
            "location_types": ["city", "town", "fortress"],
            "required_resources": [],
            "profession_category": "military"
        },
        {
            "id": "scholar",
            "name": "Scholar",
            "description": "Studies knowledge and teaches others",
            "typical_traits": {"brave": 0.3, "social": 0.6, "ambitious": 0.6},
            "typical_wealth": 0.5,
            "location_types": ["city", "academy"],
            "required_resources": ["knowledge"],
            "profession_category": "intellectual"
        }
    ]
}
```

### creatures.json - Существа в мире
```json
{
    "categories": {
        "intelligent": "Разумные существа способные к сложным взаимодействиям",
        "animals": "Обычные животные и существа без развитого интеллекта",
        "magical": "Существа с магическими способностями",
        "undead": "Нежить и духи"
    },
    "creatures": [
        {
            "id": "human",
            "name": "Human",
            "category": "intelligent",
            "description": "The most common intelligent race, adaptable and diverse",
            "typical_lifespan": 70,
            "base_traits": {"brave": 0.5, "social": 0.6, "ambitious": 0.5},
            "can_have_professions": true,
            "population_weight": 1.0
        },
        {
            "id": "elf",
            "name": "Elf", 
            "category": "intelligent",
            "description": "Long-lived magical beings with deep connection to nature",
            "typical_lifespan": 300,
            "base_traits": {"brave": 0.6, "social": 0.4, "ambitious": 0.3},
            "can_have_professions": true,
            "population_weight": 0.3
        },
        {
            "id": "dwarf",
            "name": "Dwarf",
            "category": "intelligent", 
            "description": "Hardy mountain folk known for craftsmanship and mining",
            "typical_lifespan": 150,
            "base_traits": {"brave": 0.7, "social": 0.7, "ambitious": 0.6},
            "can_have_professions": true,
            "population_weight": 0.4
        },
        {
            "id": "wolf",
            "name": "Wolf",
            "category": "animals",
            "description": "Pack hunters roaming forests and plains",
            "typical_lifespan": 12,
            "base_traits": {"brave": 0.8, "social": 0.9, "ambitious": 0.2},
            "can_have_professions": false,
            "population_weight": 0.1
        },
        {
            "id": "dragon",
            "name": "Dragon",
            "category": "magical",
            "description": "Ancient magical beings of immense power",
            "typical_lifespan": 1000,
            "base_traits": {"brave": 0.9, "social": 0.1, "ambitious": 0.9},
            "can_have_professions": false,
            "population_weight": 0.001
        }
    ]
}
```

### world_description.md - Описание мира
```markdown
# Aethermoor Chronicles - Описание Мира

## Общий Обзор
Мир Этермура представляет собой фантастический континент, где магия переплетается с повседневной жизнью. Древние цивилизации оставили свой след в виде магических артефактов и руин, а современные государства строят свое будущее на основе торговли, ремесел и дипломатии.

## Географический Контекст
Континент Этермур разделен на несколько регионов:
- **Северные Пределы**: Суровые горные земли, богатые металлами
- **Центральные Равнины**: Плодородные земли с крупными городами
- **Южные Долины**: Мягкий климат, центр торговли и культуры

## Социальная Структура
- **Правящие классы**: Лорды и маги управляют крупными городами
- **Ремесленники**: Основа экономики, объединены в гильдии  
- **Торговцы**: Связывают регионы торговыми путями
- **Крестьяне**: Большинство населения, занятое сельским хозяйством

## Магическая Система
Магия присутствует в мире, но не доминирует. Она проявляется в:
- Зачарованных предметах и инструментах
- Магических существах и явлениях
- Редких людях с врожденными способностями

## Политическая Ситуация
Мир находится в состоянии хрупкого равновесия между:
- Городами-государствами со своими интересами
- Торговыми гильдиями, влияющими на экономику
- Древними магическими орденами
- Растущей угрозой от диких земель

## Основные Конфликты
- Торговые споры между городами
- Набеги варваров с севера
- Политические интриги знати
- Противостояние магии и технологий
```

### world_rules.json - Основные правила мира
```json
{
    "rules": [
        {
            "id": "mortality",
            "name": "Закон Смертности",
            "description": "Все разумные существа смертны и стареют естественным образом"
        },
        {
            "id": "magic_rarity", 
            "name": "Редкость Магии",
            "description": "Магические способности встречаются у менее чем 5% населения"
        },
        {
            "id": "economic_balance",
            "name": "Экономическое Равновесие", 
            "description": "Ресурсы ограничены, торговля необходима для процветания"
        },
        {
            "id": "social_mobility",
            "name": "Социальная Мобильность",
            "description": "Персонажи могут изменить свой статус через труд, удачу или выдающиеся поступки"
        },
        {
            "id": "consequence_system",
            "name": "Система Последствий",
            "description": "Каждое действие имеет логические последствия, влияющие на мир"
        },
        {
            "id": "relationship_dynamics",
            "name": "Динамика Отношений",
            "description": "Отношения между персонажами развиваются на основе их взаимодействий"
        },
        {
            "id": "environmental_influence",
            "name": "Влияние Окружения",
            "description": "Погода, сезоны и природные события влияют на жизнь персонажей"
        },
        {
            "id": "cultural_diversity",
            "name": "Культурное Разнообразие",
            "description": "Разные регионы имеют уникальные традиции и ценности"
        },
        {
            "id": "information_flow",
            "name": "Поток Информации",
            "description": "Новости и слухи распространяются с реалистичной скоростью"
        },
        {
            "id": "generational_change",
            "name": "Смена Поколений",
            "description": "Молодое поколение может изменить устоявшиеся традиции"
        }
    ]
}
```

### Person Schema (people.json) - Расширенная схема с состояниями
```json
{
  "id": "npc_irongate_0042",
  "name": "Элара Кузнецова", 
  "age": 28,
  "location": "irongate_city",
  "creature_type": "human",
  "profession": "blacksmith",
  "character_state": "active",  # active/background/dormant
  "last_update_day": 432,
  
  "traits": {
    "brave": 0.8,
    "greedy": 0.2,
    "social": 0.6,
    "ambitious": 0.7
  },
  "vital_stats": {
    "health": 0.9,
    "wealth": 0.4,
    "reputation": 0.6
  },
  "relationships": {
    "npc_irongate_0031": {"type": "spouse", "strength": 0.9},
    "npc_irongate_0015": {"type": "rival", "strength": -0.4}
  },
  "goals": [
    {"type": "expand_business", "priority": 0.8, "progress": 0.3},
    {"type": "have_children", "priority": 0.6, "progress": 0.0}
  ],
  "history": [
    {"day": 420, "event": "married", "target": "npc_irongate_0031"},
    {"day": 430, "event": "won_contract", "value": "city_guard_weapons"}
  ],
  "chronicle_importance": 0.4  # Вероятность попадания в хроники
}
```

## 3.1. РАЗДЕЛЕНИЕ ЗАДАЧ: КОД vs LLM

### 🤖 Через КОД (быстро, дешево, детерминированно):

#### Вычислительные задачи
- Подсчет статистик популяции и ресурсов
- Обновление численных параметров (здоровье, богатство)
- Вычисление расстояний и времени путешествий
- Применение правил старения и смертности
- Распределение персонажей по уровням важности

#### Логические операции
- Валидация событий по установленным правилам
- Проверка совместимости профессий с локациями
- Определение возможности взаимодействий
- Управление состояниями персонажей (active/background/dormant)
- Batch-обработка групп персонажей

#### Простая генерация
- Создание имен по шаблонам и паттернам
- Базовое распределение характеристик
- Случайные события по предустановленным таблицам
- Простые экономические расчеты
- Механические обновления отношений

### 🎭 Через LLM (творчество, нарратив, сложная логика):

#### Творческие задачи
- Генерация описаний событий и их последствий
- Создание уникальных личностей персонажей
- Описания локаций, культур и традиций
- Составление хроник и повествований
- Разработка сложных конфликтов

#### Нарративные элементы
- Диалоги между персонажами
- Мотивации и цели персонажей
- Культурные особенности регионов
- Исторические события и их интерпретация
- Слухи и новости между локациями

#### Комплексные решения
- Разрешение сложных социальных конфликтов
- Генерация цепочек связанных событий
- Создание политических интриг
- Развитие долгосрочных сюжетных линий
- Адаптация под уникальный контекст мира

### 🎯 Гибридные задачи (код + LLM):
- **Генерация персонажа**: Код задает базовые параметры → LLM создает личность
- **События**: Код определяет возможность → LLM создает описание
- **Отношения**: Код вычисляет совместимость → LLM объясняет развитие
- **Экономика**: Код считает ресурсы → LLM описывает торговые события

## 3.2. СИСТЕМА МАСШТАБИРОВАНИЯ ПЕРСОНАЖЕЙ

### Состояния персонажей
```python
CHARACTER_STATES = {
    "active": {
        "description": "Полная обработка каждый тик",
        "update_frequency": 1,  # каждый день
        "max_characters": 100,
        "llm_usage": "high",
        "criteria": ["в критических локациях", "высокая важность", "активные цели"]
    },
    "background": {
        "description": "Упрощенная обработка",
        "update_frequency": 7,  # раз в неделю
        "max_characters": 500,
        "llm_usage": "medium", 
        "criteria": ["в важных локациях", "средняя важность", "стабильная ситуация"]
    },
    "dormant": {
        "description": "Минимальная обработка",
        "update_frequency": 30,  # раз в месяц
        "max_characters": 1000,
        "llm_usage": "low",
        "criteria": ["в фоновых локациях", "низкая важность", "неактивные роли"]
    }
}
```

### Переходы между состояниями
```python
def update_character_states(world_state):
    """Оптимизирует распределение персонажей по состояниям"""
    all_characters = load_all_characters()
    
    # Сортировка по важности
    characters_by_importance = sorted(all_characters, 
                                    key=calculate_character_importance, 
                                    reverse=True)
    
    # Распределение по состояниям
    active_count = world_state.config.character_limits.max_active_characters
    background_count = world_state.config.character_limits.max_background_characters
    
    for i, char in enumerate(characters_by_importance):
        if i < active_count:
            char.state = "active"
        elif i < active_count + background_count:
            char.state = "background"
        else:
            char.state = "dormant"
            
def calculate_character_importance(character):
    """Вычисляет важность персонажа для определения состояния"""
    importance = character.chronicle_importance
    
    # Бонусы за активность
    if character.goals and any(g.progress > 0 for g in character.goals):
        importance += 0.2
        
    # Бонусы за отношения
    if character.relationships:
        importance += len(character.relationships) * 0.05
        
    # Бонусы за локацию
    location = get_location(character.location)
    if location.detail_level == "critical":
        importance += 0.3
    elif location.detail_level == "important":
        importance += 0.1
        
    return min(1.0, importance)
```

### Batch-обработка для масштабирования
```python
class CharacterBatchProcessor:
    def __init__(self, batch_size=50):
        self.batch_size = batch_size
    
    def process_background_characters(self, characters):
        """Групповая обработка фоновых персонажей"""
        batches = [characters[i:i+self.batch_size] 
                  for i in range(0, len(characters), self.batch_size)]
        
        for batch in batches:
            # Групповые операции без LLM
            self.apply_aging(batch)
            self.update_basic_stats(batch)
            self.process_simple_goals(batch)
    
    def apply_aging(self, characters):
        """Применяет старение ко всем персонажам в batch"""
        for char in characters:
            days_passed = current_day - char.last_update_day
            # Простое старение без LLM
            if days_passed >= 365:  # Прошел год
                char.age += 1
                char.health *= 0.99  # Небольшое снижение здоровья
    
    def process_dormant_characters(self, characters):
        """Минимальная обработка спящих персонажей"""
        # Только критические события: смерть от старости
        for char in characters:
            if char.age > char.creature_type.typical_lifespan * 0.9:
                if random.random() < 0.01:  # 1% шанс смерти
                    self.schedule_death_event(char)
```

### Event Schema (events_queue.json)
```json
{
  "events": [
    {
      "id": "evt_433_001",
      "day": 433,
      "type": "travel",
      "actor": "npc_irongate_0042",
      "action": "travel_to",
      "target": "mistwood_village",
      "reason": "deliver_weapons",
      "duration": 2,
      "consequences": ["trade_relationship", "reputation_gain"],
      "priority": "important"
    },
    {
      "id": "evt_433_002", 
      "day": 433,
      "type": "social",
      "actor": "npc_irongate_0015",
      "action": "spread_rumors",
      "target": "npc_irongate_0042",
      "reason": "business_rivalry",
      "consequences": ["reputation_loss", "potential_conflict"]
    }
  ]
}
```

### Location State (state.yaml)
```yaml
name: "Irongate City"
type: "major_city"
population: 8500
detail_level: "critical"  # critical/important/background

resources:
  food: 0.8      # 0.0 = голод, 1.0 = изобилие
  materials: 0.9
  wealth: 0.6
  knowledge: 0.5

conditions:
  weather: "autumn_rains"
  mood: 0.7      # Общественное настроение
  stability: 0.8 # Политическая стабильность
  health: 0.9    # Эпидемии, медицина

economy:
  primary_trade: ["metalworking", "weapon_crafting"]
  trade_routes: ["mistwood_village", "goldenhaven_port"]
  market_conditions: "growing"

politics:
  ruler: "npc_irongate_0001"  # Лорд Гаррет
  government_type: "feudal_city_state"
  current_issues: ["tax_collection", "bandit_raids"]

culture:
  primary_values: ["craftsmanship", "honor", "tradition"]
  current_trends: ["military_preparation", "trade_expansion"]
  
recent_events:
  - "Major weapons order from neighboring cities"
  - "Rumors of increased bandit activity on trade routes"
  - "Harvest festival preparations beginning"
```

## 4. СИСТЕМА СОБЫТИЙ И ПРИОРИТЕТОВ

### Типы событий
```python
EVENT_TYPES = {
    # Персональные события
    "birth": {"chronicle_chance": 0.1, "local_impact": 0.2},
    "death": {"chronicle_chance": 0.8, "local_impact": 0.6}, 
    "marriage": {"chronicle_chance": 0.3, "local_impact": 0.3},
    "profession_change": {"chronicle_chance": 0.2, "local_impact": 0.3},
    
    # Социальные события  
    "trade_deal": {"chronicle_chance": 0.4, "local_impact": 0.5},
    "conflict": {"chronicle_chance": 0.7, "local_impact": 0.8},
    "festival": {"chronicle_chance": 0.5, "local_impact": 0.6},
    
    # Политические события
    "ruler_change": {"chronicle_chance": 1.0, "local_impact": 0.9},
    "law_change": {"chronicle_chance": 0.8, "local_impact": 0.7},
    "alliance": {"chronicle_chance": 0.9, "local_impact": 0.8},
    
    # Природные события
    "disaster": {"chronicle_chance": 0.9, "local_impact": 1.0},
    "resource_discovery": {"chronicle_chance": 0.7, "local_impact": 0.8},
    "epidemic": {"chronicle_chance": 0.9, "local_impact": 0.9}
}
```

### Система приоритетов
```python
def calculate_chronicle_priority(event, location, global_state):
    base_priority = EVENT_TYPES[event["type"]]["chronicle_chance"]
    
    # Модификаторы
    actor_importance = get_character_importance(event["actor"])
    location_importance = location["detail_level_multiplier"]
    global_relevance = check_global_relevance(event, global_state)
    
    final_priority = base_priority * actor_importance * location_importance * global_relevance
    return min(1.0, final_priority)
```

## 5. LLM СИСТЕМА И ПРОМПТЫ

### Специализированные промпты

#### Генератор событий локации
```python
LOCATION_EVENT_PROMPT = """
Ты управляешь симуляцией локации "{location_name}" (население: {population}).

ТЕКУЩАЯ СИТУАЦИЯ:
{current_state}

АКТИВНЫЕ ПЕРСОНАЖИ (топ-5 по важности):
{top_characters}

ВНЕШНИЕ ФАКТОРЫ:
- Погода: {weather}  
- Торговые связи: {trade_status}
- Политическая обстановка: {politics}

СОБЫТИЯ ВЧЕРА:
{yesterday_events}

ЗАДАЧА: Сгенерируй 2-4 логичных события на сегодня ({current_day}), учитывая:
- Характеры и цели персонажей
- Социально-экономическую ситуацию
- Последствия вчерашних событий
- Сезонность и внешние факторы

ФОРМАТ ОТВЕТА (строгий JSON):
{
  "events": [
    {
      "type": "event_type",
      "actor": "character_id", 
      "action": "что происходит",
      "target": "цель/объект", 
      "reason": "мотивация",
      "consequences": ["последствие1", "последствие2"]
    }
  ]
}

ВАЖНО: События должны быть реалистичными для данной культуры и эпохи.
"""

#### Генератор хроник
```python
CHRONICLE_PROMPT = """
Ты - летописец, создающий краткие исторические записи.

СОБЫТИЯ ДНЯ {day} ПО ВСЕМ ЛОКАЦИЯМ:
{all_events}

ЗАДАЧА: Выбери 3-5 самых значимых событий и запиши как историческую хронику.

КРИТЕРИИ ВАЖНОСТИ:
- Смерти/рождения важных людей
- Политические изменения  
- Крупные торговые сделки
- Конфликты и альянсы
- Стихийные бедствия
- Культурные события

ФОРМАТ: Краткие предложения в стиле средневековых хроник.

ПРИМЕР:
"День 432-й года Железного Кольца: В Железных Воротах скончался мастер-кузнец Торгрим от старости. Купец Эдвард из Золотой Гавани заключил крупную сделку на поставку оружия. В Туманном Лесу охотники сообщили о странных следах неизвестного зверя."

НЕ ВКЛЮЧАЙ: мелкие бытовые события, рутинную торговлю, обычные разговоры.
"""

#### Обновление персонажа  
```python
CHARACTER_UPDATE_PROMPT = """
Обнови персонажа после события.

ПЕРСОНАЖ:
{character_data}

СОБЫТИЕ:
{event_description}

ОБНОВИ в JSON:
- возраст (если прошло время)
- vital_stats (здоровье, богатство, репутация)  
- relationships (новые связи или изменения)
- goals (прогресс или новые цели)
- добавь в history

ВЕРНИ ТОЛЬКО обновленные поля в JSON, НЕ весь профиль.
"""
```

### Система кэширования промптов
```python
class PromptCache:
    def __init__(self):
        self.location_embeddings = {}
        self.character_summaries = {}
        
    def get_location_context(self, location_id):
        if location_id not in self.location_embeddings:
            # Создаем сжатое описание локации
            self.location_embeddings[location_id] = self.compress_location_data(location_id)
        return self.location_embeddings[location_id]
    
    def compress_location_data(self, location_id):
        # Сжимаем данные локации до ключевых параметров
        full_data = load_location_state(location_id)
        compressed = {
            "name": full_data["name"],
            "population": full_data["population"],
            "primary_trade": full_data["economy"]["primary_trade"][:2],
            "mood": full_data["conditions"]["mood"],
            "key_issues": full_data["politics"]["current_issues"][:2]
        }
        return compressed
```

## 6. ОСНОВНОЙ ЦИКЛ СИМУЛЯЦИИ

### world_engine.py
```python
import asyncio
import json
from typing import Dict, List
from llm_manager import LLMManager
from event_processor import EventProcessor
from chronicle_generator import ChronicleGenerator

class WorldEngine:
    def __init__(self, config_path: str):
        self.config = self.load_config(config_path)
        self.llm = LLMManager(self.config["llm"])
        self.event_processor = EventProcessor()
        self.chronicle_gen = ChronicleGenerator(self.llm)
        self.current_day = self.config["world"]["current_day"]
        
    async def run_simulation(self, days: int):
        """Главный цикл симуляции"""
        for day in range(self.current_day, self.current_day + days):
            print(f"Обработка дня {day}...")
            
            # 1. Загружаем все локации
            locations = self.load_all_locations()
            all_events = []
            
            # 2. Обрабатываем локации по важности
            critical_locations = [loc for loc in locations if loc["detail_level"] == "critical"]
            important_locations = [loc for loc in locations if loc["detail_level"] == "important"] 
            background_locations = [loc for loc in locations if loc["detail_level"] == "background"]
            
            # 3. Детальная обработка критических локаций
            for location in critical_locations:
                events = await self.process_location_detailed(location, day)
                all_events.extend(events)
                
            # 4. Упрощенная обработка важных локаций
            for location in important_locations:
                events = await self.process_location_standard(location, day)
                all_events.extend(events)
                
            # 5. Минимальная обработка фоновых локаций
            for location in background_locations:
                events = self.process_location_minimal(location, day)
                all_events.extend(events)
            
            # 6. Межлокационные взаимодействия
            inter_events = self.process_inter_location_events(all_events)
            all_events.extend(inter_events)
            
            # 7. Генерация хроник
            chronicles = await self.chronicle_gen.generate_daily_chronicle(all_events, day)
            self.save_chronicles(chronicles, day)
            
            # 8. Обновление глобального состояния
            self.update_global_state(day, all_events)
            
            print(f"День {day} завершен. События: {len(all_events)}")
            
    async def process_location_detailed(self, location: Dict, day: int) -> List[Dict]:
        """Детальная обработка критических локаций"""
        # 1. Обрабатываем очередь событий
        queued_events = self.event_processor.process_queue(location, day)
        
        # 2. Генерируем новые события через LLM
        context = self.build_location_context(location, day)
        new_events = await self.llm.generate_location_events(context)
        
        # 3. Валидация через правила  
        valid_events = self.validate_events(new_events, location)
        
        # 4. Обновляем персонажей
        await self.update_characters(location, valid_events)
        
        # 5. Обновляем состояние локации
        self.update_location_state(location, valid_events)
        
        all_events = queued_events + valid_events
        
        # 6. Записываем детальный лог
        self.save_location_log(location, day, all_events)
        
        return all_events
        
    async def process_location_standard(self, location: Dict, day: int) -> List[Dict]:
        """Стандартная обработка важных локаций"""
        # Упрощенная версия - без детальных логов
        queued_events = self.event_processor.process_queue(location, day)
        
        # Генерируем меньше событий
        context = self.build_simplified_context(location, day)
        new_events = await self.llm.generate_location_events(context, max_events=2)
        
        valid_events = self.validate_events(new_events, location)
        self.update_location_state(location, valid_events)
        
        return queued_events + valid_events
        
    def process_location_minimal(self, location: Dict, day: int) -> List[Dict]:
        """Минимальная обработка фоновых локаций"""
        # Только события из очереди + случайные ключевые события
        queued_events = self.event_processor.process_queue(location, day)
        
        # Простая генерация без LLM
        random_events = self.generate_random_key_events(location, day)
        
        return queued_events + random_events
```

### Валидация событий
```python
class EventValidator:
    def __init__(self, rules_path: str):
        self.rules = self.load_rules(rules_path)
        
    def validate_events(self, events: List[Dict], location: Dict) -> List[Dict]:
        """Проверяет события на корректность"""
        valid_events = []
        
        for event in events:
            if self.check_event_rules(event, location):
                if self.check_character_exists(event["actor"]):
                    if self.check_physics_rules(event):
                        valid_events.append(event)
                    else:
                        print(f"Отклонено по физике: {event}")
                else:
                    print(f"Персонаж не найден: {event['actor']}")
            else:
                print(f"Нарушены правила: {event}")
                
        return valid_events
        
    def check_event_rules(self, event: Dict, location: Dict) -> bool:
        """Проверка правил для типа события"""
        event_type = event["type"]
        
        if event_type == "death":
            # Не больше 1 смерти важного персонажа в неделю
            return self.check_death_frequency(event["actor"], location)
            
        elif event_type == "travel":
            # Проверяем возможность путешествия
            return self.check_travel_possibility(event["actor"], event["target"])
            
        return True
```

## 7. СИСТЕМА ОПТИМИЗАЦИИ И ЭКОНОМИИ ТОКЕНОВ

### Иерархическая обработка по важности
```python
def calculate_location_importance(location: Dict, global_state: Dict) -> float:
    """Рассчитывает важность локации для определения уровня детализации"""
    importance = 0.0
    
    # Население
    importance += min(1.0, location["population"] / 10000) * 0.3
    
    # Количество важных персонажей  
    important_chars = sum(1 for char in location["characters"] 
                         if char["chronicle_importance"] > 0.5)
    importance += min(1.0, important_chars / 5) * 0.3
    
    # Политическое значение
    if location["type"] in ["capital", "major_city"]:
        importance += 0.2
    elif location["type"] in ["city", "fortress"]:
        importance += 0.1
        
    # Активность событий (за последние 7 дней)
    recent_activity = get_recent_event_count(location["id"], days=7)
    importance += min(1.0, recent_activity / 20) * 0.2
    
    return min(1.0, importance)

def assign_detail_levels():
    """Распределяет локации по уровням детализации"""
    locations = load_all_locations()
    
    # Сортируем по важности
    locations_with_importance = [
        (loc, calculate_location_importance(loc, global_state)) 
        for loc in locations
    ]
    locations_with_importance.sort(key=lambda x: x[1], reverse=True)
    
    total_locations = len(locations_with_importance)
    
    # Распределяем уровни: 20% критических, 30% важных, 50% фоновых
    for i, (location, importance) in enumerate(locations_with_importance):
        if i < total_locations * 0.2:
            location["detail_level"] = "critical"
        elif i < total_locations * 0.5:
            location["detail_level"] = "important"  
        else:
            location["detail_level"] = "background"
```

### Система кэширования и переиспользования
```python
class ContextCache:
    def __init__(self):
        self.character_summaries = {}
        self.location_summaries = {}
        self.event_templates = {}
        
    def get_character_summary(self, character_id: str) -> str:
        """Возвращает краткое описание персонажа для промптов"""
        if character_id not in self.character_summaries:
            char = load_character(character_id)
            summary = f"{char['name']} ({char['age']}): {char['profession']}, " \
                     f"цели: {[g['type'] for g in char['goals'][:2]]}"
            self.character_summaries[character_id] = summary
        return self.character_summaries[character_id]
        
    def invalidate_character(self, character_id: str):
        """Сбрасывает кэш при изменении персонажа"""
        if character_id in self.character_summaries:
            del self.character_summaries[character_id]
```

### Многоуровневые LLM модели
```python
class TieredLLMManager:
    def __init__(self, config: Dict):
        # Тяжелая модель для критических задач
        self.heavy_model = "gpt-4o"  
        # Легкая модель для простых задач
        self.light_model = "gpt-4o-mini"
        # Локальная модель для кэшируемых задач
        self.local_model = "phi-3-mini"
        
    async def generate_events(self, context: Dict, importance: str):
        """Выбор модели в зависимости от важности"""
        if importance == "critical":
            return await self.call_llm(self.heavy_model, context, max_tokens=1500)
        elif importance == "important":  
            return await self.call_llm(self.light_model, context, max_tokens=800)
        else:
            return await self.call_llm(self.local_model, context, max_tokens=400)
```

## 8. MVP РЕАЛИЗАЦИЯ - ПОШАГОВЫЙ ПЛАН

### Этап 1: Основа (1-2 дня)
```bash
# 1. Создание структуры проекта
mkdir world_simulation && cd world_simulation
python -m venv venv && source venv/bin/activate
pip install pyyaml openai anthropic asyncio

# 2. Инициализация мира
python tools/init_world.py --name "TestWorld" --locations 2 --characters 10

# 3. Базовый цикл без LLM
python engine/world_engine.py --days 3 --mode debug
```

#### init_world.py
```python
#!/usr/bin/env python3
import yaml
import json
import os
import argparse
from pathlib import Path

def create_test_world(name: str, num_locations: int, num_characters: int):
    """Создает тестовый мир с базовыми данными"""
    
    # Создаем структуру папок
    base_path = Path("data")
    base_path.mkdir(exist_ok=True)
    
    # Конфиг мира
    config = {
        "world": {
            "name": name,
            "start_day": 1,
            "current_day": 1,
            "time_scale": "1_day"
        },
        "simulation": {
            "max_events_per_location_per_day": 3,
            "population_event_multiplier": 0.001
        },
        "llm": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "max_tokens": 1000
        }
    }
    
    with open("config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    
    # Создаем тестовые локации
    continent_path = base_path / "continents" / "testland"
    region_path = continent_path / "regions" / "central"
    continent_path.mkdir(parents=True, exist_ok=True)
    region_path.mkdir(parents=True, exist_ok=True)
    
    locations = ["irongate_city", "mistwood_village"][:num_locations]
    
    for i, loc_name in enumerate(locations):
        loc_path = region_path / "locations" / loc_name
        loc_path.mkdir(parents=True, exist_ok=True)
        
        # Состояние локации
        state = {
            "name": loc_name.replace("_", " ").title(),
            "type": "city" if "city" in loc_name else "village",
            "population": 5000 - i * 2000,
            "detail_level": "critical" if i == 0 else "important",
            "resources": {"food": 0.8, "materials": 0.7, "wealth": 0.6},
            "conditions": {"weather": "clear", "mood": 0.7, "stability": 0.8}
        }
        
        with open(loc_path / "state.yaml", "w") as f:
            yaml.dump(state, f, default_flow_style=False)
        
        # Персонажи
        characters = []
        chars_per_location = num_characters // num_locations
        
        for j in range(chars_per_location):
            char = {
                "id": f"npc_{loc_name}_{j:04d}",
                "name": f"Character_{j}",
                "age": 20 + j * 3,
                "location": loc_name,
                "profession": ["farmer", "trader", "guard", "crafter"][j % 4],
                "traits": {"brave": 0.5, "social": 0.5},
                "vital_stats": {"health": 0.9, "wealth": 0.5, "reputation": 0.5},
                "relationships": {},
                "goals": [{"type": "survive", "priority": 1.0}],
                "history": [],
                "chronicle_importance": 0.1 + (j % 3) * 0.3
            }
            characters.append(char)
        
        with open(loc_path / "people.json", "w") as f:
            json.dump(characters, f, indent=2)
        
        # Пустая очередь событий
        with open(loc_path / "events_queue.json", "w") as f:
            json.dump({"events": []}, f, indent=2)
    
    print(f"Создан тестовый мир '{name}' с {num_locations} локациями и {num_characters} персонажами")
    print("Запуск: python engine/world_engine.py --days 5")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="TestWorld")
    parser.add_argument("--locations", type=int, default=2)
    parser.add_argument("--characters", type=int, default=10)
    
    args = parser.parse_args()
    create_test_world(args.name, args.locations, args.characters)
```

### Этап 2: Интеграция LLM (2-3 дня)
```python
# llm_manager.py - простая версия
class SimpleLLMManager:
    def __init__(self, config):
        self.config = config
        if config["provider"] == "openai":
            import openai
            self.client = openai.OpenAI()
        
    async def generate_location_events(self, context, max_events=3):
        prompt = f"""
        Локация: {context['location_name']} (население: {context['population']})
        Текущий день: {context['day']}
        
        Сгенерируй {max_events} простых события для этого дня в JSON формате:
        {{"events": [{{"type": "social", "actor": "character_id", "action": "краткое описание"}}]}}
        
        Типы событий: social, economic, personal, travel
        """
        
        response = await self.client.chat.completions.create(
            model=self.config["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.config["max_tokens"]
        )
        
        return json.loads(response.choices[0].message.content)
```

### Этап 3: Хроники и экспорт (1 день)
```python
# chronicle_generator.py
class ChronicleGenerator:
    def generate_daily_summary(self, all_events, day):
        important_events = [e for e in all_events if e.get("chronicle_worthy", False)]
        
        if not important_events:
            return f"День {day}: Тихий день во всех землях."
        
        summary_parts = []
        for event in important_events[:5]:  # Топ 5 событий
            summary_parts.append(f"В {event['location']}: {event['action']}")
        
        return f"День {day}: " + ". ".join(summary_parts) + "."
```

## 9. ПОДВОДНЫЕ КАМНИ И РЕШЕНИЯ

### Проблема: Лавина событий
```python
def prevent_event_avalanche(location, events):
    """Ограничивает количество событий"""
    max_events = max(1, location["population"] // 1000)  # 1 событие на 1000 жителей
    return events[:max_events]
```

### Проблема: Противоречивые события
```python
class ConsistencyChecker:
    def __init__(self):
        self.global_facts = {}
        
    def check_event_consistency(self, event, global_state):
        """Проверяет событие на противоречия"""
        if event["type"] == "death":
            char_id = event["actor"]
            if char_id in self.global_facts.get("dead_characters", []):
                return False, "Character already dead"
        
        if event["type"] == "travel":
            # Проверяем, не путешествует ли персонаж уже
            if self.is_character_traveling(event["actor"]):
                return False, "Character already traveling"
        
        return True, "OK"
```

### Проблема: Деградация характеров персонажей
```python
def maintain_character_consistency(character, event):
    """Проверяет соответствие события характеру персонажа"""
    if event["type"] == "heroic_action" and character["traits"]["brave"] < 0.3:
        event["probability"] *= 0.1  # Снижаем вероятность
    
    if event["type"] == "generous_gift" and character["traits"]["greedy"] > 0.7:
        event["probability"] *= 0.1
    
    return event
```

## 10. РАСШИРЕНИЕ И МОДУЛИ

### Система модов
```python
# /mods/medieval_fantasy.py
class MedievalFantasyMod:
    def __init__(self):
        self.additional_event_types = {
            "magic_discovery": {"chronicle_chance": 0.9},
            "dragon_sighting": {"chronicle_chance": 1.0},
            "spell_casting": {"chronicle_chance": 0.3}
        }
        
    def modify_character_generation(self, character):
        # Добавляем магические способности
        character["magic_power"] = random.uniform(0, 1)
        return character
        
    def custom_event_rules(self, event, location):
        if event["type"] == "dragon_sighting":
            # Драконы не появляются в маленьких деревнях
            return location["population"] > 1000
        return True
```

### Экспорт и аналитика
```python
# tools/export_chronicles.py
class ChronicleExporter:
    def export_to_markdown(self, start_day, end_day):
        """Экспорт хроник в красивый Markdown"""
        chronicles = load_chronicles(start_day, end_day)
        
        markdown = f"# Хроники мира {self.world_name}\n\n"
        
        for day, events in chronicles.items():
            markdown += f"## День {day}\n\n"
            for event in events:
                markdown += f"- **{event['location']}**: {event['description']}\n"
            markdown += "\n"
        
        return markdown
        
    def generate_statistics(self, start_day, end_day):
        """Статистика развития мира"""
        stats = {
            "total_events": 0,
            "births": 0,
            "deaths": 0,
            "marriages": 0,
            "conflicts": 0,
            "location_activity": {}
        }
        
        chronicles = load_chronicles(start_day, end_day)
        for day, events in chronicles.items():
            for event in events:
                stats["total_events"] += 1
                stats[event["type"]] = stats.get(event["type"], 0) + 1
                
                loc = event["location"]
                stats["location_activity"][loc] = stats["location_activity"].get(loc, 0) + 1
        
        return stats
```

## 11. ГОТОВЫЙ СТАРТОВЫЙ КИТ

### Команды для запуска
```bash
# Инициализация нового мира
python tools/init_world.py --name "MyWorld" --locations 3 --characters 15

# Запуск симуляции
python engine/world_engine.py --days 30 --verbose

# Экспорт хроник  
python tools/export_chronicles.py --format markdown --days 1-30 --output chronicles.md

# Статистика мира
python tools/world_stats.py --days 1-30
```

### Файл requirements.txt
```
pyyaml>=6.0
openai>=1.0.0
anthropic>=0.18.0
asyncio
aiofiles
click>=8.0
rich>=13.0
```

## 12. АНАЛИЗ ОПТИМАЛЬНОСТИ И РЕКОМЕНДАЦИИ

### ✅ Что КРИТИЧЕСКИ ВАЖНО для интересной симуляции:

#### Основа системы (приоритет 1)
- **Персонажи с целями**: Движущая сила событий
- **Система отношений**: Создает драму и конфликты  
- **Простые правила мира**: 10 четких правил определяют логику
- **Иерархическая обработка**: Критично для масштабирования
- **Консистентность событий**: Предотвращает противоречия

#### Масштабируемость (приоритет 2)
- **Три состояния персонажей**: active/background/dormant
- **Batch-обработка**: Для больших популяций
- **Ленивая загрузка**: Экономия памяти
- **Кэширование**: Ускорение повторных операций
- **Многоуровневые LLM**: Оптимизация затрат

### ❌ Что можно УПРОСТИТЬ без потери качества:

#### Избыточные элементы
- ~~relationships.json отдельно~~ → Объединить с people.json
- ~~Детальные логи всех локаций~~ → Только для критических
- ~~Сложная экономическая модель~~ → Базовые ресурсы достаточно
- ~~Многоуровневая география~~ → Континент→Локация (без регионов)

#### Второстепенные системы
- Сложная политика (базовых отношений достаточно)
- Детальная магическая система (можно добавить позже)
- Погодная система (влияет мало на интерес)
- Комплексные торговые маршруты

### 🎯 ОПТИМАЛЬНАЯ АРХИТЕКТУРА для MVP:

```
ОСНОВНЫЕ КОМПОНЕНТЫ (обязательные):
├── Персонажи с состояниями (active/background/dormant)
├── События с приоритетами  
├── Локации с уровнями важности
├── Простая экономика (4 ресурса)
├── Система правил (10 правил)
└── Хроники важных событий

ОПТИМИЗАЦИИ (критичные для 10-1000 существ):
├── Batch-обработка фоновых персонажей
├── Многоуровневые LLM модели
├── Кэширование промптов
├── Ленивая загрузка данных
└── Параллельная обработка локаций

ДОПОЛНЕНИЯ (можно добавить позже):
├── Сложная политика
├── Детальная экономика  
├── Магическая система
├── Погода и климат
└── Подробная география
```

### 📊 МЕТРИКИ УСПЕШНОСТИ MVP:

1. **Автономность**: Симуляция работает >7 дней без вмешательства
2. **Стоимость**: <$5 на 1000 существ в месяц
3. **Производительность**: Обработка дня <30 секунд для 100 активных персонажей
4. **Интерес**: Генерируется >3 интересных событий в день
5. **Консистентность**: <1% противоречивых событий

### 🚀 ПЛАН РЕАЛИЗАЦИИ (по приоритетам):

#### Фаза 1: Минимальная база (3-5 дней)
1. Базовая структура файлов с новыми файлами конфигурации
2. Простая генерация персонажей (только код)
3. Базовые события без LLM
4. Примитивные хроники

#### Фаза 2: LLM интеграция (5-7 дней)  
1. Интеграция с OpenAI для описаний событий
2. Система промптов и кэширования
3. Валидация событий
4. Улучшенные хроники

#### Фаза 3: Масштабирование (3-5 дней)
1. Система состояний персонажей
2. Batch-обработка
3. Многоуровневые LLM модели
4. Оптимизация производительности

#### Фаза 4: Полировка (2-3 дня)
1. Улучшение интерфейса
2. Экспорт и аналитика
3. Тестирование на больших мирах
4. Документация для пользователей

### 💡 КЛЮЧЕВЫЕ ПРИНЦИПЫ ДЛЯ РЕАЛИЗАЦИИ:

1. **Начинай просто**: Сначала 10 персонажей, потом масштабируй
2. **Код первый**: Если можно сделать кодом - делай кодом
3. **LLM для креатива**: Только для того, что требует творчества
4. **Измеряй затраты**: Контролируй расходы на API с первого дня
5. **Тестируй масштабирование**: Регулярно проверяй на больших данных

---

### 🎯 ГОТОВНОСТЬ К РЕАЛИЗАЦИИ:
Архитектура теперь полная и сбалансированная. Все компоненты логично связаны, противоречия устранены, масштабируемость обеспечена. Можно начинать реализацию с уверенностью в том, что система будет работать эффективно для 10-1000 существ при разумных затратах на API.

**С чего лучше начать прямо сейчас?**
1. Создать базовую структуру проекта 
2. Реализовать init_world.py с новыми файлами конфигурации
3. Запустить простой тест с 10 персонажами без LLM