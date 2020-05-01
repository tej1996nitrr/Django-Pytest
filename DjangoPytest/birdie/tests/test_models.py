from mixer.backend.django import mixer
import pytest
pytestmark= pytest.mark.django_db

class TestPost:
    def test_model(self):
        obj = mixer.blend('birdie.Post')
        assert obj.pk ==1,'Should create a post instance'
    
    
