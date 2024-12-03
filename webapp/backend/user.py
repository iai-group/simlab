"""User."""

from __future__ import annotations

from typing import Any, Dict, Union

from bson import ObjectId
from flask_login import UserMixin


class User(UserMixin):
    def __init__(
        self,
        id: Union[str, ObjectId],
        username: str,
        email: str,
    ) -> None:
        """Initializes a new user.

        Args:
            id: User id.
            username: Username.
            email: Email.
        """
        super().__init__()
        self._id = id if isinstance(id, str) else str(id)
        self.username = username
        self.email = email

    def get_id(self) -> str:
        """Returns the user id."""
        return self._id

    @property
    def id(self) -> str:
        """Returns the user id."""
        return self._id

    @staticmethod
    def from_mongo_document(document: Dict[str, Any]) -> User:
        """Creates a new user from a MongoDB document.

        Args:
            document: MongoDB document.

        Raises:
            ValueError: If the document is missing required fields.

        Returns:
            User.
        """
        if not all(
            field in document for field in ["_id", "username", "email"]
        ):
            raise ValueError(
                "Invalid document, the fields: _id, username, email are "
                "required."
            )

        return User(
            document.get("_id"),
            document.get("username"),
            document.get("email"),
        )
