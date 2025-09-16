import reflex as rx
from app.states.auth_state import AuthState
from app.database import get_db, PeerQueue, PeerChat, ChatMessage
import uuid
import time


class PeerChatState(rx.State):
    queue_status: str = "idle"
    queue_position: int = 0
    chat_room_id: str | None = None
    current_chat_messages: list[dict] = []
    last_match_user_id: int | None = None

    @rx.var
    def in_chat(self) -> bool:
        return self.chat_room_id is not None

    @rx.event
    async def request_support(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.logged_in_user_id:
            return rx.toast.error("You must be logged in.")
        self.queue_status = "waiting"
        with get_db() as db:
            in_queue = (
                db.query(PeerQueue)
                .filter(PeerQueue.user_id == auth_state.logged_in_user_id)
                .first()
            )
            if not in_queue:
                new_queue_entry = PeerQueue(
                    user_id=auth_state.logged_in_user_id,
                    pseudonym=auth_state.current_user_data["pseudonym"],
                )
                db.add(new_queue_entry)
                db.commit()
        return PeerChatState.check_for_match

    @rx.event(background=True)
    async def check_for_match(self):
        while True:
            async with self:
                if self.queue_status != "waiting":
                    return
                auth_state = await self.get_state(AuthState)
                my_id = auth_state.logged_in_user_id
                my_pseudonym = auth_state.current_user_data["pseudonym"]
            with get_db() as db:
                waiting_peers = (
                    db.query(PeerQueue)
                    .filter(PeerQueue.status == "waiting", PeerQueue.user_id != my_id)
                    .order_by(PeerQueue.requested_at)
                    .all()
                )
                match_found = False
                for peer in waiting_peers:
                    if peer.user_id == self.last_match_user_id:
                        continue
                    room_id = str(uuid.uuid4())
                    new_chat = PeerChat(
                        room_id=room_id,
                        user1_pseudonym=my_pseudonym,
                        user2_pseudonym=peer.pseudonym,
                    )
                    db.add(new_chat)
                    my_queue_entry = (
                        db.query(PeerQueue).filter(PeerQueue.user_id == my_id).first()
                    )
                    peer_queue_entry = (
                        db.query(PeerQueue)
                        .filter(PeerQueue.user_id == peer.user_id)
                        .first()
                    )
                    if my_queue_entry:
                        db.delete(my_queue_entry)
                    if peer_queue_entry:
                        db.delete(peer_queue_entry)
                    db.commit()
                    async with self:
                        self.queue_status = "matched"
                        self.chat_room_id = room_id
                        self.last_match_user_id = peer.user_id
                    match_found = True
                    break
                if not match_found:
                    my_pos = (
                        db.query(PeerQueue)
                        .filter(
                            PeerQueue.requested_at
                            < db.query(PeerQueue)
                            .filter(PeerQueue.user_id == my_id)
                            .first()
                            .requested_at
                        )
                        .count()
                    )
                    async with self:
                        self.queue_position = my_pos + 1
            if match_found:
                yield
                return
            yield
            time.sleep(5)

    @rx.event(background=True)
    async def poll_messages(self):
        while True:
            async with self:
                if not self.chat_room_id:
                    return
                room_id = self.chat_room_id
            with get_db() as db:
                chat = db.query(PeerChat).filter(PeerChat.room_id == room_id).first()
                if not chat or chat.status == "ended":
                    async with self:
                        self.chat_room_id = None
                        self.queue_status = "idle"
                    yield rx.toast.info("Peer has left the chat.")
                    return
                messages = (
                    db.query(ChatMessage)
                    .filter(ChatMessage.chat_id == chat.id)
                    .order_by(ChatMessage.timestamp)
                    .all()
                )
                messages_data = [
                    {"pseudonym": m.pseudonym, "message": m.message} for m in messages
                ]
                async with self:
                    if len(messages_data) > len(self.current_chat_messages):
                        self.current_chat_messages = messages_data
                        yield
            time.sleep(1)

    @rx.event
    async def send_peer_message(self, form_data: dict):
        message = form_data.get("message")
        if not message or not self.chat_room_id:
            return
        auth_state = await self.get_state(AuthState)
        pseudonym = auth_state.current_user_data["pseudonym"]
        with get_db() as db:
            chat = (
                db.query(PeerChat).filter(PeerChat.room_id == self.chat_room_id).first()
            )
            if chat:
                new_message = ChatMessage(
                    chat_id=chat.id, pseudonym=pseudonym, message=message
                )
                db.add(new_message)
                db.commit()

    @rx.event
    def leave_chat(self):
        if not self.chat_room_id:
            return
        with get_db() as db:
            chat = (
                db.query(PeerChat).filter(PeerChat.room_id == self.chat_room_id).first()
            )
            if chat:
                chat.status = "ended"
                db.commit()
        self.chat_room_id = None
        self.queue_status = "idle"
        self.current_chat_messages = []
        return rx.toast.info("You have left the chat.")

    @rx.event
    async def cancel_request(self):
        auth_state = await self.get_state(AuthState)
        with get_db() as db:
            queue_entry = (
                db.query(PeerQueue)
                .filter(PeerQueue.user_id == auth_state.logged_in_user_id)
                .first()
            )
            if queue_entry:
                db.delete(queue_entry)
                db.commit()
        self.queue_status = "idle"
        return rx.toast.info("Your support request has been cancelled.")