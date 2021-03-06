import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = df['cholesterol'] > 1
df['gluc'] = df['gluc'] > 1

df_normal = df.replace({False: 0, True: 1})

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df_normal, id_vars='cardio', value_vars=[
        'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable', hue='value', col='cardio',
                      kind='count', data=df_cat)


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    height_low_percentile = df_normal['height'].quantile(0.025)
    height_high_percentile = df_normal['height'].quantile(0.975)

    weight_low_percentile = df_normal['weight'].quantile(0.025)
    weight_high_percentile = df_normal['weight'].quantile(0.975)
    df_heat = df_normal[~((df['ap_lo'] > df['ap_hi']) | (df['height'] < height_low_percentile) | (df['height'] > height_high_percentile) | (
        df['weight'] < weight_low_percentile) | (df['weight'] > weight_high_percentile))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr.columns)



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, mask=mask, annot=True,
                fmt='.1f', square=True, cbar_kws={'shrink': 0.5})


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
