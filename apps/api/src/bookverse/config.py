from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_env: str = "local"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    cors_origins: str = "*"

    db_driver: str = "postgresql+asyncpg"
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    db_user: str = "bookverse"
    db_password: str = "bookverse"
    db_name: str = "bookverse"
    db_pool_size: int = 5

    redis_url: str = "redis://127.0.0.1:6379/0"
    cache_url: str = "redis://127.0.0.1:6379/1"

    opensearch_url: str = "http://127.0.0.1:9200"
    opensearch_index_books: str = "bookverse_books"
    opensearch_index_authors: str = "bookverse_authors"

    s3_endpoint: str = "http://127.0.0.1:9000"
    s3_access_key: str = "bookverse"
    s3_secret_key: str = "bookverse"
    s3_bucket: str = "bookverse-assets"
    s3_region: str = "us-east-1"

    rate_limit_default: str = "60/minute"

    worker_concurrency: int = 4

    jwt_secret: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60


settings = Settings()
