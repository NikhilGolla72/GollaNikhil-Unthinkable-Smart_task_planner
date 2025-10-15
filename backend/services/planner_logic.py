from datetime import datetime, timedelta
import uuid

class PlannerLogic:
    def __init__(self):
        self.work_hours_per_day = 8

    def process_llm_response(self, raw: dict, request_payload):
        variants = {}
        assumptions = raw.get("assumptions", "")
        summary = raw.get("summary", "")
        
        # Get request parameters (handle both dict and Pydantic object)
        if hasattr(request_payload, 'team_size'):
            # Pydantic object
            team_size = request_payload.team_size or 1
        else:
            # Dictionary
            team_size = request_payload.get("team_size", 1)

        # Process each planning mode
        for mode in ["balanced", "aggressive", "safe"]:
            variant_data = raw.get("variants", {}).get(mode, {})
            if not variant_data:
                # Create a default variant if not provided
                variant_data = {
                    "tasks": [],
                    "critical_path": [],
                    "reasoning": f"{mode.capitalize()} approach to the project"
                }
            
            tasks = variant_data.get("tasks", [])
            computed_tasks = []
            
            # Use today as start date
            current_date = datetime.now().date()
            
            # Process tasks with team member assignments
            for task in tasks:
                est_hours = float(task.get("est_hours", 1))
                task_title = task.get("title", "")
                task_description = task.get("description", "")
                
                # Check if this is a team member task (contains "Team Member X:")
                if "Team Member" in task_title and team_size > 1:
                    # This is already a specific team member task from Gemini
                    days = max(1, int((est_hours + (self.work_hours_per_day - 1)) // self.work_hours_per_day))
                    
                    # Calculate days based on estimated hours
                    
                    start_date = current_date.isoformat()
                    end_date = (current_date + timedelta(days=days)).isoformat()
                    
                    # Extract team member number from title
                    team_member_num = "1"
                    if "Team Member 2:" in task_title:
                        team_member_num = "2"
                    elif "Team Member 3:" in task_title:
                        team_member_num = "3"
                    elif "Team Member 4:" in task_title:
                        team_member_num = "4"
                    elif "Team Member 5:" in task_title:
                        team_member_num = "5"
                    
                    computed_tasks.append({
                        "id": task.get("id", str(uuid.uuid4())[:8]),
                        "title": task_title,
                        "description": task_description,
                        "est_hours": est_hours,
                        "dependencies": task.get("dependencies", []),
                        "risk_score": task.get("risk_score", 1),
                        "start": start_date,
                        "end": end_date,
                        "team_member": team_member_num,
                        "team_size": team_size
                    })
                    
                    # For different team member tasks, they can run in parallel
                    # Only move the date forward when we've processed all team members for this phase
                    # This is handled by the task processing order from Gemini
                
                else:
                    # This is a general task that needs to be split among team members
                    if team_size > 1:
                        # Create parallel tasks for each team member
                        base_task_name = task_title.replace(" (Team of", "").split(" (Team of")[0]
                        
                        for member_num in range(1, team_size + 1):
                            member_hours = est_hours  # Each person works the full hours
                            days = max(1, int((member_hours + (self.work_hours_per_day - 1)) // self.work_hours_per_day))
                            
                             # Calculate days based on estimated hours
                            
                            start_date = current_date.isoformat()
                            end_date = (current_date + timedelta(days=days)).isoformat()
                            
                            member_task_title = f"Team Member {member_num}: {base_task_name}"
                            member_description = f"Team Member {member_num} is responsible for: {task_description}"
                            
                            computed_tasks.append({
                                "id": f"{task.get('id', str(uuid.uuid4())[:8])}_{member_num}",
                                "title": member_task_title,
                                "description": member_description,
                                "est_hours": member_hours,
                                "dependencies": task.get("dependencies", []),
                                "risk_score": task.get("risk_score", 1),
                                "start": start_date,
                                "end": end_date,
                                "team_member": str(member_num),
                                "team_size": team_size
                            })
                        
                        # Move to next activity after all team members complete their tasks
                        current_date = current_date + timedelta(days=days)
                    
                    else:
                        # Single person task
                        days = max(1, int((est_hours + (self.work_hours_per_day - 1)) // self.work_hours_per_day))
                        
                         # Calculate days based on estimated hours
                        
                        start_date = current_date.isoformat()
                        end_date = (current_date + timedelta(days=days)).isoformat()
                        
                        computed_tasks.append({
                            "id": task.get("id", str(uuid.uuid4())[:8]),
                            "title": task_title,
                            "description": task_description,
                            "est_hours": est_hours,
                            "dependencies": task.get("dependencies", []),
                            "risk_score": task.get("risk_score", 1),
                            "start": start_date,
                            "end": end_date,
                            "team_member": "1",
                            "team_size": 1
                        })
                        
                        current_date = current_date + timedelta(days=days)
            
            # Check for and fix task duplications
            computed_tasks = self._fix_task_duplications(computed_tasks, team_size)
            
            variants[mode] = {
                "tasks": computed_tasks,
                "critical_path": variant_data.get("critical_path", []),
                "reasoning": variant_data.get("reasoning", "")
            }

        return {
            "variants": variants,
            "assumptions": assumptions,
            "summary": summary
        }
    
    def _fix_task_duplications(self, tasks, team_size):
        """Fix duplicated tasks by creating different specialized tasks for each team member"""
        if team_size <= 1:
            return tasks
        
        # Check if we have duplicated tasks
        task_names = {}
        duplicated_tasks = []
        
        for task in tasks:
            base_name = task["title"].replace("Team Member 1:", "").replace("Team Member 2:", "").replace("Team Member 3:", "").replace("Team Member 4:", "").replace("Team Member 5:", "").strip()
            if base_name in task_names:
                duplicated_tasks.append(task)
            else:
                task_names[base_name] = task
        
        # If we found duplications, create specialized tasks
        if duplicated_tasks:
            print(f"Found {len(duplicated_tasks)} duplicated tasks, creating specialized tasks...")
            
            # Create specialized task templates based on the goal
            specialized_tasks = self._create_specialized_tasks(tasks, team_size)
            return specialized_tasks
        
        return tasks
    
    def _create_specialized_tasks(self, original_tasks, team_size):
        """Create individual subtasks assigned to team members in rotating pattern"""
        
        # Define individual subtasks that can be assigned to team members
        subtask_templates = [
            "Design Homepage Layout",
            "Set Up Database Schema", 
            "Create User Authentication",
            "Build API Endpoints",
            "Implement Frontend Components",
            "Add Data Validation",
            "Configure Server Environment",
            "Create Wireframes",
            "Design UI Components",
            "Build User Interface",
            "Set Up Deployment Pipeline",
            "Implement Security Features",
            "Create Content Management",
            "Add Search Functionality",
            "Optimize Performance",
            "Write Documentation",
            "Set Up Testing Framework",
            "Configure Analytics",
            "Create Admin Dashboard",
            "Implement Payment System"
        ]
        
        # Calculate how many subtasks to create (6-12 based on team size)
        num_subtasks = min(12, max(6, team_size * 3))
        selected_subtasks = subtask_templates[:num_subtasks]
        
        specialized_tasks = []
        current_date = datetime.now().date()
        
        for i, subtask_name in enumerate(selected_subtasks):
            # Assign to team member in rotating pattern (1,2,3,1,2,3...)
            team_member_num = (i % team_size) + 1
            
            # Get a sample task to extract basic info
            sample_task = original_tasks[i % len(original_tasks)] if original_tasks else {"est_hours": 8, "risk_score": 3}
            
            # Calculate task duration (shorter for individual subtasks)
            est_hours = max(2, min(8, sample_task["est_hours"] / 2))  # Individual subtasks are smaller
            days = max(1, int((est_hours + (self.work_hours_per_day - 1)) // self.work_hours_per_day))
            
            # Calculate start date (tasks can run in parallel within phases)
            phase = i // team_size
            start_date = (current_date + timedelta(days=phase)).isoformat()
            end_date = (current_date + timedelta(days=phase + days)).isoformat()
            
            # Determine dependencies (first task in each phase depends on previous phase)
            dependencies = []
            if i >= team_size:
                # This subtask depends on the corresponding subtask from previous phase
                prev_task_id = f"t{i - team_size + 1}"
                dependencies = [prev_task_id]
            
            specialized_task = {
                "id": f"t{i + 1}",
                "title": f"Team Member {team_member_num}: {subtask_name}",
                "description": f"Team Member {team_member_num} is responsible for {subtask_name}. This is a specific, focused task that contributes to the overall project goal.",
                "est_hours": est_hours,
                "dependencies": dependencies,
                "risk_score": sample_task.get("risk_score", 3),
                "start": start_date,
                "end": end_date,
                "team_member": str(team_member_num),
                "team_size": team_size
            }
            
            specialized_tasks.append(specialized_task)
        
        return specialized_tasks