import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.contrib.admin.sites import AdminSite
from ..models import Post
from .. import admin

class TestPostAdmin:
    def test_excerpt(self):
        site = AdminSite()
        post_admin  = admin.PostAdmin(Post, site)
        obj = mixer.blend('birdie.Post',body="Hello World")
        result = post_admin.excerpt(obj)
        assert result=="Hello","should return first few chars"
        

        