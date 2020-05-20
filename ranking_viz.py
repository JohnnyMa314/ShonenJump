import csv
import matplotlib.pyplot as plt
import pandas as pd


def main():
    manga_df = pd.read_csv('WSJ_data.csv')

    manga_df['rank'] = 0
    dates = manga_df['issue_date'].unique()

    # for each issue, set rank as each manga's order of appearance.
    for date in dates:
        df = manga_df[manga_df['issue_date'] == date]
        df['rank'] = range(len(df.index))  # rank from 0 - # manga
        manga_df[manga_df['issue_date'] == date] = df

    viz_manga_rank('ONE PIECE', manga_df)

# plot a manga's ranking over time.
def viz_manga_rank(manga_title, df):
    manga = df[df['manga'] == manga_title]
    rank_data = manga[['issue_date', 'rank']]
    x = manga['issue_date']
    y = manga['rank']

    plt.plot(x,y)

    plt.xlabel('Issue Date')
    plt.xticks(rotation=45)
    plt.ylabel('WSJ rank')

    plt.gca().invert_yaxis() # invert y-axis for visual clarity
    plt.title(str(manga_title) + ' ranking')
    plt.show()

if __name__ == '__main__':
    main()
