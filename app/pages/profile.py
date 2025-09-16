import reflex as rx
from app.states.auth_state import AuthState


class ProfileState(rx.State):
    interests_options: list[str] = [
        "Mental Health",
        "Anxiety",
        "Depression",
        "Relationships",
        "Work Stress",
        "Student Life",
        "Mindfulness",
        "Fitness",
    ]
    selected_interests: list[str] = []
    pseudonym: str = ""

    def on_load(self):
        return ProfileState.set_initial_pseudonym

    @rx.event
    async def set_initial_pseudonym(self):
        auth_state = await self.get_state(AuthState)
        self.pseudonym = await auth_state.get_initial_pseudonym()

    @rx.event
    def toggle_interest(self, interest: str):
        if interest in self.selected_interests:
            self.selected_interests.remove(interest)
        elif len(self.selected_interests) < 5:
            self.selected_interests.append(interest)
        else:
            return rx.toast.error("You can select a maximum of 5 interests.")

    @rx.var
    def interests_str(self) -> str:
        return ",".join(self.selected_interests)


def interest_tag(interest: str):
    is_selected = ProfileState.selected_interests.contains(interest)
    return rx.el.button(
        interest,
        on_click=lambda: ProfileState.toggle_interest(interest),
        class_name=rx.cond(
            is_selected,
            "px-3 py-1 bg-blue-500 text-white rounded-full text-sm",
            "px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm",
        ),
        type="button",
    )


def profile():
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Complete Your Profile", class_name="text-2xl font-bold text-gray-800"
            ),
            rx.el.p(
                "This information is kept confidential and helps us connect you with the right peers.",
                class_name="text-sm text-gray-500 font-medium",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Pseudonym", class_name="text-sm font-medium leading-none"
                    ),
                    rx.el.input(
                        name="pseudonym",
                        placeholder="e.g. BraveLion42",
                        default_value=ProfileState.pseudonym,
                        key=ProfileState.pseudonym,
                        class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                    ),
                    class_name="flex flex-col gap-1.5",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Age", class_name="text-sm font-medium leading-none"
                        ),
                        rx.el.input(
                            name="age",
                            type="number",
                            placeholder="13-100",
                            class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                        ),
                        class_name="flex flex-col gap-1.5 w-1/2",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Gender", class_name="text-sm font-medium leading-none"
                        ),
                        rx.el.select(
                            rx.el.option("Select...", value="", disabled=True),
                            rx.el.option("Male", value="Male"),
                            rx.el.option("Female", value="Female"),
                            rx.el.option("Non-binary", value="Non-binary"),
                            rx.el.option(
                                "Prefer not to say", value="Prefer not to say"
                            ),
                            name="gender",
                            class_name="flex h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                        ),
                        class_name="flex flex-col gap-1.5 w-1/2",
                    ),
                    class_name="flex flex-row gap-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Interests (Select up to 5)",
                        class_name="text-sm font-medium leading-none",
                    ),
                    rx.el.div(
                        rx.foreach(ProfileState.interests_options, interest_tag),
                        class_name="flex flex-wrap gap-2 pt-2",
                    ),
                    rx.el.input(
                        name="interests",
                        type="hidden",
                        default_value=ProfileState.interests_str,
                    ),
                    class_name="flex flex-col gap-1.5",
                ),
                rx.el.div(
                    rx.el.label(
                        "Bio (Optional, 500 characters max)",
                        class_name="text-sm font-medium leading-none",
                    ),
                    rx.el.textarea(
                        name="bio",
                        placeholder="Tell us a little about what you're going through...",
                        class_name="flex min-h-[80px] w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                    ),
                    class_name="flex flex-col gap-1.5",
                ),
                rx.el.button(
                    "Save Profile and Continue",
                    type="submit",
                    class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-blue-500 hover:bg-blue-600 h-10 px-4 py-2 w-full",
                ),
                on_submit=AuthState.update_profile,
                class_name="flex flex-col gap-4 mt-6",
            ),
            class_name="p-8 rounded-xl bg-white flex flex-col gap-2 shadow-sm border border-gray-200 text-black w-full max-w-lg",
        ),
        class_name="flex items-center justify-center min-h-screen bg-gray-50 p-4",
        on_mount=ProfileState.on_load,
    )