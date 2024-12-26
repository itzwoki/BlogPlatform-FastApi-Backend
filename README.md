Blog Platform

Overview

The Blog Platform is a web application built using FastAPI for the backend, with PostgreSQL as the database for storing posts, comments, and user data. This platform allows users to register, login, and manage blog posts and comments, with features for creating, updating, deleting, searching posts, and commenting on them.

Features

- User Authentication: Users can register and log in using JWT-based authentication.
- Post Management: Users can create, read, update, delete, and search blog posts.
- Commenting System: Users can comment on posts, update or delete their own comments.
- Authorization: Only authenticated users can perform actions like creating, updating, or deleting posts and comments. Users can only modify their own posts and comments.
- Pagination: Blog posts and comments are paginated for better performance and user experience.
- Search: Users can search for blog posts by title.

Routes

Authentication Routes

1. POST /signup  
   - Register a new user.  
   - Body: { "username": "example", "email": "example@mail.com", "password": "password" }  
   - Response: 201 Created

2. POST /login  
   - Login and receive a JWT token.  
   - Body: { "username": "example", "password": "password" }  
   - Response: { "access_token": "jwt_token", "token_type": "bearer" }

3. GET /user/me  
   - Get the current logged-in user's information.  
   - Authorization: Bearer token  
   - Response: User details (ID, username, email, etc.)

Post Routes

1. POST /post/create  
   - Create a new blog post.  
   - Body: { "title": "My New Post", "content": "Post content here..." }  
   - Authorization: Bearer token  
   - Response: Post details (ID, title, content)

2. GET /posts  
   - Get a list of all blog posts, with pagination.  
   - Query Params: skip (default: 0), limit (default: 10)  
   - Response: List of posts

3. GET /post/{post_id}  
   - Get a single blog post by ID.  
   - Response: Post details (ID, title, content)

4. PUT /post/update/{post_id}  
   - Update an existing blog post.  
   - Body: { "title": "Updated Title", "content": "Updated content" }  
   - Authorization: Bearer token  
   - Response: Updated post details

5. DELETE /post/delete/{post_id}  
   - Delete a blog post.  
   - Authorization: Bearer token  
   - Response: Success message (e.g., "Post with ID: 1 deleted.")

6. GET /posts/search  
   - Search for blog posts by title.  
   - Query Params: title, skip, limit  
   - Response: List of matching posts

Comment Routes

1. POST /post/{post_id}/comment/create  
   - Create a comment on a blog post.  
   - Body: { "content": "This is a comment." }  
   - Authorization: Bearer token  
   - Response: Comment details (ID, content, post ID, author)

2. GET /post/{post_id}/comments  
   - Get all comments for a specific blog post, with pagination.  
   - Query Params: skip, limit  
   - Response: List of comments for the post

3. PUT /comment/update/{comment_id}  
   - Update an existing comment.  
   - Body: { "content": "Updated comment content" }  
   - Authorization: Bearer token  
   - Response: Updated comment details

4. DELETE /comment/delete/{comment_id}  
   - Delete a comment.  
   - Authorization: Bearer token  
   - Response: Success message (e.g., "Comment with ID: 1 deleted.")

Technologies Used

- FastAPI: For building the backend API.
- PostgreSQL: For database management.
- JWT: For user authentication and authorization.
- SQLAlchemy: For interacting with the PostgreSQL database.
 

4. Run the application:
   uvicorn main:app --reload

5. Open your browser and navigate to http://127.0.0.1:8000 to access the API.

Testing

You can test the API using tools like Postman. Use the JWT token obtained from the login route for authenticated requests.


