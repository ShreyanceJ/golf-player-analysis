# -*- coding: utf-8 -*-
"""Golf_Final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cTbmmCEwdIG9g2HLulJu8XLzSP7i3ypC

## Adding required libraries
"""

import gradio as gr
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('/content/drive/MyDrive/Colab/Golf.csv', low_memory=False)

"""## EDA"""

# Understanding the spread of data
df.shape

# Viewing the data
df.head()

# Checking the structre of data
print(df.info())

# Checking if there are any missing values in the dataset
print(df.isnull().sum())

# Counting the number of unique records in each column to get information about number of tournaments, players, seasons, etc
print(df.nunique())

"""## Data Cleaning"""

# Remove unwanted columns
df.drop(columns= ['Unnamed: 2','Unnamed: 3','Unnamed: 4'], inplace= True)

# Step 1: Replace string 'Nan' with actual np.nan
df.replace('Nan', np.nan, inplace=True)

# Step 2: Define all columns except 'pos'
cols_to_check = df.columns.difference(['pos'])

# Step 3: Drop rows with NA in any column *except* 'pos'
df.dropna(subset=cols_to_check, inplace=True)

"""## Cluster Analysis
### Problem Statement 2:

How can we categorize PGA players based on their playing style and strengths using strokes gained metrics?

Why it's valuable: Coaches and fans can better understand player personas: e.g., aggressive drivers vs tactical putters.

Techniques:


1. K-Means / DBSCAN clustering
2. PCA for dimensionality reduction
3. Visualizations of clusters (e.g., radar charts)

### Data Filtering and Scaling
"""

# Segregating the columns for analysis
features = ['sg_ott', 'sg_app', 'sg_arg', 'sg_putt']
df_cluster = df[features].dropna()

# Keepign player names for labeling
player_names = df.loc[df_cluster.index, 'player']

# Standardize features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_cluster)

"""### K-means Clustering"""

# Creating K range to see where the elbow for the data lies
inertia = []
K_range = range(1, 10)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    inertia.append(kmeans.inertia_)

# Plot elbow curve
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertia, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.grid(True)
plt.show()

# Defining the number of clusters to be created based on elbow point
kmeans = KMeans(n_clusters=4, random_state=42)
df_cluster['cluster'] = kmeans.fit_predict(scaled_features)

"""### PCA Analysis and Plotting"""

# Defining PCA for plotting the clusters
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
components = pca.fit_transform(scaled_features)
df_cluster['pca1'] = components[:, 0]
df_cluster['pca2'] = components[:, 1]

plt.figure(figsize=(10, 7))
for cluster in df_cluster['cluster'].unique():
    plt.scatter(
        df_cluster[df_cluster['cluster'] == cluster]['pca1'],
        df_cluster[df_cluster['cluster'] == cluster]['pca2'],
        label=f'Cluster {cluster}'
    )

plt.title('Player Clusters based on Playing Style')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend()
plt.grid(True)
plt.show()

"""### Group Summary"""

# Add player names back
df_cluster['Player'] = player_names.values

# Mean profile of each cluster to understand the broad view for each cluster
cluster_profiles = df_cluster.groupby('cluster')[features].mean()
cluster_profiles

"""### Widget using Gradio"""

# Create a cluster name mapping for display
cluster_names = {
    0: 'Ball Strikers',
    1: 'Putting Specialists',
    2: 'Short Game Experts',
    3: 'Scrappy All-Rounders'
}

# Map cluster number to cluster name
df_cluster['cluster_name'] = df_cluster['cluster'].map(cluster_names)

# Ensure no duplicates in df_cluster: one row per player
df_cluster_clean = (
    df_cluster
    .groupby('Player')
    .first()          # or .agg(...) if you'd prefer to define aggregation
    .reset_index()
)

# Now merge
df = df.merge(
    df_cluster_clean[['Player', 'cluster', 'cluster_name']],
    left_on='player',
    right_on='Player',
    how='left'
)

# Drop redundant 'Player' column that came from df_cluster
df.drop(columns=['Player'], inplace=True)

# Function to generate radar + time series + summary
def player_dashboard(selected_player):
    player_data = df[df['player'] == selected_player]
    cluster_num = player_data['cluster'].iloc[0]
    cluster_name = player_data['cluster_name'].iloc[0]

    # Radar chart: player vs cluster avg
    player_means = player_data[features].mean()
    cluster_means = cluster_profiles.loc[cluster_num]

    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=player_means.values,
        theta=features,
        fill='toself',
        name=selected_player
    ))
    radar_fig.add_trace(go.Scatterpolar(
        r=cluster_means.values,
        theta=features,
        fill='toself',
        name=f'Cluster Avg ({cluster_name})'
    ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title="Strokes Gained Profile"
    )

    # Time series: sg_app and sg_putt over seasons
    ts_fig = go.Figure()
    ts_fig.add_trace(go.Scatter(
        x=player_data['season'],
        y=player_data['sg_app'],
        mode='lines+markers',
        name='SG App'
    ))
    ts_fig.add_trace(go.Scatter(
        x=player_data['season'],
        y=player_data['sg_putt'],
        mode='lines+markers',
        name='SG Putt'
    ))
    ts_fig.update_layout(
        title="Strokes Gained Over Seasons",
        xaxis_title="Season",
        yaxis_title="Strokes Gained",
        xaxis=dict(type='category')
    )

        # Summary info
    match_count = len(player_data)
    season_count = player_data['season'].nunique()

    # Clean pos column for win calculation
    pos_cleaned = player_data['pos'].astype(str).str.upper().str.strip()

    if 'tournament' in player_data.columns:
        num_tournaments = player_data['tournament name'].nunique()
        # Unique tournaments with win (1, 1.0, T1 etc.)
        win_tourneys_numeric = player_data.loc[player_data['pos'] == 1.0, 'tournament name'].unique()
        win_tourneys_text = player_data.loc[pos_cleaned == '1', 'tournament name'].unique()
        win_tourneys_t1 = player_data.loc[pos_cleaned == 'T1', 'tournament name'].unique()
        num_wins = len(set(win_tourneys_numeric) | set(win_tourneys_text) | set(win_tourneys_t1))
    else:
        num_tournaments = match_count  # fallback
        num_wins = (player_data['pos'] == 1.0).sum() + pos_cleaned.isin(['1', 'T1']).sum()

    summary = f"""
    **Player Name:** {selected_player}\n
    **Cluster:** {cluster_num}\n
    **Cluster Name:** {cluster_name}\n
    **Tournaments Played:** {num_tournaments}\n
    **Seasons Played:** {season_count}\n
    **Number of Wins:** {num_wins}
    """


    return radar_fig, ts_fig, summary

# Gradio interface
player_list = df['player'].dropna().unique().tolist()

with gr.Blocks() as demo:
    gr.Markdown("# 🏌️ PGA Player Dashboard")
    with gr.Row():
      with gr.Column(scale=1):
        player_dropdown = gr.Dropdown(choices=player_list, label="Select Player")
        summary_card = gr.Markdown()

      with gr.Column(scale=2):
        radar_plot = gr.Plot(label="Radar Chart")
        ts_plot = gr.Plot(label="Time Series Chart")


    player_dropdown.change(fn=player_dashboard, inputs=[player_dropdown],
                           outputs=[radar_plot, ts_plot, summary_card])

demo.launch()