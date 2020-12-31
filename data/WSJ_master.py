import WSJ_Classes
import ScrapeVolumes
import prepare_data
import ranking_viz
import pandas as pd
import pickle
import numpy as np

def main():
    #====== web scrape JP Media DB for WSJ data using Selenium+Chrome ====#
    # volume_urls = ScrapeVolumes.get_wsj_collection(webpage='https://mediaarts-db.bunka.go.jp/id/C119459') # get list of urls for WSJ volumes
    # issues = ScrapeVolumes.fill_issue_data(volume_urls[-200:-190])  # fill WSJ data found at each volume's url
    # with open('WSJ_issues_310521.pickle', 'wb') as f:   # save collection of Issues into pickle
    #     pickle.dump(issues, f, pickle.HIGHEST_PROTOCOL)

    with open('WSJ_issues_080621.pickle', 'rb') as f:  # open data
        issues = pickle.load(f)

    #==== prepare data ====#
    df = prepare_data.issues_to_df(issues)  # make pandas dataframe from issues class.
    manga_df = df[df['details'].str.contains('マンガ作品')]  # select only manga works
    manga_df = manga_df.drop_duplicates(['manga', 'issue_date'])  # TEMPORARY SOLUTION: NEED TO ADD TOTAL NUMBER OF PAGES TOGETHER, COLOR BINARY, ETC.
    manga_df.to_csv('WSJ_data.csv')  # output data as necessary

    #==== visualize ranking data ====#
    manga_XC = pd.read_csv('MangaJPCrossEN.csv', skipinitialspace=True)
    manga_list = list(manga_XC.JP[0:100])
    ranked_df = ranking_viz.set_rank_by_volume(manga_df)  # set manga ranking by order of appearence
    ranking_viz.viz_vol_ranks(manga_list, ranked_df)  # graph rankings

    xs = ranked_df[ranked_df.manga == 'ONE PIECE']['issue_date']
    ys = ranked_df[ranked_df.manga == 'ONE PIECE']['rank']
    data = np.array([xs, ys])
    ranking_viz.animated_linegraph(data)


if __name__ == '__main__':
    main()
