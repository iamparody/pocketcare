import reflex as rx
from typing import TypedDict
from app.database import (
    get_db,
    User as UserModel,
    Profile as ProfileModel,
    Subscription as SubscriptionModel,
)
from sqlalchemy.orm import Session
import random
from app.models.user import UserProfile


class AuthState(rx.State):
    logged_in_user_id: int | None = None
    language: str = "English"
    profile_update_trigger: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.logged_in_user_id is not None

    @rx.var
    def current_user_data(self) -> UserProfile | None:
        if not self.logged_in_user_id:
            return None
        _ = self.profile_update_trigger
        with get_db() as db:
            user = (
                db.query(UserModel)
                .filter(UserModel.id == self.logged_in_user_id)
                .first()
            )
            if not user:
                return None
            profile = user.profile
            subscription = user.subscription
            return {
                "username": user.username,
                "role": user.role,
                "pseudonym": profile.pseudonym if profile else "",
                "age": profile.age if profile else None,
                "gender": profile.gender if profile else None,
                "interests": profile.interests if profile else None,
                "bio": profile.bio if profile else None,
                "completed": profile.completed if profile else False,
                "subscription_plan": subscription.plan_type
                if subscription
                else "Basic",
                "subscription_status": subscription.status if subscription else "N/A",
            }

    @rx.var
    def logged_in_user(self) -> str:
        return self.current_user_data["username"] if self.current_user_data else ""

    @rx.event
    def sign_up(self, form_data: dict):
        username = form_data["username"]
        password = form_data["password"]
        if not username or not password:
            return rx.toast.error("Username and password cannot be empty.")
        with get_db() as db:
            if db.query(UserModel).filter(UserModel.username == username).first():
                return rx.toast.error("Username already exists.")
            new_user = UserModel(username=username, password=password, role="user")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            new_profile = ProfileModel(user_id=new_user.id, completed=False)
            new_subscription = SubscriptionModel(user_id=new_user.id)
            db.add(new_profile)
            db.add(new_subscription)
            db.commit()
            self.logged_in_user_id = new_user.id
            return rx.redirect("/profile")

    @rx.event
    def sign_in(self, form_data: dict):
        username = form_data["username"]
        password = form_data["password"]
        with get_db() as db:
            user = db.query(UserModel).filter(UserModel.username == username).first()
            if user and user.password == password:
                self.logged_in_user_id = user.id
                if user.role == "admin":
                    return rx.redirect("/admin-dashboard")
                if not user.profile or not user.profile.completed:
                    return rx.redirect("/profile")
                return rx.redirect("/")
            return rx.toast.error("Invalid username or password.")

    def _generate_pseudonym(self, db: Session) -> str:
        adjectives = ["Swift", "Silent", "Clever", "Brave", "Wise", "Gentle"]
        animals = ["Fox", "Wolf", "Hawk", "Bear", "Lion", "Dove"]
        while True:
            adjective = random.choice(adjectives)
            animal = random.choice(animals)
            number = random.randint(10, 99)
            pseudonym = f"{adjective}{animal}{number}"
            if (
                not db.query(ProfileModel)
                .filter(ProfileModel.pseudonym == pseudonym)
                .first()
            ):
                return pseudonym

    @rx.event
    def update_profile(self, form_data: dict):
        if not self.logged_in_user_id:
            return rx.toast.error("You must be logged in to update your profile.")
        age = form_data.get("age")
        if not age or not 13 <= int(age) <= 100:
            return rx.toast.error("Age must be between 13 and 100.")
        if not form_data.get("gender"):
            return rx.toast.error("Gender is required.")
        if not form_data.get("interests"):
            return rx.toast.error("Please select at least one interest.")
        if len(form_data.get("interests", "").split(",")) > 5:
            return rx.toast.error("You can select a maximum of 5 interests.")
        if len(form_data.get("bio", "")) > 500:
            return rx.toast.error("Bio must be 500 characters or less.")
        with get_db() as db:
            profile = (
                db.query(ProfileModel)
                .filter(ProfileModel.user_id == self.logged_in_user_id)
                .first()
            )
            if not profile:
                return rx.toast.error("Profile not found.")
            new_pseudonym = form_data.get("pseudonym")
            if new_pseudonym != profile.pseudonym:
                if (
                    db.query(ProfileModel)
                    .filter(ProfileModel.pseudonym == new_pseudonym)
                    .first()
                ):
                    new_sugg = self._generate_pseudonym(db)
                    return rx.toast.error(f"Pseudonym already taken. Try: {new_sugg}")
                profile.pseudonym = new_pseudonym
            profile.age = int(age)
            profile.gender = form_data["gender"]
            profile.interests = form_data["interests"]
            profile.bio = form_data.get("bio", "")
            profile.completed = True
            db.commit()
        self.profile_update_trigger = not self.profile_update_trigger
        return [rx.toast.success("Profile updated successfully!"), rx.redirect("/")]

    @rx.event
    def sign_out(self):
        self.logged_in_user_id = None
        return rx.redirect("/sign-in")

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/sign-in")
        user_data = self.current_user_data
        if user_data and (not user_data["completed"]):
            if self.router.page.path != "/profile":
                return rx.redirect("/profile")

    @rx.event
    def check_admin_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/sign-in")
        user = self.current_user_data
        if not user or user.get("role") != "admin":
            return rx.redirect("/")

    @rx.event
    async def get_initial_pseudonym(self) -> str:
        with get_db() as db:
            return self._generate_pseudonym(db)