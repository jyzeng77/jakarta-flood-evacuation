# Flood extent and evacuation in Jakarta

## Project brief

This project examines whether the number of flooded neighbourhoods is enough to guide evacuation planning. It uses the January 2020 flood in DKI Jakarta to compare how quickly flooding receded and how long residents continued to use evacuation sites. The analysis also compares January with other recorded flood months to see how closely flood extent tracked peak displacement.

## Data and method

- The daily series covers 1–7 January 2020. It records evacuees, evacuation sites and flooded neighbourhood units (*Rukun Warga*, or RW). The briefing gives no comparable RW count for 1 January, so that value is blank. [Jakarta Flood Recovery 2020, pp. 3–5](https://www.scribd.com/document/459137424/Jakarta-Flood-Recovery-2020)
- The historical series contains 14 months listed in Jakarta's 2014–2020 flood summary. It records affected RW and the highest reported evacuee count in each listed month. [Pantau Banjir, “TERTINGGI” tab](https://docs.google.com/spreadsheets/d/1ZgyMQY0o0tFDIXn7tA5kcjfTk3wzasj28RTMW4puA4U/edit)

The script uses pandas to calculate daily changes and divide the reported evacuee count by the number of reported sites. It uses NumPy to calculate the Spearman rank correlation between affected RW and peak evacuees across the 14 months.

## Results

| January 2020 | Flooded RW | Reported evacuees | Reported sites | Evacuees per site |
| --- | ---: | ---: | ---: | ---: |
| 1 Jan | — | 31,232 | 269 | 116.1 |
| 2 Jan | 390 | 36,445 | 247 | 147.6 |
| 5 Jan | 3 | 3,206 | 10 | 320.6 |
| 7 Jan | 0 | 691 | 6 | 115.2 |

Reported evacuees peaked on 2 January, up 16.7% from the previous day, while the number of sites fell 8.2%. The ratio of evacuees to sites peaked three days later, at about 321 per site. On 7 January, the city reported zero flooded RW, but still recorded 691 evacuees and six sites.

Across the 14 listed months, affected RW and peak evacuees tended to rise together (Spearman ρ = 0.771). February 2020 illustrates the limits of that relationship. It had 49.0% more affected RW than January, but 62.1% fewer evacuees at its peak. Tracking evacuee counts alongside flood extent gives planners a better basis for deciding when to scale back site staffing and supplies.

The counts are citywide and cannot establish occupancy or capacity at individual sites. The recovery briefing also notes that residents used sites while cleaning their homes, so the daily figures cannot establish overnight shelter demand.

## Reproduce

Run with Python 3.12 from the repository directory.

```sh
python -m pip install -r requirements.txt
python analyze.py
```

The script reads the included CSVs and writes [daily metrics](results/daily_metrics.csv) and a [summary](results/summary.json).
