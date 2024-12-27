**Blog Platform API**

This is a FastAPI-based backend for a Blog Platform with features for user authentication, post management, and comment management. Users can create, update, delete, and view posts and comments. The API also supports liking comments and viewing user-specific data like post and comment counts.

**Features**

**User Authentication:**
User Registration (Signup)
User Login
User Details (including number of posts and likes)

**Post Management:**
Create a Post
Get All Posts
Get Post by ID
Update a Post (Fully or Partially)
Delete a Post
Search Posts by Title

**Comment Management:**
Create a Comment on a Post
Get All Comments for a Post
Update a Comment
Delete a Comment
Get All Comments by a User
Like a Comment

**Technologies**
FastAPI: For building the RESTful API.
SQLAlchemy: ORM for database interactions.
PostgreSQL: Database for storing data.
Pydantic: Data validation and serialization.
JWT (JSON Web Tokens): For user authentication.
Passlib: For password hashing and verification.
SQLAlchemy Mixin: For handling timestamps (created_at, updated_at).

Models and Schemas
**1. User Model (Database)**
Fields:
id: Integer (Primary Key)
username: String (Unique)
email: String (Unique)
hashed_password: String (Password stored securely)

**Relationships:**
A user can have many posts and comments.

**2. Post Model (Database)**
Fields:
id: Integer (Primary Key)
title: String
content: String
author_id: Integer (Foreign Key to User)
**Relationships:**
A post is associated with one user (author).
A post can have many comments.

**3. Comment Model (Database)**
Fields:
id: Integer (Primary Key)
content: String
likes: Integer (Default: 0)
post_id: Integer (Foreign Key to Post)
author_id: Integer (Foreign Key to User)

**Relationships:**
A comment is associated with one post and one user (author).

**4. TimeStamp Mixin**
Adds created_at and updated_at fields to models to track the creation and update timestamps.

**5. Pydantic Schemas**
UserCreate: For user registration (username, email, password).

UserLogin: For user login (username, password).

UserResponse: For returning user details (id, username, email, created_at).

UserDetails: For returning user statistics (posts_count, total_likes).

PostCreate: For creating a post (title, content).

PostUpdate: For updating a post (title, content).

PostResponse: For returning post details (id, title, content, created_at, updated_at).

CommentCreate: For creating a comment (content).

CommentUpdate: For updating a comment (content).

CommentResponse: For returning comment details (id, author_id, likes, created_at, updated_at).

**Routes and Endpoints
Authentication Routes**
POST /auth/signup: Registers a new user.
POST /auth/login: Logs in a user and returns a JWT token.
GET /auth/user-details: Returns the details of the current user, including their post count and total likes.
Post Routes
POST /post/create-post: Creates a new post.
GET /post/: Retrieves all posts with pagination (skip, limit).
GET /post/{post_id}: Retrieves a specific post by ID.
GET /post/title/search: Search for posts by title with pagination (skip, limit).
PUT /post/update/{post_id}: Updates an existing post by ID.
DELETE /post/delete/{post_id}: Deletes a post by ID.

**Comment Routes**
POST /comment/{post_id}: Creates a new comment on a post.
GET /comment/getcomments/{post_id}: Retrieves all comments for a specific post with pagination (skip, limit).
PUT /comment/{comment_id}: Updates an existing comment by ID.
DELETE /comment/{comment_id}: Deletes a comment by ID.
GET /comment/user-comments: Retrieves all comments made by the current user.
PATCH /comment/likes/{comment_id}: Likes a comment.



This API uses JWT tokens for authentication. Upon logging in, a user receives an access_token which must be included in the Authorization header of each request as a bearer token.
Login Example:
{
    "username": "example_user",
    "password": "password123"
}

Authorization Header:
Authorization: Bearer <access_token>

Database Setup
Install dependencies:
Install PostgreSQL and create a database.

Install the required Python packages:
pip install -r requirements.txt

Database Migration:
Use SQLAlchemy to create the tables:
python manage.py migrate


Run the FastAPI Server:
Start the server:
**uvicorn main:app --reload**

Example Usage:

**Register a new user:**
POST /auth/signup

Content-Type: application/json

{
    "username": "new_user",
    "email": "newuser@example.com",
    "password": "password123"
}

**Log in with credentials:**

POST /auth/login

Content-Type: application/json

{
    "username": "new_user",
    "password": "password123"
}

**Create a post:**
POST /post/create-post

Authorization: Bearer <your_access_token>

Content-Type: application/json

{
    "title": "My First Post",
    "content": "This is the content of the post."
}

**Create a comment on a post:**

POST /comment/{post_id}
Authorization: Bearer <your_access_token>
Content-Type: application/json
{
    "content": "This is a comment."
}
