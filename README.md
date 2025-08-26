# README.md

This is a project folder for my final project for CS50.

#### Video Demo:  <URL HERE>

## STUDY BUDDY

### What is Study Buddy?

STUDY BUDDY is a tool for lifelong learners. It is a simple task manager that helps you keep track of all the self-organised studying you do - all while looking cute to keep you motivated.

### What can Study Buddy do?

Study Buddy works in a hierarchical order based on the different skills you want to acquire or improve on.

In Study Buddy you first define the skill you want to work on, e.g. coding or cooking. As Study Buddy focusses mostly on organising structured learning resources,for each skill you can then define courses you want to work through. Courses are divided into lessons, that in turn can be further broken down into tasks.

By checking off lessons you finished working through, Study Buddy helps to keep track of your progress on a course.

The intention behind Study Bunny is to give passionate learners a space to organise and see progress on their studies. I believe that giving yourself a dedicated space for self-organised study, it helps you motivate yourself and really focus on your goals.

### How does Study Buddy work?

Study Buddy is a web-based application brought to life with a back-end in Flask and Python and a front-end in HTML/CSS, some Bootstrap and a tiny bit of Javascript.

Let's take a closer look at the files and file structure:

#### Filetree

- `static`
    - `styles.css`
- `templates`
    - `layout.html`
    - `index.html`
    - `skill.html`
    - `course.html`
- `app.py`
- `studybuddy.db`: SQLite database.

---

### User-Interface / Front-end

Study Buddy, in essence, consists of three different pages or views: An overview of skills, an overview of courses, and an overview for a specific course. The user starts off by choosing a skill, then gets to see all courses related to the skill. When choosing a course, the user get redirected to its course overview page with the related lessons and tasks.

The folder `templates` holds all the templates for these pages. Let's dive deeper.

#### `layout.html`

Since several elements across all pages remain the same, this file is the overarching template file for the website. It loads all necessary modules for Bootstrap to work and loads the custom stylesheet `static/styles.css`.

Most importantly, this file defines the header section of the page with a button to navigate to the previous page, a smiley face as a logo and a speech bubble. The content of the speech bubble can be and is altered for each page. This as well as the precise redirect for the back button and the content of the body gets altered within the specific template files for each page.

Using Bootstraps predefined responsive classes, the header layout adapts to the users screen size.

#### `index.html`

This is the landing page. The user gets greeted by Study Buddy and is presented with several cards displaying their skills. Each skill card displays the skill name as well as a trash icon to delete this particular skill. There is also an additional card that triggers a modal, which allows the user to create a new skill.

The cards and card layout utilises the card component Bootstrap provides and also changes in response to device screen size.

When clicking on a skill card the user gets redirected to a page with the corresponding courses, which is created with the following template file.

#### `skill.html`

Similarly to the index page, this template draws on Bootstrap cards to create a clickable section for each course. However, these cards span the full grid width.

Again, each element has a trash button for deletion and there is an extra card create a new course.

Additionally, each course has its own progress bar that indicates the progress the user has made on this particular course so far.

#### `course.html`

After choosing a course card, the user gets presented with an overview page for the course. At the top, the user now sees a larger version of their taskbar. The card underneath display the lessons, and for each lesson the related tasks. 

Each lesson and task have their own checkbox icon, which the user can click to toggle the completion status of the object. Completing a task is mostly for personal tracking. Completing a lesson contributes to the aforementioned progress bar.

Of course, there is also an option to add or delete lessons and tasks respectively.

### Design

To create the overall layout of the page I relied heavily on Bootstrap`s grid and column functionality. This created an visually aesthetic as well as responsive layout.

#### `styles.css`

With the overall layout in place, I wanted to include my own design aesthetic in this project and create an interesting and engaging look for the website. To do so, I used some basic CSS to change colors, fonts and overall styling.

I also built some custom elements, like Study Buddy's speech bubble, and added some interactive behaviour: When hovering over them, the cards increase in size to indicate clickability (transform). On page reload the speech bubble fades in and wiggles (keyframes). I made this design choice mostly because it smoothes the transition when changing messages in the speech bubble - but it looks really cute as well.

### Data Storage

#### `studybuddy.db`

A SQLite database to store all the data Study Buddy needs. Consists of four tables: `skills`, `courses`, `lessons`, `tasks`. As the name suggests, each of the tables keeps track of one level of data. The tables relate to each other by ids: Except for skills, each of the tables stores for the current item the id of the item in the table directly above in hierarchy that it relates to. To be clear: Each task also stores the id of the lessons it belongs to, each lesson stores the id of its course, each course stores the id of its related skill.

[Include info on special fields in each table?]

### Backend

#### `app.py`

This really is the heart and soul of Study Buddy. This is where the magic happens. Let's dive in.

The heavy lifting in this project is done by two libraries: `Flask` - to help build and pass data to the webpages - and `sqlite3` - to interact with and save changes to `studybuddy.db`.

`@app.route('/')`: In this first route, there isn't happening much. This route generates the index page. The corresponding function simply filters all skills in the database and passes them as an argument when returning the rendered index template.

`@app.route("/skill<skill_id>")`: Making use of Flask's feature to build URLs, I was able to generate different pages for all skills depending on solely their id.

What happens it this: Inside of `index.html`, each card works as a button-link to one of these skill pages. The `skill()` function takes the id in the URL as input and uses it to filter the database for all related courses. For each course, the function uses another custom function `get_progress()` to calculate a progress value for the course, which is then stored inside a dictionary. All courses and progress data is then passed when rendering `skill.html`.

`get_progress()`: This is a simply helper function to calculate a progress value. It takes a course id as input. First, it filters all related lessons from the database and then counts how many have the status `completed`. It then calculates the quota of completed lessons and returns the value.

`@app.route("/course<course_id>")`: This route works similarly to its skill equivalent. The main difference being that it filters for related lessons instead of other courses. It also utilises the `get_progress()` function.

In addition to the other data, this function also loops over all related lessons found and filters their related tasks. This data is then stored in a dictionary with all lesson ids as keys for sqlite's iterator objects with the tasks inside.

`@app.route("/add_item", methods=["POST"])`: This route is what powers all ´add item`-buttons on any page.

When clicking on any of the `add item`-buttons, a modal gets triggered prompting the user for input. Submitting this form triggers this route. Along with all the visible input data, like an item's name, the form also submits a hidden value `item_type`. Based on this value `add_item()` knows what kind of item the user wants to create and adds all data into the appropriate table. On completion the page gets reloaded, so the user can see the added item.

`@app.route("/delete_item", methods=["POST"])`: Works similarly to `add_item()`. The trash icon for each element is a hidden form that submits data like item type and id to this route. Based on that `delete_item()` knows how to delete the item.

The function is defined recursively so that all data for this item gets deleted, not just the item itself. This means: When deleting a skill, not only the skill itself gets deleted but all related courses, lessons and tasks as well. After deleting the top-level item, the function triggers a page reload.

`@app.route("/update_status", methods=["POST"])`: This route changes the completion status of a lesson or task. Each task / lesson has its own checkbox that serves as a hidden form. If clicked, the form submits either `completed` or `incomplete` depending on what the status should change to. Using the provided id (submitted as another hidden value) `update_status` then changes the completion status of this particular item and triggers a page reload.