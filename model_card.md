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

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
