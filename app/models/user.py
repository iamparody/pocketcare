from typing import TypedDict


class UserProfile(TypedDict):
    username: str
    role: str
    pseudonym: str
    age: int | None
    gender: str | None
    interests: str | None
    bio: str | None
    completed: bool
    subscription_plan: str
    subscription_status: str