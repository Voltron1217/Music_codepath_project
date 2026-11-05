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

Each song earns points for how well it matches the user, for a maximum of 9.0. Every point added is listed as a reason, for example `genre match ('lofi' vs 'lofi') (+2.00)`.

| Feature | Max points | How it is scored |
|---|---|---|
| Energy | 3.5 | Scaled by closeness to the target: `3.5 * (1 - abs(song - target))` |
| Valence | 2.0 | Scaled by closeness to the target valence |
| Genre | 2.0 | Exact match earns the full 2.0. A related genre earns half (for example `pop` and `indie pop`). |
| Mood | 1.0 | Exact match earns the full 1.0. A related mood earns half (for example `chill` and `relaxed`). |
| Acousticness | 0.5 | Scaled by closeness to the user's preference |

Why these points:

- **Energy counts the most.** It is the only feature with many different values across the catalog, so it separates songs best.
- **Genre is a fixed bonus.** Most genres appear only once in this catalog, so it works like a tiebreaker for songs that fit the user's taste.
- **Related labels get partial credit.** This keeps near matches from scoring zero.
- **Missing preferences earn nothing.** If a user gives no preference for a feature, songs earn no points for it, so the maximum possible score for that user is lower.

### How songs are chosen

1. Remove songs and genres in the user's filter list.
2. Score every remaining song against the user's profile.
3. Sort by score, highest first. Ties are broken by title.
4. Return the top `k` songs (no more than 2 from the same genre, so one cluster can't fill the list), each with a short explanation of why it scored that way.
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

Terminal output of `python3 -m src.main`: the two standard profiles, then the adversarial / edge-case profiles. Invalid profiles are skipped with the validation error.

```text
Loaded songs: 18

================================================================
 Top 5 recommendations for Chill lofi
================================================================

1. Focus Flow by LoRoom
   Score: 7.87 / 9
   Why:
     - energy 0.40 is 0.00 from target (+3.50)
     - valence 0.59 is 0.01 from target (+1.98)
     - genre match ('lofi' vs 'lofi') (+2.00)
     - acousticness 0.78 fits acoustic taste (+0.39)

2. Library Rain by Paper Lanterns
   Score: 7.75 / 9
   Why:
     - energy 0.35 is 0.05 from target (+3.32)
     - valence 0.60 is 0.00 from target (+2.00)
     - genre match ('lofi' vs 'lofi') (+2.00)
     - acousticness 0.86 fits acoustic taste (+0.43)

3. Coffee Shop Stories by Slow Stereo
   Score: 6.62 / 9
   Why:
     - energy 0.37 is 0.03 from target (+3.40)
     - valence 0.71 is 0.11 from target (+1.78)
     - genre related ('jazz' vs 'lofi') (+1.00)
     - acousticness 0.89 fits acoustic taste (+0.45)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 6.44 / 9
   Why:
     - energy 0.28 is 0.12 from target (+3.08)
     - valence 0.65 is 0.05 from target (+1.90)
     - genre related ('ambient' vs 'lofi') (+1.00)
     - acousticness 0.92 fits acoustic taste (+0.46)

5. Dust Road Lullaby by Hollow Pines
   Score: 5.69 / 9
   Why:
     - energy 0.45 is 0.05 from target (+3.32)
     - valence 0.58 is 0.02 from target (+1.96)
     - acousticness 0.81 fits acoustic taste (+0.41)

----------------------------------------------------------------

================================================================
 Top 5 recommendations for Intense rock
================================================================

1. Storm Runner by Voltline
   Score: 7.88 / 9
   Why:
     - energy 0.91 is 0.01 from target (+3.46)
     - valence 0.48 is 0.02 from target (+1.96)
     - genre match ('rock' vs 'rock') (+2.00)
     - acousticness 0.10 fits non-acoustic taste (+0.45)

2. Iron Requiem by Black Cathedral
   Score: 6.22 / 9
   Why:
     - energy 0.97 is 0.05 from target (+3.33)
     - valence 0.21 is 0.29 from target (+1.42)
     - genre related ('metal' vs 'rock') (+1.00)
     - acousticness 0.04 fits non-acoustic taste (+0.48)

3. Gym Hero by Max Pulse
   Score: 5.40 / 9
   Why:
     - energy 0.93 is 0.01 from target (+3.46)
     - valence 0.77 is 0.27 from target (+1.46)
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

----------------------------------------------------------------

================================================================
 Top 5 recommendations for Conflict: high energy + sad
================================================================

1. Tears in the Rain by Willow & Ash
   Score: 5.93 / 9
   Why:
     - energy 0.33 is 0.57 from target (+1.50)
     - valence 0.22 is 0.02 from target (+1.96)
     - genre match ('folk' vs 'folk') (+2.00)
     - acousticness 0.93 fits acoustic taste (+0.47)

2. Iron Requiem by Black Cathedral
   Score: 5.26 / 9
   Why:
     - energy 0.97 is 0.07 from target (+3.26)
     - valence 0.21 is 0.01 from target (+1.98)
     - acousticness 0.04 fits acoustic taste (+0.02)

3. Storm Runner by Voltline
   Score: 4.95 / 9
   Why:
     - energy 0.91 is 0.01 from target (+3.46)
     - valence 0.48 is 0.28 from target (+1.44)
     - acousticness 0.10 fits acoustic taste (+0.05)

4. Dust Road Lullaby by Hollow Pines
   Score: 4.57 / 9
   Why:
     - energy 0.45 is 0.45 from target (+1.93)
     - valence 0.58 is 0.38 from target (+1.24)
     - genre related ('country' vs 'folk') (+1.00)
     - acousticness 0.81 fits acoustic taste (+0.41)

5. Night Drive Loop by Neon Echo
   Score: 4.50 / 9
   Why:
     - energy 0.75 is 0.15 from target (+2.98)
     - valence 0.49 is 0.29 from target (+1.42)
     - acousticness 0.22 fits acoustic taste (+0.11)

----------------------------------------------------------------

================================================================
 Top 5 recommendations for Conflict: high energy + peaceful classical
================================================================

1. Moonlit Sonata by Elena Voss
   Score: 5.29 / 9
   Why:
     - energy 0.18 is 0.77 from target (+0.80)
     - valence 0.40 is 0.00 from target (+2.00)
     - genre match ('classical' vs 'classical') (+2.00)
     - acousticness 0.97 fits acoustic taste (+0.48)

2. Storm Runner by Voltline
   Score: 5.25 / 9
   Why:
     - energy 0.91 is 0.04 from target (+3.36)
     - valence 0.48 is 0.08 from target (+1.84)
     - acousticness 0.10 fits acoustic taste (+0.05)

3. Iron Requiem by Black Cathedral
   Score: 5.07 / 9
   Why:
     - energy 0.97 is 0.02 from target (+3.43)
     - valence 0.21 is 0.19 from target (+1.62)
     - acousticness 0.04 fits acoustic taste (+0.02)

4. Night Drive Loop by Neon Echo
   Score: 4.73 / 9
   Why:
     - energy 0.75 is 0.20 from target (+2.80)
     - valence 0.49 is 0.09 from target (+1.82)
     - acousticness 0.22 fits acoustic taste (+0.11)

5. Gym Hero by Max Pulse
   Score: 4.72 / 9
   Why:
     - energy 0.93 is 0.02 from target (+3.43)
     - valence 0.77 is 0.37 from target (+1.26)
     - acousticness 0.05 fits acoustic taste (+0.03)

----------------------------------------------------------------

================================================================
 Top 5 recommendations for Unknown genre and mood
================================================================

1. Concrete Crown by Rhyme Atlas
   Score: 5.50 / 9
   Why:
     - energy 0.78 is 0.08 from target (+3.22)
     - valence 0.62 is 0.08 from target (+1.84)
     - acousticness 0.12 fits non-acoustic taste (+0.44)

2. Rooftop Lights by Indigo Parade
   Score: 5.40 / 9
   Why:
     - energy 0.76 is 0.06 from target (+3.29)
     - valence 0.81 is 0.11 from target (+1.78)
     - acousticness 0.35 fits non-acoustic taste (+0.33)

3. Night Drive Loop by Neon Echo
   Score: 5.29 / 9
   Why:
     - energy 0.75 is 0.05 from target (+3.32)
     - valence 0.49 is 0.21 from target (+1.58)
     - acousticness 0.22 fits non-acoustic taste (+0.39)

4. Sunrise City by Neon Echo
   Score: 5.21 / 9
   Why:
     - energy 0.82 is 0.12 from target (+3.08)
     - valence 0.84 is 0.14 from target (+1.72)
     - acousticness 0.18 fits non-acoustic taste (+0.41)

5. Velvet Hours by Amber Lune
   Score: 5.18 / 9
   Why:
     - energy 0.52 is 0.18 from target (+2.87)
     - valence 0.69 is 0.01 from target (+1.98)
     - acousticness 0.33 fits non-acoustic taste (+0.33)

----------------------------------------------------------------

================================================================
 Top 5 recommendations for Messy labels ('Rock ', 'INTENSE')
================================================================

1. Storm Runner by Voltline
   Score: 7.88 / 9
   Why:
     - energy 0.91 is 0.01 from target (+3.46)
     - valence 0.48 is 0.02 from target (+1.96)
     - genre match ('rock' vs 'Rock ') (+2.00)
     - acousticness 0.10 fits non-acoustic taste (+0.45)

2. Iron Requiem by Black Cathedral
   Score: 6.16 / 9
   Why:
     - energy 0.97 is 0.07 from target (+3.26)
     - valence 0.21 is 0.29 from target (+1.42)
     - genre related ('metal' vs 'Rock ') (+1.00)
     - acousticness 0.04 fits non-acoustic taste (+0.48)

3. Night Drive Loop by Neon Echo
   Score: 5.34 / 9
   Why:
     - energy 0.75 is 0.15 from target (+2.98)
     - valence 0.49 is 0.01 from target (+1.98)
     - acousticness 0.22 fits non-acoustic taste (+0.39)

4. Gym Hero by Max Pulse
   Score: 5.33 / 9
   Why:
     - energy 0.93 is 0.03 from target (+3.40)
     - valence 0.77 is 0.27 from target (+1.46)
     - acousticness 0.05 fits non-acoustic taste (+0.47)

5. Concrete Crown by Rhyme Atlas
   Score: 5.28 / 9
   Why:
     - energy 0.78 is 0.12 from target (+3.08)
     - valence 0.62 is 0.12 from target (+1.76)
     - acousticness 0.12 fits non-acoustic taste (+0.44)

----------------------------------------------------------------

================================================================
 Top 5 recommendations for Happy labels, low valence
================================================================

1. Sunrise City by Neon Echo
   Score: 6.36 / 9
   Why:
     - energy 0.82 is 0.02 from target (+3.43)
     - valence 0.84 is 0.74 from target (+0.52)
     - genre match ('pop' vs 'pop') (+2.00)
     - acousticness 0.18 fits non-acoustic taste (+0.41)

2. Gym Hero by Max Pulse
   Score: 6.18 / 9
   Why:
     - energy 0.93 is 0.13 from target (+3.04)
     - valence 0.77 is 0.67 from target (+0.66)
     - genre match ('pop' vs 'pop') (+2.00)
     - acousticness 0.05 fits non-acoustic taste (+0.47)

3. Rooftop Lights by Indigo Parade
   Score: 5.26 / 9
   Why:
     - energy 0.76 is 0.04 from target (+3.36)
     - valence 0.81 is 0.71 from target (+0.58)
     - genre related ('indie pop' vs 'pop') (+1.00)
     - acousticness 0.35 fits non-acoustic taste (+0.33)

4. Iron Requiem by Black Cathedral
   Score: 5.17 / 9
   Why:
     - energy 0.97 is 0.17 from target (+2.91)
     - valence 0.21 is 0.11 from target (+1.78)
     - acousticness 0.04 fits non-acoustic taste (+0.48)

5. Night Drive Loop by Neon Echo
   Score: 4.93 / 9
   Why:
     - energy 0.75 is 0.05 from target (+3.32)
     - valence 0.49 is 0.39 from target (+1.22)
     - acousticness 0.22 fits non-acoustic taste (+0.39)

----------------------------------------------------------------

Skipped Out-of-range energy (invalid): target_energy must be between 0 and 1, got 1.5

Skipped Empty profile (invalid): user profile has no preferences to score against
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



