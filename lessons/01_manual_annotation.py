#!/usr/bin/env python
# coding: utf-8

# # Manual Annotation
# 
# One of the common bioimage analysis tasks in manual annotation. This annotation could be to provide ground truth data for a machine learning algorithm or quality control any automated process.
# 
# There are 3 main types of manual annotation that napari provides, each corresponding to a different layer type
# - adding points to mark particular locations in an image with the **Points** layer
# - drawing 2D polygons to identify particular regions of interest with the **Shapes** layer
# - painting labels to provide a pixel-wise annotation of an image with the **Labels** layer
# 
# This tutorial will explore these three manual annotations in **[napari](https://napari.org/)**, using that same data from the image visualization tutorial.

# ## Setup

# In[ ]:


# this cell is required to run these notebooks on Binder
# if running on Binder, remember to **WAIT 5 SECONDS** after
# running the '%gui qt' cell below. If you get an error,
# click on "Kernel -> Restart" and try again. Make sure also
# that you have a desktop tab open.
import os
if 'BINDER_SERVICE_HOST' in os.environ:
    os.environ['DISPLAY'] = ':1.0'


# As was explained in the image visaulation tutorial, napari uses Qt for Graphical User Interface (GUI) so we must first create the Qt application before we can get started with `napari`.

# In[39]:


get_ipython().run_line_magic('gui', 'qt')


# We can then import `napari`, our `nbscreenshot` utility and instantiate an empty viewer

# In[40]:


import napari
from napari.utils import nbscreenshot

# Create an empty viewer
viewer = napari.Viewer()


# In this tutorial we will just load our data directly into napari using out builtin plugin reader

# In[41]:


viewer.open('data/nuclei.tif', plugin='builtins');


# This now loads the 3D data into the napari viewer, and scrolling to the 30th z-slice should look as follows:

# In[81]:


nbscreenshot(viewer)


# ## Annotating dividing and non-dividing cells using the points layer

# One simple task that a biologist or bioimage analyst might be interseted in annotating each cell as diving or non-dividng.
# 
# In order to do this we are going to add two points layers to the viewer, one called `dividing` and one called `non-dividing` and set some basic properties on these layers.
# 
# You can add the layers using the new points button in the middle of the left panel of the viewer (left-most button featuring with many small dots), or you can add them programatically from the viewer. We'll add them programatically from the viewer for this example.

# In[82]:


# add the first points layer for dividing cells
viewer.add_points(name='dividing', face_color='red', n_dimensional=True);

# add the second points layer for non-dividing cells
viewer.add_points(name='non-dividing', face_color='blue', n_dimensional=True);


# Notice now how two new layers have been created, and that these layers have different controls (top-left corner) compared to the image layer. These layers now have properties like `face color`, `point size`, and `symbol` that can be adjusted. Note we have also enabled something called `n_dimensional` mode for these `Points` layers. This setting will be the points an `n-dimensional` extent when scrolling through z-planes and is useful when looking at 3D data.

# In[83]:


nbscreenshot(viewer)


# To add points you must enter add mode. This can be done by clicking on the add mode button in the top row of the control panel (2nd from the left, circle with a plus in it), or programatically from the notebook.

# In[84]:


# programatically enter add mode for both Points layers to enable editing
viewer.layers['dividing'].mode = 'add'
viewer.layers['non-dividing'].mode = 'add'


# In[85]:


nbscreenshot(viewer)


# Now start adding points, clicking once per cell, approximately in the center of the cell, with the appropriate `Points` layer selected. You can tell which `Points` layer is selected because it will be highlighted left in the layers list in the bottom left hand corner of the screen. You can rapidly switch between selected layers using the up and down keys. Also don't forget this is a z-slice so you should move up and down the slice, which can also be done with the left/ right key.
# 
# After annotation, my data looks as follows:

# In[86]:


nbscreenshot(viewer)


# Or in 3D, which can be enabled by clicking 3D rendering button (which looks like a wireframe of a cube, second from the left) like this:

# In[87]:


nbscreenshot(viewer)


# You can also get the number of cells of each class and an array of their centers as follows:

# In[88]:


print('Number of diving cells:', len(viewer.layers['dividing'].data))
print('Number of non-diving cells:', len(viewer.layers['non-dividing'].data))


# In[89]:


# Locations of non-dividing cells
viewer.layers['non-dividing'].data


# To save a `csv` file with these values for each layer you can use our builtin writer functionality. Note these csv files can easily be opened up into tools like excel for further analysis.

# In[90]:


# Save out Points layer data to a csv file
viewer.layers['dividing'].save('dividing.csv', plugin='builtins');
viewer.layers['non-dividing'].save('non-dividing.csv', plugin='builtins');


# We are working on additional features for the `Points` layer like a properties dictionary that would enable you to just one layer with points that can then have many attributes like `dividing` or `non-dividing`. You can learn more about the these advanced points annotations from the [tutorial](https://napari.org/tutorials/applications/annotate_points).

