import reflex as rx
import os
import google.generativeai as genai
import logging
from app.states.auth_state import AuthState
from dotenv import load_dotenv
load_dotenv()


class ChatMessage(rx.Base):
    role: str
    message: str


class ChatState(rx.State):
    chats: dict[str, list[ChatMessage]] = {}
    current_user_message: str = ""

    @rx.var
    async def current_chat(self) -> list[ChatMessage]:
        auth = await self.get_state(AuthState)
        if auth.logged_in_user:
            return self.chats.get(auth.logged_in_user, [])
        return []

    @rx.event(background=True)
    async def send_message(self, form_data: dict):
        message_text = form_data.get("user_message", "").strip()
        if not message_text:
            return
        async with self:
            auth = await self.get_state(AuthState)
            if not auth.logged_in_user:
                return
            user_message = ChatMessage(role="user", message=message_text)
            self.chats.setdefault(auth.logged_in_user, []).append(user_message)
            self.current_user_message = ""
            user_profile = auth.current_user_data
            logged_in_user = auth.logged_in_user
        yield
        try:
            if not user_profile:
                raise ValueError("User profile not found.")
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"You are a mental health assistant named Serenity. The user you are talking to is {user_profile.get('age', 'N/A')} years old, identifies as {user_profile.get('gender', 'N/A')}. Here is their profile information: Name: {user_profile.get('name', 'N/A')}, Bio: {user_profile.get('bio', 'N/A')}, Interests: {user_profile.get('interests', 'N/A')}. Please tailor your responses to be supportive and relevant to their profile. User message: {message_text}"
            response = await model.generate_content_async(prompt)
            ai_message = ChatMessage(role="ai", message=response.text)
            async with self:
                self.chats[logged_in_user].append(ai_message)
        except Exception as e:
            logging.exception(f"Error getting AI response: {e}")
            ai_message = ChatMessage(
                role="ai",
                message="Error: Could not get a response. Please try again later.",
            )
            async with self:
                self.chats[logged_in_user].append(ai_message)