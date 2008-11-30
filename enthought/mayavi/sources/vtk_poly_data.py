""" A module that allows a user to create one of several standard VTK
poly data sources.  
"""

#Author: Suyog Dutt Jain <suyog.jain@aero.iitb.ac.in>
#        Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2008,  Enthought, Inc.
# License: BSD Style.

# Enthought library imports.
from enthought.traits.api import Instance, Enum, Dict, Str
from enthought.traits.ui.api import View, Item, Group
from enthought.tvtk.api import tvtk

# Local imports
from enthought.mayavi.core.source import Source
from enthought.mayavi.core.pipeline_info import PipelineInfo


######################################################################
# `VTKPolyData` class.
######################################################################
class VTKPolyData(Source):
    # The version of this class.  Used for persistence.
    __version__ = 0

    # Flag to set the poly data type.
    source = Enum('arrow','cone','cube','cylinder','disk','earth','line',
                  'outline','plane','point', 'polygon','sphere',
                  'superquadric','textured sphere', 
                  desc='which poly data source to be used')

    # Define the trait 'vtk_poly_data_source' whose value must be an instance of
    # type PolyData
    vtk_poly_data_source = Instance(tvtk.PolyDataAlgorithm, allow_none=False,
                                    record=True)

    # Information about what this object can produce.
    output_info = PipelineInfo(datasets=['poly_data'], 
                               attribute_types=['any'],
                               attributes=['any'])

    # Create the UI for the traits.
    view = View(Group(Item(name='source'),
                  Item(name='vtk_poly_data_source',
                       style='custom',
                       resizable=True),
                   label='VTKPolyDataSource',
                    show_labels=False),          
             resizable=True)
    
    
    ########################################
    # Private traits.
    
    # A dictionary that maps the source names to instances of the
    # poly data sources.
    _source_dict = Dict(Str,
                          Instance(tvtk.PolyDataAlgorithm,
                                   allow_none=False))

    ######################################################################
    # `object` interface
    ######################################################################
    def __init__(self, **traits):
        # Call parent class' init.
        super(VTKPolyData, self).__init__(**traits)

        # Initialize the source to the default mode's instance from
        # the dictionary if needed.
        if 'source' not in traits:
            self._source_changed(self.source)
        
    ######################################################################
    # Non-public methods.
    ######################################################################
    def _source_changed(self, value):
        """This method is invoked (automatically) when the `source`
        trait is changed.
        """
        self.vtk_poly_data_source = self._source_dict[self.source]
     
    
    def _vtk_poly_data_source_changed(self, old, new):
        """This method is invoked (automatically) when the
        poly data source is changed ."""

        self.outputs = [self.vtk_poly_data_source.output]
        
        if old is not None:
            old.on_trait_change(self.render, remove=True)
        new.on_trait_change(self.render)        
       
    def __source_dict_default(self):
        """Default value for source dict."""
        sd = {'arrow':tvtk.ArrowSource(),             
              'cone':tvtk.ConeSource(),
              'cube':tvtk.CubeSource(),
              'cylinder':tvtk.CylinderSource(),
              'disk':tvtk.DiskSource(),
              'earth':tvtk.EarthSource(),
              'line':tvtk.LineSource(),
              'outline':tvtk.OutlineSource(),
              'plane':tvtk.PlaneSource(),
              'point':tvtk.PointSource(),
              'polygon':tvtk.RegularPolygonSource(),
              'sphere':tvtk.SphereSource(),
              'superquadric':tvtk.SuperquadricSource(),
              'textured sphere':tvtk.TexturedSphereSource()}
        return sd
    

   
