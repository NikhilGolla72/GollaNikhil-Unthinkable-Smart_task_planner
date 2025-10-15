# Smart Task Planner

An AI-powered Smart Task Planner that transforms high-level goals into structured, time-bound, and dependency-aware task plans. This project leverages LLM-powered reasoning to break down goals, determine dependencies, generate multiple planning strategies, and present plans in a visually appealing Gantt timeline interface.

## Features

- **AI-Powered Task Breakdown**: Uses Gemini API to intelligently decompose complex goals into actionable tasks
- **Team Collaboration**: Automatically assigns tasks to team members in a rotating pattern
- **Multiple Planning Strategies**: Generates balanced, aggressive, and safe planning approaches
- **Visual Timeline**: Interactive Gantt charts with critical path analysis
- **Individual Subtasks**: Creates specific, focused tasks for each team member instead of large umbrella tasks
- **Modern UI**: Built with React, Tailwind CSS, and Framer Motion for smooth animations

## Tech Stack

### Backend
- **FastAPI**: Python web framework for building APIs
- **Gemini API**: Google's generative AI for intelligent task planning
- **Pydantic**: Data validation and settings management

### Frontend
- **React**: JavaScript library for building user interfaces
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Animation library for React
- **React Router**: Client-side routing


Screenshots:


<img width="1919" height="979" alt="image" src="https://github.com/user-attachments/assets/21cf490e-9200-4863-aadb-d8311597ef56" />
<img width="1917" height="962" alt="image" src="https://github.com/user-attachments/assets/ad08f1bc-832b-4d90-93d6-89892dd11681" />
<img width="1890" height="958" alt="image" src="https://github.com/user-attachments/assets/c8c430f0-c2ab-432d-b216-0f4606e82342" />

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Gemini API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd smart-task-planner/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
```bash
# Create .env file with your Gemini API key
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
BACKEND_PORT=8001
```

6. Start the backend server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd smart-task-planner/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Usage

1. **Enter Your Goal**: Describe what you want to accomplish
2. **Set Team Size**: Specify how many people will work on the project
3. **Choose Planning Mode**: Select between balanced, aggressive, or safe approaches
4. **Generate Plan**: Let AI create a comprehensive task breakdown
5. **View Results**: Explore the generated plan with Gantt charts and task details

## Project Structure

```
smart-task-planner/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── routes/
│   │   └── planner.py          # API endpoints for plan generation
│   ├── models/
│   │   └── schemas.py          # Pydantic models for request/response
│   ├── services/
│   │   ├── llm_client.py       # Gemini API integration
│   │   └── planner_logic.py    # Task processing and scheduling logic
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.js         # Main input form
│   │   │   └── PlannerView.js  # Plan visualization
│   │   ├── components/
│   │   │   ├── TaskCard.js     # Individual task display
│   │   │   ├── GanttChart.js   # Timeline visualization
│   │   │   └── ModeSelector.js # Planning mode selector
│   │   └── App.js             # Main application component
│   ├── package.json           # Node.js dependencies
│   └── tailwind.config.js     # Tailwind CSS configuration
└── README.md                  # This file
```

## Key Features Explained

### Individual Subtask Assignment
Unlike traditional project management tools that create large umbrella tasks, this system:
- Breaks down projects into 6-12 individual, specific subtasks
- Assigns each subtask to team members in a rotating pattern
- Ensures each team member gets multiple focused tasks rather than one large combined task

### AI-Powered Planning
The system uses Gemini API to:
- Analyze goals and create relevant, specific tasks
- Determine appropriate dependencies between tasks
- Generate multiple planning strategies (balanced, aggressive, safe)
- Create detailed descriptions for each task

### Visual Timeline
Interactive Gantt charts show:
- Task durations and dependencies
- Critical path analysis
- Team member assignments
- Parallel task execution

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please open an issue in the GitHub repository.
