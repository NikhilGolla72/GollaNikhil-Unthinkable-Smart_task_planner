import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

    def generate_plan(self, payload: dict) -> dict:
        goal = payload.get('goal', '')
        team_size = payload.get('team_size', 1)
        mode = payload.get('mode', 'balanced')
        
        print(f"Using Gemini API for goal: {goal}")
        
        try:
            # Create the prompt for Gemini
            prompt = self._create_gemini_prompt(goal, team_size, mode)
            
            # Call Gemini API
            response = self._call_gemini_api(prompt)
            
            # Parse the response
            parsed_response = self._parse_gemini_response(response, payload)
            
            print(f"Successfully generated plan with Gemini API")
            return parsed_response
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            raise Exception(f"Gemini API error: {e}")

    def _create_gemini_prompt(self, goal: str, team_size: int, mode: str) -> str:
        return f"""
You are an expert project manager and task planner. Generate a detailed project plan for the following goal:

GOAL: {goal}
TEAM SIZE: {team_size} people
PLANNING MODE: {mode}

You are a project manager creating a task plan. Here's what you MUST do:

GOAL: {goal}
TEAM SIZE: {team_size} people

CRITICAL INSTRUCTIONS:
1. Break down the project into 6-12 INDIVIDUAL, SPECIFIC subtasks
2. Each subtask should be a single, actionable item (not a combination of multiple activities)
3. Assign each subtask to a specific team member in a rotating pattern
4. Each team member gets multiple individual subtasks, not one big combined task

EXAMPLE FOR 2-PERSON TEAM (6 subtasks total):
- Subtask 1: "Team Member 1: Design Homepage Layout"
- Subtask 2: "Team Member 2: Set Up Database Schema" 
- Subtask 3: "Team Member 1: Create User Authentication"
- Subtask 4: "Team Member 2: Build API Endpoints"
- Subtask 5: "Team Member 1: Implement Frontend Components"
- Subtask 6: "Team Member 2: Deploy to Production"

EXAMPLE FOR 3-PERSON TEAM (9 subtasks total):
- Subtask 1: "Team Member 1: Create Wireframes"
- Subtask 2: "Team Member 2: Set Up Database"
- Subtask 3: "Team Member 3: Configure Server"
- Subtask 4: "Team Member 1: Design UI Components"
- Subtask 5: "Team Member 2: Build User API"
- Subtask 6: "Team Member 3: Implement Authentication"
- Subtask 7: "Team Member 1: Create Frontend Pages"
- Subtask 8: "Team Member 2: Add Data Validation"
- Subtask 9: "Team Member 3: Deploy Application"

REQUIRED FORMAT:
Each task must have:
- title: "Team Member X: [SINGLE SPECIFIC ACTION]"
- description: "Detailed explanation of this ONE specific task"
- est_hours: [realistic hours for this single task]
- dependencies: [which tasks must be completed first]
- risk_score: [1-5 rating]

DO NOT CREATE:
- Combined tasks like "UI/UX Design & Content Curation"
- Umbrella tasks that include multiple activities
- Tasks that span multiple responsibilities

CREATE:
- Individual, atomic subtasks
- Rotating assignment pattern (1,2,3,1,2,3...)
- Each subtask is a single, clear action

3. Generate THREE variants:
   - BALANCED: Standard timeline with moderate risk
   - AGGRESSIVE: Faster timeline with higher risk
   - SAFE: Slower timeline with lower risk

4. Include reasoning for each variant explaining the approach

Return your response as a valid JSON object with this exact structure:

{{
  "assumptions": "Brief assumptions about the project",
  "summary": "Brief summary of the plan",
  "variants": {{
    "balanced": {{
      "tasks": [
        {{
          "id": "t1",
          "title": "Task Title",
          "description": "Detailed task description",
          "est_hours": 8.0,
          "dependencies": [],
          "risk_score": 3
        }}
      ],
      "critical_path": ["t1", "t2"],
      "reasoning": "Explanation of balanced approach"
    }},
    "aggressive": {{
      "tasks": [...],
      "critical_path": [...],
      "reasoning": "Explanation of aggressive approach"
    }},
    "safe": {{
      "tasks": [...],
      "critical_path": [...],
      "reasoning": "Explanation of safe approach"
    }}
  }}
}}

Make sure the tasks are specific to the goal "{goal}" and not generic. Focus on what actually needs to be done for this particular project.
"""

    def _call_gemini_api(self, prompt: str) -> str:
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }
        
        url = f"{self.gemini_api_url}?key={self.gemini_api_key}"
        
        print(f"Calling Gemini API...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.status_code} - {response.text}")
        
        result = response.json()
        
        if 'candidates' not in result or not result['candidates']:
            raise Exception(f"Invalid Gemini response: {result}")
        
        return result['candidates'][0]['content']['parts'][0]['text']

    def _parse_gemini_response(self, response_text: str, payload: dict) -> dict:
        """Parse the Gemini response and return structured data"""
        
        # Clean up the response
        response_text = response_text.strip()
        
        # Try to find JSON in the response
        json_match = self._extract_json_from_response(response_text)
        
        if json_match:
            try:
                parsed_data = json.loads(json_match)
                print(f"Successfully parsed Gemini JSON response")
                return parsed_data
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Response text: {response_text[:200]}...")
        
        # If JSON parsing fails, create a structured response from the text
        return self._create_structured_response_from_text(response_text, payload)

    def _extract_json_from_response(self, text: str) -> str:
        """Extract JSON from the response text"""
        import re
        
        # Look for JSON block markers
        json_patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
            r'(\{[\s\S]*?\})',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                json_text = matches[0].strip()
                # Try to clean up common JSON issues
                json_text = self._clean_json_text(json_text)
                return json_text
        
        return None
    
    def _clean_json_text(self, json_text: str) -> str:
        """Clean up common JSON formatting issues"""
        # Remove trailing commas before closing braces/brackets
        json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
        
        # Fix unescaped quotes in strings (basic cleanup)
        # This is a simple approach - for production, you'd want more robust handling
        
        return json_text

    def _create_structured_response_from_text(self, text: str, payload: dict) -> dict:
        """Create a structured response when JSON parsing fails"""
        
        goal = payload.get('goal', '')
        team_size = payload.get('team_size', 1)
        mode = payload.get('mode', 'balanced')
        
        # Extract key information from the text
        assumptions = f"AI-generated plan for {goal} using Gemini API"
        summary = f"Gemini-generated plan for: {goal}"
        
        # Create basic tasks based on the text content
        tasks = self._extract_tasks_from_text(text, goal, team_size)
        
        return {
            "assumptions": assumptions,
            "summary": summary,
            "variants": {
                "balanced": {
                    "tasks": tasks,
                    "critical_path": [task["id"] for task in tasks],
                    "reasoning": f"Gemini-generated balanced approach for {goal}: {text[:100]}..."
                },
                "aggressive": {
                    "tasks": self._create_aggressive_variant(tasks),
                    "critical_path": [task["id"] for task in self._create_aggressive_variant(tasks)],
                    "reasoning": f"Gemini-generated aggressive timeline for {goal}: {text[:100]}..."
                },
                "safe": {
                    "tasks": self._create_safe_variant(tasks),
                    "critical_path": [task["id"] for task in self._create_safe_variant(tasks)],
                    "reasoning": f"Gemini-generated safe approach for {goal}: {text[:100]}..."
                }
            }
        }

    def _extract_tasks_from_text(self, text: str, goal: str, team_size: int) -> list:
        """Extract task information from Gemini's text response"""
        
        # Simple task extraction based on common patterns
        import re
        
        # Look for numbered lists or bullet points
        task_patterns = [
            r'\d+\.\s*([^.\n]+)',
            r'•\s*([^.\n]+)',
            r'-\s*([^.\n]+)',
        ]
        
        tasks = []
        task_id = 1
        
        for pattern in task_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:5]:  # Limit to 5 tasks
                if len(match.strip()) > 10:  # Only substantial tasks
                    title = self._extract_title_from_text(match.strip())
                    description = self._create_detailed_description(match.strip(), goal, task_id)
                    
                    # Scale hours based on team size
                    base_hours = max(4, 8 - (task_id * 1.5))
                    scaled_hours = base_hours / max(1, team_size) if team_size > 1 else base_hours
                    
                    task = {
                        "id": f"t{task_id}",
                        "title": title,
                        "description": description,
                        "est_hours": max(2, scaled_hours),  # Minimum 2 hours
                        "dependencies": [] if task_id == 1 else [f"t{task_id-1}"],
                        "risk_score": 2 + (task_id % 3)
                    }
                    tasks.append(task)
                    task_id += 1
                    
                    if len(tasks) >= 5:
                        break
        
        # If no tasks found, create basic ones with better descriptions
        if not tasks:
            tasks = self._create_fallback_tasks(goal, team_size)
        
        return tasks
    
    def _extract_title_from_text(self, text: str) -> str:
        """Extract a concise title from text"""
        words = text.split()
        # Take first 2-4 words that are meaningful
        key_words = [w for w in words[:4] if len(w) > 2 and w.lower() not in ['the', 'and', 'for', 'with', 'this', 'that', 'will', 'should']]
        
        if len(key_words) >= 2:
            return " ".join(key_words[:3]).title()
        else:
            return text[:30] + "..." if len(text) > 30 else text
    
    def _create_detailed_description(self, text: str, goal: str, task_id: int) -> str:
        """Create a detailed description that's different from the title"""
        base_desc = f"Detailed implementation of: {text.strip()}"
        
        # Add goal-specific context
        if "learn" in goal.lower() or "study" in goal.lower():
            base_desc += f". This involves comprehensive study and practice to master the concepts for {goal}."
        elif "build" in goal.lower() or "create" in goal.lower():
            base_desc += f". This involves hands-on development and implementation for {goal}."
        elif "organize" in goal.lower() or "plan" in goal.lower():
            base_desc += f". This involves coordination and logistics for {goal}."
        
        return base_desc

    def _create_fallback_tasks(self, goal: str, team_size: int) -> list:
        """Create fallback tasks if transformer doesn't generate useful content"""
        
        # Scale hours based on team size
        def scale_hours(hours):
            if team_size > 1:
                return max(2, hours / team_size)
            return hours
        
        return [
            {
                "id": "t1",
                "title": "Goal Analysis",
                "description": f"Conduct thorough analysis of requirements and constraints for '{goal}'. Define scope, objectives, and success criteria.",
                "est_hours": scale_hours(4),
                "dependencies": [],
                "risk_score": 2
            },
            {
                "id": "t2", 
                "title": "Planning & Preparation",
                "description": f"Create comprehensive project plan with timelines, resources, and deliverables for '{goal}'. Gather necessary materials and tools.",
                "est_hours": scale_hours(6),
                "dependencies": ["t1"],
                "risk_score": 2
            },
            {
                "id": "t3",
                "title": "Implementation",
                "description": f"Execute the core activities and deliverables for '{goal}'. Apply best practices and maintain quality standards throughout the process.",
                "est_hours": scale_hours(8),
                "dependencies": ["t2"],
                "risk_score": 3
            },
            {
                "id": "t4",
                "title": "Review & Delivery",
                "description": f"Conduct final review, testing, and quality assurance for '{goal}'. Prepare deliverables and ensure all requirements are met.",
                "est_hours": scale_hours(4),
                "dependencies": ["t3"],
                "risk_score": 2
            }
        ]

    def _create_aggressive_variant(self, tasks: list) -> list:
        """Create aggressive variant"""
        aggressive = []
        for i, task in enumerate(tasks[:4]):  # Take first 4 tasks
            new_task = task.copy()
            new_task["est_hours"] = max(2, task["est_hours"] * 0.7)
            new_task["risk_score"] = min(5, task["risk_score"] + 1)
            new_task["id"] = f"t{i+1}"
            new_task["dependencies"] = [] if i == 0 else [f"t{i}"]
            aggressive.append(new_task)
        return aggressive

    def _create_safe_variant(self, tasks: list) -> list:
        """Create safe variant"""
        safe = []
        for i, task in enumerate(tasks):
            new_task = task.copy()
            new_task["est_hours"] = task["est_hours"] * 1.3
            new_task["risk_score"] = max(1, task["risk_score"] - 1)
            new_task["id"] = f"t{i+1}"
            new_task["dependencies"] = [] if i == 0 else [f"t{i}"]
            safe.append(new_task)
        return safe