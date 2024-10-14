# Algo-sphere

## Overview
**Algo-sphere** is an interactive platform aimed at helping users learn data structures and algorithms through visualization, step-by-step explanations, and AI-powered debugging. The project is inspired by the need for a comprehensive solution to enhance the learning experience in computer science, particularly for students struggling with understanding complex algorithms.

The platform offers:
- **Algorithm Visualization**: Real-time visual representation of algorithms such as sorting, searching, and dynamic programming.
- **Step-by-Step Solutions**: Detailed walkthroughs of the execution process of algorithms, allowing users to grasp the underlying concepts effectively.
- **AI Debugger**: An AI-powered tool that helps users solve code issues by providing detailed explanations and suggesting improvements.

## Features
- **Algorithm Explorer**: Browse through a variety of popular algorithms, including sorting (e.g., QuickSort, MergeSort), searching (e.g., Binary Search, BFS, DFS), and advanced algorithms (e.g., Dijkstra’s, Floyd-Warshall).
- **Interactive Visualization**: Watch algorithms in action as the platform breaks down the problem-solving process step by step.
- **Code Debugging**: Upload code snippets or write your own in the platform’s editor and let the AI debugger identify issues and provide suggestions for optimization.
- **Learning Paths**: Pre-defined paths for learning algorithms, from basic to advanced levels, along with practice problems.
- **Gamified Experience**: Unlock achievements and compete with others on leaderboards based on your learning progress.

## How It Works
1. **Choose an Algorithm**: Select an algorithm from the library, either to visualize or test your understanding.
2. **View Visualization**: The platform displays a step-by-step visual representation of the algorithm’s operation on input data.
3. **Solve Problems**: Users can solve predefined problems, submit their own solutions, and receive feedback from the AI debugger.
4. **AI Debugging**: If stuck, users can activate the AI debugger, which will highlight code issues and suggest fixes.

## Installation

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/algo-sphere.git
   ```
2. Navigate to the project directory:
```bash

cd algo-sphere
```
3. Install dependencies:
```bash
pip install requirements.txt
```
4. Run the development server:
```bash
python app.py
```


## Usage
1. Open your browser and navigate to `http://localhost:3000`.
2. Explore the algorithms by selecting from the menu.
3. Use the editor to write code and get feedback from the AI debugger.
4. Visualize the algorithms with sample inputs or provide your own.

## Technologies Used
- **Frontend**: React.js, HTML5, CSS3
- **Backend**: Node.js, Express
- **AI Model**: OpenAI's GPT for debugging and problem-solving suggestions
- **Visualization**: Manim, D3.js for creating interactive algorithm animations
- **Database**: MongoDB for user data and problem storage
- **Deployment**: Docker and AWS (planned for future implementation)

## Contributing
We welcome contributions to improve the platform! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Future Enhancements
- Expanding the AI debugger to support more languages (currently supports Python and JavaScript).
- Adding more algorithms and visualizations.
- Integration with cloud services for scalability (AWS, Azure).
- Introducing a mobile app for learning on-the-go.
