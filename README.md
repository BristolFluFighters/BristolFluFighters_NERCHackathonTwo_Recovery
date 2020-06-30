# Covid_Hackathon_2

Repository for managing the submission to COVID-19 Digital Sprint Hackathon 2 (June 15 09:00 to June 19 23:59)

The submission for team BristolFluFighters can be found in [main.md](main.md) which presents a report into our solution
to the Hackathon. 

## Useful links

1. [Covid-19 Digital Sprint Hackathon](https://digitalenvironment.org/home/covid-19-digital-sprint-hackathons/#entry)
2. [Entry Details](https://digitalenvironment.org/home/covid-19-digital-sprint-hackathons/#entry)
3. [Help Forum](https://digitalenvironment.org/forum/)
4. [Data Sources](https://digitalenvironment.org/home/covid-19-digital-sprint-hackathons/covid-19-hackathons-data-resources/)

## Challenge Description

* What are the positive and negative aspects of lockdown and recovery measures on meeting Paris and net zero targets?
* Using multivariate signals to highlight these impacts and their inter-relationships to inform decision making.

Multivariate signals and their interrelationships can be used to highlight the path to recovery. The pandemic is essentially a large unplanned experiment, allowing us to consider the ex-ante/mid-post/ex-post aspects of the effectiveness of the lockdown measures. It further allows us to study the positive and negative aspects of lockdown behaviours and to differentiate between the two. It can also help us to better understand the challenges associated with reaching the 8% target of the Paris Accord and reaching net zero (lockdown restrictions have currently delivered both a 5% reduction in emissions, and a 14% reduction in GDP). Solutions addressing this theme can draw from a variety of data sources including EO, social media and other potential sources.

## Installation

Clone the repository with:

    git clone https://github.com/BristolFluFighters/BristolFluFighters_NERCHackathonTwo_Recovery.git

We provide to conda environment files. One supports usage of the correlation framework while the other features heavier dependencies (`iris` and `cartopy`) and
also allows execution of the data preprocessing notebooks.

* `conda env create --file environment.yml` (bff-hack2) for the execution environment (lighter).
* `conda env create --file environment-preprocess.yml` (bff-covhack2-datapreproc) for the preprocessing environment.

Note: `bff-covhack2-datapreproc` is a super set of `bff-covhack2` as such there should be no need to install both.
