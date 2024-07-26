# Backend_Assginment 프로젝트에 대한 설명

# 설치 방법 
1) redis 설치 방법
```
sudo apt install lsb-release curl gpg

curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```
<br/>

`sudo vi redis/redis.conf`에서 `requirepass` 주석을 지우고 원하는 비밀번호를 설정 <br/>

<br/>
2) python 패키지 설치 방법 <br/>

`pip install -r requirements.txt` 로 패키지 설치 <br/>
<br/>
# 실행 방법
`main.py` 파일이 위치한 곳에 `.env` 파일을 생성<br/>
`.env'파일은 아래와 같이 작성 <br/>
```
REDIS_HOST='{your redis host}'
REDIS_PORT='{your redis port}'
REDIS_PASSWORD='{your redis password}'
REDIS_DB='{your db name}'
```
터미널에서 `nohup python main.py`를 실행하여 fastapi 서버 실행
<br/>
# 데이터베이스를 왜 Redis로 선택하였는가?
1) 확장성<br/>
 - 클러스터링 기능을 통해 다수의 노드에 분산시켜 처리 가능<br/>
 - 인메모리 데이터 저장소로 빠른 읽기 및 쓰기 속도를 제공<br/>
 - 대규모 트래픽을 효율적으로 처리 가능<br/>
2) 애플리케이션의 특성<br/>
 - 원본 URL <-> 짧은 URL 형태의 데이터로 Key-Value 형태의 데이터<br/>
 - 만료 기능, 통계 기능 구현이 용이<br/>
3) 관리의 용이성<br/>
 - 설치, 설정이 간단<br/>
 - 다양한 명령어와 관리도구<br/>
<br/>
# 테스트 코드 실행하는 방법
`pytest -v test.py`를 터미널에서 입력하여 테스트 코드를 실행하고 결과 확인 가능
<br/>
# Swagger 확인하는 방법
`http://localhost:8000/docs`에서 Swagger 문서 확인 가능