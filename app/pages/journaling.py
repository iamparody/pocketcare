import reflex as rx
from app.states.journal_state import JournalState, JournalEntry, Badge
from app.components.sidebar import sidebar
from app.components.header import header
from app.states.dashboard_state import DashboardState


def mood_selector():
    return rx.el.div(
        rx.el.p("How are you feeling today?", class_name="text-lg font-medium mb-2"),
        rx.el.div(
            rx.foreach(
                JournalState.mood_options,
                lambda mood: rx.el.button(
                    mood,
                    on_click=lambda: JournalState.set_current_mood(mood),
                    class_name=rx.cond(
                        JournalState.current_mood == mood,
                        "px-4 py-2 rounded-full text-white bg-blue-500 font-semibold",
                        "px-4 py-2 rounded-full bg-gray-200 hover:bg-gray-300 font-semibold",
                    ),
                ),
            ),
            class_name="flex flex-wrap gap-3",
        ),
        class_name="mb-6",
    )


def journal_editor():
    return rx.el.form(
        rx.el.textarea(
            name="content",
            placeholder="Write about your day...",
            class_name="w-full h-40 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500",
        ),
        rx.el.button(
            "Save Entry",
            type="submit",
            class_name="mt-4 px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700",
        ),
        on_submit=JournalState.save_entry,
        reset_on_submit=True,
        class_name="w-full",
    )


def journal_entry_card(entry: JournalEntry):
    return rx.el.div(
        rx.el.div(
            rx.el.p(entry["created_at"], class_name="text-sm text-gray-500"),
            rx.cond(
                entry["is_special"],
                rx.el.span(
                    "Special",
                    class_name="ml-2 px-2 py-1 bg-purple-200 text-purple-800 text-xs font-semibold rounded-full",
                ),
                rx.fragment(),
            ),
            class_name="flex items-center",
        ),
        rx.el.p(f"Mood: {entry['mood']}", class_name="font-semibold my-2"),
        rx.el.p(entry["content"], class_name="text-gray-700"),
        class_name="p-4 bg-white rounded-lg border shadow-sm",
    )


def badge_card(badge: Badge):
    return rx.el.div(
        rx.icon("award", class_name="w-10 h-10 text-yellow-500"),
        rx.el.p(badge["badge_name"], class_name="font-bold mt-2"),
        rx.el.p(
            f"Awarded on {badge['awarded_at']}", class_name="text-sm text-gray-500"
        ),
        class_name="flex flex-col items-center p-4 bg-white rounded-lg border shadow-sm text-center",
    )


def placeholder_badge(icon: str, name: str):
    return rx.el.div(
        rx.icon(icon, class_name="w-10 h-10 text-gray-300"),
        rx.el.p(name, class_name="font-bold mt-2 text-sm text-gray-400"),
        class_name="flex flex-col items-center p-4 bg-gray-100 rounded-lg border border-dashed text-center",
    )


def special_journaling_widget():
    return rx.el.div(
        rx.el.h2("Special Journaling", class_name="text-2xl font-bold mb-4"),
        rx.el.p(
            "For moments when you need to track triggers or intense feelings.",
            class_name="text-gray-600 mb-4",
        ),
        rx.cond(
            JournalState.is_special_journaling,
            rx.el.button(
                "End Special Journaling",
                on_click=JournalState.end_special_journal,
                class_name="w-full bg-red-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-600",
            ),
            rx.el.button(
                "Start Special Journaling",
                on_click=JournalState.start_special_journal,
                class_name="w-full bg-purple-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-600",
            ),
        ),
        class_name="p-6 bg-white rounded-xl border shadow-sm",
    )


def journaling_page():
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.h1(
                    "My Journal", class_name="text-3xl font-bold text-gray-800 mb-6"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2("New Entry", class_name="text-2xl font-bold mb-4"),
                        mood_selector(),
                        journal_editor(),
                        class_name="p-6 bg-white rounded-xl border shadow-sm",
                    ),
                    rx.el.div(
                        special_journaling_widget(),
                        rx.el.div(
                            rx.el.h2("My Badges", class_name="text-2xl font-bold mb-4"),
                            rx.cond(
                                JournalState.badges.length() > 0,
                                rx.el.div(
                                    rx.foreach(JournalState.badges, badge_card),
                                    class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Keep journaling to earn badges!",
                                        class_name="text-gray-600 mb-4",
                                    ),
                                    rx.el.div(
                                        placeholder_badge("book-check", "First Entry"),
                                        placeholder_badge("flame", "7-Day Streak"),
                                        placeholder_badge(
                                            "calendar-days", "30-Day Milestone"
                                        ),
                                        placeholder_badge("sunrise", "Morning Lark"),
                                        class_name="grid grid-cols-2 md:grid-cols-4 gap-4",
                                    ),
                                ),
                            ),
                            class_name="p-6 bg-white rounded-xl border shadow-sm mt-8",
                        ),
                        class_name="flex flex-col gap-8",
                    ),
                    class_name="grid lg:grid-cols-2 gap-8 mb-8",
                ),
                rx.el.div(
                    rx.el.h2("Past Entries", class_name="text-2xl font-bold mb-4"),
                    rx.el.div(
                        rx.foreach(JournalState.journal_entries, journal_entry_card),
                        class_name="space-y-4",
                    ),
                ),
                class_name="p-6",
            ),
            class_name=rx.cond(
                DashboardState.sidebar_open,
                "transition-all ml-0 md:ml-64",
                "transition-all ml-0 md:ml-16",
            ),
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen text-gray-800",
        on_mount=JournalState.load_journal_data,
    )