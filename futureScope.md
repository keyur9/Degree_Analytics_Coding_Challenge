# Degree Analytics Coding Challenge

## Requirements:

Create a python flask/django API that shows a chart and data projection for the amount of Python and R Repos that will be created over the next 5 years on Github (use the github api for retrieving data)

## Future Scope

Following features could be added to improve the experience.

####  Confidence Interval

We could plot confidence interval along with prediction graph using Google charts, matplotlib or other similar API/packages.

####  Github Authentication

We could provide authentication functionality with Github which would increase the rate fetching limit per minute.

####  Nginx

We could deploy Nginx proxy server in front of API server and have Nginx redirect request to API server which will not expose API to the external sources.

####  User Interface

We could make User Interface interactive and dynamic.

####  How to make model better?

We could go to more granular level by fetching data on month/day basis instead of year to gather more data points. NOTE: This would be possible based on Github API rate fetching limit at that point in time.
