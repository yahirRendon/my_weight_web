# My Weight Web App

Inspired by my work on an Android mobile app that allowed a user to track their weight towards a target goal, this project pushed me to develop my on backend to serve a similar functionality as the original. The desire to create a database that connects to a frontend via an API has always been an interest of mine. This project sought to explore this and implement some new features to the original design. Along with along users to enter their ongoing weight they can also enter a message with each entry. A note about the day, their progress, their struggles, and attitudes towards their goal. These posts are also displayed to the community to encourage others through the process of reaching their goals.

This project was also used as one of my capstone project at SNHU as example of working with databases. Relevant images and code snips are displayed below:

#### User Table
A view of the user data table

<img width="1626" alt="my_weight_user_tb" src="https://user-images.githubusercontent.com/33650498/115184512-d8ecd080-a092-11eb-8dd4-b25d66e617ba.png">

#### Post Table
A view of the post data table

<img width="1626" alt="my_weight_post_tb" src="https://user-images.githubusercontent.com/33650498/115184549-e5712900-a092-11eb-912b-6cb1ce8ae4c9.png">

Relevant code snip for database:
``` SQL
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  goalweight TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  weight TEXT NOT NULL,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
```

#### User Page
A view of UI for the user page in which the user can view and edit their entries. 

![my_weight_user](https://user-images.githubusercontent.com/33650498/115184579-f1f58180-a092-11eb-9265-7ea21237c6c8.jpg)

Relevant code snip for GET request

```Python
@bp.route('/user/<int:id>/posts')
def get_all_user_posts(id):
  """
  get all of the posts by user
  :param id: user id
  :return: data as json
  """ 

  # return all posts
  db = get_db()
  posts = db.execute(
      'SELECT p.id, weight, body, created, author_id, username, goalweight'
      ' FROM post p JOIN user u ON p.author_id = u.id'
      ' WHERE u.id = ?'
      ' ORDER BY created DESC',
      (id,)
  ).fetchall()

  # data = json.dumps(tuple(post), indent=4, sort_keys=True, default=str)
  data = json.dumps(posts)

  return data
```

```JavaScript
/**
 * Display all of the logged in user's post
 */
function displayUserPosts() {
  // get the data
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", 'http://127.0.0.1:5000/user/'+userId+'/posts', false ); // false for synchronous request
  // xmlHttp.open( "GET", 'http://127.0.0.1:5000/test/2/posts', false ); // false for synchronous request
  xmlHttp.send( null );

  var data = JSON.parse(xmlHttp.responseText);

  // build the post display
  buildUserPostHTML(data);
}
```

#### Community Page!
The layout for displaying community posts when not logged in. Users can find motivation and encouragment through watching others pursuing their goals. 

<img width="1375" alt="my_weight_community" src="https://user-images.githubusercontent.com/33650498/115184661-2bc68800-a093-11eb-9564-e16b2d7a1b25.png">

Relevant code snips:

```Python
@bp.route('/posts')
def get_all_posts():
  """
  get all the posts from the database 
  :return: json data
  """ 

  # return all posts
  db = get_db()
  posts = db.execute(
      'SELECT p.id, weight, body, created, author_id, username, goalWeight'
      ' FROM post p JOIN user u ON p.author_id = u.id'
      ' ORDER BY created DESC'
  ).fetchall()

  data = json.dumps(posts)

  return data
```

```JavaScript
/**
 * Display all the posts in the database
 */
function displayPosts() {
  // get the data
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", 'http://127.0.0.1:5000/posts', false ); // false for synchronous request
  // xmlHttp.open( "GET", 'http://127.0.0.1:5000/test/2/posts', false ); // false for synchronous request
  xmlHttp.send( null );

  var data = JSON.parse(xmlHttp.responseText);

  // build the post display
  buildPostHTML(data);
}
```
