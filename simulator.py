# 📁 simulator.py - Core world simulator logic
# 🎯 Core function: Manages simulation, NPCs, events and time
# 🔗 Key dependencies: models, llm_clients, config, json, random
# 💡 Usage: Central class, used in main.py

import json
import random
import asyncio
from typing import Dict, List, Optional

from models import NPC, Location
from llm_clients import LLMManager
from config import CONFIG


class WorldSimulator:
    """Main world simulation class"""
    
    def __init__(self):
        print("🌍 Initializing world...")
        self.current_day = 0
        self.npcs: Dict[str, NPC] = {}
        self.locations: Dict[str, Location] = {}
        self.daily_logs: List[Dict] = []
        self.llm_manager = None
        
        self._init_world()
        
    async def initialize_llm(self):
        """Initialize LLM clients"""
        self.llm_manager = LLMManager(
            CONFIG["ollama_model"],
            CONFIG["deepseek_api_key"]
        )
        await self.llm_manager.initialize()

    def _init_world(self):
        """Initialize game world"""
        # Create locations
        for name, loc_type, desc in CONFIG["locations"]:
            self.locations[name] = Location(name, loc_type, desc)

        # Create NPCs
        for npc_id, name, role, location in CONFIG["npc_data"]:
            npc = NPC(npc_id, name, role, location)
            self.npcs[npc_id] = npc
            self.locations[location].add_npc(npc_id)

        # Initialize relationships between NPCs
        self._init_relationships()
        
        print(f"✅ Created {len(self.npcs)} NPCs in {len(self.locations)} locations")

    def _init_relationships(self):
        """Initialize relationships between NPCs"""
        npc_list = list(self.npcs.keys())
        for npc_id in npc_list:
            for other_id in npc_list:
                if npc_id != other_id:
                    # Base relations with slight randomness
                    base_relation = random.randint(-30, 50)
                    self.npcs[npc_id].relationships[other_id] = base_relation

    async def run_simulation(self):
        """Main simulation loop"""
        print(f"\n🚀 Starting simulation for {CONFIG['max_days']} days\n")
        
        for day in range(1, CONFIG["max_days"] + 1):
            self.current_day = day
            print(f"📅 Day {day}")
            
            # Clear daily data
            self._clear_daily_data()

            # Main day loop
            self._update_aging()
            self._rule_based_decisions()
            await self._llm_decisions()
            self._random_events()
            
            # Logging and saving
            self._log_day()
            self._save_world_state()
            
            # Pause for observation
            await asyncio.sleep(0.1)

        # Final chronicle generation
        await self._generate_final_chronicle()
        print(f"\n🎉 Simulation finished! Check world_state.json and chronicles.md")

    def _clear_daily_data(self):
        """Clear daily data"""
        for npc in self.npcs.values():
            npc.actions_today = []
        for loc in self.locations.values():
            loc.clear_daily_events()

    def _update_aging(self):
        """Update age and health of NPCs"""
        dead_npcs = []
        
        for npc in self.npcs.values():
            if not npc.alive:
                continue
                
            # Aging (very slow for demo)
            npc.age += 0.1
            
            # Natural energy and hunger reduction
            npc.update_stat("energy", -random.randint(10, 25))
            npc.update_stat("hunger", random.randint(15, 30))
            
            # Age effect on health
            if npc.age > 65:
                npc.update_stat("health", -random.randint(1, 3))
                
            # Death from disease/old age
            if npc.stats["health"] <= 0:
                npc.alive = False
                npc.add_action(f"💀 {npc.name} died")
                dead_npcs.append(npc.name)
                print(f"💀 {npc.name} died at age {npc.age:.1f}")
                
        # Remove dead NPCs from locations
        for npc_name in dead_npcs:
            dead_npc = next(npc for npc in self.npcs.values() if npc.name == npc_name)
            self.locations[dead_npc.location].remove_npc(dead_npc.id)

    def _rule_based_decisions(self):
        """Rule-based decisions for NPCs (food, sleep, work)"""
        for npc in self.npcs.values():
            if not npc.alive:
                continue

            # Food - priority №1
            if npc.stats["hunger"] > 70:
                npc.update_stat("hunger", -40)
                npc.update_stat("energy", 15)
                npc.update_stat("mood", 10)
                npc.add_action(f"🍞 {npc.name} ate")

            # Sleep/rest - if low energy
            elif npc.stats["energy"] < 30:
                npc.update_stat("energy", 50)
                npc.update_stat("mood", 15)
                npc.add_action(f"😴 {npc.name} rested")

            # Work based on role - if energy is high
            elif npc.stats["energy"] > 60 and random.random() < 0.6:
                action = CONFIG["role_actions"].get(npc.role, "worked")
                npc.add_action(f"{npc.name} {action}")
                npc.update_stat("energy", -15)
                npc.update_stat("mood", 5)

    async def _llm_decisions(self):
        """LLM-powered decisions for social interactions"""
        if not self.llm_manager:
            return

        for npc in self.npcs.values():
            if not npc.alive or random.random() > CONFIG["llm_decision_chance"]:
                continue

            # Get other NPCs in the same location
            location_npcs = self.locations[npc.location].get_alive_npcs(self.npcs)
            location_npcs = [npc_id for npc_id in location_npcs if npc_id != npc.id]

            if not location_npcs:
                continue

            # Formulate context for LLM
            context = {
                "nearby_npcs": location_npcs[:3],  # Top 3 closest
                "location": npc.location
            }

            # Get decision from LLM
            decision = await self.llm_manager.get_npc_decision(npc.to_dict(), context)
            
            if decision:
                await self._apply_llm_decision(npc, decision, location_npcs)

    async def _apply_llm_decision(self, npc: NPC, decision: Dict, available_npcs: List[str]):
        """Apply LLM decision"""
        action = decision.get("action", "ignore")
        target_id = decision.get("target", "")
        reason = decision.get("reason", "unknown reason")
        
        if target_id not in available_npcs:
            return

        target_npc = self.npcs[target_id]
        
        if action == "chat":
            # Friendly conversation
            npc.update_relationship(target_id, 10)
            target_npc.update_relationship(npc.id, 5)
            npc.update_stat("mood", 10)
            npc.add_action(f"💬 {npc.name} talked to {target_npc.name} ({reason})")
            
        elif action == "help":
            # Helping
            npc.update_relationship(target_id, 15)
            target_npc.update_relationship(npc.id, 20)
            target_npc.update_stat("mood", 15)
            npc.update_stat("energy", -10)
            npc.add_action(f"🤝 {npc.name} helped {target_npc.name} ({reason})")
            
        elif action == "argue":
            # Conflict
            npc.update_relationship(target_id, -20)
            target_npc.update_relationship(npc.id, -15)
            npc.update_stat("mood", -10)
            target_npc.update_stat("mood", -15)
            npc.add_action(f"😠 {npc.name} argued with {target_npc.name} ({reason})")

    def _random_events(self):
        """Generate random events in locations"""
        for location in self.locations.values():
            if random.random() < CONFIG["random_event_chance"]:
                possible_events = CONFIG["location_events"].get(location.name, ["strange event"])
                event = random.choice(possible_events)
                
                # Affect NPCs in the location
                alive_npcs = location.get_alive_npcs(self.npcs)
                for npc_id in alive_npcs:
                    npc = self.npcs[npc_id]
                    self._apply_event_effects(npc, event)
                
                location.add_event(f"🎲 {event}")
                print(f"📍 {location.name}: {event}")

    def _apply_event_effects(self, npc: NPC, event: str):
        """Apply effects of the event to NPCs"""
        if any(word in event for word in ["feast", "wedding", "festival"]):
            npc.update_stat("mood", 20)
        elif "attack" in event:
            npc.update_stat("health", -15)
            npc.update_stat("mood", -20)
        elif "treasure" in event:
            npc.update_stat("mood", 30)
        elif "harvest" in event:
            npc.update_stat("mood", 15)

    def _log_day(self):
        """Log events of the day"""
        day_summary = {
            "day": self.current_day,
            "alive_npcs": sum(1 for npc in self.npcs.values() if npc.alive),
            "locations": {}
        }
        
        for loc_name, location in self.locations.items():
            alive_count = len(location.get_alive_npcs(self.npcs))
            actions = []
            
            for npc_id in location.npc_ids:
                npc = self.npcs[npc_id]
                if npc.alive and npc.actions_today:
                    actions.extend(npc.actions_today)
            
            day_summary["locations"][loc_name] = {
                "npc_count": alive_count,
                "events": location.events_today.copy(),
                "actions": actions
            }
        
        self.daily_logs.append(day_summary)

    def _save_world_state(self):
        """Save world state to JSON"""
        world_data = {
            "current_day": self.current_day,
            "npcs": {npc_id: npc.to_dict() for npc_id, npc in self.npcs.items()},
            "locations": {loc_name: loc.to_dict() for loc_name, loc in self.locations.items()},
            "daily_logs": self.daily_logs
        }
        
        with open("world_state.json", "w", encoding="utf-8") as f:
            json.dump(world_data, f, ensure_ascii=False, indent=2)

    async def _generate_final_chronicle(self):
        """Generate final chronicle"""
        if not self.llm_manager:
            print("⚠️ LLM Manager not initialized")
            return

        # Collect data for the chronicle
        key_events = []
        deaths = []
        
        # Recent events
        for day_log in self.daily_logs[-10:]:
            for loc_name, loc_data in day_log["locations"].items():
                key_events.extend(loc_data["events"])
                key_events.extend(loc_data["actions"][:3])  # Take 3 actions from location
        
        # Deaths
        for npc in self.npcs.values():
            if not npc.alive:
                deaths.append(f"{npc.name} ({npc.role})")

        # Relationships
        relationships_summary = []
        for npc in self.npcs.values():
            if npc.alive and npc.relationships:
                best_friend = max(npc.relationships.items(), key=lambda x: x[1], default=("no one", 0))
                worst_enemy = min(npc.relationships.items(), key=lambda x: x[1], default=("no one", 0))
                
                if best_friend[1] > 50:
                    friend_name = self.npcs[best_friend[0]].name
                    relationships_summary.append(f"{npc.name} is friends with {friend_name}")
                if worst_enemy[1] < -30:
                    enemy_name = self.npcs[worst_enemy[0]].name
                    relationships_summary.append(f"{npc.name} is enemies with {enemy_name}")

        # Prepare data for LLM
        events_data = {
            "key_events": key_events,
            "deaths": deaths,
            "relationships_summary": relationships_summary,
            "current_day": self.current_day,
            "alive_count": sum(1 for npc in self.npcs.values() if npc.alive),
            "total_count": len(self.npcs)
        }

        # Generate chronicle
        chronicle = await self.llm_manager.generate_chronicle(events_data)
        
        # Add statistics
        stats = f"""

## 📊 Simulation Statistics

**Days simulated**: {self.current_day}
**Alive NPCs**: {events_data['alive_count']}/{events_data['total_count']}
**Dead**: {len(deaths)}

### NPCs by location:
"""
        for loc_name, location in self.locations.items():
            alive_here = len(location.get_alive_npcs(self.npcs))
            stats += f"- **{loc_name}**: {alive_here} NPC\n"

        final_chronicle = chronicle + stats
        
        # Save chronicle
        with open("chronicles.md", "w", encoding="utf-8") as f:
            f.write(final_chronicle)
            
        print("✅ Chronicle saved to chronicles.md")

    def get_world_status(self) -> Dict:
        """Get current world status"""
        return {
            "day": self.current_day,
            "alive_npcs": sum(1 for npc in self.npcs.values() if npc.alive),
            "total_npcs": len(self.npcs),
            "locations": {
                name: len(loc.get_alive_npcs(self.npcs)) 
                for name, loc in self.locations.items()
            }
        } 