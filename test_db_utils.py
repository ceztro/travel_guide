import unittest
from flask import Flask
from db_utils import db, Post

class TestPostModel(unittest.TestCase):
    
    def setUp(self):
        """Set up a test Flask app and database."""
        # Create a Flask application configured for testing
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Bind the Flask app and the SQLAlchemy object
        db.init_app(self.app)
        
        # Create all tables in the test database
        with self.app.app_context():
            db.create_all()
        
        # Set up a testing client
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up the test database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        """Test creating a new Post."""
        with self.app.app_context():
            # Create a new post
            new_post = Post(title="Test Post", content="This is a test post.")
            db.session.add(new_post)
            db.session.commit()

            # Retrieve the post
            post = Post.query.first()
            self.assertIsNotNone(post)
            self.assertEqual(post.title, "Test Post")
            self.assertEqual(post.content, "This is a test post.")

    def test_update_post(self):
        """Test updating a Post."""
        with self.app.app_context():
            # Create a new post
            post = Post(title="Original Post", content="Original content.")
            db.session.add(post)
            db.session.commit()

            # Update the post
            post.title = "Updated Post"
            post.content = "Updated content."
            db.session.commit()

            # Retrieve the post
            updated_post = Post.query.first()
            self.assertEqual(updated_post.title, "Updated Post")
            self.assertEqual(updated_post.content, "Updated content.")

    def test_delete_post(self):
        """Test deleting a Post."""
        with self.app.app_context():
            # Create a new post
            post = Post(title="Post to delete", content="Content to delete.")
            db.session.add(post)
            db.session.commit()

            # Delete the post
            db.session.delete(post)
            db.session.commit()

            # Ensure the post is deleted
            deleted_post = Post.query.first()
            self.assertIsNone(deleted_post)

    def test_read_posts(self):
        """Test reading posts."""
        with self.app.app_context():
            # Create two new posts
            post1 = Post(title="Post 1", content="Content 1")
            post2 = Post(title="Post 2", content="Content 2")
            db.session.add_all([post1, post2])
            db.session.commit()

            # Retrieve all posts
            posts = Post.query.all()
            self.assertEqual(len(posts), 2)
            self.assertEqual(posts[0].title, "Post 1")
            self.assertEqual(posts[1].title, "Post 2")

if __name__ == '__main__':
    unittest.main()