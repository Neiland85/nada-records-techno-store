# Code Citations

## License: desconocido
[https://github.com/rafsaf/new_earthsea/blob/e4adaf5d9e2a906b55172e00fde6af7aaa457230/backend/app/api/api.py](https://github.com/rafsaf/new_earthsea/blob/e4adaf5d9e2a906b55172e00fde6af7aaa457230/backend/app/api/api.py)

```
users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router
```


## License: desconocido
[https://github.com/bareos/bareos/blob/a3f149ad3c4a07b914db48146f47f48f3554c494/rest-api/bareos-restapi.py](https://github.com/bareos/bareos/blob/a3f149ad3c4a07b914db48146f47f48f3554c494/rest-api/bareos-restapi.py)

```
.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret"
```


## License: desconocido
[https://github.com/scriptkid23/fastapi-mongodb-skeleton/blob/d24bfb878c53cb0ab337f10f3a82060306e352d7/Authentication/app/services/SecurityService.py](https://github.com/scriptkid23/fastapi-mongodb-skeleton/blob/d24bfb878c53cb0ab337f10f3a82060306e352d7/Authentication/app/services/SecurityService.py)

```
.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret"
```


## License: MIT
[https://github.com/JungeAlexander/kbase_db_api/blob/f3ec5e8b9ae509f9e8d962183efef21be61ef425/source/db_api/core/security.py](https://github.com/JungeAlexander/kbase_db_api/blob/f3ec5e8b9ae509f9e8d962183efef21be61ef425/source/db_api/core/security.py)

```
.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret"
```


## License: desconocido
[https://github.com/parth1618/python_fastapi_docker/blob/8812f3598656c3b4df7d8cea6f4600c07f495193/fastapi_service/app/api/auth_manager.py](https://github.com/parth1618/python_fastapi_docker/blob/8812f3598656c3b4df7d8cea6f4600c07f495193/fastapi_service/app/api/auth_manager.py)

```
.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret"
```

