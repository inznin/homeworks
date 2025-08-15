import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ::. Generate synthetic data ::.
def generate_data(num_rows=1000):
    np.random.seed(42)

    date_range = pd.date_range(start="2025-05-01", end="2025-07-31", freq="H")
    event_types = ["comment", "like", "play_video", "login", "logout"]
    platforms = ["web", "iOS", "android"]

    df = pd.DataFrame({
        "event_id": np.arange(1, num_rows + 1),
        "user_id": np.random.randint(1, 201, size=num_rows),
        "timestamp": np.random.choice(date_range, size=num_rows),
        "platform": np.random.choice(platforms, size=num_rows),
        "event_type": np.random.choice(event_types, size=num_rows)
    })

    df["video_id"] = np.where(
        df["event_type"] == "play_video",
        "vid_" + np.random.randint(1, 51, size=num_rows).astype(str),
        None
    )
    df["watch_time_sec"] = np.where(
        df["event_type"] == "play_video",
        np.random.randint(10, 301, size=num_rows),
        None
    )

    return df

df = generate_data()

# .:: Convert timestamp ::.
df["timestamp"] = pd.to_datetime(df["timestamp"])

# .:: Map engagement scores ::.
score_map = {
    "comment": 5,
    "like": 3,
    "play_video": 1,
    "login": 0,
    "logout": 0
}
df["engagement_score"] = df["event_type"].map(score_map)

# .:: Aggregate by date and platform ::.
df["date"] = df["timestamp"].dt.date
daily_df = df.groupby(["date", "platform"])["engagement_score"].sum().reset_index()

# .:: Pivot data ::.
pivot_df = daily_df.pivot(index="date", columns="platform", values="engagement_score").fillna(0)

# .:: Plot heatmap ::.
plt.figure(figsize=(12, 10))
sns.heatmap(pivot_df, cmap="YlOrRd", linewidths=0.5)
plt.title("Daily Engagement Score by Platform", fontsize=14)
plt.xlabel("Platform")
plt.ylabel("Date")
plt.tight_layout()
plt.show()