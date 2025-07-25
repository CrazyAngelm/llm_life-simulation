# 📁 main.py - Program entry point
# 🎯 Core function: Launch simulation and manage process
# 🔗 Key dependencies: simulator, asyncio
# 💡 Usage: python main.py - starts the simulation

import asyncio
import sys
from dotenv import load_dotenv
from simulator import WorldSimulator

load_dotenv()


async def main():
    """Main simulation launch function"""
    print("🌍 LLM Life Simulator MVP")
    print("=" * 50)
    print("Life simulator with AI agents and LLM integration")
    
    try:
        # Create simulator
        simulator = WorldSimulator()
        
        # Initialize LLM
        await simulator.initialize_llm()
        
        # Initialize world with random names
        await simulator.initialize_world_with_random_names()
        
        # Show initial status
        status = simulator.get_world_status()
        print(f"🎯 Initial status:")
        print(f"   📅 Day: {status['day']}")
        print(f"   👥 NPCs: {status['alive_npcs']}/{status['total_npcs']}")
        print(f"   🏰 Locations: {', '.join(status['locations'].keys())}")
        print()
        
        # Run simulation
        await simulator.run_simulation()
        
        # Show final status
        final_status = simulator.get_world_status()
        print(f"\n🏁 Final status:")
        print(f"   📅 Days passed: {final_status['day']}")
        print(f"   👥 Survivors: {final_status['alive_npcs']}/{final_status['total_npcs']}")
        for loc, count in final_status['locations'].items():
            print(f"   📍 {loc}: {count} NPCs")
        
        print(f"\n📂 Results:")
        print(f"   📝 world_state.json - Complete world state")
        print(f"   📜 chronicles.md - Generated chronicles")
        
    except KeyboardInterrupt:
        print("\n⏹️ Simulation stopped by user")
    except Exception as e:
        print(f"\n❌ Simulation error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 Starting LLM Life Simulator...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Run async simulation
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Critical error: {e}")
        sys.exit(1) 