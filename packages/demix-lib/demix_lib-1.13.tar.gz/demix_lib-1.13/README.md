<p align="center"><img  src="https://visioterra.fr/telechargement/P317_DEMIX/logos/logo4_v2-3_200x200_white_demix_background.png" ></p>
<h1 align="center"> DEMIX library</h1> 

<p>The DEMIX Library allow you to get scores for specific DEMIX tiles and DEM.<br/>
You also can download DEMIX Tile associated DEM Layers like SourceMask, Heights, ...</p>

---

<h2> Table of contents: </h2>

1. <a href="#Installation">Installation</a><br/>
2. <a href="#demix_lib_functions"> DEMIX lib functions</a><br/>
    2.1 <a href="#getting_demix_tile">Getting DEMIX Tile ID</a><br/>
    2.2 <a href="#getting_score">Getting Scores</a><br/>
    2.3 <a href="#getting_dem">Getting DEM</a><br/>
3. <a href="#utility_functions">Utility functions</a><br/>
4. <a href="#dem_and_criterions">Available DEMs and criterions</a><br/>
    4.1 <a href="#Dem">Dem list</a><br/>
    4.2 <a href="#Criterion">Criterion list</a><br/>
    4.3 <a href="#Layers">Layer list</a><br/>

5. <a href="#usage_example">Usage example</a><br/>
   5.1 <a href="#jupyter_notebook">Jupyter Notebook</a><br/>
   5.2 <a href="#custom_indicator">Getting a DEMIX layer and compute an indicator</a><br/>
<br/>

---

<h2 align="center" id='Installation'> Installation</h2>
To install the DEMIX library on your python environment :

```
pip install demix_lib
```


<h2 align="center" id='demix_lib_functions'>DEMIX lib functions</h2>
This section is a step-by-step guide on how to use the DEMIX lib functions. By getting through this guide, you'll learn how to:<br/>
*   Get a DEMIX tile id from a given longitude and latitude<br/>
*   Apply a criterion to a DEM, over a given DEMIX tile<br/>
*   Retrieve a raster of DEM layer over a DEMIX tile

<h3 id="getting_demix_tile">Getting DEMIX Tile ID</h3>
The DEMIX api enables you to get a DEMIX tile id from a given longitude and latitude.

```Python
import demix_lib as dl
lon = 14.44799
lat = 35.81923
print(dl.get_demix_tile_info(lon, lat))
print(dl.get_demix_tile_name(lon, lat))
```

<h3 id='getting_score'>Getting Scores</h3>
First thing first, you can use the demix api to get directly stats from the desired DEMIX Tile and Criterion
<br/>
In order to get scores to specific dem and tile, you need to choose a criterion.
The criterion list is available <a href="#Criterion">here</a>. List of supported dems is also visible <a href="#Dem">here</a>.


```Python
import demix_lib as dl

#getting the list of implemented criterions
criterions = dl.get_criterion_list()
#getting the list of supported dems
dems = dl.get_supported_dem_list()

#defining the wanted DEMIX Tile name 
demix_tile_name = "N35YE014F"

#getting the score of each dem, for the criterion 
for dem in  dems:
    for criterion in criterions:
        print(dl.get_score(demix_tile_name=demix_tile_name, dem=dem, criterion=criterion))
```


<h3 id='getting_dem'>Getting DEM</h3>
To go further :
You can always use your own criterions by downloading the wanted layer on your DEMIX tile and apply custom code to it.
<br/>To download a DEM layer for a specific DEMIX Tile :

```Python
import demix_lib as dl
import matplotlib as plt #we use matplotlib to visualise the downloaded layer
from matplotlib import cm #we use cm to make a legend/colormap
from matplotlib.lines import Line2D #to add colored line in the legend

#defining wanted tile
demix_tile_name = "N35YE014F"
#asking for the SourceMask layer for the CopDEM_GLO-30 dem and the tile N64ZW019C
response = dl.download_layer(demix_tile_name=demix_tile_name,dem="CopDEM_GLO-30",layer="SourceMask")

#creating legend for the plot
legend_handle = list(map(int, response['values'].keys()))
legend_label = list(response['values'].values())
#defining the colormap for the layer (the layer has 6 values)
color_map = cm.get_cmap("rainbow",6)
#we use plt to look at the data
plt.imshow(response["data"], interpolation='none', cmap=color_map, vmin=0, vmax=6)
#creating legend values using the color map and the values stored
custom_handles = []
for value in legend_handle:
    custom_handles.append(Line2D([0], [0], color=color_map(value), lw=4))
plt.legend( custom_handles,legend_label)
#show the layer with custom legend and color map
plt.show()
```

