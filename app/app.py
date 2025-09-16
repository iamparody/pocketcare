"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from app.states.auth_state import AuthState
from app.pages.sign_in import sign_in
from app.pages.sign_up import sign_up
from app.pages.dashboard import dashboard
from app.pages.profile import profile
from app.pages.subscription import subscription
from app.pages.reports import reports
from app.pages.ai_chat import ai_chat
from app.pages.journaling import journaling_page
from app.pages.admin_dashboard import admin_dashboard

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.database import init_db
from app.pages.peer_chat import peer_chat

init_db()
app.add_page(dashboard, route="/", on_load=AuthState.check_auth)
app.add_page(sign_in, route="/sign-in")
app.add_page(sign_up, route="/sign-up")
app.add_page(profile, route="/profile", on_load=AuthState.check_auth)
app.add_page(subscription, route="/subscription", on_load=AuthState.check_auth)
app.add_page(reports, route="/reports", on_load=AuthState.check_auth)
app.add_page(ai_chat, route="/ai-chat", on_load=AuthState.check_auth)
app.add_page(peer_chat, route="/peer-chat", on_load=AuthState.check_auth)
app.add_page(journaling_page, route="/journaling", on_load=AuthState.check_auth)
app.add_page(
    admin_dashboard, route="/admin-dashboard", on_load=AuthState.check_admin_auth
)