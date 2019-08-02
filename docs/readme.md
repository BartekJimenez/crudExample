# crudExample App

crudExample is a simple CRUD app using the REST api via python and flask. 

## Installation

Use git to clone the repository https://github.com/BartekJimenez/crudExample.git

```bash
git clone https://github.com/BartekJimenez/crudExample.git
```

## Setup

Make sure you have the following python packages:
- requests
- flask
- flask_sqlalchemy
- flask_marshmallow
- marshmallow-sqlalchemy

pip commands for non-windows machines:
```bash
pip install requests
pip install flask
pip install flask_sqlalchemy
pip install flask_marshmallow
pip install marshmallow-sqlalchemy
```

Now install the db You can enter python via the console at the root and then:

```python
from crudExample import db
db.create_all()
exit()
```


## Usage



Navigate to the root, and type in your console on windows:
```bash
python crudExample.py

```

If your packages are all installed, you should be running the app. Get the url from the console, it should be : http://127.0.0.1:5000/


## Example 1

Post user Josh:

![step one](images/post.png)

Get all users:

![step two](images/get.png)

Add another user Amanda:

![step three](images/post2.png)

Update Josh's incorrect spelling in 'Australia':

![step four](images/put.png) 


Delete Amanda:

![step five](images/delete.png)

Search by Josh's ID:

![step six](images/get2.png)

Search by all:

![step seven](images/get3.png)