# ## Drawing polygons around cells

# Another common task for research biologists and bioimage analysts is drawing polygons around regions of interest, in this case nuclei. These polygons might be used for segmentation and to quantify properties of interest.
# 
# For this example we'll work with a 2D maximum intensity projection of our cells in order to keep things simple. We can take the data we've already loaded into napari and use it for the projection.

# In[4]:


# Take the maximum intensity projection of the cells
nuclei_mip = viewer.layers['nuclei'].data.max(axis=0)


# In[5]:


# Remove select and remove all the current layers from the viewer
viewer.layers.select_all()
viewer.layers.remove_selected()

# Add in the maximum intensity projection
viewer.add_image(nuclei_mip);


# In[6]:


nbscreenshot(viewer)


# We can now add an empty new shapes layer from the GUI using the new shapes button (middle of the left panel, 2nd from the left with a polygon on it) or programatically from the notebook.

# In[9]:


viewer.add_shapes(name='nuclei outlines', face_color='red', edge_color='white', opacity=0.7);


# Notice now in top left corner of the viewer we have a new controls panel corresponding to the shapes layer with buttons for creating and editing shapes. They include a select mode for dragging and resizing shapes, a direct select mode for dragging vertices, tools for adding and subtracting vertices from existing shapes, buttons for reordering shapes, and tools for drawing lines, ellipses, rectangles, paths, and polygons.

# In[10]:


nbscreenshot(viewer)


# We will draw some shapes with the polygon tool around a couple of different nuclei.

# In[11]:


nbscreenshot(viewer)


# The vertices for these shapes can be obtained from the shapes layer as follows:

# In[12]:


# The list of vertices for each shape
viewer.layers['nuclei outlines'].data


# These shapes, and the underlying image can be saved as an svg file using our dedicated svg writer. This functionality is useful if you want to put the image and the shapes into a tool like illustrator when preparing a figure or a presentation.

# In[13]:


viewer.layers.save('nuclei-outlines.svg', plugin='svg');


# Similarly to the points layer, we're working on adding support for properties dictionary to the shapes layer which would allow you to assign attributes to each shape and do things like adjust shape color based on them.
# 
# One common thing to use a shapes for is creating a binary mask or labels image where each pixel is assigned an integer label of the shape it is contained within, if any. napari provides some tooling to make these conversions easy.

# In[16]:


# Convert the polygons into labels
shape = viewer.layers['nuclei_mip'].data.shape
nuclei_labels = viewer.layers['nuclei outlines'].to_labels(labels_shape=shape)

print('Number of labels:', nuclei_labels.max())


# We can now add this labels image to the viewer as a labels layer.

# In[20]:


# Add the cell segmenation labels as a labels layer
viewer.add_labels(nuclei_labels);

# Turn off the visibility of the shapes layer so as not to get confused
viewer.layers['nuclei outlines'].visible = False


# In[22]:


nbscreenshot(viewer)


# ## Painting labels for pixel-wise annotations
# 
# With the labels layer we can now make pixel-wise annotaions using a paintbrush, fill bucket, and eraser tools (see the row of buttons in the control panel in the top left of the viewer).
# 
# Using these tools we can touch up any of the labels that we got from our polygon masks or draw entirely new ones.

# In[23]:


nbscreenshot(viewer)


# We can save out these labels to image formats like `tif` using our builtin plugin writer. Note that these can

# In[24]:


# Save out the nuclei labels as a tiff file
viewer.layers['nuclei_labels'].save('nuclei-labels.tif', plugin='builtins');


# In[30]:


# Note that the cell labels could be reloaded into the viewer as follows
viewer.open('nuclei-labels.tif', name='saved nuclei', plugin='builtins');

viewer.layers['nuclei_labels'].visible = False


# In[36]:


nbscreenshot(viewer)


# One simple thing someone might want to do is quantify the total amount of signal inside our original image relative to the total amount of area for each of our labels. Using some basic python command we can easily do this as follows: 

# In[37]:


n_labels = viewer.layers['nuclei_labels'].data.max()

ratios = []
for label_id in range(n_labels):
    inside_pixels = viewer.layers['nuclei_labels'].data == label_id
    area = inside_pixels.sum()
    signal = viewer.layers['nuclei_mip'].data[inside_pixels].sum()
    ratios.append(signal / area)
    
print('Signal per unit area for our labels:', ratios)


# As with the points and shapes layers we are current adding support for a properties dictionart to the labels layer to make it easy to attach annotations per labeled region.

# ## Conclusions

# We've now seen how to use the **Points**, **Shapes**, and **Labels** layers to produce manual annotations in napari and save those annotations in meaningful formats.
# 
# The next lessons will teach us how to perform interactive analyses in napari and more!
