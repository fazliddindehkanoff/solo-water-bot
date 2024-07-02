from typing import Optional, Dict, Any
from django.contrib.admin.widgets import AdminDateWidget


BASE_CLASSES = [
    "border",
    "bg-white",
    "font-medium",
    "rounded-md",
    "shadow-sm",
    "text-gray-500",
    "text-sm",
    "focus:ring",
    "focus:ring-primary-300",
    "focus:border-primary-600",
    "focus:outline-none",
    "group-[.errors]:border-red-600",
    "group-[.errors]:focus:ring-red-200",
    "dark:bg-gray-900",
    "dark:border-gray-700",
    "dark:text-gray-400",
    "dark:focus:border-primary-600",
    "dark:focus:ring-primary-700",
    "dark:focus:ring-opacity-50",
    "dark:group-[.errors]:border-red-500",
    "dark:group-[.errors]:focus:ring-red-600/40",
]

BASE_INPUT_CLASSES = [
    *BASE_CLASSES,
    "px-3",
    "py-2",
    "w-full",
]

INPUT_CLASSES = [*BASE_INPUT_CLASSES, "max-w-2xl"]


class UnfoldAdminSingleDateWidget(AdminDateWidget):
    template_name = "unfold/widgets/date.html"

    def __init__(
        self, attrs: Optional[Dict[str, Any]] = None, format: Optional[str] = None
    ) -> None:
        attrs = {
            "class": "vDateField " + " ".join(INPUT_CLASSES),
            "size": "10",
            **(attrs or {}),
        }
        super().__init__(attrs=attrs, format=format)
