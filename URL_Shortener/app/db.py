from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ------------------------------------------
# DATABASE CONFIGURATION AND SETUP
# ------------------------------------------

# Define the database connection URL.
# Here, SQLite is used, and the database file is named 'test.db'.
# The "sqlite:///" prefix specifies the SQLite database.

DATABASE_URL = "sqlite:///./test.db"

# Create the SQLAlchemy Engine.
# The engine is responsible for establishing a connection to the database.
# - `connect_args={"check_same_thread": False}`:
#   Required for SQLite when used with multiple threads, ensuring proper connection handling.

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class.
# `sessionmaker` is a factory for creating database session instances.
# - `autocommit=False`: Transactions won't be committed automatically.
# - `autoflush=False`: Data won't be flushed to the database automatically before queries.
# - `bind=engine`: Associates the session with the previously created engine.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for ORM models.
# All database models will inherit from this class, enabling SQLAlchemy to map models to database tables.

Base = declarative_base()