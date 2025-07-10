# 📁 config.py - Simulation configuration
# 🎯 Core function: Centralized project settings
# 🔗 Key dependencies: None (basic Python)
# 💡 Usage: Imported in simulator.py and main.py

CONFIG = {
    # Simulation settings
    "max_days": 10,
    "llm_decision_chance": 0.3,  # 30% decisions via LLM
    "random_event_chance": 0.25,
    
    # World generation settings
    "world_generation": {
        "location_count": 3,
        "npc_count": 10
    },
    
    # LLM settings
    "ollama_model": "qwen2.5:3b",  # Ollama model
    "deepseek_api_key": "sk-60184baa615d4f9a97e1cafe57d62d6b",
    
    # Locations
    "locations": [
        ("Castle", "royal", "Majestic castle with stone walls"),
        ("Village", "settlement", "Cozy village with houses and workshops"),
        ("Forest", "wilderness", "Dark forest full of game and dangers")
    ],
    
    # NPC data
    "npc_data": [
        ("king_1", "King Aldric", "king", "Castle"),
        ("guard_1", "Sir Marcus", "guard", "Castle"),
        ("peasant_1", "Farmer John", "peasant", "Village"),
        ("peasant_2", "Baker Anna", "peasant", "Village"),
        ("peasant_3", "Smith Tom", "peasant", "Village"),
        ("merchant_1", "Trader Paul", "merchant", "Village"),
        ("hunter_1", "Hunter Bob", "hunter", "Forest"),
        ("hunter_2", "Ranger Kate", "hunter", "Forest"),
        ("sage_1", "Wise Elena", "sage", "Castle"),
        ("child_1", "Little Tim", "child", "Village")
    ],
    
    # Events by location
    "location_events": {
        "Castle": ["royal feast", "ambassador visit", "knight tournament"],
        "Village": ["market day", "harvest", "wedding", "festival"],
        "Forest": ["wolf attack", "treasure discovery", "stranger encounter"]
    },
    
    # Actions by role
    "role_actions": {
        "king": "👑 ruled the kingdom",
        "guard": "⚔️ patrolled",
        "peasant": "🌾 worked in the field",
        "merchant": "💰 traded",
        "hunter": "🏹 hunted",
        "sage": "📚 studied books",
        "child": "🎮 played"
    }
} 