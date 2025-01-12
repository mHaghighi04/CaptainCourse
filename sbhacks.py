import requests

def convert_24h_to_am_pm(time_str: str) -> str:
    """
    Convert various time string formats to an AM/PM time string.
    """
    # Handle TBA
    if time_str.upper() == "TBA":
        return "TBA"

    # Remove whitespace
    time_str = time_str.strip()

    # Check for "HH:MM"
    if len(time_str) == 5 and time_str[2] == ':':
        hh, mm = time_str.split(':')
        try:
            hour = int(hh)
            minute = int(mm)
        except ValueError:
            return time_str
        suffix = "AM"
        if hour == 0:
            hour = 12
        elif hour == 12:
            suffix = "PM"
        elif hour > 12:
            hour -= 12
            suffix = "PM"
        return f"{hour}:{minute:02d} {suffix}"

    # Zero-pad if 3 digits (e.g., '900' -> '0900')
    if len(time_str) == 3 and time_str.isdigit():
        time_str = "0" + time_str

    # Parse "HHMM"
    if len(time_str) == 4 and time_str.isdigit():
        hour = int(time_str[:2])
        minute = int(time_str[2:])
        suffix = "AM"
        if hour == 0:
            hour = 12
        elif hour == 12:
            suffix = "PM"
        elif hour > 12:
            hour -= 12
            suffix = "PM"
        return f"{hour}:{minute:02d} {suffix}"

    return time_str

def main():

    year = int(input())
    quarter = int(input())
    yearq = str(year) + str(quarter)
    API_KEY = "gPWeE7ueiYGFVSIrZscjs0ZZvkI8IwS6"  
    # QUARTER = "20241"             
    DEPT_CODE = "CMPSC"           

    API_ENDPOINT = f"https://api.ucsb.edu/academics/curriculums/v3/classes/search?quarter={yearq}&pageNumber=1&pageSize=10&includeClassSections=true"
    headers = {
        "accept": "application/json",
        "ucsb-api-version": "1.0",
        "ucsb-api-key": API_KEY
    }
    params = {
        "quarter": yearq,
        "deptCode": DEPT_CODE
    }

    response = requests.get(API_ENDPOINT, headers=headers, params=params)

    if response.status_code != 200:
        print(f"API request failed with status {response.status_code}: {response.text}")
        return

    data = response.json()
    classes = data.get("classes", [])

    for course in classes:
        course_id = course.get("courseId", "N/A")
        title = course.get("title", "N/A")

        class_sections = course.get("classSections", [])
        if class_sections:
            section = class_sections[0]
            enroll_code = section.get("enrollCode", "N/A")
            enrolled = section.get("enrolledTotal", 0)
            max_enroll = section.get("maxEnroll", 0)

            time_locations = section.get("timeLocations", [])
            if time_locations:
                first_meeting = time_locations[0]
                meeting_days = first_meeting.get("days", "N/A")
                begin_time_24h = first_meeting.get("beginTime", "N/A")
                end_time_24h = first_meeting.get("endTime", "N/A")

                begin_time = convert_24h_to_am_pm(begin_time_24h)
                end_time = convert_24h_to_am_pm(end_time_24h)
            else:
                meeting_days = "N/A"
                begin_time = "N/A"
                end_time = "N/A"

            instructors = section.get("instructors", [])
            if instructors:
                professor = instructors[0].get("instructor", "N/A")
            else:
                professor = "N/A"
        else:
            enroll_code = "N/A"
            enrolled = 0
            max_enroll = 0
            meeting_days = "N/A"
            begin_time = "N/A"
            end_time = "N/A"
            professor = "N/A"

        print("-------------------------------------------------")
        print(f"Course ID:       {course_id}")
        print(f"Course Title:    {title}")
        print(f"Enroll Code:     {enroll_code}")
        print(f"Current Size:    {enrolled} / {max_enroll}")
        print(f"Meeting Days:    {meeting_days}")
        print(f"Meeting Time:    {begin_time} - {end_time}")
        print(f"Professor:       {professor}")

if __name__ == "__main__":
    main()