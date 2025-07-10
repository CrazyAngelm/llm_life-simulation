# 📁 prompt_loader.py - Prompt template loader
# 🎯 Core function: Load and render Jinja2 prompt templates
# 🔗 Key dependencies: jinja2, os
# 💡 Usage: Used in llm_clients.py for prompt management

import os
from pathlib import Path
from typing import Dict, Any

try:
    from jinja2 import Environment, FileSystemLoader, TemplateNotFound
except ImportError:
    print("⚠️ Jinja2 not installed: pip install jinja2")
    Environment = None


class PromptLoader:
    """Loader for Jinja2 prompt templates"""
    
    def __init__(self, templates_dir: str = "prompts"):
        self.templates_dir = Path(templates_dir)
        self.env = None
        
        if Environment:
            if self.templates_dir.exists():
                self.env = Environment(
                    loader=FileSystemLoader(str(self.templates_dir)),
                    trim_blocks=True,
                    lstrip_blocks=True
                )
                print(f"✅ Prompt templates loaded from {self.templates_dir}")
            else:
                print(f"⚠️ Templates directory not found: {self.templates_dir}")
        else:
            print("⚠️ Jinja2 unavailable - falling back to simple prompts")
    
    def render_template(self, template_name: str, **kwargs) -> str:
        """Render a template with given parameters"""
        if not self.env:
            return self._fallback_prompt(template_name, **kwargs)
        
        try:
            template = self.env.get_template(f"{template_name}.j2")
            return template.render(**kwargs)
        except TemplateNotFound:
            print(f"⚠️ Template not found: {template_name}.j2")
            return self._fallback_prompt(template_name, **kwargs)
        except Exception as e:
            print(f"⚠️ Template render error: {e}")
            return self._fallback_prompt(template_name, **kwargs)
    
    def _fallback_prompt(self, template_name: str, **kwargs) -> str:
        """Fallback prompts if Jinja2 is unavailable"""
        if template_name == "generate_locations":
            count = kwargs.get('count', 3)
            return f"""Generate {count} medieval fantasy location names with descriptions.
Each location should be unique and atmospheric.
Return ONLY JSON in this format:
{{"locations": [
  {{"name": "Castle Ravencrest", "type": "royal", "description": "Dark fortress on a cliff"}},
  {{"name": "Willowbrook", "type": "settlement", "description": "Peaceful village by a stream"}},
  {{"name": "Shadowwood", "type": "wilderness", "description": "Mysterious forest full of ancient secrets"}}
]}}"""
        
        elif template_name == "generate_npcs":
            count = kwargs.get('count', 10)
            return f"""Generate {count} medieval fantasy character names with roles and locations.
Mix different social classes and professions.
Return ONLY JSON in this format:
{{"npcs": [
  {{"id": "king_1", "name": "King Aldwin", "role": "king", "location": "Castle"}},
  {{"id": "guard_1", "name": "Sir Garrett", "role": "guard", "location": "Castle"}},
  {{"id": "peasant_1", "name": "Farmer Beck", "role": "peasant", "location": "Village"}},
  {{"id": "merchant_1", "name": "Trader Magnus", "role": "merchant", "location": "Village"}},
  {{"id": "hunter_1", "name": "Hunter Lysa", "role": "hunter", "location": "Forest"}}
]}}"""
        
        elif template_name == "npc_decision":
            return f"""You are a {kwargs.get('npc_role', 'person')} named {kwargs.get('npc_name', 'Unknown')} in {kwargs.get('npc_location', 'somewhere')}.
Your stats: health={kwargs.get('health', 100)}, energy={kwargs.get('energy', 100)}, mood={kwargs.get('mood', 50)}.
Your relationships with nearby people: {kwargs.get('relationships', '{}')}

Make ONE social decision. Reply ONLY JSON:
{{"action": "chat/help/argue/ignore", "target": "other_npc_id", "reason": "brief reason"}}"""
        
        elif template_name == "generate_chronicle":
            current_day = kwargs.get('current_day', 0)
            key_events = kwargs.get('key_events', [])[:20]
            deaths = kwargs.get('deaths', [])
            relationships_summary = kwargs.get('relationships_summary', [])[:10]
            alive_count = kwargs.get('alive_count', 0)
            total_count = kwargs.get('total_count', 0)
            
            events_str = '\n'.join(key_events)
            deaths_str = ', '.join(deaths) if deaths else "Nobody died"
            relationships_str = '\n'.join(relationships_summary)
            
            return f"""Write an epic chronicle of medieval world life simulation for {current_day} days.

KEY EVENTS:
{events_str}

DEATHS: {deaths_str}

RELATIONSHIPS: 
{relationships_str}

ALIVE NPCs: {alive_count}/{total_count}

Write a beautiful story in medieval chronicle style. Use emojis. Be creative but base it on the data."""
        
        else:
            return f"Unknown template: {template_name}"


# Global prompt loader instance
prompt_loader = PromptLoader() 