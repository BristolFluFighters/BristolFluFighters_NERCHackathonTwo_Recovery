# Obtaining data for GHG Emissions
This review has found three potential methods for analysing GHG emissions: remote-sensing, local sensing and predictive. The following sections provide a summary of these methods and discuss some of the pros and cons.

## Remote Sensing Options for GHG emissions
An overview of NASA remote sensing capabilties for CO<sub>2</sub> can be found [here](https://co2.jpl.nasa.gov/#mission=OCO-2).
* EASA Copernicus Satellite Constellation
	* Sentinel 4 and Sentinel 5 satellites are focussed on...
* [NASA Orbiting Carbon Observatory](https://oco.jpl.nasa.gov/)
	+ Two remote sensing solutions:
		- OCO-2. Active from July 2014 - 
		- OCO-3. Launched in May 2019
	+ Only for CO<sub>2</sub>
	* [Description of data products](https://ocov2.jpl.nasa.gov/product-info/)

Satellite data is classified using 4 levels:
* Level 1 - Raw data
* Level 2 - 
* Level 3 - 
* Level 4 - 	

### Pros
* Provides the "column-stack"coposition of the atmosphere as opposed to the 
* Near real-time atmospheric data. The data is "near real-time" as it goes through several processing steps in order to convert the raw data into a useful product.
* [Standardised data format](https://observer.gsfc.nasa.gov/)
* Huge dataset and capability available through [Google Earth Engine]9https://earthengine.google.com/).

### Cons
* Sensitive to sensor calibration
* Resolution of the data is restricted by the sensor's Field of View (FoV). 
* Sensitive to cloud cover - can be improved by having a higher resolution in order to see through

## Local Sensing Options for GHG emissions
There are a number of initiatives which are trying to standardise the measurement of GHG emissions across the world and provide the data to research scientists. One such initiative is the Integrated Carbon Observation Scheme [ICOS]](https://www.icos-cp.eu/) consisting of a set of sensing stations located throughout Eurpoe. There are 4 areas that ICOS focsses on:
1. 
2. 
3. 
4. 


## Remote vs. local sensing
Recently, [some work was completed] (https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/890579/verification-uk-greenhouse-gas-emissions-atmospheric-observations-annual-report-2018.pdf) where they compared the ...

## Predictive CO<sub>2</sub> Data
This [paper](https://www.nature.com/articles/s41558-020-0797-x.pdf) argues that real-time CO<sub>2</sub> monitoring via remote sensing is not yet mature enough to determine anthropogenic emissions. Instead, they propose a method for estimating the emissions during the Covid-19 lockdown by calculating the change in energy, activity and policy across 6 sectors and then using historical CO<sub>2</sub> data from these sectors to extrapolate the change in emissions during the lockdown. This provides a surrogate for the *actual* CO<sub>2</sub> data which should be available from other sources such as EO (Earth Observation) and weather stations. The 6 sectors and their sources of data are:
1. Power - Derived from electricity data
2. Industry - Derived from industrial data from China and steel production in United States
3. Surface Transport - Derived from traffic data
4. Public Buildings and Commerce  - Assumptions based on the level of confinement
5. Residential - Derived from UK smart meters
6. Aviation - Derived from number of flights

The advantage of this work is that the analysis is applied globally allowing comparisons to be made between different countries, however this comes at the expense of accuracy. For example, the effect of the lockdown on industry is inferred from data from China and the US and then extrapolated to other countries. Another example if the data for the residential sector, this is taken from UK smart meters and then applied across the globe. This is not a bad approach but it must be recognised that much of the data is based on extrapolating trends, and not observing trends in raw data. 

Regarding lockdown measures, this papers classifies the severity of the lockdown restrictions using 4 levels:
* **Level 0** - No restrictions
* **Level 1** - Policies targetted at long distance travel or groups of individuals where outbreak first nucleates
* **Level 2** - Regional policies that restrict an entire city, policy, region or ~50% of society from normal daily routines
* **Level 3** - National policies that substantially restrict the daily routine of all but key workers