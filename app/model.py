from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from app.database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts_sql"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    # it should be table name in the below line=> "user.id"
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    # it should be Class name in the below line=>
    user = relationship("User")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "vote"

    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts_sql.id", ondelete="CASCADE"), nullable=False, primary_key=True)
