"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import MAX_SCORE, load_songs, recommend_songs


WIDTH = 64


def print_recommendations(name: str, recommendations) -> None:
    """Print one profile's results: rank, title, score, and a bullet per reason."""
    print("\n" + "=" * WIDTH)
    print(f" Top {len(recommendations)} recommendations for {name}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / {MAX_SCORE:g}")
        print("   Why:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")

    print("\n" + "-" * WIDTH)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = {
        "Chill lofi": {
            "favorite_genre": "lofi", "favorite_mood": "chill",
            "target_energy": 0.40, "target_valence": 0.60, "likes_acoustic": True,
        },
        "Intense rock": {
            "favorite_genre": "rock", "favorite_mood": "intense",
            "target_energy": 0.92, "target_valence": 0.50, "likes_acoustic": False,
        },
    }

    for name, user_prefs in profiles.items():
        print_recommendations(name, recommend_songs(user_prefs, songs, k=5))


if __name__ == "__main__":
    main()
