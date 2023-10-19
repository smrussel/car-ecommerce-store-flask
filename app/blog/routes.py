from flask import Blueprint, render_template, flash, \
                redirect, url_for, request, session
from app.models import Blog


blogs = Blueprint('blogs', __name__)


@blogs.route('/blogs')
def all_blogs():
    posts = Blog.query.all()
    return render_template('blog/all-blogs.html', posts=posts)


@blogs.route('/blog-detail/<int:post_id>')
def blog_detail(post_id):
    post = Blog.query.get_or_404(post_id)
    return render_template('blog/blog-detail.html', post=post)
