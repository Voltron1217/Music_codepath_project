# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender works like a judge with a scorecard. For every song in the catalog it asks how well the song fits what the listener likes, hands out points, and then ranks the songs from highest total to lowest. The top few become the recommendations.

**What it looks at.** For each song it uses the genre, the mood, and three numbers between 0 and 1: energy (how intense or calm the song feels), valence (how happy or sad it sounds), and acousticness (how much it sounds like real instruments rather than electronics). Tempo and danceability are stored but not used yet.

**What it knows about the listener.** The listener gives a favorite genre, a favorite mood, a target energy level, optionally a target happiness level, and whether they like acoustic sounds.

**How points are handed out.** A song can earn up to 9 points:

- **Energy, up to 3.5 points.** The closer the song's energy is to the listener's target, the more points it earns. A perfect match earns all 3.5, and the points shrink steadily as the song gets further away.
- **Happiness (valence), up to 2.0 points.** Scored the same way as energy.
- **Genre, 2.0 points.** The full amount for the exact genre. Related genres, such as pop and indie pop, earn half.
- **Mood, 1.0 point.** The full amount for the exact mood. Related moods, such as chill and relaxed, earn half.
- **Acoustic taste, up to 0.5 points.** More points the closer the song is to what the listener prefers.

Related genres and moods earn partial credit so a near miss isn't treated the same as a complete mismatch. Energy counts the most because it is the one feature with many different values across the songs, so it separates them best. Most genres appear only once in the catalog, so a big genre bonus would favor a single song and hide everything else.

**Why you see an explanation.** Each song's points are listed next to the reason they were earned, such as "genre match (+2.00)", so the listener can see why a song was picked instead of getting a mystery ranking. When two songs tie, they are ordered alphabetically by title.

**What changed from the starter logic.** The scoring now awards points per feature instead of an all-or-nothing match, gives partial credit to related genres and moods, and returns the reasons along with each score.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The system over prioritize pop because its the majority genre in my dataset of selected songs. It doesnt follow the user song they select. Scoring the weight can more readable for the person seeing what is the best song out there. 

- **Energy gap favors the middle.** The penalty is linear and symmetric, so mid-range songs are never far from anyone. Across 132 synthetic numeric-only users, *Library Rain* reached the top 5 for 61 of them and *Island Breeze* for 21.
- **Extreme tastes are served worse.** The quietest song has energy 0.18, so a user targeting 0.0 can earn at most 2.87 of 3.5 energy points. The catalog is also lopsided: 8 songs at energy 0.7 or higher, 5 at 0.4 or lower.
- **Filter bubble in the low-energy cluster.** Five songs sit at energy 0.3 to 0.4, and the top-5 scores for a 0.3 target differ by only 0.25. Chill/lofi users got near-identical lists. A cap of 2 songs per genre now reduces this, but it does not add songs the catalog lacks.
- **Genre is a one-slot bonus.** 12 of 15 genres have one song, so a hip hop, reggae or classical fan gets one on-genre match and then the same filler as everyone else. The related-genre groups are hand-written: lofi has two related genres, while classical, hip hop, reggae and R&B have none.
- **Features not used.** Tempo and danceability are stored but never scored, and `likes_acoustic` is yes/no rather than a degree. The related-mood groups lean calm: "confident" and "romantic" have no neighbors.
- **Feedback-loop risk.** If the planned popularity ranking fed back into scoring, popular songs would be recommended more and added more.

---

## 7. Evaluation  

Profiles run through `python3 -m src.main` (output in the README): Chill lofi, Intense rock, and adversarial cases: high energy + sad, high energy + peaceful classical, unknown genre/mood, messy labels (`"Rock "`, `"INTENSE"`), happy labels with low valence, out-of-range energy, and an empty profile. This is the person favorite type of music when doing something active.

- **What I looked for:** whether label matches could outweigh large numeric mismatches, and whether bad input failed quietly.
- **What surprised me:** genre plus mood is worth 3 points, enough to put a 0.18-energy classical song at #1 for a 0.95-energy user. Messy labels silently lost their match points.
- **Fixes made:** labels are lowercased and trimmed, invalid targets and empty profiles raise an error, "sad" joined the melancholic mood group, and each genre is limited to 2 slots per list.
- **Experiment:** with the mood check disabled, only the order of close results changed (for example the three lofi songs reordered), and the top score fell by exactly 1.0.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
I have learned that the system might not go in the right way you wanted and i need to figure out why its not working. trying to debug something
- Something unexpected or interesting you discovered  
I discover that the output changes every single time i run main.py and that there are different result.
- How this changed the way you think about music recommendation apps  
It made me change on how much it got to change and keep track of the user task in music. Weighting how much the person like this music.
