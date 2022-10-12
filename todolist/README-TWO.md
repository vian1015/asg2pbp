# HEROKU APP: [LINK](https://pbp-asg2.herokuapp.com/todolist/)
## Difference Between Asynchronous and Synchronous Programming
Asynchronous Programming allows multiple operations to run together at the same time. Synchronous Programming on the other hand, can only run one operation at any time. 

## Event-Driven Programming
In the event-driven programming paradigm, user actions (such as mouse clicks and key pushes) are used to control the program's flow. Some example used on this application are the buttons. Some button such as "Add Task" will react to a user's click.

## Implementation of Asynchronous Programming in AJAX
One of the simplest implementation of asynchronous programming in AJAX is the use of `async function`.

## Implementation
### Creating a view that returns whole data task in the form of JSON.
Create `show_json` function on `views.py`
```py
...
def show_json(request):
    data = Task.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
...
```
### Create a path containing `/todolist/json` that redirects to the new view
Create a new path to `urls.py`
```py
...
from todolist.views import show_json
path('json/', show_json, name='show_json')
...
```
### Do the AJAX GET method to get the list of task
On `todolist.html`, create a function `getTodolist`.
```html
async function getTodolist() {
      return fetch("{% url 'todolist:show_json' %}").then((res) => res.json())
    }
```
### Create an Add Task button that opens to a modal with a form to add new tasks.
The `data-bs-dismiss="modal"` attribue makes it so that after you click the element, it will dismiss/close the modal.
```html
<form id="form" onsubmit="return false;">
    {% csrf_token %}
    <div class="modal fade" id="createTaskModal" tabindex="-1" aria-labelledby="createTaskModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="createTaskModalLabel">Add Task</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label class="col-form-label">Title</label>
                  <input type="text" class="form-control" name="title">
                </div>
                <div class="mb-3">
                  <label class="col-form-label">Description</label>
                  <textarea class="form-control" name="description"></textarea>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-primary" value="Submit" onclick="addTask()" data-bs-dismiss="modal">Submit</button>
            </div>
          </div>
        </div>
    </div>
</form>
```
### Refresh on the main page asyncronically to show the latest list without having to reload the entire page.
Create a function `refreshTodolist`, which will show the latest list by recreating the tasklist.
```html
async function refreshTodolist() {
    document.getElementById("todolist-cards").innerHTML = ""
    const task_list = await getTodolist()
    let cnt = 0
    let htmlString = ''
    task_list.forEach((task) => {
        // console.log(task)
        cnt += 1
        const btn_type = task.fields.is_finished ? 'btn-outline-success' : 'btn-outline-warning'
        const style_color = task.fields.is_finished ? 'style="color: #43835c;"' : 'style="color: #f3c343;"'
        const mark_text = task.fields.is_finished ? 'Mark Undone' : 'Mark as Done'
        htmlString += `
        <div id="accordion">
            <div class="card mb-2 meow" style="max-width: 70vw;">
            <button class="btn ${btn_type} text-start text-decoration-none" data-bs-toggle="collapse" href="#collapse-${cnt}" aria-expanded="true" aria-controls="collapse-${cnt}" style="color:#F3DE8A; background-color: rgb(39, 40, 56, 0.9);">
                <div class="card-header" id="headingOne" style="background-color: transparent;">
                <h5 class="mb-0">
                    <i class="fa fa-circle" ${style_color}></i>
                    ${task.fields.title}
                </h5>
                </div>
            </button>
            <div id="collapse-${cnt}" class="collapse multi-collapse">
                <div class="card-body text-primary">
                <p class="card-subtitle mb-2 text-muted">Created on ${task.fields.date}</p>
                <p class="card-text" style="color:rgb(39, 40, 56)">${task.fields.description}</p>
                <button class="btn ${btn_type}" onclick="inverseTask(${task.pk})">
                    <a class="text-decoration-none text-reset">
                    ${mark_text}
                    </a>
                </button>
                <button class="btn btn-outline-danger" onclick="delTask(${task.pk})">
                    <a class="text-decoration-none text-reset">
                    Delete Task
                    </a>
                </button>
                </div>
            </div>
            </div>
        </div>
        ` 
    })
    
    document.getElementById("todolist-cards").innerHTML = htmlString
}
```

