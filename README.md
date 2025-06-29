# Golf Player Performance Analysis (2015–2022)

This project analyzes PGA Tour golf player performance data from 2015 to 2022. The goal is to uncover patterns in player strengths, segment players into meaningful clusters, and provide an interactive tool for analyzing player metrics.

---

## 📌 Project Motivation

### Why this dataset?
I chose the [PGA Tour Golf Data 2015-2022](https://www.kaggle.com/datasets/robikscube/pga-tour-golf-data-20152022) from Kaggle because:
- It provides detailed performance metrics (e.g., strokes gained in different aspects of the game) over multiple seasons.
- It covers a long enough time span (8 seasons) to identify trends and player consistency.
- Golf performance data is rich in potential for clustering, time series, and comparative analytics.

### Why this problem statement?
I aimed to answer:
- **Can we segment players based on their playing style and strengths?**
- **How can we visually compare players within these segments?**
- **Can we make performance analysis easier with an interactive tool?**

By doing this, we can:
- Help fans, analysts, and coaches quickly identify player archetypes.
- Enable easy comparisons of players’ strengths and weaknesses.
- Track individual or group performance trends over time.

---

## 🔍 Approach

### Data preparation
- Cleaned the dataset to handle missing values.
- Focused on key metrics: strokes gained in approach, putting, off the tee, and around the green.
- Aggregated data at the player-season level to provide stable performance indicators.

### Clustering
- Applied **K-Means clustering** to group players into segments:
  - *Ball Strikers*
  - *Putting Specialists*
  - *Short Game Experts*
  - *Scrappy All-Rounders*
- Each cluster represents a distinct player profile based on strokes gained data.

### Visualizations
- **Radar charts:** Compare an individual player’s metrics to the average of their cluster.
- **Time series plots:** Show performance trends over seasons (e.g., strokes gained in approach vs. putting).
- **Summary cards:** Show cluster info, wins, tournaments played.

### Interactive tool
This project includes an interactive dashboard (via `Gradio` / `Streamlit`):
- Select a player from a dropdown.
- View their cluster, radar chart comparison, time series of key metrics.
- Quickly explore player data without modifying code.

💡 *Run the Python script and follow the browser link to explore the dashboard.*

---

## ⚡ How to Run

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/golf-player-analysis.git
cd golf-player-analysis
```
## Requirements
See requirements.txt.

## License
MIT License (see LICENSE file).

## Author
Shreyance Jain
