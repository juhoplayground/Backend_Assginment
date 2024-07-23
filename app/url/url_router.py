from app.redis.redis_client import RedisClient
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import status,  APIRouter, status
from pydantic import BaseModel
from datetime import datetime
import hashlib

url_router = APIRouter(tags=['url'])

class UrlDefintion(BaseModel):
    url: str
    input_datetime_str: str | None = None


@url_router.post('/shorten', summary='입력받은 긴 URL을 고유한 단축 키로 변환하고 데이터베이스에 저장', include_in_schema=True)
async def make_shorten(url:UrlDefintion):
    try:
        url_bytes = url.url.encode('utf-8')
        sha256 = hashlib.sha256(b'MementoAI')
        sha256.update(url_bytes)
        short_url = sha256.hexdigest()
        
        time_diff = None
        if url.input_datetime_str:
            input_datetime = datetime.strptime(url.input_datetime_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_diff = input_datetime - now
            if time_diff.total_seconds() < 0:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': '만료 기간은 미래 시점으로 입력 해야함'})
        r = RedisClient()
        r.set_value(key=short_url, value=url.url, timeout=time_diff)

        return JSONResponse(status_code=status.HTTP_200_OK, content={'short_url': short_url})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': f'오류 발생 {e}'})
        
    
@url_router.get("/{short_key}", summary='단축된 키를 통해 원본 URL로 리디렉션', include_in_schema=True)
async def get_url(short_key: str):
    try:
        r = RedisClient()
        url = r.get_value(short_key)
        r.set_statistics(f'{short_key}_stat')
        if url:
            return RedirectResponse(url=url, status_code=status.HTTP_301_MOVED_PERMANENTLY)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'HTTP_404_NOT_FOUND'})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': f'오류 발생 {e}'})
    
    
@url_router.get("/stats/{short_key}", summary='각 단축 키의 조회 수를 추적하고 이를 반환', include_in_schema=True)
async def get_url(short_key: str):
    try:
        r = RedisClient()
        stat = r.get_value(f'{short_key}_stat')
       
        if stat:
            return JSONResponse(status_code=status.HTTP_200_OK, content={'message': f'해당 URL의 조회 수 {stat}'})
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'HTTP_404_NOT_FOUND'})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': f'오류 발생 {e}'})