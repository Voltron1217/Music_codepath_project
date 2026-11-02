# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This design focuses on the song itself. The data/songs.csv currently holds only 18 songs, so growing the catalog is the first priority. Each song is compared to a user's taste profile, given a score, and the highest-scoring songs are recommended.
In Which the User can select the song they like and see other recommended song related to the User likes. and remove the dislike songs or genres. The system might prioritize the genre more than anything else which can be a big issue. 
### Song features

Each `Song` is a row in `data/songs.csv`:

- `id` and `artist` identify a song and who made it. `id` is the unique key, and `artist` is used for display and filtering.
- `genre` and `mood` are labels (for example `lofi` / `chill`).
- `energy`, `valence` and `acousticness` are numbers from 0 to 1 used for closeness scoring.
- `title`, `tempo_bpm` and `danceability` are stored with each song. The current score does not use them.

### UserProfile

A `UserProfile` stores:

- `favorite_genre`, `favorite_mood` and `target_energy`, plus optional `target_valence`.
- A **playlist** of songs the user connects with. Other people can see it to learn what this person listens to. The user can set it to **private** if they don't want to share their taste.
- A **filter list** of songs that should not appear again, and genres unrelated to the user's taste.

### How a song is scored

Each song gets a score from 0 to 1. It is a weighted sum of how well the song matches the user:

| Feature | Weight | How it is scored |
|---|---|---|
| Energy | 0.35 | Closeness to the target: `1 - abs(song - target)` |
| Mood | 0.25 | Exact match earns full credit. A related mood earns half credit (for example `chill` and `relaxed`). |
| Valence | 0.20 | Closeness to the target valence |
| Genre | 0.15 | Exact match earns full credit. A related genre earns half credit (for example `pop` and `indie pop`). |
| Acousticness | 0.05 | Closeness to the user's preference |

Why these weights:

- **Energy ranks highest.** It is the only feature with many different values across the catalog, so it separates songs best.
- **Mood outranks genre.** In this catalog most genres appear once, so a large genre weight would boost a single song and drown out everything else. Mood describes how a song feels, and it groups many genres together.
- **Related labels get partial credit.** This keeps near matches from scoring zero.
- **Missing preferences are dropped.** If a user gives no preference for a feature, that feature is left out and the remaining weights are renormalized.

### How songs are chosen

1. Remove songs and genres in the user's filter list.
2. Score every remaining song against the user's profile.
3. Sort by score, highest first. Ties are broken by title.
4. Return the top `k` songs, each with a short explanation of why it scored that way.
5. Build a ranking of popular songs from the songs users connect with (playlist additions).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

1. Library Rain by Paper Lanterns
   Score: 8.75 / 9
   Why:
     - energy 0.35 is 0.05 from target (+3.32)
     - valence 0.60 is 0.00 from target (+2.00)
     - mood match ('chill' vs 'chill') (+1.00)
     - genre match ('lofi' vs 'lofi') (+2.00)
     - acousticness 0.86 fits acoustic taste (+0.43)

2. Midnight Coding by LoRoom
   Score: 8.71 / 9
   Why:
     - energy 0.42 is 0.02 from target (+3.43)
     - valence 0.56 is 0.04 from target (+1.92)
     - mood match ('chill' vs 'chill') (+1.00)
     - genre match ('lofi' vs 'lofi') (+2.00)
     - acousticness 0.71 fits acoustic taste (+0.35)

3. Focus Flow by LoRoom
   Score: 8.37 / 9
   Why:
     - energy 0.40 is 0.00 from target (+3.50)
     - valence 0.59 is 0.01 from target (+1.98)
     - mood similar ('focused' vs 'chill') (+0.50)
     - genre match ('lofi' vs 'lofi') (+2.00)
     - acousticness 0.78 fits acoustic taste (+0.39)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 7.44 / 9
   Why:
     - energy 0.28 is 0.12 from target (+3.08)
     - valence 0.65 is 0.05 from target (+1.90)
     - mood match ('chill' vs 'chill') (+1.00)
     - genre related ('ambient' vs 'lofi') (+1.00)
     - acousticness 0.92 fits acoustic taste (+0.46)

5. Coffee Shop Stories by Slow Stereo
   Score: 7.12 / 9
   Why:
     - energy 0.37 is 0.03 from target (+3.40)
     - valence 0.71 is 0.11 from target (+1.78)
     - mood similar ('relaxed' vs 'chill') (+0.50)
     - genre related ('jazz' vs 'lofi') (+1.00)
     - acousticness 0.89 fits acoustic taste (+0.45)

----------------------------------------------------------------

================================================================
 Top 5 recommendations for Intense rock
================================================================

1. Storm Runner by Voltline
   Score: 8.88 / 9
   Why:
     - energy 0.91 is 0.01 from target (+3.46)
     - valence 0.48 is 0.02 from target (+1.96)
     - mood match ('intense' vs 'intense') (+1.00)
     - genre match ('rock' vs 'rock') (+2.00)
     - acousticness 0.10 fits non-acoustic taste (+0.45)

2. Iron Requiem by Black Cathedral
   Score: 6.72 / 9
   Why:
     - energy 0.97 is 0.05 from target (+3.33)
     - valence 0.21 is 0.29 from target (+1.42)
     - mood similar ('aggressive' vs 'intense') (+0.50)
     - genre related ('metal' vs 'rock') (+1.00)
     - acousticness 0.04 fits non-acoustic taste (+0.48)

3. Gym Hero by Max Pulse
   Score: 6.40 / 9
   Why:
     - energy 0.93 is 0.01 from target (+3.46)
     - valence 0.77 is 0.27 from target (+1.46)
     - mood match ('intense' vs 'intense') (+1.00)
     - acousticness 0.05 fits non-acoustic taste (+0.47)

4. Night Drive Loop by Neon Echo
   Score: 5.27 / 9
   Why:
     - energy 0.75 is 0.17 from target (+2.90)
     - valence 0.49 is 0.01 from target (+1.98)
     - acousticness 0.22 fits non-acoustic taste (+0.39)

5. Concrete Crown by Rhyme Atlas
   Score: 5.21 / 9
   Why:
     - energy 0.78 is 0.14 from target (+3.01)
     - valence 0.62 is 0.12 from target (+1.76)
     - acousticness 0.12 fits non-acoustic taste (+0.44)



```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



