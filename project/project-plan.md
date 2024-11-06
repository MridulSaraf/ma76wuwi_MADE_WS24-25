# Project Plan

## Title
<!-- Give your project a short title. -->
Impact of Electric Vehicle Adoption on Climate Change in the Americas

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
Is there a measurable correlation between adopting electric vehicles (EVs) and reductions in greenhouse gas (GHG) emissions, indicating a positive impact on climate change in the Americas?
## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
This project aims to assess whether the increase in electric vehicle (EV) adoption in the Americas contributes to climate change mitigation. EVs are promoted as a sustainable alternative to traditional vehicles, with the potential to reduce greenhouse gas emissions and reliance on fossil fuels. By examining trends in EV adoption alongside reductions in CO2 emissions and other climate-relevant factors, this project will evaluate if EV adoption has an observable impact on slowing climate change. ## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: International Energy Agency (IEA) – Global EV Data Explorer
* Metadata URL: https://www.iea.org/reports/global-ev-outlook-2023
* Data URL: https://www.iea.org/data-and-statistics/data-tools/global-ev-data-explorer
* Data Type: CSV
This dataset provides information on electric vehicle(EV) adoption rates, including EV stock, sales data, and infrastructure(charging points) across various major and populated cities/countries in the Americas

### Datasource2: International Monetary Fund (IMF) – Climate Change Indicators Dashboard
* Metadata URL:  https://climatedata.imf.org/
* Data URL: https://climatedata.imf.org/pages/greenhouse-gas-emissions
* Data Type: CSV 

The IMF's Climate Change Indicators Dashboard offers data on greenhouse gas emissions, including CO2 emissions, for various countries. This resource allows for examining changes in emissions levels over time, which can be compared with EV adoption rates to assess any potential correlation.
## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Prior to conducting correlation analysis, we will preprocess both datasets by cleaning unwanted columns and ensuring consistency in date and country code formats [#1][i1]
2. Make the working pipeline to get curated data [#2][i2]
3. Plot EDA trends of CO<sub>2</sub> emissions and EV sales in the same time frame. Using these parameters we will try to find the impact regarding the increase in EV sales and Climate change[#3][i3]
4. Make assumptions and try to find the correlation between the two datasets (CO<sub>2</sub>emissions and EV sales) [#4][i4]


[i1]: https://github.com/MridulSaraf/ma76wuwi_MADE_WS24-25/issues/1
[i2]: https://github.com/MridulSaraf/ma76wuwi_MADE_WS24-25/issues/2
[i3]: https://github.com/MridulSaraf/ma76wuwi_MADE_WS24-25/issues/3
[i4]: https://github.com/MridulSaraf/ma76wuwi_MADE_WS24-25/issues/4
