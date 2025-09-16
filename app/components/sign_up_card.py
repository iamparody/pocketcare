import reflex as rx
from app.states.auth_state import AuthState


def sign_up_card():
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Create an Account", class_name="text-2xl font-bold text-gray-800"
            ),
            rx.el.p(
                "Join Serenity to find or offer support.",
                class_name="text-sm text-gray-500 font-medium",
            ),
            class_name="flex flex-col text-center",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label("Username", class_name="text-sm font-medium leading-none"),
                rx.el.input(
                    placeholder="choose a username",
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
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "I am a...", class_name="text-sm font-medium leading-none"
                    ),
                    rx.el.select(
                        rx.el.option("Member", value="Member"),
                        rx.el.option("Therapist", value="Therapist"),
                        name="role",
                        default_value="Member",
                        class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                    ),
                    class_name="flex flex-col gap-1.5 w-full",
                ),
                rx.el.div(
                    rx.el.label("Age", class_name="text-sm font-medium leading-none"),
                    rx.el.input(
                        type="number",
                        name="age",
                        required=True,
                        class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                    ),
                    class_name="flex flex-col gap-1.5 w-full",
                ),
                class_name="flex flex-row gap-4",
            ),
            rx.el.div(
                rx.el.label("Gender", class_name="text-sm font-medium leading-none"),
                rx.el.select(
                    rx.el.option("Male", value="Male"),
                    rx.el.option("Female", value="Female"),
                    rx.el.option("Other", value="Other"),
                    rx.el.option("Prefer not to say", value="Prefer not to say"),
                    name="gender",
                    default_value="Prefer not to say",
                    class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.button(
                "Create Account",
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-blue-500 hover:bg-blue-600 h-10 px-4 py-2 w-full",
            ),
            rx.el.div(
                rx.el.span(
                    "Already have an account?",
                    class_name="text-sm text-gray-500 font-medium",
                ),
                rx.el.a(
                    "Sign In",
                    href="/sign-in",
                    class_name="text-sm text-blue-500 font-medium underline hover:text-blue-600 transition-colors",
                ),
                class_name="flex flex-row gap-2 justify-center mt-2",
            ),
            class_name="flex flex-col gap-4",
            on_submit=AuthState.sign_up,
            reset_on_submit=True,
        ),
        class_name="p-8 rounded-xl bg-white flex flex-col gap-6 shadow-sm border border-gray-200 text-black w-full max-w-md",
    )