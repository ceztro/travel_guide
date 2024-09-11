from flask import Flask, render_template, request, redirect
from aws_utils import discover_rds_secret_name, get_rds_credentials, get_rds_endpoint_and_dbname
from db_utils import db, Post
import os

# Initialize the Flask application
app = Flask(__name__)

# Discover the AWS-managed RDS secret name based on the DB instance identifier
db_instance_identifier = os.getenv("DB_INSTANCE_IDENTIFIER", "travel-guide-rds")
secret_name = discover_rds_secret_name(db_instance_identifier)

# Fetch the RDS credentials (username, password) from AWS Secrets Manager
rds_credentials = get_rds_credentials(secret_name)

# Fetch the RDS endpoint (host) and DB name dynamically using boto3
rds_endpoint, db_name = get_rds_endpoint_and_dbname(db_instance_identifier)

# Set up the database URI using the credentials fetched from Secrets Manager and the dynamic RDS endpoint
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{rds_credentials['username']}:{rds_credentials['password']}@{rds_endpoint}:{rds_credentials.get('port', '5432')}/{db_name}"

# Initialize the database with SQLAlchemy
db.init_app(app)

# Create the database tables (if they don't already exist)
with app.app_context():
    db.create_all()

# Define the route for the home page
@app.route("/")
def index():
    posts = Post.query.all()  # Fetch all posts from the database
    return render_template("index.html", posts=posts)  # Render the template with posts

# Define the route to add a new post
@app.route("/add", methods=["POST"])
def add_post():
    title = request.form["title"]  # Get the title from the form
    content = request.form["content"]  # Get the content from the form
    new_post = Post(title=title, content=content)  # Create a new Post object
    db.session.add(new_post)  # Add the new post to the session
    db.session.commit()  # Commit the session to save the post to the database
    return redirect("/")  # Redirect back to the home page

# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)