<h2 align="center" id='utility_functions'>Utility functions</h2>
The DEMIX lib give you some utility functions that allow you to get or print informations about currently implemented criterions, available DEMs, layers...

```python
import demix_lib as dl

#get or show the layers that you can ask in a download_layer function
layer_list = dl.get_layer_list()
dl.print_layer_list()

#get or show the full dem list
dem_list = dl.get_dem_list()
dl.print_dem_list()

#get or show the supported dem list
supported_dem_list = dl.get_supported_dem_list()
dl.print_supported_dem_list()

#get or show the implemented criterion list
criterion_list = dl.get_criterion_list()
dl.print_criterion_list()

#get or show the implemented colormaps
criterion_list = dl.get_colormap_list()
dl.print_colormap_list()

```


<h2 align="center" id='dem_and_criterions'>Available DEMs and criterions</h2>
<h3 id='Dem'>DEMs list</h3>

| DEM name | supported |
| :-------------: | :-------------: |
| ALOS World 3D | <span style="color:green">yes</span> |
| ASTERGDEM | <span style="color:green">yes</span> |
| CopDEM GLO-30 | <span style="color:green">yes</span> |
| CopDEM GLO-90 | <span style="color:green">yes</span> |
| EU-DEM | <span style="color:green">yes</span> |
| NASADEM | <span style="color:green">yes</span> |
| SRTMGL1 | <span style="color:green">yes</span> |

<h3 id='Criterion'>Criterion list</h3>


| Criterion name | Criterion id | version | Author | Date | Category | Target | Description |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |:---: |
| Product fractional cover | A01 |  0.1 | Peter Strobl | 20211103 | A-completeness | <span style="color:green">All</span> | <a href="https://visioterra.fr/telechargement/P317_DEMIX/criterions/A01_v0-1.pdf" target="_blank">read</a> |
| Valid data fraction | A02 |  0.1 | Peter Strobl | 20211103 | A-completeness | <span style="color:green">All</span> | <a href="" target="_blank"></a> |
| Primary data | A03 |  0.1 | Peter Strobl | 20211103 | A-completeness | <span style="color:green">All</span> | <a href="" target="_blank"></a> |
| Valid land fraction | A04 |  0.1 | Peter Strobl | 20211103 | A-completeness | <span style="color:green">All</span> | <a href="" target="_blank"></a> |
| Primary land fraction | A05 |  0.1 | Peter Strobl | 20211103 | A-completeness | <span style="color:green">All</span> | <a href="" target="_blank"></a> |


<h3 id='Layers'>Layer list</h3>

| Layer name |
| :-------------: |
| Heights |
| validMask | 
| SourceMask |
| landWaterMask |

<h2 align="center" id='usage_example'>Usage example</h2>

<h3 id='jupyter_notebook'>Jupyter Notebook</h3>
<p>A jupyter notebook has been made to demonstrate how can be used the DEMIX lib.<br> 
Download the latest Jupyter Notebook file of the following repository and execute it in you favorite jupyter 
environnement (like <a href="https://colab.research.google.com/" target="_blank">Colab</a> for example) to get an
idea of what is possible.</p>

<a href="https://visioterra.fr/telechargement/P317_DEMIX/notebook/" target="_blank"> Jupyter notebook repository</a>


<h3 id='custom_indicator'>Getting a DEMIX layer and compute an indicator</h3>
In this section, we will use the DEMIX lib to compute our own criterion on the SRTMGL1.

<h4>1 Define the criterion</h4>
First, we define a criterion

```python
def max_height_custom_criterion(response):
    """take height data and return a score based on altitude, if a point is higher than Everest highest point, 
    score is reduce by maximum_value / everest_max_height *10"""
    maximum_value=response["data"][0][0]
    everest_max_height = 8848
    for line in response["data"]:
        if max(line) > maximum_value :
            maximum_value = max(line)
    #if result < 1, score = 100, else : 
    result = maximum_value / everest_max_height
    if result < 1 :
        return 100
    else :
        return 100 - (result*10)
    return score
```

<h4>2 Get the wanted layer</h4>
Second, we use the DEMIX lib to download the wanted tile and layer for SRTMGL1

```python
lat = 27.986065
lon = 86.922623
response = dl.download_layer(demix_tile_name=dl.get_demix_tile_name(lon, lat),dem='SRTMGL1',layer='heights', print_request=False)
```

<h4>3 Compute the criterion on the layer</h4>
Finally, we compute the criterion on the downloaded layer and we plot the result

```python
print(max_height_custom_criterion(response))
```

