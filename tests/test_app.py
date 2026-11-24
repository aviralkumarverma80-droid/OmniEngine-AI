import asyncio, io, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import app as a
import httpx
from fastapi.testclient import TestClient
from pptx import Presentation

def test_local_flow(tmp_path,monkeypatch):
    monkeypatch.setattr(a,'DB',tmp_path/'test.db');a.init()
    for _,prefix,_ in a.PROVIDERS.values(): monkeypatch.setenv(prefix+'_API_KEY','')
    c=TestClient(a.app)
    assert c.get('/').status_code==200
    assert c.get('/api/providers').status_code==401
    assert c.post('/api/signup',json={'email':'test@example.com','name':'Test','password':'testpass123'}).status_code==200
    assert c.get('/api/me').json()['name']=='Test'
    assert c.get('/api/providers').json()[0]['configured']==False
    r=c.post('/api/ask-all',json={'prompt':'Hello','providers':['gemini'],'search':False}).json()
    assert r['results'][0]['status']=='error' and r['consensus']['status']=='unavailable'
    assert c.post('/api/ask-all',json={'prompt':'Hello','providers':['unknown'],'search':False}).status_code==400
    assert c.get('/api/export-pptx').status_code==200
    out=c.post('/api/export-results',json={'prompt':'Hello','consensus':'Unavailable','results':r['results']})
    assert out.status_code==200 and len(Presentation(io.BytesIO(out.content)).slides)==3
    assert c.post('/api/logout',json={}).status_code==200
    assert c.get('/api/me').status_code==401
    assert c.post('/api/login',json={'email':'test@example.com','password':'wrongpass'}).status_code==401
    assert c.post('/api/login',json={'email':'test@example.com','password':'testpass123'}).status_code==200

def test_real_adapter_contracts(monkeypatch):
    for _,prefix,_ in a.PROVIDERS.values(): monkeypatch.setenv(prefix+'_API_KEY','test-only')
    def handler(req):
        if 'googleapis' in req.url.host: return httpx.Response(200,json={'candidates':[{'content':{'parts':[{'text':'Gemini response'}]}}]})
        if 'anthropic' in req.url.host: return httpx.Response(200,json={'content':[{'type':'text','text':'Claude response'}]})
        if 'duckduckgo' in req.url.host: return httpx.Response(200,text='<div class="result"><a class="result__a" href="https://example.com">Example</a><div class="result__snippet">Example snippet</div></div>')
        return httpx.Response(200,json={'choices':[{'message':{'content':'API response'}}]})
    async def go():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as c:
            rs=await asyncio.gather(*(a.run_provider(c,k,'test') for k in a.PROVIDERS),a.web_search(c,'test'))
            assert len(rs)==6 and all(r['status']=='ok' for r in rs)
            assert rs[-1]['sources'][0]['url']=='https://example.com'
            consensus=await a.synthesize(c,'test',rs)
            assert consensus['status']=='ok' and consensus['contributors']==5
    asyncio.run(go())
