import os
import json
import argparse
from core.controller import EXPAIAgent
from core import granules

def main():
    parser = argparse.ArgumentParser(description="Minimal EXPAI Trainer")
    parser.add_argument('--cycles', type=int, default=10, help='Total number of training cycles')
    parser.add_argument('--cycles_per_goal', type=int, default=1, help='Number of times to repeat each goal per cycle')
    args = parser.parse_args()

    # Load simple goals
    goals_path = os.path.join(os.path.dirname(__file__), 'goals', 'simple_goals.json')
    with open(goals_path, 'r') as f:
        goals = json.load(f)
    print(f"Loaded {len(goals)} goals.")

    # Initialize granules if needed
    granules.load_granules()
    granules.initialize_basic_granules()

    # Initialize agent
    agent = EXPAIAgent(sandbox_path=os.path.join(os.path.dirname(__file__), 'sandbox'))

    total_cycles = 0
    for cycle in range(args.cycles):
        print(f"\n=== Training Cycle {cycle+1}/{args.cycles} ===")
        for idx, goal in enumerate(goals):
            for repeat in range(args.cycles_per_goal):
                print(f"\n--- Goal {idx+1}/{len(goals)} (repeat {repeat+1}/{args.cycles_per_goal}) ---")
                agent.load_goal(goal)
                agent.run_cycle()
                total_cycles += 1

    # Save granules
    granules.save_granules()
    print(f"Training complete. Total cycles: {total_cycles}. Granules saved.")

if __name__ == "__main__":
    main() 