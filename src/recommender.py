import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None

# Maximum points each feature can earn.
POINTS = {
    "energy": 3.5,
    "mood": 1.0,
    "valence": 2.0,
    "genre": 2.0,
    "acoustic": 0.5,
}
MAX_SCORE = sum(POINTS.values())

# Related labels earn partial credit instead of an all-or-nothing match.
PARTIAL_CREDIT = 0.5
RELATED_MOODS = [
    {"chill", "relaxed", "focused", "peaceful"},
    {"intense", "aggressive"},
    {"happy", "uplifting", "euphoric"},
    {"moody", "melancholic", "nostalgic"},
]
RELATED_GENRES = [
    {"rock", "metal"},
    {"pop", "indie pop"},
    {"lofi", "ambient", "jazz"},
    {"folk", "country"},
    {"edm", "synthwave"},
]


def _closeness(value: float, target: float) -> float:
    """1.0 at the target, falling linearly with distance (inputs in 0-1)."""
    return max(0.0, 1.0 - abs(value - target))


def _label_match(value: str, favorite: str, groups: List[set]) -> float:
    """1.0 for an exact match, PARTIAL_CREDIT for related labels, else 0.0."""
    if value == favorite:
        return 1.0
    if any(value in g and favorite in g for g in groups):
        return PARTIAL_CREDIT
    return 0.0


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
            "target_valence": user.target_valence,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = self._prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda s: (-score_song(prefs, asdict(s))[0], s.title),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = score_song(self._prefs(user), asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    int_fields = ["id", "tempo_bpm"]
    float_fields = ["energy", "valence", "danceability", "acousticness"]
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for name in int_fields:
                row[name] = int(row[name])
            for name in float_fields:
                row[name] = float(row[name])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Returns (score in points, reasons), where score is at most MAX_SCORE and each
    reason shows the points it added, e.g. "genre match (+2.00)".
      - Genre / mood: full points for an exact match, half for a related label.
      - Numeric features (energy, valence, acousticness): max points scaled by
        closeness, i.e. max_points * (1 - abs(song value - target)).
    Features the user gave no preference for earn nothing.
    """
    score = 0.0
    reasons: List[str] = []

    def add(key: str, fraction: float, reason: str) -> None:
        """Add POINTS[key] scaled by fraction (0-1) to the score and log why."""
        nonlocal score
        points = POINTS[key] * fraction
        score += points
        if points > 0:
            reasons.append(f"{reason} (+{points:.2f})")

    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        c = _closeness(song["energy"], target_energy)
        add("energy", c, f"energy {song['energy']:.2f} is {abs(song['energy'] - target_energy):.2f} from target")

    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        c = _closeness(song["valence"], target_valence)
        add("valence", c, f"valence {song['valence']:.2f} is {abs(song['valence'] - target_valence):.2f} from target")

    favorite_mood = user_prefs.get("favorite_mood")
    if favorite_mood is not None:
        m = _label_match(song["mood"], favorite_mood, RELATED_MOODS)
        kind = "match" if m == 1.0 else "similar"
        add("mood", m, f"mood {kind} ('{song['mood']}' vs '{favorite_mood}')")

    favorite_genre = user_prefs.get("favorite_genre")
    if favorite_genre is not None:
        g = _label_match(song["genre"], favorite_genre, RELATED_GENRES)
        kind = "match" if g == 1.0 else "related"
        add("genre", g, f"genre {kind} ('{song['genre']}' vs '{favorite_genre}')")

    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        a = _closeness(song["acousticness"], 1.0 if likes_acoustic else 0.0)
        add("acoustic", a, f"acousticness {song['acousticness']:.2f} fits {'acoustic' if likes_acoustic else 'non-acoustic'} taste")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Scores every song with score_song and returns the top k as
    (song, score, explanation), highest score first. Ties sort by title.
    """
    scored = (
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    )
    return sorted(scored, key=lambda r: (-r[1], r[0]["title"]))[:k]
