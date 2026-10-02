# 📺 TV Channel Broadcast & Engagement Performance Report

## Executive Summary
This analytical report delivers comprehensive intelligence on television broadcasting metrics, viewer engagement levels, digital outreach (YouTube, Social Media), and content ratings across major broadcasting networks.

---

## 🚀 Key Network KPIs
- **Total Monitored Broadcast Records**: 60,249
- **Distinct Channels Evaluated**: 10
- **Distinct Shows Catalogued**: 27
- **Average Viewership**: 6,136,496 viewers (Median: 6,116,831)
- **Average Show Rating**: 3.65 / 5.0 (Range: 0.0 - 4.9)
- **Average YouTube Views**: 49,984,069
- **Average Social Followers**: 4,049,336
- **Average Monthly Reach**: 17,438,601
- **Average Subscription Fee**: ₹274.78

---

## 🧹 Data Quality & Preprocessing Audit
- **Initial Raw Rows**: 60,249
- **Missing Value Imputations**: Resolved across all numeric and categorical attributes using hierarchical group-aware median/mode imputation.
- **Entity Resolution**: Canonicalized channel variations (e.g. *SunTV* → *Sun TV*, *Vijay  TV* → *Vijay TV*, *ZeeTamil* → *Zee Tamil*, *Colorstamil* → *Colors Tamil*).
- **Out of Range Cleanups**: Corrected 48 invalid ratings and 44 negative subscription fees.
- **Final Valid Dataset Records**: 60,249 (0 nulls remaining).

---

## 🏆 TV Channel Leaderboard & Power Index
The **Power Index** represents a weighted composite score combining Viewership (35%), Content Ratings (25%), Social Likes (15%), YouTube Views (15%), and Social Followers (10%).

| Channel_Name   |   Avg_Viewers |   Avg_Rating |   Total_Likes |   YouTube_Views |   Social_Media_Followers |   Monthly_Reach |   Subscription_Fee |   Record_Count |   Power_Index |
|:---------------|--------------:|-------------:|--------------:|----------------:|-------------------------:|----------------:|-------------------:|---------------:|--------------:|
| Star Sports    |   6.1826e+06  |      3.65725 |        496113 |     5.0148e+07  |              4.06457e+06 |     1.76222e+07 |            272.749 |           6035 |         89.22 |
| Colors Tamil   |   6.16203e+06 |      3.65923 |        490435 |     5.00935e+07 |              4.04316e+06 |     1.7445e+07  |            278.013 |           5931 |         74.02 |
| Jaya TV        |   6.16031e+06 |      3.65242 |        493663 |     5.02587e+07 |              4.05629e+06 |     1.73677e+07 |            273.213 |           6004 |         76    |
| Raj TV         |   6.15454e+06 |      3.63965 |        491099 |     5.00726e+07 |              4.02378e+06 |     1.75932e+07 |            276.197 |           5829 |         49.14 |
| Zee Tamil      |   6.1504e+06  |      3.64115 |        493017 |     4.98346e+07 |              4.04905e+06 |     1.754e+07   |            274.1   |           5934 |         52.58 |
| KTV            |   6.14352e+06 |      3.66114 |        499025 |     4.96786e+07 |              4.05404e+06 |     1.75195e+07 |            274.949 |           5978 |         71.84 |
| Vijay TV       |   6.13909e+06 |      3.63706 |        489664 |     5.01144e+07 |              4.03907e+06 |     1.74628e+07 |            274.701 |           5982 |         45.4  |
| Kalaignar TV   |   6.10992e+06 |      3.64644 |        486052 |     5.0085e+07  |              4.04681e+06 |     1.72788e+07 |            273.125 |           6544 |         43.55 |
| Sun TV         |   6.09667e+06 |      3.66432 |        486639 |     4.94392e+07 |              4.0599e+06  |     1.72465e+07 |            274.086 |           6023 |         47.71 |
| Sony Sports    |   6.06902e+06 |      3.63894 |        479797 |     5.01096e+07 |              4.05597e+06 |     1.73304e+07 |            276.901 |           5989 |         21.88 |

---

## 🎭 Performance by Show Category
Evaluation of content genres by average viewership, audience ratings, and digital engagement.

| Show_Category   |   Avg_Viewers |   Avg_Rating |   Total_Likes |   YouTube_Views |   Monthly_Reach |   Total_Episodes_Count |
|:----------------|--------------:|-------------:|--------------:|----------------:|----------------:|-----------------------:|
| Music           |   6.1642e+06  |      3.63688 |        490477 |     5.0066e+07  |     1.75558e+07 |                   5990 |
| Reality         |   6.16185e+06 |      3.64838 |        492700 |     4.99326e+07 |     1.75697e+07 |                  10731 |
| Movies          |   6.13572e+06 |      3.65466 |        496217 |     4.98018e+07 |     1.74777e+07 |                   9684 |
| Comedy          |   6.13008e+06 |      3.65469 |        487441 |     5.00375e+07 |     1.73392e+07 |                   7316 |
| Serial          |   6.12539e+06 |      3.65562 |        489482 |     4.99316e+07 |     1.73163e+07 |                  13191 |
| Sports          |   6.12437e+06 |      3.64701 |        487615 |     5.01278e+07 |     1.74682e+07 |                  12128 |
| Cooking         |   6.062e+06   |      3.62084 |        484180 |     5.03023e+07 |     1.70213e+07 |                   1209 |

---

## 🌟 Top Flagship Shows
### Most Viewed Shows per Channel
| Channel_Name   | Popular_Show     | Show_Category   |   Avg_Viewers |
|:---------------|:-----------------|:----------------|--------------:|
| Vijay TV       | Serials          | Serial          |      11999964 |
| Sony Sports    | Cricket          | Sports          |      11999757 |
| Jaya TV        | Special Programs | Reality         |      11999427 |
| Raj TV         | Comedy Shows     | Comedy          |      11999407 |
| Kalaignar TV   | Special Programs | Reality         |      11999393 |

### Highest Rated Shows per Channel
| Channel_Name   | Popular_Show     | Show_Category   |   Avg_Rating |
|:---------------|:-----------------|:----------------|-------------:|
| Colors Tamil   | Comedy Shows     | Comedy          |          4.9 |
| Jaya TV        | Special Programs | Reality         |          4.9 |
| KTV            | Comedy Movies    | Movies          |          4.9 |
| Kalaignar TV   | Music Shows      | Music           |          4.9 |
| Raj TV         | Serials          | Serial          |          4.9 |

---

## 📡 HD vs. Standard Definition (SD) Impact
| HD_Available   |   Avg_Viewers |   Avg_Rating |   Total_Likes |   YouTube_Views |   Total_Broadcasts |
|:---------------|--------------:|-------------:|--------------:|----------------:|-------------------:|
| No             |   6.18191e+06 |      3.64511 |        493126 |     4.96556e+07 |               7158 |
| Yes            |   6.13037e+06 |      3.6504  |        490154 |     5.00284e+07 |              53091 |

---

## 📊 Visual Artifacts
High-resolution visualizations have been rendered to `reports/figures/`:
1. `01_viewers_by_channel.png`: Channel-wise Average Viewership
2. `02_ratings_by_channel.png`: Channel-wise Average Ratings
3. `03_digital_engagement.png`: YouTube Views vs. Social Media Followers
4. `04_viewers_by_show_category.png`: Viewership Across Show Categories
5. `05_distributions.png`: Audience Viewership & Rating Distribution Curves
6. `06_channel_market_share.png`: Broadcast Catalog Share by Channel
7. `07_correlation_heatmap.png`: Cross-Metric Correlation Matrix
