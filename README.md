## Flappy Bird AI Project

![AI playing Flappy Bird in 9:16 aspect ratio](docs/images/ai_demo.gif)

This project implements the classic Flappy Bird game and integrates a reinforcement learning algorithm (which reads a saved `.pkl` model) to train and run an AI agent to play the game autonomously.

---

## Getting Started

These instructions will guide you through setting up and running the project on your local machine.

### Prerequisites

Before running the code, you need to install the required Python packages.

1.  **Install Dependencies:** Navigate to the project's root directory in your terminal and run the following command:

    ```bash
    pip install -r requirements.txt
    ```

---

## How to Run

### Running the Algorithm (AI Mode)

If you wish to see the **trained algorithm** (which reads the `.pkl` model) play the game, use the following command:

```bash
python replay.py
```

### Playing Manually (User Mode)

If you want to play the game yourself, you need to run the main application file:

```bash
python main.py
```
Controls: Use the **W** key or the **Up** Arrow key on your keyboard to make the bird jump.


