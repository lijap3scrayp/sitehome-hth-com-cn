from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SITE_URL = "https://sitehome-hth.com.cn"
CORE_KEYWORD = "华体会"

def generate_uid(seed: str = "122007e1390505b1") -> str:
    """Generate a simple UID based on timestamp and seed."""
    base = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"note-{base}-{seed[:6]}"

@dataclass
class KeywordNote:
    """A data class representing a keyword note with metadata."""
    title: str
    content: str
    keyword: str
    source_url: str
    uid: str = field(default_factory=generate_uid)
    created_at: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    importance: int = 3  # 1-5

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if not self.tags:
            self.tags = ["general"]
        self.importance = max(1, min(5, self.importance))

    def short_display(self) -> str:
        """Return a one-line summary of this note."""
        tag_str = ", ".join(self.tags)
        return f"[{self.uid}] {self.title} ({self.keyword}) [{tag_str}]"

    def full_summary(self) -> str:
        """Return a formatted multi-line summary."""
        lines = [
            f"UID: {self.uid}",
            f"Title: {self.title}",
            f"Keyword: {self.keyword}",
            f"Source: {self.source_url}",
            f"Created: {self.created_at}",
            f"Importance: {self.importance}/5",
            f"Tags: {', '.join(self.tags)}",
            "---",
            self.content,
        ]
        return "\n".join(lines)


@dataclass
class NoteCollection:
    """A collection of KeywordNote objects with utility methods."""
    notes: List[KeywordNote] = field(default_factory=list)
    collection_name: str = "Default Collection"

    def add_note(self, note: KeywordNote) -> None:
        """Add a note to the collection."""
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """Return notes containing the specified keyword."""
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def filter_by_importance(self, min_imp: int = 1, max_imp: int = 5) -> List[KeywordNote]:
        """Return notes within a given importance range."""
        return [n for n in self.notes if min_imp <= n.importance <= max_imp]

    def format_all_short(self) -> str:
        """Return a list of all notes in short format."""
        if not self.notes:
            return "No notes in collection."
        return "\n".join(n.short_display() for n in self.notes)

    def format_all_full(self) -> str:
        """Return all notes in full summary format, separated by blank lines."""
        if not self.notes:
            return "No notes in collection."
        return "\n\n".join(n.full_summary() for n in self.notes)

    def display_summary(self) -> None:
        """Print a summary of the collection to stdout."""
        print(f"=== {self.collection_name} ===")
        print(f"Total notes: {len(self.notes)}")
        if self.notes:
            print("Recent notes (short form):")
            for n in self.notes[-3:]:
                print(f"  - {n.short_display()}")


def create_example_notes() -> NoteCollection:
    """Create a pre-populated collection for demo purposes."""
    collection = NoteCollection(collection_name="Example Notes")

    note1 = KeywordNote(
        title="Example Homepage Note",
        content=f"This is a sample note related to {CORE_KEYWORD} from {SITE_URL}.",
        keyword=CORE_KEYWORD,
        source_url=SITE_URL,
        tags=["example", "homepage"],
        importance=4
    )

    note2 = KeywordNote(
        title="Second Keyword Note",
        content=f"Another note discussing {CORE_KEYWORD} and its related topics. Visit {SITE_URL} for more info.",
        keyword=CORE_KEYWORD,
        source_url=f"{SITE_URL}/about",
        tags=["example", "about"],
        importance=3
    )

    note3 = KeywordNote(
        title="Third Note - Other Keyword",
        content="This note uses a different keyword for variety.",
        keyword="Python",
        source_url="https://python.org",
        tags=["programming", "example"],
        importance=2
    )

    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)
    return collection


def main():
    """Run a quick demonstration of the KeywordNote system."""
    collection = create_example_notes()
    collection.display_summary()

    print("\n--- Full details of first note ---")
    print(collection.notes[0].full_summary())

    print("\n--- All notes (short) ---")
    print(collection.format_all_short())

    print("\n--- Notes filtered by keyword '华体会' ---")
    filtered = collection.filter_by_keyword(CORE_KEYWORD)
    for note in filtered:
        print(f"  - {note.short_display()}")


if __name__ == "__main__":
    main()