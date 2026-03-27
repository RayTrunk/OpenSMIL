import logging
from sqlmodel import Session, select
from app.core.db import engine, init_db
from app.models.user import User, UserCreate, UserRole
from app.core.security import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_admin_user(session: Session) -> None:
    user = session.exec(select(User).where(User.username == "admin")).first()
    if not user:
        admin_user = User(
            username="admin",
            email="admin@opensmil.local",
            full_name="Administrator",
            hashed_password=get_password_hash("admin"), # Change this in production!
            role=UserRole.ADMIN,
            is_active=True,
        )
        session.add(admin_user)
        session.commit()
        logger.info("Admin user created")
    else:
        logger.info("Admin user already exists")

def main() -> None:
    logger.info("Creating initial data")
    init_db()
    with Session(engine) as session:
        create_admin_user(session)
    logger.info("Initial data created")

if __name__ == "__main__":
    main()
