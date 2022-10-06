# HEROKU APP: [LINK](https://pbp-asg2.herokuapp.com/todolist/)
## Account 1:
`username`: test
`password`: pbpasg4!
## Account 2:
`username`: dummy
`password`: pbpasg4!
# Assignment 4
## What `{% csrf_token %}` do
Django uses the `{% csrf_token %}` tag to protect itself from malicious attacks. When rendering the page, it creates a token on the server-side and makes sure to cross-check this token for any incoming requests. The inbound requests are not carried out if they lack the token. Without `{% csrf_token %}`, our applications are vulnerable to malicious attacks.

## Creating `<form>` manually
`form.as_table` basically creates these elements:
```HTML
<tr>
  <th><label for="id_username">Username:</label></th>
  <td>
    
    <input type="text" name="username" maxlength="150" autocapitalize="none" autocomplete="username" autofocus required id="id_username">
    
      <br>
      <span class="helptext">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>
    
    
  </td>
</tr>

<tr>
  <th><label for="id_password1">Password:</label></th>
  <td>
    
    <input type="password" name="password1" autocomplete="new-password" required id="id_password1">
    
      <br>
      <span class="helptext"><ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul></span>
    
    
  </td>
</tr>

<tr>
  <th><label for="id_password2">Password confirmation:</label></th>
  <td>
    
    <input type="password" name="password2" autocomplete="new-password" required id="id_password2">
    
      <br>
      <span class="helptext">Enter the same password as before, for verification.</span>
    
    
      
    
  </td>
</tr>
```
So yes, we can create our own form element manually. Generally, what we need in order to create form elements are input elements. For example, the input elements from `form.as_table` above are `username` and `password`.

## Data flow process
When the user first opens `./todolist/create_task`, `urls.py` will route the request to `create_task` function in `todolist/views.py`.
```python title="/views.py"
...
def create_task(request):
    # upon openin
    if request.method == 'POST':
        ...
    context = {}
    return render(request, 'create_task.html', context)
...
```
When `create_task` function is ran, the `request.method` won't be `POST`, therefore it won't go in the `if` statement. So it will return the user `create_task.html`
```HTML title="templates/create_task.html"
...
<form method="POST" action="">
        {% csrf_token %}
        <table>
            <tr>
                <td>title: </td>
                <td><input type="text" name="title" placeholder="Insert Task Title Here" class="form-control"></td>
            </tr>

            <tr>
                <td>description: </td>
                <td><input type="description" name="description" placeholder="Insert Task Description Here" class="form-control"></td>
            </tr>

            <tr>
                <td></td>
                <td><input class="btn create_task_btn" type="submit" value="Create Task!"></td>
            </tr>
        </table>
    </form>
...
```
When the user is directed to `create_task.html` they can fill in the forms. Note that the form method is `POST`. After the user filled in the forms, and clicked the "Submit" button, the application will run `create_task` function again. But this time, the `request.method` will be `POST`. Therefore we will go in the `if` statement and run the codes insided it. 
```python title="views.py"
...
if request.method == 'POST':
      title = request.POST.get('title')
      description = request.POST.get('description')
      Task.objects.create(title=title, 
                          description=description, 
                          user=request.user, 
                          date=datetime.datetime.now())
      response = HttpResponseRedirect(reverse('todolist:show_todolist'))
      response.set_cookie('last_update', str(datetime.datetime.now()))
      return response
...
```
Inside the `if` statement, we transfer whatever the user fills on the form into our data storage, then redirect back to `show_todolist` function. 
```python title="todolist/views.py"
...
def show_todolist(request):
    task_list = Task.objects.filter(user=request.user)
    context = {
        'task_list': task_list,
        'name': 'Jovian',
        'npm': 2106720891,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "todolist.html", context)
...
```
Inside the `show_todolist` function, we take the data from our data storage, and send it as a parameter to render with `todolist.html`, which will show the user the datas they previous inputted.
## Implementation
### Create a new application `todolist`
Create a new app
```cmd
python manage.py startapp todolist
```
Register the new app into `settings.py` in `project_django` folder.
```python title="project_django/urls.py"
INSTALLED_APPS = [
    ...
    'todolist'
]
```
### Add the path `todolist`
```python title="project_django/urls.py"
urlpatterns = [
    ...
    path('todolist/', include('todolist.urls'))
]
```
### Creating a task model
```python title="todolist/models.py"
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=55)
    description = models.TextField()
    is_finished = models.BooleanField(default=False)
```
### Implement registration, login, and logout forms
Create the routing in `urls.py`
```python title="todolist/urls.py"
...
from todolist.views import register
from todolist.views import login_user
from todolist.views import logout_user

app_name = 'todolist'

urlpatterns = [
    ...
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
```
Create the functions on `views.py`
```python title="todolist/views.py"
from django.shortcuts import render
from todolist.models import Task
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created!')
            return redirect('todolist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # login first
            response = HttpResponseRedirect(reverse("todolist:show_todolist")) # create response
            response.set_cookie('last_login', str(datetime.datetime.now())) # create last_login cookie and add it to response
            return response
        else:
            messages.info(request, 'Wrong Username or Password!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    return response
```
Create the HTML for login and register forms
```HTML title="todolist/templates/register.html"
{% extends 'base.html' %}

{% block meta %}
<title>Account Registration</title>
{% endblock meta %}

{% block content %}

<div class = "login">
    <h1>Registration Form</h1>

        <form method="POST" >
            {% csrf_token %}
            <table>
                {{ form.as_table }}
                <tr>
                    <td></td>
                    <td><input type="submit" name="submit" value="Register"/></td>
                </tr>
            </table>
        </form>

    {% if messages %}
        <ul>
            {% for message in messages %}
                <li>{{ message }}</li>
                {% endfor %}
        </ul>
    {% endif %}

</div>

{% endblock content %}
```
```HTML title="todolist/templates/login.html"
{% extends 'base.html' %}

{% block meta %}
<title>Login</title>
{% endblock meta %}

{% block content %}

<div class = "login">

    <h1>Login</h1>

    <form method="POST" action="">
        {% csrf_token %}
        <table>
            <tr>
                <td>Username: </td>
                <td><input type="text" name="username" placeholder="Username" class="form-control"></td>
            </tr>

            <tr>
                <td>Password: </td>
                <td><input type="password" name="password" placeholder="Password" class="form-control"></td>
            </tr>

            <tr>
                <td></td>
                <td><input class="btn login_btn" type="submit" value="Login"></td>
            </tr>
        </table>
    </form>

    {% if messages %}
        <ul>
            {% for message in messages %}
                <li>{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}

    Don't have an account? <a href="{% url 'todolist:register' %}">Create Account</a>

</div>

{% endblock content %}
```

