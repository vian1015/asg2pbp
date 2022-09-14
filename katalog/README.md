# MVT (Models, Views, and Template)
## Diagram
![](diagram.png)

## Why Virutal Environment is Necessary
By using a virtual environment, multiple versions of Python, packages, library and modules can coexist peacefully on our machine. This will come in handy, when for example, the current project we are working on requires django version 1.1, while another project requires django ver 2.2. Under normal circumstances, it would be impossible for our computer to run two versions of django simultaneously, hence why virtual environment is necessary.

## Implementation
### 1. Create a function on `views.py`
First off,  import the model `CatalogItem` from `katalog.models`
```py
from katalog.models import CatalogItem
```
Collect the QuerySet from `CatalogItem`, then parse it as `context` with other datas. We then call the render function, which will combine the given template (in this case `katalog.html`) with `context`, and returns an HTTP Response.
```py
def show_katalog(request):
    data_katalog_item = CatalogItem.objects.all()
    context = {
        'list_item': data_katalog_item,
        'name': 'Jovian',
        'student_id': '2106720891'
    }

    return render(request, "katalog.html", context)
```
### 2. Create a routing map to `views.py`
Implement the routing via `urls.py`
```py
# urls.py
from django.urls import path
from katalog.views import show_katalog


app_name = 'katalog'

urlpatterns = [
    path('', show_katalog, name='show_katalog'),
]
```

### 3. Mapping the data into HTML
This function will loop through each data. It will show all images from `img_url`, and when any of the images are clicked, it will trigger the `createTable()` function. `createTable` function will take `item_name`, `rating`, `item_price`, `item_stock`, `description`, `item_url` as its parameter.
```HTML
{% for item in list_item %}
      <img src={{item.img_url}} onclick="createTable(['{{item.item_name}}',
                                                      '{{item.rating}}',
                                                      '{{item.item_price}}',
                                                      '{{item.item_stock}}',
                                                      '{{item.description}}',
                                                      '{{item.item_url}}'])">
{% endfor %}
```
This javascript function will create a table based on the data passed on its parameter.
```js
function createTable(arr){
      const item_tbl = document.querySelector('table.item-tbl')
      if(item_tbl) {item_tbl.remove()}

      const string_arr = ["Product Name", "Rating", "Price", "Stock", "Description", "URL"]
      const container = document.querySelector('div.table-ctr')
      const tbl = document.createElement('table');
      tbl.setAttribute('class', 'item-tbl')

      arr[1] = "★".repeat(arr[1]) + "☆".repeat(5 - arr[1])
      arr[2] = "Rp" + arr[2].toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1.");

      for (i = 0; i < 5; i++){
        tr = tbl.insertRow();
        td = tr.insertCell();
        td.appendChild(document.createTextNode(string_arr[i]));
        td = tr.insertCell();
        if(i == 0){
          a = document.createElement('a')
          a.innerText = arr[0]
          a.href = arr[5]
          a.target = "_blank"
          td.appendChild(a);
        }
        else {td.appendChild(document.createTextNode(arr[i]))};
      }

      container.appendChild(tbl);
      document.querySelector('table.item-tbl').scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
```
### 4. Deploy to Heroku
Create a new app on Heroku. Then go to settings on the GitHub repository to create a new **Secret**. Input Heroku API Key and the App name, and we're goof to go!
# HEROKU APP: [LINK](https://pbp-asg2.herokuapp.com/katalog/)
