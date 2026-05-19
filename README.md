# Josephus Problem — Prediction Game

An interactive desktop application that simulates the classic **Josephus Problem**. Players stand in a circle, every *k-th* person is eliminated, and the process continues until only one survivor remains. Before starting the simulation, you can predict who the final survivor will be and test your logic against the algorithm.

---

## About the Josephus Problem

The Josephus Problem is a famous mathematical and computer science puzzle.

Given:

* **n** people standing in a circle
* A counting step **k**

Starting from person **1**, every **k-th** living person is eliminated. Counting then resumes from the next remaining person until only one person survives.

This project transforms the problem into a visual and interactive prediction game with real-time simulation.

---

## Features

### Circle Visualization

* People are arranged visually in a circle
* Current counting position is highlighted
* Eliminated players are marked differently
* Final survivor is emphasized

### Elimination Order Table

* Displays the exact elimination sequence
* Helps track the algorithm step-by-step

### Full Simulation Mode

* Automatically runs the entire elimination process
* Includes short delays for animation effect

### Step-by-Step Mode

* Eliminate one person at a time manually
* Useful for learning and debugging

### Prediction Game

* Predict the final survivor before simulation
* See whether your prediction was correct

### Clean Code Structure

* Logic separated from GUI for better maintainability
* Algorithm handled independently from visualization

---

## Requirements

* Python 3.7 or higher
* tkinter (usually included with Python)

### Linux Users

On some Linux distributions, install tkinter manually:

```bash
sudo apt install python3-tk
```

---


## Usage

Run the application:

```bash
python josephus_gui.py
```

---

## Controls

| Input                | Description                      |
| -------------------- | -------------------------------- |
| Number of people (n) | Range: 1–100                     |
| Elimination step (k) | Range: 2–10                      |
| Predict person       | Optional survivor prediction     |
| START SIMULATION     | Automatically run the simulation |
| STEP BY STEP         | Advance one elimination manually |

---

## How to Play

1. Enter the number of people (**n**).
2. Enter the elimination step (**k**).
3. Optionally predict the survivor.
4. Click **START SIMULATION** for automatic mode
   or use **STEP BY STEP** mode.
5. Watch eliminations occur around the circle.
6. At the end, compare your prediction with the actual survivor.

---

## Project Structure

```text
josephus/
├── josephus_logic.py   # Core Josephus algorithm and game state
├── josephus_gui.py     # Tkinter graphical interface
└── README.md
```

---

## Algorithm Explanation

The elimination process works as follows:

1. Start from the current position.
2. Count **k** living people.
3. Eliminate the **k-th** person.
4. Continue counting from the next living person.
5. Repeat until only one person remains.

---

## Educational Value

This project demonstrates important computer science concepts including:

* Circular data structures
* Simulation algorithms
* Recursion and recurrence relations
* Visualization techniques
* GUI programming with tkinter
* Event-driven programming

---

