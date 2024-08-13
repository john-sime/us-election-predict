##Motivation
I collated the data used in this project, with the underlying data coming from various sources:
*FiveThirtyEight: A polling aggregator from which the final pre-election polling numbers for each state were sourced, as well as the current polling numbers for the 2024 election. https://projects.fivethirtyeight.com/polls/president-general/2024/
*Wikipedia: Used to cross-reference final pre-election polling numbers where available, and the final statewise election vote numbers for 2016 and 2020. https://en.wikipedia.org/wiki/2020_United_States_presidential_election#Results
FiveThirtyEight is a subsidiary of the ABC news group, and performs political analysis to inform their users about relevant information regarding politics and elections. They are known for aggregating polling data and for predicting election results.

##Composition
The pre-election polling data consists of percentages that supported the Democratic or Republican candidate, or were otherwise uncommitted or support third party candidates, in the period just prior to the election date.
These are taken from polling aggregators to provide an "average" polling figure.
The election results data consists of percentages that voted for the Democratic or Republican candidate, or voted for a different candidate (denoted as "Other").
The current polling data consists of percentages that support the presumptive Democratic or Republican candidate at the time of the polls, or were otherwise uncommitted or supported third party candidates.
The current polling data date used for this project is 20 July 2024, which is the day prior to when President Biden stood down as the Democratic candidate. The Republican candidate for these polls is President Trump.

The data is broken down by state and by congressional district where applicable.
This means that for the pre-election polling data there are 112 rows of data - 50 states, 3 congressional districts of Nebraksa, 2 congressional districts of Maine, plus the District of Columbia, across two elections each.
The current polling data is similarly broken down by state and by congressional district where applicable, but with absences for Delaware, the District of Columbia, and the first and third congressional districts of Nebraska.
There have not been any polls reported for these locations in the 2024 Election Cycle. This is presumably due to Delaware and D.C. being considered as Democrat strongholds, and similarly for the congressional districts of Nebraska being considered strongholds for the Republicans.
This means that for the current polling data there are 52 rows of data.

##Collection Process
The polling aggregation data was collected by FiveThirtyEight and wikipedia as a consequence of the underlying pollsters publishing their findings. These are typically from sample sizes of 700-1000 from either "Likely Voters" or from Registered Voters.
The timeframe for each underlying poll is typically between 3-14 days.

##Preprocessing/cleaning/labelling
For the pre-election polling data and for the election results data, some data cleaning was required due to the percentages not adding to 100% in some instances. This cleaning was performed manually by cross-referencing between the data sources.
Further, the data was pre-processed by putting the Libertarian/Green party support %s into an "Other" category, alongside any residual % from uncommitted voters, or support for other minor candidates.
The data relating to Utah 2016 was removed from the final dataset due to the outlier support and vote share for an independent candidate in that state.

For the current polling data, the average was taken from polls dated within 30 days of 20 July 2024, or the nearest dated poll where no polls within 30 days existed.
Where there is a choice between a poll that considers 2 candidates only, and a poll with multiple candidates, chosen the poll with 2 candidates for the sake of consistency with the pre-election polling data.
Where multiple polls are from the same source, these polls are averaged to avoid weighting issues between poll sources.

##Uses
The dataset can be used for any analysis relating to the relationship between pre-election polling averages and final election results for the US presidential elections. In particular, this project can be updated to consider future polling numbers.

##Distribution
The dataset can be viewed and used from this publicly available google sheet: https://docs.google.com/spreadsheets/d/1byPOPY8E6ImigvaPBOo7npWcA5zB4IWwFhoRuKYUzpg/edit?usp=sharing

##Maintenance
I am responsible for maintaining this dataset, however I will likely not update it in future.
