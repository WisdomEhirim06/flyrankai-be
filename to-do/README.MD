# Flyrank AI: CRUD Assignement

## Tech Stack Used

- Fast API and HTML

Pydantic was used for the data validation and FastAPI for building the API.

It is a simple to-do list application that can be used to manage tasks in a todo list.

Here are the CRUD endpoints:

- GET "/" - Returns a welcome message
- POST "/tasks" - Creates a new task
- GET "/tasks" - Returns all tasks
- GET "/tasks/{task_id}" - Returns a specific task
- DELETE "/tasks/{task_id}" - Deletes a specific task
- PUT "/tasks/{task_id}" - Updates a specific task

To run the application, use the commands
pip install fastapi uvicorn
python -m uvicorn app:app --reload

Here is the view of the swagger docs
![Swagger UI](swagger-image.png)

The swagger UI can be accessed on the following URL:
http://127.0.0.1:8000/docs
