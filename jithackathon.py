import os
import re
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import load_dotenv
load_dotenv()

anthropic = Anthropic(api_key=os.getenv("API_KEY"))

class Course:
    def __init__(self, name, rating, start, end, day, prof):
        self.name = name
        self.rating = rating
        self.start = start
        self.end = end
        self.day = day
        self.prof = prof
        

    def to_dict(self):
        """Convert the course object to a dictionary."""
        return {
            "name": self.name,
            "rating": self.rating,
            "start": self.start,
            "end": self.end,
            "day": self.day,
            "prof": self.prof,
        }

    def __repr__(self):
        """String representation for debugging."""
        return f"Course(name={self.name}, rating={self.rating}, start={self.start}, end={self.end}, day={self.day} prof={self.prof})"




def generateSchedules(serialized_courses, max_courses):
    prompt = f"""You are an expert scheduler. Your task is to create multiple possible schedules for the given courses. 
    Each schedule should:
    1. Select up to {max_courses} courses.
    2. Prioritize courses with the highest ratings.
    3. Ensure no time overlap between selected courses.
    4. Provide a clear list of each schedule with course names and times.
    5. Ensure that courses on the same day do not overlap.

    Courses:
    {serialized_courses}

    Generate at least 3 different possible schedules, considering the constraints.
    """
    response = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=1000,
        prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
        temperature=0.7,
    )

    return response.completion.strip()

def parse_schedules(api_response, courses, max_courses):
    # Map course names to Course objects
    course_map = {course.name: course for course in courses}

    # Parse the response
    schedules = []
    for line in api_response.split("\n"):
        if line.startswith("-"):
            # Use regular expression to extract the course name
            match = re.search(r"-\s*(Course [A-Z])", line)
            if match:
                course_name = match.group(1).strip()
                #print(course_name)  # Debug print
                if course_name in course_map:
                    # Add the course object to the current schedule
                    if not schedules or len(schedules[-1]) >= max_courses:
                        schedules.append([])
                    schedules[-1].append(course_map[course_name])

    return schedules


courses = [
        Course(
            "Course A", 4.8, 9, 11, ["Tuesday", "Thursday"]
        ),
        Course(
            "Course B", 4.5, 10, 12, ["Monday", "Wednesday"]
        ),
        Course(
            "Course C", 3.2, 13, 15, ["Tuesday", "Thursday"]
        ),
        Course(
            "Course D", 3.1, 14, 15, ["Monday", "Wednesday"]
        ),
        Course(
            "Course E", 2.0, 16, 17, ["Monday", "Wednesday", "Friday"]
        ),
        Course(
            "Course F", 5.0, 18, 19, ["Tuesday", "Thursday"]
        ),
        Course(
            "Course G", 3.1, 14, 15, ["Monday", "Wednesday"]
        ),
        Course(
            "Course H", 2.0, 16, 17, ["Tuesday", "Thursday"]
        ),
        Course(
            "Course I", 5.0, 18, 19, ["Monday", "Wednesday"]
        ),
    ]
serialized_courses = [course.to_dict() for course in courses]


api_response = generateSchedules(serialized_courses, 4)

schedules = parse_schedules(api_response, courses, 4)
# for i in schedules[0]:
#     print(f"{i.name} {i.day} {i.start} {i.end} {i.prof}")
    