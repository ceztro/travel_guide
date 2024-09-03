from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Set up the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# Initialize the database with SQLAlchemy
db = SQLAlchemy(app)

# Define a model for the Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Define the route for the home page
@app.route('/')
def index():
    posts = Post.query.all()  # Fetch all posts from the database
    return render_template('index.html', posts=posts)  # Render the template with posts

# Define the route to add a new post
@app.route('/add', methods=['POST'])
def add_post():
    title = request.form['title']  # Get the title from the form
    content = request.form['content']  # Get the content from the form
    new_post = Post(title=title, content=content)  # Create a new Post object
    db.session.add(new_post)  # Add the new post to the session
    db.session.commit()  # Commit the session to save the post to the database
    return redirect('/')  # Redirect back to the home page

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
