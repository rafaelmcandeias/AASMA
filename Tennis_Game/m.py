import pandas as pd

for mode in ('random', 'beginner', 'expert', 'pro'):
    path = 'results/' + mode + '.csv'
    df = pd.read_csv(path)

    df.columns = ['Wins', 'Score']
    df.to_csv(path)