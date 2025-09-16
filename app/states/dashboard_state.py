import reflex as rx
import random


class DashboardState(rx.State):
    sidebar_open: bool = True
    languages: list[str] = ["English", "Swahili", "Sheng"]
    motivational_tips: list[str] = [
        "Your feelings are valid. Don't let anyone tell you otherwise.",
        "It's okay not to be okay. Seeking help is a sign of strength.",
        "Small progress is still progress. Be proud of every step you take.",
        "You are not alone. Many people are going through similar struggles.",
        "Be kind to your mind. Practice self-compassion.",
    ]

    @rx.var
    def current_tip(self) -> str:
        return random.choice(self.motivational_tips)

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open