This project was developed as a personal initiative with no intention of participating in the Smart India Hackathon 2023.

# PROBLEM STATEMENT DETAILS
| Problem Statement ID              | 1369                           |
|-----------------------------------|--------------------------------|
| Problem Statement Title           | Online integrated platform for projects taken up by the students of various universities/colleges |
| Description                       | Innovation is the key to betterment of education and students in the Indian universities/colleges put a lot of efforts on the projects as a part of the academic requirements. If a common knowledge platform (with a facility for plagiarism) is created to bring all project works taken up at various levels by the students in Technical / Higher Educational Institutes and Universities throughout the country, then it will be a great source of knowledge and also will help the student community to take up unique/innovative project works Summary: An integrated platform should be developed where in all the universities/Colleges provide information about the projects done by the students. The information on this platform will help in the peer learning and this will also help in cross functional research between various universities/colleges. Objective: To develop an online integrated platform for projects taken up by the students of various universities/colleges. |
| Organization                      | Government of Jharkhand          |
| Category                          | Software                         |
| Domain Bucket                     | Smart Education                  |

# Technology Stack
| Python |
|--------|
| Django|
|Sqlite3 / Mysql|
|Bootstrap v4.5.0|

# Main Idea
- The primary objective is to bring together students and their projects exclusively from various colleges, universities, schools, and institutions.
- Students can register and log in, or they can try the demo user to explore all available projects.
- Form Teams: Assign Team Leaders and Team Members.
- Create Projects: Specify Project Details, Deadline, Technology Stack, and Progress.
- Create Tasks: Team leaders can assign tasks to everyone, while members can self-assign tasks.
- View all projects and their details created by students across Bharat.
- Comment Section

![image](https://github.com/Akshay-Arjun/National-Project-Management/assets/68991993/b1fc3907-a1d9-46c2-8f5f-cabac21ef3a5)

# Installion & Usage
## Make sure you have the following installed:
- Python3
## Add the Database if you need mysql at https://github.com/Akshay-Arjun/National-Project-Management/blob/895ca43cc50b7edfb105d751329e596b2d2706c7/national-pm/local_settings.py#L31
## Change email settings ( this is used for reset password emails sent to users ) at https://github.com/Akshay-Arjun/National-Project-Management/blob/895ca43cc50b7edfb105d751329e596b2d2706c7/national-pm/local_settings.py#L45
## 1. **Clone the repository:**
   ```
   git clone https://github.com/Akshay-Arjun/National-Project-Management
   cd National-Project-Management
   ```
## 2. Create a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
## 3. Install dependencies:
```
pip install -r requirements.txt
```
## 4. Apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```
## 5. Create Super user aka admin:
```
python manage.py createsuperuser
```
## 6. Run the App
Start the development server:
```
python manage.py runserver
```
Visit http://127.0.0.1:8000/admin in your browser login with admin and in users add new user with username and password from https://github.com/Akshay-Arjun/National-Project-Management/blob/895ca43cc50b7edfb105d751329e596b2d2706c7/national-pm/local_settings.py#L60 https://github.com/Akshay-Arjun/National-Project-Management/blob/895ca43cc50b7edfb105d751329e596b2d2706c7/national-pm/local_settings.py#L61
Now make click on edit this user and click on checkbox which says Demo User.
## 7. Logout 
## 8. Home Page
Visit http://127.0.0.1:8000/ in your browser (This page is for users aka students).


# Modules
## Teams
Teams are made up of members, and every team has a leader. Team leaders have
special privileges like being able to assign tasks to other team members and
changing the members of the team. 

## Projects
Every project is assigned to a team and thus has members and a leader associated
with it. A project can only be assigned to one team but a team can have many
projects. Once a project is over it can be marked as completed.

## Tasks
Tasks are assigned to projects. Once a task has been assigned to a project it
can be assigned to a member of the project's team, it will then appear on a list
of their active tasks. Tasks can be assigned by team members to themselves or by
the team leader to anyone on the team. Any member of a project's team can create
a task for the project. Every task is given a unique number that can be used to
refer to it independent of the project or user it is assigned to. Tasks can also
be marked as completed, this is generally done by the user that the task is
assigned to, but may also be done by the team leader.

## The Dashboard
One of the main features of the site is the user's dashboard.
Currently this shows six key tables, though this may change in the
future.

### 1 & 2 ) Graphs
There are two graphs , 1st one shows technologies used in all projects and the 2nd one shows all active v/s completed projects.
Note: Graph data is independent of user, i.e it shows graphs for all available projects in database.

### 3) Top tasks
This is a list of the user's top seven tasks, tasks are ranked firstly by due
date and then by priority (in other words the highest priority task that is due
today is at the top).

### 4) Unassigned tasks
A list of the top seven unassigned tasks from projects where the user is the
team leader, again sorted by due date and priority.

### 5) User's projects
A list of all active projects the user is a part of.

### 6) User's teams
A list of teams the user is a part of.
