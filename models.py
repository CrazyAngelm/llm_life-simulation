# 📁 models.py - NPC and location data models
# 🎯 Core function: Defines NPC and Location object structure
# 🔗 Key dependencies: random for initial stats generation
# 💡 Usage: Used in simulator.py to create game world

import random


class NPC:
    """NPC class - autonomous agent with state and behavior"""
    
    def __init__(self, npc_id, name, role, location):
        self.id = npc_id
        self.name = name
        self.role = role
        self.location = location
        self.age = random.randint(18, 60)
        self.stats = {
            "health": random.randint(70, 100),
            "energy": random.randint(40, 100),
            "hunger": random.randint(20, 80),
            "mood": random.randint(30, 90)
        }
        self.relationships = {}  # other_id: level (-100 to 100)
        self.alive = True
        self.actions_today = []

    def to_dict(self):
        """Serialize to dictionary for JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "location": self.location,
            "age": self.age,
            "stats": self.stats,
            "relationships": self.relationships,
            "alive": self.alive,
            "actions_today": self.actions_today
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize from dictionary"""
        npc = cls(data["id"], data["name"], data["role"], data["location"])
        npc.age = data["age"]
        npc.stats = data["stats"]
        npc.relationships = data["relationships"]
        npc.alive = data["alive"]
        npc.actions_today = data.get("actions_today", [])
        return npc

    def add_action(self, action):
        """Add action to daily actions list"""
        self.actions_today.append(action)
        
    def update_relationship(self, other_id, change):
        """Update relationship with another NPC"""
        current = self.relationships.get(other_id, 0)
        new_value = max(-100, min(100, current + change))
        
        # Log significant relationship changes
        if abs(change) >= 5:
            direction = "+" if change > 0 else ""
            print(f"  💕 {self.name} → relationship {direction}{change}: {current} → {new_value}")
        
        self.relationships[other_id] = new_value
        
    def update_stat(self, stat_name, change):
        """Update stat with limits"""
        if stat_name in self.stats:
            old_value = self.stats[stat_name]
            new_value = max(0, min(100, old_value + change))
            
            # Log significant stat changes
            if abs(change) >= 10:
                direction = "+" if change > 0 else ""
                stat_icon = {
                    "health": "❤️",
                    "energy": "⚡",
                    "hunger": "🍽️",
                    "mood": "😊"
                }.get(stat_name, "📊")
                print(f"  {stat_icon} {self.name} → {stat_name} {direction}{change}: {old_value} → {new_value}")
            
            self.stats[stat_name] = new_value


class Location:
    """Location class with NPCs and events"""
    
    def __init__(self, name, location_type, description):
        self.name = name
        self.type = location_type
        self.description = description
        self.npc_ids = []
        self.events_today = []

    def to_dict(self):
        """Serialize to dictionary for JSON"""
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "npc_ids": self.npc_ids,
            "events_today": self.events_today
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize from dictionary"""
        loc = cls(data["name"], data["type"], data["description"])
        loc.npc_ids = data["npc_ids"]
        loc.events_today = data.get("events_today", [])
        return loc

    def add_npc(self, npc_id):
        """Add NPC to location"""
        if npc_id not in self.npc_ids:
            self.npc_ids.append(npc_id)
            
    def remove_npc(self, npc_id):
        """Remove NPC from location"""
        if npc_id in self.npc_ids:
            self.npc_ids.remove(npc_id)
            
    def add_event(self, event):
        """Add event to location"""
        self.events_today.append(event)
        
    def clear_daily_events(self):
        """Clear daily events"""
        self.events_today = []

    def get_alive_npcs(self, npcs_dict):
        """Get list of alive NPCs in location"""
        return [npc_id for npc_id in self.npc_ids if npcs_dict[npc_id].alive] 