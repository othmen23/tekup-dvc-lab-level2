import numpy as np
from sklearn.datasets import load_iris

rng = np.random.default_rng(42)
df = load_iris(as_frame=True).frame
df = df.sample(n=600, replace=True, random_state=42).reset_index(drop=True)

feature_cols = [c for c in df.columns if c != "target"]
df[feature_cols] = df[feature_cols] + rng.normal(0, 0.05, size=(600, len(feature_cols)))
df[feature_cols] = df[feature_cols].round(2)

df.to_csv("data/iris.csv", index=False)
print(df.shape)