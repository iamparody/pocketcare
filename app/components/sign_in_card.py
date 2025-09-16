import reflex as rx
from app.states.auth_state import AuthState


def sign_in_card():
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Sign in to Serenity", class_name="text-2xl font-bold text-gray-800"
            ),
            rx.el.p(
                "Welcome back. Please enter your details.",
                class_name="text-sm text-gray-500 font-medium",
            ),
            class_name="flex flex-col text-center",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label("Username", class_name="text-sm font-medium leading-none"),
                rx.el.input(
                    placeholder="your-username",
                    name="username",
                    required=True,
                    class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.div(
                rx.el.label("Password", class_name="text-sm font-medium leading-none"),
                rx.el.input(
                    type="password",
                    name="password",
                    required=True,
                    class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.button(
                "Sign In",
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-blue-500 hover:bg-blue-600 h-10 px-4 py-2 w-full",
            ),
            rx.el.div(
                rx.el.span(
                    "Don't have an account?",
                    class_name="text-sm text-gray-500 font-medium",
                ),
                rx.el.a(
                    "Sign Up",
                    href="/sign-up",
                    class_name="text-sm text-blue-500 font-medium underline hover:text-blue-600 transition-colors",
                ),
                class_name="flex flex-row gap-2 justify-center mt-2",
            ),
            class_name="flex flex-col gap-4",
            on_submit=AuthState.sign_in,
            reset_on_submit=True,
        ),
        class_name="p-8 rounded-xl bg-white flex flex-col gap-6 shadow-sm border border-gray-200 text-black w-full max-w-md",
    )