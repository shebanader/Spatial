# -*- coding: utf-8 -*-import arcpyclass Toolbox(object):    def __init__(self):        """Define the toolbox (the name of the toolbox is the name of the        .pyt file)."""        self.label = "Toolbox"        self.alias = "toolbox"        self.description = "Custom Toolbox"        # List of tool classes associated with this toolbox        self.tools = [BufferIntersectTool]class BufferIntersectTool(object):    def __init__(self):        """Define the tool (tool name is the name of the class)."""        self.label = "BufferIntersectTool"        self.description = "Returns points within buffer"        self.canRunInBackground = False    def getParameterInfo(self):        """Define parameter definitions"""        # Input Features parameter        in_feature1 = arcpy.Parameter(            displayName="Input Features for Aggregation",            name="in_feature1",            datatype="GPFeatureLayer",            parameterType="Required",            direction="Input")        in_feature1.filter.list = ["Point"]        in_feature1.description = "Input features for aggregation. Intersect tool will be used to\        determine which of these points are in the buffer"        # Derived Output Table parameter        in_feature2 = arcpy.Parameter(            displayName="Input Features for Buffer",            name="in_feature2",            datatype="GPFeatureLayer",            parameterType="Required",            direction="Input")        in_feature2.filter.list = ["Point"]        in_feature2.description = "Input features for buffer. Points which buffer will be created off of."        buffer_distance = arcpy.Parameter(            displayName="Buffer Distance",            name="buffer_distance",            datatype="GPLong",            parameterType="Optional",            direction="Input")        buffer_distance.value = 1000  # Default buffer distance of 1000 meters        # Output features parameter        out_features = arcpy.Parameter(            displayName="Output Features",            name="out_features",            datatype="GPFeatureLayer",            parameterType="Required",            direction="Output")        out_features.parameterDependencies = [in_feature1.name, in_feature2.name, buffer_distance.name]        out_features.schema.clone = True        return [in_feature1, in_feature2, buffer_distance, out_features]    def isLicensed(self):        """Set whether tool is licensed to execute."""        return True    def updateParameters(self, parameters):        """Modify the values and properties of parameters before internal        validation is performed.  This method is called whenever a parameter        has been changed."""        return    def updateMessages(self, parameters):        """Modify the messages created by internal validation for each tool        parameter.  This method is called after internal validation."""        return    def execute(self, parameters, messages):        """The source code of the tool."""        # Get the input parameters        in_feature1 = parameters[0].valueAsText        in_feature2 = parameters[1].valueAsText        buffer_distance = parameters[2].valueAsText        out_features = parameters[3].valueAsText        # Buffer the input points for buffer        buffer = arcpy.Buffer_analysis(in_feature2, "in_memory/buffer", buffer_distance)        # Use the Intersect tool to find points for aggregation within buffer        intersect_output = arcpy.Intersect_analysis([in_feature1, buffer], "in_memory/points_within_buffer")        # Copy the intersect output to the output parameter        arcpy.CopyFeatures_management(intersect_output, out_features)        return