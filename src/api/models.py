from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    avatar: Mapped[str] = mapped_column(
        String(255), nullable=False, default="https://i.pravatar.cc/300")
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)
    token_version: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    todos: Mapped[list["Todos"]] = db.relationship(
        "Todos", back_populates="user", cascade="all, delete-orphan", lazy="selectin")

    # Password helpers
    def set_password(self, plaintext: str):
        self.password_hash = generate_password_hash(plaintext)

    def check_password(self, plaintext: str) -> bool:
        return check_password_hash(self.password_hash, plaintext)

    def revoke_all_tokens(self):
        # increment token_version to make existing tokens invalid if you include token_version in JWT
        self.token_version = (self.token_version or 0) + 1

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "lastname": self.lastname,
            "is_active": self.is_active,
            "avatar": self.avatar,
            # omit password_hash
        }


class Todos(db.Model):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_done: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=False)
    due_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id"), nullable=False, index=True)

    user: Mapped["User"] = db.relationship(
        "User", back_populates="todos", lazy="joined")

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "is_done": self.is_done,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "user_id": self.user_id,
        }


# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(
#         String(120), unique=True, nullable=False)
#     lastname: Mapped[str] = mapped_column(String(120), nullable=False)
#     password: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
#     avatar: Mapped[str] = mapped_column(
#         String(150), nullable=False, default="https://i.pravatar.cc/300")
#     salt: Mapped[str] = mapped_column(String(100), nullable=False, default=1)
#     created_at: Mapped[datetime] = mapped_column(
#         default=lambda: datetime.now(UTC))
#     updated_at: Mapped[datetime] = mapped_column(
#         default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

#     todos: Mapped[list["Todos"]] = db.relationship(back_populates="user")

#     def __repr__(self):
#         return f'<User {self.email}>'

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             "lastname": self.lastname,
#             "is_active": self.is_active,
#             "avatar": self.avatar,
#             # do not serialize the password, its a security breach
#             "todos": [todo.serialize() for todo in self.todos]
#         }


# class Todos(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     label: Mapped[str] = mapped_column(String(255), nullable=False)
#     is_done: Mapped[bool] = mapped_column(Boolean(), nullable=False)
#     user_id: Mapped[int] = mapped_column(
#         db.ForeignKey('user.id'), nullable=False)

#     user: Mapped["User"] = db.relationship(back_populates="todos")

#     def __repr__(self):
#         return f'<Todos {self.label}>'

#     def serialize(self):
#         return {
#             "id": self.id,
#             "label": self.label,
#             "is_done": self.is_done,
#             "user_id": self.user_id
#         }


class RevokedToken(db.Model):
    __tablename__ = "revoked_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    jti: Mapped[str] = mapped_column(
        String(120), unique=True, index=True, nullable=False)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(
        timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, nullable=False)

    def __repr__(self) -> str:
        return f"<RevokedToken jti={self.jti} expires_at={self.expires_at}>"

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "jti": self.jti,
            "revoked_at": self.revoked_at.isoformat() if self.revoked_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
