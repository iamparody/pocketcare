import reflex as rx
from app.components.sign_in_card import sign_in_card


def sign_in():
    return rx.el.div(
        sign_in_card(),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 p-4",
    )