### Creating todolist main page
```HTML title="todolist/templates/todolist.html"
{% extends 'base.html' %}
{% load static %}

{% block meta %}
<title>Todolist</title>
{% endblock meta %}

{% block content %}
  <h1>Hello, {{ user }}!</h1>
  <table>
    <tr>
        <th>Title</th>
        <th>Description</th>
        <th>Date Created</th>
    </tr>
    {% for task in task_list %}
    <tr>    
        <th>{{task.title}}</th>
        <th>{{task.description}}</th>
        <th>{{task.date}}</th>
        <th><input type="checkbox" onclick='location.href="{% url 'todolist:inverse_checkbox' task.id %}"' {% if task.is_finished %}checked="checked"{% endif %}></th>
        <th><button><a href="{% url 'todolist:delete_task' task.id %}">Delete Task</a></button></th>
    </tr>
    {% endfor %}
  </table>
  <button><a href="{% url 'todolist:create_task' %}">Create Task</a></button>
  <button><a href="{% url 'todolist:logout' %}">Logout</a></button>
{% endblock content %}
```

### Creating a form page for task creation
```HTML title="todolist/templates/create_task.html"
{% extends 'base.html' %}

{% block meta %}
<title>Login</title>
{% endblock meta %}

{% block content %}

<div class = "create_task">

    <h1>Create Task</h1>

    <form method="POST" action="">
        {% csrf_token %}
        <table>
            <tr>
                <td>title: </td>
                <td><input type="text" name="title" placeholder="Insert Task Title Here" class="form-control"></td>
            </tr>

            <tr>
                <td>description: </td>
                <td><input type="description" name="description" placeholder="Insert Task Description Here" class="form-control"></td>
            </tr>

            <tr>
                <td></td>
                <td><input class="btn create_task_btn" type="submit" value="Create Task!"></td>
            </tr>
        </table>
    </form>

</div>

{% endblock content %}
```

### Deploying to Heroku
Simply push the file to github

# Assignment 5
## Difference between Inline, Internal and External CSS
Inline CSS is used to style a specific HTML element. The advantages of using Inline CSS is that we don't need to create a separate file for styling our HTML elements. This method is time-consuming though and it also makes your HTML structure looks more messy. Internal CSS is used to style the whole HTML page with a remote CSS file. Similar to Internal CSS, the External CSS is used to style the whole HTML page, but is used by linking out web pages to an external `.css` file. By using External CSS, our HTML files will have a cleaner structure and smaller in size. 

## HTML5 tags
`<a>` defines a hyperlink
`<body>` defines the document body
`<button>` create a clickable button
`<div>` specify a division or section in a document
`<footer>` Represents the footer of a document or a section
`<form>` Defines a HTML form for user input
`<head>` Defines the head portion of the document
`<header>` Represents the header of a document or a section
`<h1>` to `<h6>` Defines HTML heading
`<html>` Defines the root fo an HTML document
`<img>` Represents an image
`<input>` Defines an input control
`<label>` Defines a label for `<input>` control
`<li>` Defines a list of items
`<p>` Defines a pragraph
`<span>` Defines an inline styleless section in a document
`<table>` Defines a data table
`<td>` Defines a cell in a table
`<tfoot>` Defines table footer
`<th>` Defines a header cell in a table
`<thead>` Groups a set of rows that describes the column labels of a table.
`<tr>` Defines a row of cells in a table
`<ul>` Defines an unordered list
`<var>` Defines a variable

## CSS Selectors
`.class` Select all elements with this class
`:first-child` Select the first child of an element
`:hover` Select elements on mouse over
`:last-child` Select the last child of an element
`:nth-child()` Select certain child 

## Implementation
### Internal CSS
Create `style.css` in `static/css` directory. 
Link the css file to `base.html`
```html
...
<head>
    ...
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    ...
</head>
...
```
### External CSS
I'm using Bootstrap for this assignment. Link bootstrap to `base.html`
```html
...
<head>
    ...
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
    ...
</head>
...
```
Using Bootstrap, I createed a navbar. I also used bootstrap to create the cards on `login.html`, `register.html`, and `todolist.html`
### Inline CSS
I implement some Inline CSS too!
