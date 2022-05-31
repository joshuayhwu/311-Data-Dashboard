# 311-Data-Repository

This repository is the prototype dashboard for the HackForLA 311 Data Project version 2 website.

City of LA provided open access to 311 Request Data reported by residents on incidents such as bulky items, animal remains, or water waste present in the area.

The current prototype has two dashboards, one containing the summary for the neighborhood dashboard, the other one contains a dashboard for comparison between neighbhood councils. 

Neighborhood Council Summary Dashboard: 

![plotly_mvp_v1 2](https://user-images.githubusercontent.com/77765986/171287642-c660ab76-ae0e-4871-b9aa-5b45692c81f1.PNG)

Visuals: 
1) Line Chart: Total number of 311 Requests over the time range as defined by the earliest request create date and latest request create date. This shows which specific time range has the most request
2) Pie Chart: Share of request type based on the data available. This shows what kind of request has the highest/lowest demand in a particular neighborhood council
3) Histogram: Distribution of request time to close This shows how long it takes for each request to complete (proxied by close request) as a distribution


Features:
1) Selecting individual neighbhood council
2) Removing particular request types
3) Data Quality Toggle to filter data with quality issues (where the time to close is less than 1 day or longer than 100 days)

Neighborhood Council Comparison Dashboard

![plotly_mvp_v1 2_2](https://user-images.githubusercontent.com/77765986/171287996-f6b75172-1112-426e-9c14-78a0e32c66e4.PNG)


Visuals: 
1) Indicator Visuals: Total number of requests and the number of days of the data available 
2) Bar Chart: Number of requests by sources. This indicators show the variety of mediums individuals make request through
3) Line chart: total number of 311 request comparison


## Setting Up

1) Pull the 311-Data-Dashboard repository on your terminal. Or just download it.
```
git pull https://github.com/joshuayhwu/311-Data-Dashboard/
```
3) Run the following in the terminal 
```
pip install -r requirements.txt
```
4) Run the dash app locally 
```
python app.py
```
