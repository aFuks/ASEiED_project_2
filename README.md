## ASEiED_project_2

# Air Traffic Data Analysis

## Project Objective

The objective of this project is to analyze air traffic data to identify major trends and patterns. The analyzed data is sourced from the OpenSky Network, enabling a comprehensive understanding of air traffic dynamics on selected routes.

## Data Source

The data for this analysis is sourced from the OpenSky Network: [OpenSky Network Datasets](https://opensky-network.org/datasets/states/)

## Technologies

The following technologies are utilized in this project:
- **AWS EMR**: Managed big data platform in the cloud
- **Apache Spark**: Data processing engine
- **Python**: Programming language used for data analysis and visualization

## Project Requirements

1. **Data Analysis**: Analyze air traffic data on selected routes.
2. **Visualization**: Visualize the relationship between the number of flights and global events.
3. **Publication**: Publish the source code and report on GitHub.
4. **Documentation**: Document the project details in the README.md file.

## Implementation summary

The project is carried out in several stages:
1. **Data Collection**: Download and prepare data from the OpenSky Network.
2. **Data Processing**: Use Apache Spark to process large datasets.
3. **Analysis and Visualization**: Analyze the data using Python and create visualizations of the results.
4. **Documentation and Publication**: Prepare a detailed report and publish the results on GitHub.

## Implementation details

### Data Collection
Data were collected on the following days: "2020-06-29", "2021-08-30", "2021-11-29", "2021-12-20", "2022-02-28". We considered data from the entire day to ensure that time zones would not affect our analysis. One day's data occupies a little over 10GB, so we decided to select only a few specific days that we believed would best reflect changes in air traffic.

We extracted data for three locations for the analysis: Warsaw, Ukraine, and Louisiana. The selection of these places was not random and was related to global events.

- 2020-06-29: the period during which airports in Poland were closed due to the pandemic. We associated this date with Warsaw.
- 2021-08-30: Hurricane Ida passed through Louisiana.
- 2021-11-29: the eruption of the Cumbre Vieja volcano on La Palma, which created a large smoke cloud.
- 2021-12-20: the approaching holiday season, during which we wanted to observe an increased number of flights.
- 2022-02-28: the escalation of the conflict in Ukraine.

### Data Processing
To extract the connections of interest from the massive dataset, we used AWS EMR and a cluster with Apache Spark, which created a smaller file with the data we were interested in. We encountered an issue with accessing the data in S3, but we resolved it by adding the AmazonS3FullAccess policy to the AmazonEMR-InstanceProfile and AmazonEMR-ServiceRole roles.

### Analysis and Visualization
The data can be visualized in the program. The user can select the area and date, based on which flights in that region will be displayed on the map, and a graph showing the number of flights per hour will be created.

![att TUcJvawOAl-rh-OSKfLnnQPs96n82TjWpHlFZnhbNsY](https://github.com/aFuks/ASEiED_project_2/assets/96986297/0f61fe17-6113-47f2-9308-03bd5f43edfb)
<p align="center"><i>fig. 1 Main GUI layout without any data selected.</i></p>
<br>

![att MI0V_nKf1-mlqgvBJqFwpqGPBIrsMdjHAVAnS5KpV3g](https://github.com/aFuks/ASEiED_project_2/assets/96986297/8a983662-9224-4f80-a4be-226f3a604d80)
<p align="center"><i>fig. 2 GUI showing data from Warsaw region on 28.02.2022.</i></p>
<br>

![att YLGzM2QVQSo98if1RZqYdBkmbX94Kyi3jQzXvGSS9rc](https://github.com/aFuks/ASEiED_project_2/assets/96986297/618dcb7c-1da5-4336-ab62-8aa229e0fed0)
<p align="center"><i>fig. 3 GUI showing data from Ukraine region on 30.08.2021.</i></p>
<br>

![att 9rsemSbzHLtkdNBe7tTxgBZjkLRk__Jcx5FSgWeigYQ](https://github.com/aFuks/ASEiED_project_2/assets/96986297/96150c90-dfa8-4d8b-a5bd-6f222e1f9156)
<p align="center"><i>fig. 4 GUI showing data from Louisiana region on 28.02.2022. On the chart, the difference in time zones is clearly visible compared to fig. 1 and fig. 2.</i></p>
<br>

![att u9oQQ95YytkFVSxgSuiProfSLbwQIcNDIwih6bxoobs](https://github.com/aFuks/ASEiED_project_2/assets/96986297/d22f455a-ca00-4afc-a3bc-fa830467678e)
<p align="center"><i>fig. 5 Handling a situation where there is no data for a given day.</i></p>
<br>

A summary graph showing flight intensity in the regions for all dates was also created.
![obraz](https://github.com/aFuks/ASEiED_project_2/assets/106777205/2552de7c-0a85-4077-a8e9-5c5432bc70d4)
<p align="center"><i>fig. 6 Chart with all combined data.</i></p>

<br>

As seen in the attached graphs, global events have a noticeable impact on the number of flights. A noticeable decrease in flights in all locations is observed during the pandemic. At the time of the escalation of the conflict in Ukraine, all air traffic was suspended. Increased air traffic in all locations is visible during the pre-holiday period.

![image](https://github.com/aFuks/ASEiED_project_2/assets/106623070/465cf4af-6197-4415-9bdb-7f0c4804e818)



---



