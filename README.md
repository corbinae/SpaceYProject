# SpaceYProject
Final Project for IBM Data Science Certificate

## Overview
- we will predict if the Falcon 9 first stage will land successfully.
- SpaceX advertises Falcon 9 rocket launches on its website, with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.

## Module 1
- we use a REST API to connect to info about the SpaceX launches
- extract all the Falcon 9 launches and saved it dataset_part_1.csv (notebook spacex-data-collection)
- did additional webscrapping from wiki pages and added to dataset_part_1 (notebook labs-webscrapping)

## Module 2
- worked on data wrangling to better format the data (notebook spacex-Data wrangling)
- one hot encoded landing outcomes
- boolean for success vs failure outcomes
- csv dataset_part_2

## Module 3
- sql analysis (notebook eda sql)
    -  data exploration on landing sites, landing outcomes, booster variables, etc.
- then did EDA via visualization - final csv dataset part 3 (notebook eda-dataviz)