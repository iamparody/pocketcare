import reflex as rx
from typing import TypedDict
from app.database import get_db, Journal, JournalBadge
from app.states.auth_state import AuthState
import datetime


class JournalEntry(TypedDict):
    id: int
    content: str
    mood: str
    created_at: str
    is_special: bool


class Badge(TypedDict):
    id: int
    badge_name: str
    awarded_at: str


class JournalState(rx.State):
    journal_entries: list[JournalEntry] = []
    badges: list[Badge] = []
    current_mood: str = "Neutral"
    mood_options: list[str] = ["Happy", "Sad", "Anxious", "Calm", "Excited", "Neutral"]
    is_special_journaling: bool = False
    special_journal_id: int | None = None

    @rx.event(background=True)
    async def load_journal_data(self):
        async with self:
            auth_state = await self.get_state(AuthState)
            if not auth_state.logged_in_user_id:
                return
            user_id = auth_state.logged_in_user_id
        with get_db() as db:
            entries = (
                db.query(Journal)
                .filter(Journal.user_id == user_id)
                .order_by(Journal.created_at.desc())
                .all()
            )
            user_badges = (
                db.query(JournalBadge)
                .filter(JournalBadge.user_id == user_id)
                .order_by(JournalBadge.awarded_at.desc())
                .all()
            )
            active_special_session = (
                db.query(Journal)
                .filter(
                    Journal.user_id == user_id,
                    Journal.is_special == True,
                    Journal.end_time == None,
                )
                .order_by(Journal.start_time.desc())
                .first()
            )
            async with self:
                self.journal_entries = [
                    {
                        "id": entry.id,
                        "content": entry.content,
                        "mood": entry.mood,
                        "created_at": entry.created_at.strftime("%Y-%m-%d %H:%M"),
                        "is_special": entry.is_special,
                    }
                    for entry in entries
                ]
                self.badges = [
                    {
                        "id": badge.id,
                        "badge_name": badge.badge_name,
                        "awarded_at": badge.awarded_at.strftime("%Y-%m-%d"),
                    }
                    for badge in user_badges
                ]
                if active_special_session:
                    self.is_special_journaling = True
                    self.special_journal_id = active_special_session.id
                else:
                    self.is_special_journaling = False
                    self.special_journal_id = None

    @rx.event(background=True)
    async def save_entry(self, form_data: dict):
        content = form_data.get("content")
        async with self:
            mood = self.current_mood
            if not content:
                yield rx.toast.error("Journal entry cannot be empty.")
                return
            auth_state = await self.get_state(AuthState)
            if not auth_state.logged_in_user_id:
                yield rx.toast.error("You must be logged in to save an entry.")
                return
            is_special = self.is_special_journaling
        with get_db() as db:
            new_entry = Journal(
                user_id=auth_state.logged_in_user_id,
                content=content,
                mood=mood,
                is_special=is_special,
            )
            db.add(new_entry)
            db.commit()
        yield rx.toast.success("Journal entry saved!")
        yield JournalState.load_journal_data

    @rx.event(background=True)
    async def start_special_journal(self):
        async with self:
            auth_state = await self.get_state(AuthState)
            if not auth_state.logged_in_user_id:
                return
            user_id = auth_state.logged_in_user_id
        with get_db() as db:
            new_special_entry = Journal(
                user_id=user_id,
                content="Special journaling session started.",
                mood="Special Session",
                is_special=True,
                start_time=datetime.datetime.utcnow(),
            )
            db.add(new_special_entry)
            db.commit()
            db.refresh(new_special_entry)
            async with self:
                self.special_journal_id = new_special_entry.id
                self.is_special_journaling = True
        yield rx.toast.info("Special journaling session started.")
        yield JournalState.load_journal_data

    @rx.event(background=True)
    async def end_special_journal(self):
        async with self:
            if not self.special_journal_id:
                yield rx.toast.info("No active special journaling session to end.")
                return
            special_id = self.special_journal_id
        with get_db() as db:
            entry = db.query(Journal).filter(Journal.id == special_id).first()
            if entry and entry.start_time and (not entry.end_time):
                entry.end_time = datetime.datetime.utcnow()
                duration_seconds = (entry.end_time - entry.start_time).total_seconds()
                duration_minutes = round(duration_seconds / 60, 2)
                db.commit()
                msg = f"Special journaling session ended. Duration: {duration_minutes} minutes."
                async with self:
                    self.is_special_journaling = False
                    self.special_journal_id = None
            else:
                msg = "Could not find special journal session to end."
                async with self:
                    self.is_special_journaling = False
                    self.special_journal_id = None
        yield rx.toast.info(msg)
        yield JournalState.load_journal_data