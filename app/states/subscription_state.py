import reflex as rx
from app.states.auth_state import AuthState
from app.database import get_db, Subscription as SubscriptionModel
import datetime
from typing import TypedDict


class Payment(TypedDict):
    date: str
    amount: float
    plan: str
    status: str


class SubscriptionState(rx.State):
    payment_history: list[Payment] = []

    @rx.event
    async def load_history(self):
        self.payment_history = []
        auth_state = await self.get_state(AuthState)
        plan = auth_state.current_user_data["subscription_plan"]
        amount = 6.99 if plan == "Basic" else 9.99
        for i in range(3):
            self.payment_history.append(
                {
                    "date": (
                        datetime.date.today() - datetime.timedelta(days=30 * i)
                    ).isoformat(),
                    "amount": amount,
                    "plan": plan,
                    "status": "Paid",
                }
            )

    @rx.event
    async def change_plan(self, new_plan: str):
        auth_state = await self.get_state(AuthState)
        if not auth_state.logged_in_user_id:
            return rx.toast.error("You must be logged in.")
        with get_db() as db:
            subscription = (
                db.query(SubscriptionModel)
                .filter(SubscriptionModel.user_id == auth_state.logged_in_user_id)
                .first()
            )
            if subscription:
                subscription.plan_type = new_plan
                db.commit()
        if new_plan == "Plus":
            prorated_charge = 3.0
            self.payment_history.insert(
                0,
                {
                    "date": datetime.date.today().isoformat(),
                    "amount": prorated_charge,
                    "plan": "Prorated Upgrade to Plus",
                    "status": "Paid",
                },
            )
        return rx.toast.success(f"Successfully changed to {new_plan} plan!")