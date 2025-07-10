# 📁 llm_clients.py - LLM clients
# 🎯 Core function: Integration with Ollama and DeepSeek API
# 🔗 Key dependencies: ollama, openai
# 💡 Usage: Used in simulator.py for LLM decisions and chronicles

import json
import asyncio
from typing import Optional, Dict, Any

try:
    import ollama
except ImportError:
    print("⚠️ Ollama not installed: pip install ollama")
    ollama = None

try:
    import openai
except ImportError:
    print("⚠️ OpenAI not installed: pip install openai")
    openai = None


class OllamaClient:
    """Client for working with Ollama"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = None
        if ollama:
            self.client = ollama.AsyncClient()
    
    async def check_connection(self) -> bool:
        """Check Ollama connection"""
        if not self.client:
            return False
        try:
            models = await self.client.list()
            available_models = []
            if hasattr(models, 'models') and models.models:
                for model in models.models:
                    if hasattr(model, 'name'):
                        available_models.append(model.name)
                    elif hasattr(model, 'model'):
                        available_models.append(model.model)
                    elif isinstance(model, dict):
                        model_name = model.get('name') or model.get('model') or model.get('id', '')
                        if model_name:
                            available_models.append(model_name)
            elif isinstance(models, dict) and 'models' in models:
                for model in models['models']:
                    if isinstance(model, dict):
                        model_name = model.get('name') or model.get('model') or model.get('id', '')
                        if model_name:
                            available_models.append(model_name)
            
            print(f"🔍 Available models: {available_models}")
            
            if self.model_name not in available_models and available_models:
                # Use first available model
                self.model_name = available_models[0]
                print(f"🔄 Switching to model: {self.model_name}")
            elif self.model_name in available_models:
                print(f"✅ Using configured model: {self.model_name}")
            
            return True
        except Exception as e:
            print(f"❌ Ollama connection error: {e}")
            print(f"🔧 Try running: ollama serve")
            return False
    
    async def generate_random_names(self, name_type: str, count: int) -> Optional[Dict]:
        """Generate random names for locations or NPCs"""
        if not self.client:
            return None
            
        try:
            print(f"🎲 [LLM] Generating {count} random {name_type} names...")
            
            if name_type == "locations":
                prompt = f"""Generate {count} medieval fantasy location names with descriptions.
Each location should be unique and atmospheric.
Return ONLY JSON in this format:
{{"locations": [
  {{"name": "Castle Ravencrest", "type": "royal", "description": "Dark fortress on a cliff"}},
  {{"name": "Willowbrook", "type": "settlement", "description": "Peaceful village by a stream"}},
  {{"name": "Shadowwood", "type": "wilderness", "description": "Mysterious forest full of ancient secrets"}}
]}}"""
            
            elif name_type == "npcs":
                prompt = f"""Generate {count} medieval fantasy character names with roles and locations.
Mix different social classes and professions.
Return ONLY JSON in this format:
{{"npcs": [
  {{"id": "king_1", "name": "King Aldwin", "role": "king", "location": "Castle"}},
  {{"id": "guard_1", "name": "Sir Garrett", "role": "guard", "location": "Castle"}},
  {{"id": "peasant_1", "name": "Farmer Beck", "role": "peasant", "location": "Village"}},
  {{"id": "merchant_1", "name": "Trader Magnus", "role": "merchant", "location": "Village"}},
  {{"id": "hunter_1", "name": "Hunter Lysa", "role": "hunter", "location": "Forest"}}
]}}"""
            else:
                return None

            print(f"🔄 [LLM] Sending name generation request to {self.model_name}...")
            
            response = await self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            content = response["message"]["content"].strip()
            
            print(f"📝 [LLM] Received name data: {content[:200]}...")
            
            # Remove markdown formatting if present
            if content.startswith("```"):
                content = content.split("```")[1].strip()
            if content.startswith("json"):
                content = content[4:].strip()
                
            names_data = json.loads(content)
            print(f"✅ [LLM] Generated {len(names_data.get(name_type, []))} {name_type}")
            return names_data
            
        except Exception as e:
            print(f"⚠️ [LLM] Name generation error: {e}")
            return None

    async def get_npc_decision(self, npc_data: Dict, context: Dict) -> Optional[Dict]:
        """Get NPC decision via LLM"""
        if not self.client:
            return None
            
        try:
            print(f"🤖 [LLM] Requesting decision for {npc_data['name']} ({npc_data['role']})...")
            
            # Form context
            relationships_str = {
                k: v for k, v in npc_data['relationships'].items() 
                if k in context.get('nearby_npcs', [])
            }
            
            prompt = f"""You are a {npc_data['role']} named {npc_data['name']} in {npc_data['location']}.
Your stats: health={npc_data['stats']['health']}, energy={npc_data['stats']['energy']}, mood={npc_data['stats']['mood']}.
Your relationships with nearby people: {relationships_str}

