import reflex as rx
import datetime
from app.states.auth_state import AuthState
from app.database import get_db, DistressLog


class DistressState(rx.State):
    @rx.event
    async def trigger_alert(self):
        auth = await self.get_state(AuthState)
        if auth.is_authenticated and auth.logged_in_user_id:
            user_data = auth.current_user_data
            with get_db() as db:
                new_log = DistressLog(
                    user_id=auth.logged_in_user_id,
                    pseudonym=user_data.get("pseudonym", "Unknown"),
                    details="User clicked the distress button.",
                    severity="High",
                )
                db.add(new_log)
                db.commit()
            print(
                f"ADMIN NOTIFICATION: Distress signal from {user_data.get('pseudonym')}"
            )
            return rx.toast.success("Distress signal sent. An admin has been notified.")
        return rx.toast.error("You must be logged in to send a distress signal.")