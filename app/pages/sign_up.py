import reflex as rx
from app.components.sign_up_card import sign_up_card


def sign_up():
    return rx.el.div(
        sign_up_card(),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 p-4",
    )