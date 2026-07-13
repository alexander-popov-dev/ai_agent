from pathlib import Path



class PromptLoader:
    BASE_PATH: Path = Path(__file__).parent

    @classmethod
    def load(cls, name: str) -> str:
        return (
            cls.BASE_PATH
            .joinpath(f"{name}.md")
            .read_text(encoding="utf-8")
        )