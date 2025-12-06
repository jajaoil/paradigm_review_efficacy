import pandas as pd
import krippendorff

def compute_alpha(path='../data/coding_sheet.csv'):
    df = pd.read_csv(path)
    # assumes columns coder1_label coder2_label
    matrix = df[['coder1_label','coder2_label']].T.values
    alpha = krippendorff.alpha(reliability_data=matrix, level_of_measurement='nominal')
    return alpha

if __name__ == '__main__':
    alpha = compute_alpha()
    print('Krippendorff alpha', alpha)
