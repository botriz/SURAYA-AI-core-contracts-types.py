from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class IntentType(str, Enum):
    CHAT = "chat"
    QUESTION = "question"
    TASK = "task"
    RESEARCH = "research"
    CODE = "code"
    MEMORY = "memory"
    SYSTEM = "system"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Intent:
    type: IntentType
    confidence: float
    raw_command: str
    parameters: dict[str, str]


def detect_intent(command: str) -> Intent:
    text = command.strip()

    if not text:
        return Intent(
            type=IntentType.UNKNOWN,
            confidence=1.0,
            raw_command=text,
            parameters={},
        )

    normalized = text.lower()

    code_words = (
        "code",
        "coding",
        "program",
        "programming",
        "کد",
        "برنامه نویسی",
        "برنامه‌نویسی",
    )

    research_words = (
        "research",
        "study",
        "investigate",
        "تحقیق",
        "بررسی علمی",
        "مطالعه",
    )

    memory_words = (
        "remember",
        "memory",
        "یادآوری",
        "حافظه",
        "به خاطر بسپار",
        "یادت باشد",
    )

    system_words = (
        "system",
        "runtime",
        "guardian",
        "executor",
        "سیستم",
        "گاردین",
        "اجرا",
    )

    task_words = (
        "do ",
        "create ",
        "build ",
        "make ",
        "run ",
        "انجام",
        "بساز",
        "ایجاد کن",
        "اجرا کن",
    )

    question_markers = (
        "?",
        "what ",
        "why ",
        "how ",
        "چی",
        "چرا",
        "چگونه",
        "چطور",
        "آیا",
    )

    if any(word in normalized for word in code_words):
        intent_type = IntentType.CODE
        confidence = 0.95
    elif any(word in normalized for word in research_words):
        intent_type = IntentType.RESEARCH
        confidence = 0.93
    elif any(word in normalized for word in memory_words):
        intent_type = IntentType.MEMORY
        confidence = 0.92
    elif any(word in normalized for word in system_words):
        intent_type = IntentType.SYSTEM
        confidence = 0.90
    elif any(word in normalized for word in task_words):
        intent_type = IntentType.TASK
        confidence = 0.85
    elif any(word in normalized for word in question_markers):
        intent_type = IntentType.QUESTION
        confidence = 0.80
    else:
        intent_type = IntentType.CHAT
        confidence = 0.60

    return Intent(
        type=intent_type,
        confidence=confidence,
        raw_command=text,
        parameters={},
    )
