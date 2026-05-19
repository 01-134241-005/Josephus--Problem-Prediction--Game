class JosephusGameLogic:
    """
    Core game logic for The Josephus Problem.
    Handles all data structures, elimination algorithm, and prediction.
    No dependency on tkinter.
    """

    def __init__(self):
        """Initialize all game state variables."""
        # ==================== GAME VARIABLES ====================
        self.n = 0               # Number of people
        self.k = 0               # Elimination step
        self.people = []         # List of dicts with keys: id, eliminated
        self.current_index = 0   # Index of currently active person
        self.elimination_order = []  # List to track elimination sequence
        self.user_prediction = None  # User's predicted survivor number
        self.game_won = False     # Flag if user's prediction was correct

    # ==================== GAME SETUP & RESET ====================

    def setup_game(self, n, k):
        """
        Initialize a new game with given n and k.
        
        Parameters:
            n: Number of people (1-100)
            k: Elimination step (>=2)
            
        Returns:
            bool: True if setup successful, False otherwise
        """
        # Validation
        if n < 1 or n > 100:
            return False
        if k < 2:
            return False
            
        self.n = n
        self.k = k
        self.current_index = 0
        self.elimination_order = []
        self.game_won = False
        
        # Keep prediction only if valid for new n
        if self.user_prediction and self.user_prediction > self.n:
            self.user_prediction = None
        
        # Initialize people list 
        self.people = []
        for i in range(self.n):
            self.people.append({
                'id': i + 1,
                'eliminated': False
            })
        
        return True

    def reset_game(self):
        """Reset the game state keeping current n, k if they are valid."""
        if self.n > 0 and self.k >= 2:
            self.setup_game(self.n, self.k)
        else:
            self.n = 0
            self.k = 0
            self.people = []
            self.current_index = 0
            self.elimination_order = []
            self.user_prediction = None
            self.game_won = False

    # ==================== PREDICTION FEATURE ====================

    def set_prediction(self, pred):
        """
        Set user's prediction for the survivor.
        
        Parameters:
            pred: integer prediction (1-100)
            
        Returns:
            bool: True if prediction is valid and set, False otherwise
        """
        if pred < 1 or pred > 100:
            return False
        if self.n > 0 and pred > self.n:
            return False
        
        self.user_prediction = pred
        return True

    def get_prediction_status(self):
        """Return current prediction (or None if not set)."""
        return self.user_prediction

    def check_prediction(self, survivor):
        """
        Check if user's prediction matches the survivor.
        Updates game_won flag and returns boolean result.
        
        Parameters:
            survivor: The actual survivor number
            
        Returns:
            bool: True if prediction correct, False otherwise
            None if no prediction was made
        """
        if self.user_prediction is None:
            return None
        self.game_won = (self.user_prediction == survivor)
        return self.game_won

    # ==================== ELIMINATION LOGIC ====================

    def find_survivor(self):
        """
        Find the survivor after elimination process.
        
        Returns:
            int: Survivor's person number, or None if no survivor
        """
        if not self.people:
            return None
        for person in self.people:
            if not person['eliminated']:
                return person['id']
        return None

    def is_game_finished(self):
        """
        Check if only one person remains alive.
        
        Returns:
            bool: True if game finished, False otherwise
        """
        if not self.people:
            return True
        alive_count = sum(1 for p in self.people if not p['eliminated'])
        return alive_count <= 1

    def eliminate_one(self):
        """
        Eliminate one person based on current k value.
        Counting logic: Count k living people, eliminate the k-th.
        
        Returns:
            int or None: ID of eliminated person, or None if cannot eliminate
        """
        if not self.people or self.is_game_finished():
            return None
        
        # Find active people indices
        active_indices = [i for i, p in enumerate(self.people) if not p['eliminated']]
        if len(active_indices) <= 1:
            return None
        
        # Count k living people starting from current_index
        count = 0
        idx = self.current_index
        while count < self.k:
            if not self.people[idx]['eliminated']:
                count += 1
                if count == self.k:
                    eliminate_idx = idx
            if count < self.k:
                idx = (idx + 1) % len(self.people)
        
        # Perform elimination
        if not self.people[eliminate_idx]['eliminated']:
            person_id = self.people[eliminate_idx]['id']
            self.elimination_order.append(person_id)
            self.people[eliminate_idx]['eliminated'] = True
            
            # Move to next person after eliminated
            self.current_index = (eliminate_idx + 1) % len(self.people)
            while self.people[self.current_index]['eliminated']:
                self.current_index = (self.current_index + 1) % len(self.people)
            
            return person_id
        
        return None

    # ==================== STATE ACCESSORS ====================

    def get_people_state(self):
        """
        Return list of people with their elimination status.
        Used by GUI for drawing.
        """
        return self.people.copy() if self.people else []

    def get_elimination_order(self):
        """Return the elimination order list."""
        return self.elimination_order.copy()

    def get_current_index(self):
        """Return current index (0-based) of active person."""
        return self.current_index

    def get_n(self):
        return self.n

    def get_k(self):
        return self.k