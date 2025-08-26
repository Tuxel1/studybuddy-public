# README.md

This is a project folder for my final project for CS50.

## Project ideas

- I want to create some sort of data dashboard.
    - I want to build a website and webapp building HTML/CSS with bootstrap, 
as well as Flask and Python.
    - I want to include some form of user input.
    - Maybe use some javascript as well.
    - I need to figure out what data I want to use and how to get it.
    - It would be cool to use some real-time data. It would also be really cool 
to scrape that data myself. But a regular scrape is difficult without an external server.
    - I also need to figure out how to visualise the data and how to embed it on the website.
- I want to build a self-study app! Similar to a to do list app or something 
similar. But something that is focussed on self-study.
    - I get to work with databases, track time, build a web-based interface. 


## The project: Study Buddy

With STUDY BUNNY I want to build a companion app for self-study enthusiasts to 
keep track of their learning progress. Similar to a to-do-list app, but more 
focussed on learning and encouraging self-structured advancement.

Since I plan to run this locally and share the source-code for personal use, I 
won't concern myself with user logins for now. Everything in the database will 
the data of the current user who uses the code for their own purposes.

## Structure

I want everything to be structured based on `skills`. `skills` are what the user
chooses to learn. Whether those are specific skills or just topics or whatever.
The guideline here is: The user wants to IMPROVE at SOMETHING. We are 
interest-driven.

Organised under those `skills` are so-called (at least I call them this for now)
`courses`. Those can either be specific courses online or at university, or
books for example. Anything that provides some form of structured learning.

`Courses` are then divided into `Lessons`, which in turn are comprised of 
`Subtasks` (optionally).

### Data Structure

Everything should be stored in a database `studybuddy.db`.

Tables: 

- `skills`: Holds all skills.
    - `id`
    - `skill`
- `courses`
    - `id`: id for the course itself.
    - `skill_id`: id of the skill the course relates to.
    - `url`: optional. to keep track of where to find the resource. useful for 
        online courses and resources.
- `lessons`
    - `id`
    - `course_id`
    - `name`
- `subtasks`
    - `id`
    - `lesson_id`
    - `name`

All the commands I used to create the database:

````SQL
CREATE TABLE skills (
    skill_id INTEGER PRIMARY KEY,
    skill_name TEXT NOT NULL
);
````

````SQL
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    skill_id INTEGER NOT NULL,
    course_name TEXT NOT NULL,
    url TEXT
);
````

````SQL
CREATE TABLE lessons (
    lesson_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    lesson_name TEXT NOT NULL
);
````

````SQL
ALTER TABLE lessons ADD COLUMN status TEXT DEFAULT "incomplete";
````

````SQL
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY,
    lesson_id INTEGER NOT NULL,
    task_name TEXT NOT NULL,
    status TEXT DEFAULT "incomplete"
);
````


Notes i put somewhere else: 

- make studybuddy prettier by using a color scheme. make some ux choices.
- include login functionality for studybuddy.
- implement missing functionality (add/delete/ rename maybe?) as I can do right now!
- Move buttons: New skill button as a new skill (style slightly differently); delete and rename within the box for each skill.
- add url to course in view!!!

- fix studybuddy in way so that the page doesnt reload all the time? (when adding or deleting an object)

- learn more whimsical webdesign / design in general.
- do more projects to challenge me.
- find projects to recreate in my own way. or something that is actually useful.
- learn AJAX
- force myself to learn and get more comfortable with JS (especially when interacting with a backend)

- make a portfolio website with only HTML/CSS - make it pretty and responsive and non-static. (Without bootstrap! try to do this on your own)

- built a cool github portfolio!

- study projects and code of stephanie ran
- study projects and code of the code den (?)



RENAME INTO STUDY BUNNY?????


## TODO

- [ ] Check code for redundancy -> maybe move stuff around. Think about how i can avoid repetition i currently have.
- [ ] Generate requirements file.
- [ ] Finish project for CS50
    - [ ] Write README for CS50
    - [ ] Produce video for CS50
    - [ ] Upload project to VS Code CS50
    - [ ] Submit project! -> Celebrate!
- [ ] Add feature: rename values
- [ ] Add feature: user login
- [ ] With JS and AJAX: Avoid reload of page when altering database. (We stay on the same page after all.)
- [ ] Figure out how to turn into mobile app?
- [ ] Deploy app as a webservice?
- [ ] Make source code public on github?