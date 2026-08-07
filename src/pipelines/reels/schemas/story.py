from html import escape

from pydantic import BaseModel, Field

from src.pipelines.reels.schemas.idea import GenerateIdeaOutput
from src.core.enums import Language

MAX_MESSAGE_LENGTH = 4000

class StoryContext(BaseModel):
    instructions: list[str] = []

class ParseUserAnswerContext(BaseModel):
    instruction: str | None = None
    scenes: list[int] = Field(default_factory=list)

class GenerateStoryInput(BaseModel):
    language: Language = Language.UA
    idea: GenerateIdeaOutput
    instructions: StoryContext = Field(default_factory=StoryContext)

class GenerateStoryScene(BaseModel):
    order: int
    screen_text: str
    image_description: str
    narration: str


class GenerateStoryOutput(BaseModel):
    caption: str
    character_description: str
    visual_style: str
    scenes: list[GenerateStoryScene]

    def to_markdown(self) -> str:

        from html import escape

        parts = [
            f"🎬 <b>Название видео</b>\n"
            f"{escape(self.caption)}\n\n"
            f"👤 <b>Персонаж</b>\n"
            f"{escape(self.character_description)}\n\n"
            f"🎨 <b>Визуальный стиль</b>\n"
            f"{escape(self.visual_style)}\n"
        ]

        for scene in self.scenes:
            parts.append(
                f"\n━━━━━━━━━━━━━━━━━━━━\n"
                f"🎞 <b>Сцена {scene.order}</b>\n\n"
                f"📝 <b>Текст на экране</b>\n"
                f"{escape(scene.screen_text)}\n\n"
                f"🖼 <b>Описание изображения</b>\n"
                f"{escape(scene.image_description)}\n\n"
                f"🎙 <b>Озвучка</b>\n"
                f"{escape(scene.narration)}"
            )

        return "\n".join(parts)\

    def to_html_messages(self) -> list[str]:

        header = (
            f"🎬 <b>Название видео</b>\n"
            f"{escape(self.caption)}\n\n"
            f"👤 <b>Персонаж</b>\n"
            f"{escape(self.character_description)}\n\n"
            f"🎨 <b>Визуальный стиль</b>\n"
            f"{escape(self.visual_style)}"
        )

        messages: list[str] = []
        current = header

        for scene in self.scenes:

            scene_text = (
                f"\n\n━━━━━━━━━━━━━━━━━━━━\n"
                f"🎞 <b>Сцена {scene.order}</b>\n\n"
                f"<b>📝 Текст на экране</b>\n"
                f"{escape(scene.screen_text)}\n\n"
                f"<b>🖼 Описание изображения</b>\n"
                f"{escape(scene.image_description)}\n\n"
                f"<b>🎙 Озвучка</b>\n"
                f"{escape(scene.narration)}"
            )

            if len(current) + len(scene_text) > MAX_MESSAGE_LENGTH:
                messages.append(current)
                current = scene_text.lstrip()
            else:
                current += scene_text

        messages.append(current)

        return messages


class ParseUserAnswerInput(BaseModel):
    instruction: str


class ParseUserAnswerOutput(BaseModel):
    regenerate: bool
    scenes: list[int] = Field(default_factory=list)
    instruction: str


class EditStoryInput(BaseModel):
    language: Language = Language.UA
    story: GenerateStoryOutput
    scenes: list[GenerateStoryScene]
    instruction: str


class EditStoryOutput(BaseModel):
    scenes: list[GenerateStoryScene]

