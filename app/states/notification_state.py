import reflex as rx
from app.database import get_db, Notification
from app.states.auth_state import AuthState
from typing import TypedDict
import datetime


class NotificationData(TypedDict):
    id: int
    message: str
    link: str | None
    is_read: bool
    created_at: str


class NotificationState(rx.State):
    notifications: list[NotificationData] = []
    unread_count: int = 0

    @rx.event(background=True)
    async def load_notifications(self):
        async with self:
            auth_state = await self.get_state(AuthState)
            if not auth_state.logged_in_user_id:
                return
            logged_in_user_id = auth_state.logged_in_user_id
        with get_db() as db:
            user_notifications = (
                db.query(Notification)
                .filter(Notification.user_id == logged_in_user_id)
                .order_by(Notification.created_at.desc())
                .all()
            )
            unread = (
                db.query(Notification)
                .filter(
                    Notification.user_id == logged_in_user_id,
                    Notification.is_read == False,
                )
                .count()
            )
            async with self:
                self.notifications = [
                    {
                        "id": n.id,
                        "message": n.message,
                        "link": n.link,
                        "is_read": n.is_read,
                        "created_at": n.created_at.strftime("%b %d, %H:%M"),
                    }
                    for n in user_notifications
                ]
                self.unread_count = unread

    @rx.event
    async def mark_as_read(self, notification_id: int):
        with get_db() as db:
            notification = (
                db.query(Notification)
                .filter(Notification.id == notification_id)
                .first()
            )
            if notification and (not notification.is_read):
                notification.is_read = True
                db.commit()
        yield NotificationState.load_notifications

    @rx.event
    async def mark_all_as_read(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.logged_in_user_id:
            return
        with get_db() as db:
            db.query(Notification).filter(
                Notification.user_id == auth_state.logged_in_user_id,
                Notification.is_read == False,
            ).update({"is_read": True})
            db.commit()
        yield NotificationState.load_notifications

    @staticmethod
    async def create_notification(user_id: int, message: str, link: str | None = None):
        with get_db() as db:
            new_notification = Notification(user_id=user_id, message=message, link=link)
            db.add(new_notification)
            db.commit()