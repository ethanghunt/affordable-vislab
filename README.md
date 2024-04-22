# Affordable VisLab

A project to visualize house prices and affordabilty by neighborhoods and local regions.

Please note that not all the code used to generate this data and provide this experience is included. Many Jupyter notebooks and datasets were too large to include on Github. If you are interested in the methodology, please contact [ethanghunt](https://github.com/ethanghunt).

Thanks you to Mapbox for enabling this demo and continued development of their responsive mapping tool.

## Run the Demo

Get a Mapbox token, and replace `MAPBOX_ACCESS_TOKEN_HERE` in `demo/public/js/mapbox.js` on line 1.

Create a python virtual environment of your choice. Activate it. Ensure you are in the `demo` directory.

```
pip install -r requirements.txt
```
```
python router.py
```

Navigate to `localhost:8000`.


## Model Creation and Data Merging

Handles exploratory data analysis and creation of model types.

Uses Ridge and Lasso regression models to perform informed variable selection, and then saves the final model as a pickle file. If you would like to load this model, please use the `joblib` package as shown in `model.py`.

In addendum, this handles the merging of dispersed data files including merging based off of nearest longitude, latitude pairs.

## Data Scraping

Contains nearly all scraped files and data collection required for the reproducability. This includes compressed zillow scrape data, official neighborhood boundaries, the official Atlanta city boundary, and multitudes of region-specific datasets. In addition, it handles the scraping from the Google API.

Other scraping methods are not detailed here since they lacked fully automatic processes, felt exploitive, or were not available by the time of code compilation (deleted).
