"""Configuración global para los tests de Nada Records Techno Store."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.models.base import Base


# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la función get_db para usar la base de datos de prueba."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def engine_fixture():
    """Fixture del engine de base de datos."""
    return engine


@pytest.fixture(scope="function")
def db_session(engine_fixture):
    """Fixture de sesión de base de datos para cada test."""
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine_fixture)
    
    # Crear sesión
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Limpiar después del test
        Base.metadata.drop_all(bind=engine_fixture)


@pytest.fixture(scope="function")
def client(db_session):
    """Fixture del cliente de prueba de FastAPI."""
    from app.main import app
    
    # Override de la dependencia de DB
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpiar override
    app.dependency_overrides.clear()
