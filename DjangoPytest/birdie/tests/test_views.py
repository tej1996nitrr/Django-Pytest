from django.test import RequestFactory 
from .. import views
import pytest
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.http import Http404
pytestmark = pytest.mark.django_db

class TestHomeView:
    def test_anonymous(self):
        req = RequestFactory().get('/')
        resp = views.HomeView.as_view()(req)
        assert resp.status_code==200,'Should be callable by anyone'

class TestAdminView:
    def test_anonymous(self):
        req  =RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = views.AdminView.as_view()(req)
        assert 'login' in resp.url
    def test_superuser(self):
        user = mixer.blend('auth.User', is_superuser=True)
        req = RequestFactory().get('/')
        req.user = user
        resp = views.AdminView.as_view()(req)
        assert resp.status_code == 200, 'Authenticated User can access'

class TestPostUpdateView:
    def test_get(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        obj = mixer.blend('birdie.Post')
        resp = views.PostUpdateView.as_view()(req, pk=obj.pk)
        assert resp.status_code==200,'Should be callable'
    
    def test_post(self):
        post = mixer.blend('birdie.Post')
        data = {'body':'New Body Text!!'}
        req = RequestFactory().post('/',data=data)
        req.user = AnonymousUser()
        resp = views.PostUpdateView.as_view()(req, pk=post.pk)
        assert resp.status_code == 302, 'Should redirect to success view'
        post.refresh_from_db()
        assert post.body=='New Body Text!!', 'Should update the post'

    def test_security(self):
        user = mixer.blend('auth.User',first_name='Python')
        post = mixer.blend('birdie.Post')
        req = RequestFactory().post('/',data={})
        req.user=user
        with pytest.raises(Http404):
            views.PostUpdateView.as_view()(req,pk=post.pk)
            
