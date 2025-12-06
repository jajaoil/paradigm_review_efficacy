import pandas as pd

def compute_average_tlx(df):
    cols = ['mental_demand','physical_demand','temporal_demand','performance','effort','frustration']
    for c in cols:
        if c not in df.columns:
            raise ValueError(f"Missing column {c}")
    # simple average method
    df['tlx_score'] = df[cols].mean(axis=1)
    return df

if __name__ == '__main__':
    df = pd.read_csv('../data/nasa_tlx_raw.csv')
    df = compute_average_tlx(df)
    df.to_csv('../data/nasa_tlx_scored.csv', index=False)
    print(df[['participant_id','session_id','tlx_score']].head())
