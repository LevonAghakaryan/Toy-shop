from pydantic_settings import BaseSettings
from urllib.parse import quote_plus


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    # ԱՎԵԼԱՑՎԱԾ: Admin-ի կրեդենցիալներ
    admin_username: str = "admin"
    admin_password: str
    admin_secret_key: str = "your-secret-key-here"
    class Config:
        env_file = ".env"

    @property
    def database_url(self):
        """Generates the database URL with a properly encoded password."""
        encoded_password = quote_plus(self.db_password)
        return f"mysql+pymysql://{self.db_user}:{encoded_password}@{self.db_host}/{self.db_name}"


settings = Settings()