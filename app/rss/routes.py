from feedwerk.atom import AtomFeed
from urllib.parse import urljoin
from app.models import Blog
from flask import request, Blueprint

rss_bp = Blueprint('rss_bp', __name__)


def get_abs_url(url):
    return urljoin(request.url_root, url)


@rss_bp.route('/feeds/')
def feeds():
    feed = AtomFeed(title='Latest Posts from Our Blog',
                    feed_url=request.url, url=request.url_root)

    posts = Blog.query.filter().all()

    for post in posts:
        feed.add(post.title, updated=post.created_at,
                 content_type='html',
                 url=get_abs_url('blog-detail/' + str(post.id)),
                 author="Admin",
                 published=post.created_at)

    return feed.get_response()
