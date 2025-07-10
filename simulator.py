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
        self.world_initialized = False
        
    async def initialize_llm(self):
        """Initialize LLM clients"""
        self.llm_manager = LLMManager(
            CONFIG["ollama_model"],
            CONFIG["deepseek_api_key"]
        )
        await self.llm_manager.initialize()
    
    async def initialize_world_with_random_names(self):
        """Initialize world with LLM-generated names or fallback to config"""
        if not self.world_initialized:
            print("🎲 Attempting to generate random names...")
            
            # Try to generate random location names
            generated_locations = None
            if self.llm_manager and self.llm_manager.ollama_available:
                generated_locations = await self.llm_manager.generate_random_names("locations", CONFIG["world_generation"]["location_count"])
            
            # Try to generate random NPC names
            generated_npcs = None
            if self.llm_manager and self.llm_manager.ollama_available:
                generated_npcs = await self.llm_manager.generate_random_names("npcs", CONFIG["world_generation"]["npc_count"])
            
            # Initialize world with generated or fallback data
            await self._init_world_with_data(generated_locations, generated_npcs)
            self.world_initialized = True

    async def _init_world_with_data(self, generated_locations=None, generated_npcs=None):
        """Initialize game world with generated or fallback data"""
        
        # Create locations (generated or fallback)
        if generated_locations and "locations" in generated_locations:
            print("🎲 Using LLM-generated location names")
            for loc_data in generated_locations["locations"]:
                name = loc_data["name"]
                loc_type = loc_data["type"]
                desc = loc_data["description"]
                self.locations[name] = Location(name, loc_type, desc)
        else:
            print("🔄 Using fallback location names from config")
            for name, loc_type, desc in CONFIG["locations"]:
                self.locations[name] = Location(name, loc_type, desc)

        # Get location names for NPC placement
        location_names = list(self.locations.keys())
        if not location_names:
            print("❌ No locations available!")
            return

        # Create NPCs (generated or fallback)
        if generated_npcs and "npcs" in generated_npcs:
            print("🎲 Using LLM-generated NPC names")
            for npc_data in generated_npcs["npcs"]:
                npc_id = npc_data["id"]
                name = npc_data["name"]
                role = npc_data["role"]
                # Map location to existing locations
                target_location = self._map_location_name(npc_data["location"], location_names)
                
                npc = NPC(npc_id, name, role, target_location)
                self.npcs[npc_id] = npc
                self.locations[target_location].add_npc(npc_id)
        else:
            print("🔄 Using fallback NPC names from config")
            for npc_id, name, role, location in CONFIG["npc_data"]:
                # Map location to existing locations
                target_location = self._map_location_name(location, location_names)
                
                npc = NPC(npc_id, name, role, target_location)
                self.npcs[npc_id] = npc
                self.locations[target_location].add_npc(npc_id)

        # Initialize relationships between NPCs
        self._init_relationships()
        
        print(f"✅ Created {len(self.npcs)} NPCs in {len(self.locations)} locations")
    
    def _map_location_name(self, original_location: str, available_locations: List[str]) -> str:
        """Map location name to existing location"""
        # Try exact match first
        if original_location in available_locations:
            return original_location
        
        # Try to find similar location type
        location_mapping = {
            "Castle": ["Castle", "Fortress", "Keep", "Citadel"],
            "Village": ["Village", "Town", "Settlement", "Hamlet"],
            "Forest": ["Forest", "Woods", "Wilderness", "Grove"]
        }
        
        for available_loc in available_locations:
            for key, variants in location_mapping.items():
                if original_location in variants and any(v in available_loc for v in variants):
                    return available_loc
        
        # Fallback to first available location
        return available_locations[0]
    
    def _init_world(self):
        """Initialize game world (legacy method, kept for compatibility)"""
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
        # Initialize world with random names if not done yet
        if not self.world_initialized:
            await self.initialize_world_with_random_names()
        
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
            energy_loss = random.randint(10, 25)
            hunger_gain = random.randint(15, 30)
            npc.update_stat("energy", -energy_loss)
            npc.update_stat("hunger", hunger_gain)
            
            # Age effect on health
            if npc.age > 65:
                health_loss = random.randint(1, 3)
                print(f"  👴 Aging: {npc.name} loses health due to age")
                npc.update_stat("health", -health_loss)
                
            # Death from disease/old age
            if npc.stats["health"] <= 0:
                npc.alive = False
                npc.add_action(f"💀 {npc.name} died")
                dead_npcs.append(npc.name)
                print(f"💀 DEATH: {npc.name} died at age {npc.age:.1f}")
                
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
                print(f"  🍞 Basic: {npc.name} eats (hunger: {npc.stats['hunger']})")
                npc.update_stat("hunger", -40)
                npc.update_stat("energy", 15)
                npc.update_stat("mood", 10)
                npc.add_action(f"🍞 {npc.name} ate")

            # Sleep/rest - if low energy
            elif npc.stats["energy"] < 30:
                print(f"  😴 Basic: {npc.name} rests (energy: {npc.stats['energy']})")
                npc.update_stat("energy", 50)
                npc.update_stat("mood", 15)
                npc.add_action(f"😴 {npc.name} rested")

            # Work based on role - if energy is high
            elif npc.stats["energy"] > 60 and random.random() < 0.6:
                action = CONFIG["role_actions"].get(npc.role, "worked")
                print(f"  🔨 Basic: {npc.name} works ({npc.role})")
                npc.add_action(f"{npc.name} {action}")
                npc.update_stat("energy", -15)
                npc.update_stat("mood", 5)

    async def _llm_decisions(self):
        """LLM-powered decisions for social interactions"""
        if not self.llm_manager:
            return

        llm_active_npcs = []
        
        for npc in self.npcs.values():
            if not npc.alive or random.random() > CONFIG["llm_decision_chance"]:
                continue

            # Get other NPCs in the same location
            location_npcs = self.locations[npc.location].get_alive_npcs(self.npcs)
            location_npcs = [npc_id for npc_id in location_npcs if npc_id != npc.id]

            if not location_npcs:
                continue

            llm_active_npcs.append(npc.name)

            # Formulate context for LLM
            context = {
                "nearby_npcs": location_npcs[:3],  # Top 3 closest
                "location": npc.location
            }

            # Get decision from LLM
            decision = await self.llm_manager.get_npc_decision(npc.to_dict(), context)
            
            if decision:
                await self._apply_llm_decision(npc, decision, location_npcs)
        
        if llm_active_npcs:
            print(f"🧠 [LLM SESSION] Processed {len(llm_active_npcs)} NPCs: {', '.join(llm_active_npcs)}")
        else:
            print(f"🎲 [NO LLM] All decisions made through basic logic")

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
            print(f"  💬 Social: {npc.name} talks to {target_npc.name}")
            npc.update_relationship(target_id, 10)
            target_npc.update_relationship(npc.id, 5)
            npc.update_stat("mood", 10)
            npc.add_action(f"💬 {npc.name} talked to {target_npc.name} ({reason})")
            
        elif action == "help":
            # Helping
            print(f"  🤝 Social: {npc.name} helps {target_npc.name}")
            npc.update_relationship(target_id, 15)
            target_npc.update_relationship(npc.id, 20)
            target_npc.update_stat("mood", 15)
            npc.update_stat("energy", -10)
            npc.add_action(f"🤝 {npc.name} helped {target_npc.name} ({reason})")
            
        elif action == "argue":
            # Conflict
            print(f"  😠 Social: {npc.name} argues with {target_npc.name}")
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
            print(f"  🎉 Event effect: {npc.name} enjoys {event}")
            npc.update_stat("mood", 20)
        elif "attack" in event:
            print(f"  ⚔️ Event effect: {npc.name} suffers from {event}")
            npc.update_stat("health", -15)
            npc.update_stat("mood", -20)
        elif "treasure" in event:
            print(f"  💰 Event effect: {npc.name} benefits from {event}")
            npc.update_stat("mood", 30)
        elif "harvest" in event:
            print(f"  🌾 Event effect: {npc.name} enjoys {event}")
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
        print(f"\n📜 Generating final chronicle...")
        print(f"🤖 [LLM] Starting final chronicle generation...")
        
        # Collect data for chronicle
        events_data = {
            "current_day": self.current_day,
            "alive_count": len([npc for npc in self.npcs.values() if npc.alive]),
            "total_count": len(self.npcs),
            "key_events": [],
            "deaths": [],
            "relationships_summary": []
        }

        # Collect key events from all days
        for day_log in self.daily_logs:
            for npc_id, actions in day_log.get("actions", {}).items():
                for action in actions:
                    if any(keyword in action.lower() for keyword in ["died", "talked", "helped", "argued"]):
                        events_data["key_events"].append(f"Day {day_log['day']}: {action}")

        # Collect deaths
        for npc in self.npcs.values():
            if not npc.alive:
                events_data["deaths"].append(f"{npc.name} (age {npc.age:.1f})")

        # Collect interesting relationships
        for npc in self.npcs.values():
            if npc.alive:
                for other_id, relation in npc.relationships.items():
                    if relation > 50 or relation < -30:
                        other_npc = self.npcs.get(other_id)
                        if other_npc:
                            status = "friends" if relation > 50 else "enemies"
                            events_data["relationships_summary"].append(
                                f"{npc.name} and {other_npc.name} are {status} ({relation})"
                            )

        print(f"📊 [DATA] Collected: {len(events_data['key_events'])} events, {len(events_data['deaths'])} deaths, {len(events_data['relationships_summary'])} relationships")

        # Generate chronicle
        if self.llm_manager:
            chronicle = await self.llm_manager.generate_chronicle(events_data)
        else:
            print(f"⚠️ [LLM] LLM Manager unavailable, creating basic chronicle...")
            chronicle = self._create_simple_chronicle(events_data)

        # Save chronicle
        try:
            with open("chronicles.md", "w", encoding="utf-8") as f:
                f.write(chronicle)
            print(f"💾 [SAVE] Chronicle saved to chronicles.md")
        except Exception as e:
            print(f"❌ [SAVE] Error saving chronicle: {e}")

    def _create_simple_chronicle(self, events_data: Dict) -> str:
        """Create simple chronicle without LLM"""
        print(f"📝 [LOCAL] Creating local chronicle...")
        
        current_day = events_data.get('current_day', 0)
        alive_count = events_data.get('alive_count', 0)
        total_count = events_data.get('total_count', 0)
        key_events = events_data.get('key_events', [])
        
        chronicle = f"""# 📜 Simulation Chronicle

## Simulation days: {current_day}
## Surviving NPCs: {alive_count}/{total_count}

### Key events of recent days:
"""
        
        for i, event in enumerate(key_events[-15:], 1):
            chronicle += f"{i}. {event}\n"
        
        chronicle += "\n*Chronicle generated locally (LLM unavailable)*"
        return chronicle

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