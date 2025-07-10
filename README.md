# 🚀 LLM Life Simulator - Quick Start

## 📁 Project Structure
```
life_simulator_mvp/
├── config.py            # Simulation settings
├── models.py            # NPC and Location classes
├── llm_clients.py       # Ollama & DeepSeek integration
├── simulator.py         # Core simulation logic
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── README_QUICK_START.md # This guide

# Generated at runtime:
├── world_state.json   # Current world state
└── chronicles.md      # Narrative chronicles
```

## ⚡ Quick Start (5 minutes)

### 1. Install dependencies
```bash
python -m venv venv
.\venv\scripts\activate
pip install -r requirements.txt
```

### 2. Launch Ollama
```bash
# In a separate terminal:
ollama serve
ollama pull qwen2.5:3b
```

### 3. Configure DeepSeek API (optional)
Edit `config.py`, line:
```python
"deepseek_api_key": "your-key-here"  # Replace
```

### 4. Run the simulation
```bash
python main.py
```

## 🎯 What It Demonstrates

### AI AGENT aspects
- ✅ **10 autonomous NPCs** with state (health, energy, mood, hunger)
- ✅ **Roles & behaviour**: king, peasants, hunters, sage, merchant
- ✅ **Social relationships**: dynamic links between agents
- ✅ **Decision-making**: reacts to internal state & environment

### LLM aspects
- ✅ **Ollama integration**: 30 % of decisions via local LLM
- ✅ **DeepSeek API**: generates final chronicles
- ✅ **Hybrid approach**: deterministic code + creative LLM
- ✅ **Context awareness**: LLM sees full world state

## 📊 Output
After execution you receive:

1. **world_state.json** – Full simulation state:
   - Stats of all NPCs
   - Relationships between characters
   - Events per location
   - Daily logs

2. **chronicles.md** – Epic fantasy-style chronicle (via DeepSeek)

## ⚙️ Configuration
In `config.py` you can tweak:
- `max_days` – simulation length
- `llm_decision_chance` – share of LLM decisions (0.3 = 30 %)
- `random_event_chance` – frequency of random events
- `ollama_model` – Ollama model to use

## 🛠️ Troubleshooting

**Ollama not running:**
```bash
ollama serve
ollama list          # check models
ollama pull qwen2.5:3b # if model is missing
```

**DeepSeek error:**
- Verify API key in `config.py`
- Simulation works without DeepSeek (simpler chronicle)

**Python errors:**
- Requires Python 3.8+
- Make sure to install: `pip install ollama openai`

## 🎓 For Presentation

### Key Points
1. **Modular architecture** – each component has a clear responsibility
2. **Hybrid AI** – rule-based logic + LLM creativity
3. **Living simulation** – NPCs age, die, build relationships
4. **Scalable** – easy to add new NPCs or locations
5. **Practical demo** – showcases AI Agent + LLM patterns

### Technology
- **Python 3.8+** – primary language
- **Ollama** – local LLM for decision making
- **DeepSeek API** – powerful LLM for chronicles
- **JSON** – state persistence
- **Async/Await** – efficient LLM interaction