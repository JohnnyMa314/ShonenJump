# Weekly Shōnen Jump Ranking Analysis
![IMAGE ALT TEXT HERE](https://dwgkfo5b3odmw.cloudfront.net/manga/thumbs/thumb-30705-p000_Cov_071618-3.jpg)

![](http://i.imgur.com/9oUdCJg.png)

Weekly Shōnen Jump is the best-selling manga magazine in Japan. Many iconic manga series such as *Dragon Ball Z*, *One Piece*, and *Slam Dunk*, were originally published in the magazine. Each volume of WSJ contains 10-20 serialized manga, each with 15-20 pages of content, separated by advertisements and other materials. The magazine contains largely narratives targeted towards young boys (the definition of *shōnen* being "boy" or "youth"), and typically feature action, drama, and comedy centered around male protagonists. However, the readership demographics are diverse in both age and gender and have wide international appeal. While WSJ volume sales peaked in the mid 1990s, the cultural significance of manga and anime franchises that first appear in WSJ are increasing, especially as licensed English translations published by Viz Media and english anime distributed by Netflix and Crunchyroll are becoming more available. 

In this project, we are interested in one specific aspect of WSJ: the weekly ranking system. For each issue of *Jump*, readers send in a survey postcard detailing their favorite three series that week, how many series they read, and demographic information. These ratings are collected by the editors at the publishing company, *Shueisha*, who spend 6 or so weeks to create weighted ranking of the series each week. The 6 week lagged rankings roughly determine the order in which the manga appear in the volume, with each week's most popular series closest to the front and the least popular in the back. While some series may be placed in the front due to special events (anime announcement, anniversary), we can back engineer the rankings from the Table of Contents and understand when each series gains or loses popularity on a roughly week-to-week basis. 

While many of these details are obscured by the WSJ editing staff, the authors, or *mangaka*, often share the details of their work schedule and reactions to the rankings. One popular manga series *Bakuman* details the journey of a teenage manga artist and writer duo as they aspire to become succesful *mangaka*, sharing much of the previous information and more. 

We are interested in analyzing the content of Weekly Shōnen Jump to understand manga popularity. Specifically, we want to extract various visual and textual features from each manga series and correlate these factors with either weekly or monthly ranking changes.  

---

This is the methodology we plan to employ. We will align the rankings with manga release 8 weeks ago. 

### RANKINGS

- [x] Extract table of contents data for WSJ volumes (1990s-2019) from Japanese database "Media Arts Database" created by the Agency for Cultural Affairs.
- [x] Recreate rankings over time by series using ToC, including color + anniversary placements
- [ ] *OPTIONAL: Scrape sales data by vol. for each series*
- [ ] *OPTIONAL: Scrape reddit comments for each chapter from /r/manga*
- [ ] Recreate the following graphs
![](https://lh5.googleusercontent.com/-KTOhUBDM9CI/UoySCn7qWRI/AAAAAAAAevE/z0iT_Ue4VgY/w969-h724-no/TOC-2013.png)

### CONTENT

- [ ] Scrape high quality series pages (official translation + orignial japanese). 
- [ ] Collect dialogue data from each page (translate to english)
- [ ] Use visual classifier to identify and count number of panel types. (Manga109 Dataset, CNN for scene extraction.)
- [ ] Scrape plot summaries from wikipedia (or fan source such as *MyAnimeList.com* and Fandom.org)