Make ONE social decision. Reply ONLY JSON:
{{"action": "chat/help/argue/ignore", "target": "other_npc_id", "reason": "brief reason"}}"""

            print(f"🔄 [LLM] Sending request to model {self.model_name}...")
            
            response = await self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            content = response["message"]["content"].strip()
            
            print(f"📝 [LLM] Received response: {content}")
            
            # Remove markdown formatting if present
            if content.startswith("```"):
                content = content.split("```")[1].strip()
            if content.startswith("json"):
                content = content[4:].strip()
                
            decision = json.loads(content)
            print(f"✅ [LLM] Decision processed: {decision}")
            return decision
            
        except Exception as e:
            print(f"⚠️ [LLM] Error for {npc_data['name']}: {e}")
            return None


class DeepSeekClient:
    """Client for working with DeepSeek API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        if openai and api_key != "sk-your-deepseek-key-here":
            self.client = openai.OpenAI(
                base_url="https://api.deepseek.com/v1",
                api_key=api_key
            )
    
    def is_available(self) -> bool:
        """Check DeepSeek availability"""
        return self.client is not None
    
    async def generate_chronicle(self, events_data: Dict) -> str:
        """Generate chronicle via DeepSeek"""
        if not self.client:
            print("🤖 [LLM] DeepSeek unavailable, generating simple chronicle...")
            return self._create_simple_chronicle(events_data)
        
        try:
            print(f"🤖 [LLM] Requesting chronicle generation from DeepSeek...")
            
            key_events = events_data.get('key_events', [])
            deaths = events_data.get('deaths', [])
            relationships = events_data.get('relationships_summary', [])
            current_day = events_data.get('current_day', 0)
            alive_count = events_data.get('alive_count', 0)
            total_count = events_data.get('total_count', 0)

            prompt = f"""Write an epic chronicle of medieval world life simulation for {current_day} days.

KEY EVENTS:
{key_events[:20]}  

DEATHS: {deaths if deaths else "Nobody died"}

RELATIONSHIPS: {relationships[:10]}

ALIVE NPCs: {alive_count}/{total_count}

Write a beautiful story in medieval chronicle style. Use emojis. Be creative but base it on the data."""

            print(f"🔄 [LLM] Sending chronicle generation request...")

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.8
            )
            
            chronicle_text = response.choices[0].message.content
            print(f"✅ [LLM] Chronicle generated ({len(chronicle_text)} characters)")
            print(f"📝 [LLM] Chronicle preview: {chronicle_text[:100]}...")
            
            return chronicle_text
            
        except Exception as e:
            print(f"⚠️ [LLM] DeepSeek error: {e}")
            print("🤖 [LLM] Switching to local chronicle generation...")
            return self._create_simple_chronicle(events_data)
    
    def _create_simple_chronicle(self, events_data: Dict) -> str:
        """Create simple chronicle without API"""
        current_day = events_data.get('current_day', 0)
        alive_count = events_data.get('alive_count', 0)
        total_count = events_data.get('total_count', 0)
        key_events = events_data.get('key_events', [])
        
        print(f"📝 [LOCAL] Creating local chronicle for {current_day} days...")
        
        chronicle = f"""# 📜 Simulation Chronicle

## Simulation days: {current_day}
## Surviving NPCs: {alive_count}/{total_count}

### Key events of recent days:
"""
        
        for i, event in enumerate(key_events[-10:], 1):
            chronicle += f"{i}. {event}\n"
        
        chronicle += "\n*Chronicle generated locally (DeepSeek unavailable)*"
        return chronicle


class LLMManager:
    """Manager for working with multiple LLMs"""
    
    def __init__(self, ollama_model: str, deepseek_key: str):
        self.ollama = OllamaClient(ollama_model)
        self.deepseek = DeepSeekClient(deepseek_key)
        self.ollama_available = False
        
    async def initialize(self):
        """Initialize LLM clients"""
        print("🔄 Initializing LLM clients...")
        
        # Check Ollama
        self.ollama_available = await self.ollama.check_connection()
        if self.ollama_available:
            print("✅ Ollama connected")
        else:
            print("⚠️ Ollama unavailable")
        
        # Check DeepSeek
        if self.deepseek.is_available():
            print("✅ DeepSeek API ready")
        else:
            print("⚠️ DeepSeek API unavailable (will use simple chronicle)")
    
    async def generate_random_names(self, name_type: str, count: int) -> Optional[Dict]:
        """Generate random names"""
        if self.ollama_available:
            return await self.ollama.generate_random_names(name_type, count)
        return None
    
    async def get_npc_decision(self, npc_data: Dict, context: Dict) -> Optional[Dict]:
        """Get NPC decision"""
        if self.ollama_available:
            return await self.ollama.get_npc_decision(npc_data, context)
        return None
    
    async def generate_chronicle(self, events_data: Dict) -> str:
        """Generate chronicle"""
        return await self.deepseek.generate_chronicle(events_data) 