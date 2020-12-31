import csv
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

def set_rank_by_volume(manga_df):
    manga_df['rank'] = 0
    dates = manga_df['issue_date'].unique()

    # for each issue, set rank as each manga's order of appearance.
    for date in dates:
        df = manga_df[manga_df['issue_date'] == date]
        df['rank'] = range(len(df.index))  # rank from 0 - # manga
        manga_df[manga_df['issue_date'] == date] = df

    return manga_df

def viz_vol_ranks(manga_list, manga_df):
    manga_XC = pd.read_csv('MangaJPCrossEN.csv', skipinitialspace=True) # import cross walk

    df = manga_df[manga_df['manga'].isin(manga_list)]  # select specific manga
    df = df.merge(manga_XC, left_on='manga', right_on='JP')  # merge in English name
    df = df.pivot(index='EN', columns='issue_date', values='rank')  # pivot to fill in time series manga rankings
    dates = np.array(df.columns)

    # set font
    plt.rc('font', family='TakaoPGothic')
    plt.clf()
    fig, ax = plt.subplots()
    for index, row in df.iterrows():  # plot each manga's rankings over the dates
        ax.plot(dates, row.values)

    ax.set_title('Weekly Shōnen Jump manga rankings')
    ax.legend(df.index)
    plt.gca().invert_yaxis()
    plt.xlabel('Volume Issue')
    plt.xticks(rotation=45)
    plt.ylabel('WSJ rank')
    plt.show()

    fig.set_size_inches(20, 10)
    fig.savefig('test.png', dpi=200)


# plot a manga's ranking over time.
def viz_manga_rank(manga_title, df):
    manga = df[df['manga'] == manga_title]
    x = manga['issue_date']
    y = manga['rank']

    # plot
    plt.plot(x, y)
    plt.xlabel('Issue Date')
    plt.xticks(rotation=45)
    plt.ylabel('WSJ rank')

    plt.gca().invert_yaxis()  # invert y-axis for visual clarity
    plt.title(str(manga_title) + ' ranking')
    plt.show()

def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

def animated_linegraph(data):
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

    fig1 = plt.figure()
    plt.xlabel('x')
    plt.title('test')
    line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data),  interval=50)
    line_ani.save('lines.mp4', writer=writer)

def main():
    manga_df = pd.read_csv('WSJ_data.csv')

    manga_df = set_rank_by_volume(manga_df)

    viz_manga_rank('ONE PIECE', manga_df)
    manga_list = ['ONE PIECE', 'BLEACH', 'HUNTER×HUNTER', 'NARUTO-ナルト-']
    viz_vol_ranks(manga_list, manga_df)


if __name__ == '__main__':
    main()
