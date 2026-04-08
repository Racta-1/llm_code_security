from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Database Setup
Base = declarative_base()
engine = create_engine("sqlite:///:memory:")  # In-memory for demonstration
Session = sessionmaker(bind=engine)
session = Session()

# 2. Define the User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(String)
    email = Column(String)

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"

# Initialize database and seed data
Base.metadata.create_all(engine)
session.add_all([
    User(username="alice", role="admin", email="alice@example.com"),
    User(username="bob", role="user", email="bob@example.com"),
    User(username="charlie", role="admin", email="charlie@example.com"),
])
session.commit()

# 3. The search_users Function
def search_users(filters: dict):
    """
    Dynamically filters users based on provided dictionary keys.
    """
    query = session.query(User)
    
    for attr, value in filters.items():
        # check if the User model actually has the attribute to avoid errors
        if hasattr(User, attr):
            query = query.filter(getattr(User, attr) == value)
            
    return query.all()

# --- Example Usage ---
if __name__ == "__main__":
    # Test 1: Multiple filters
    print("Searching for admins named Alice:")
    results = search_users({"username": "alice", "role": "admin"})
    print(results)

    # Test 2: Single filter
    print("\nSearching for all admins:")
    admins = search_users({"role": "admin"})
    for user in admins:
        print(f" - {user.username}")

    # Test 3: No results
    print("\nSearching for non-existent user:")
    none_found = search_users({"username": "eve"})
    print(none_found)