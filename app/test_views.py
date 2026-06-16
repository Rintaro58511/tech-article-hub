from main.views import fetch_qiita_article
import requests

class MockResponce():
    def json(self):
        return [
            {"title" : "サプーが教えるpython", "url" : "https://example.com/sapu"},
            {"title" : "pythonで始める機械学習", "url" : "https://example.com/sklearn"}
        ]
    
def test_fetch_qiita_article_success(monkeypatch):

    def mock_get(url):
        return MockResponce()
    
    monkeypatch.setattr(requests, "get", mock_get)
    result = fetch_qiita_article("python")
    assert result == [
        {"title" : "サプーが教えるpython", "url" : "https://example.com/sapu"},
        {"title" : "pythonで始める機械学習", "url" : "https://example.com/sklearn"}
    ]

def test_fetch_qiita_article_error(monkeypatch):

    def mock_get(url):
        raise requests.exceptions.ConnectionError 
       
    monkeypatch.setattr(requests, "get", mock_get)
    assert fetch_qiita_article("python") is None
