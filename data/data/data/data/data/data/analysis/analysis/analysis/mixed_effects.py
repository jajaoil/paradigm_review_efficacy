import pandas as pd
import statsmodels.formula.api as smf

# mixed effects for comprehension time in within participant design
df = pd.read_csv('../data/timing_raw.csv')
# ensure paradigm is categorical
df['paradigm'] = df['paradigm'].astype('category')
# mixed effects model
md = smf.mixedlm("comprehension_time_seconds ~ C(paradigm) + participant_role", df, groups=df["participant_id"])
mdf = md.fit(reml=False)
print(mdf.summary())

# for defect detection per participant using logistic regression aggregated per participant
df_def = pd.read_csv('../data/defects_per_participant.csv')
import statsmodels.api as sm
model = sm.GLM(df_def['total_found'], sm.add_constant(pd.get_dummies(df_def['participant_id'], drop_first=True)), family=sm.families.Binomial())
# model here is a placeholder show how to adapt per design
print('Please run custom logistic mixed effects in R lme4 or Python using binomial mixed models depending on defect level data')
