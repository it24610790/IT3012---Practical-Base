# agent.py
class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SimpleReflexAgent:
    def __init__(self):
        # No Memory
        pass

    def sense_and_act(self, percept: dict) -> str:
        """Simple Reflex Agent using strictly Condition-Action (IF-THEN) rules."""
        wall_ahead = percept.get('wall_ahead', False)
        food_here = percept.get('food_here', False)

        # Condition-Action Rules (IF-THEN Logic)
        if food_here:
            return 'suck'  # Food is available, then suck it up
        elif wall_ahead:
            return 'Left'  # test_suite is checking 'Left', 'Right', 'Up', 'Down'
        else:
            return 'Up'  # Forward going return 'Up'

class ModelBasedAgent:
    def __init__(self):
        # Internal State / keep the Memory
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
        wall_ahead = percept.get('wall_ahead', False)
        food_here = percept.get('food_here', False)

        # Rule 1: Food is present -> Suck it up
        if food_here:
            action = 'suck'
        
        # Rule 2: Wall is ahead, use Memory (last_action) to determine next action
        elif wall_ahead:
            if self.last_action == 'Left':
                action = 'Down'
            elif self.last_action == 'Down':
                action = 'Right'
            elif self.last_action == 'Right':
                action = 'Up'
            else:
                action = 'Left'
        
        # Rule 3: there is no wall ahead and no food, just move forward (Up)
        else:
            action = 'Up'

        # Store Action in Memory
        self.last_action = action
        return action

class SearchAgent:
    def __init__(self):
        pass

    def bfs_search(self, start, goal, walls, grid_size):
        return []