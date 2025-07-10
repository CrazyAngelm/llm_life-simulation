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
            available_models = [model['name'] for model in models['models']]
            
            if self.model_name not in available_models and available_models:
                # Use first available model
                self.model_name = available_models[0]
                print(f"🔄 Switching to model: {self.model_name}")
            
            return True
        except Exception as e:
            print(f"❌ Ollama connection error: {e}")
            return False
    
    async def get_npc_decision(self, npc_data: Dict, context: Dict) -> Optional[Dict]:
        """Get NPC decision via LLM"""
        if not self.client:
            return None
            
        try:
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

            response = await self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                timeout=10.0
            )
            
            # Parse response
            content = response["message"]["content"].strip()
            
            # Remove markdown formatting if present
            if content.startswith("```"):
                content = content.split("```")[1].strip()
            if content.startswith("json"):
                content = content[4:].strip()
                
            decision = json.loads(content)
            return decision
            
        except Exception as e:
            print(f"⚠️ LLM error for {npc_data['name']}: {e}")
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
            return self._create_simple_chronicle(events_data)
        
        try:
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

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️ DeepSeek error: {e}")
            return self._create_simple_chronicle(events_data)
    
    def _create_simple_chronicle(self, events_data: Dict) -> str:
        """Create simple chronicle without API"""
        current_day = events_data.get('current_day', 0)
        alive_count = events_data.get('alive_count', 0)
        total_count = events_data.get('total_count', 0)
        key_events = events_data.get('key_events', [])
        
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
    
    async def get_npc_decision(self, npc_data: Dict, context: Dict) -> Optional[Dict]:
        """Get NPC decision"""
        if self.ollama_available:
            return await self.ollama.get_npc_decision(npc_data, context)
        return None
    
    async def generate_chronicle(self, events_data: Dict) -> str:
        """Generate chronicle"""
        return await self.deepseek.generate_chronicle(events_data) 