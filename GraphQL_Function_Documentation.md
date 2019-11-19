GraphQLWFS Function

What does the function do?

	The function, def graphqlwfs():, goes into a WFS website, and converts the data from GML format into GeoJSON format. 
	The initial parameter is the url of the WFS, which returns the request GetCapabilities. (&request=GetCapabilities)
	Get Capabilities will return a list of all the different feature types.
	Inside the function, there is another constant called filterRequest. This contains 2 URIs, the typename, which is the name of the Feature Type in your WFS, and outputformat, which is geoJSON. This is where the WFS is converted into geoJSON format.
	If you want a different feature type, you can do this by looking at the WFS for GetCapabilities. The typename value will be the value inside the wfs: Name tag, which itself is nested inside the wfs: FeatureType tag. An example structure is shown below, with the Feature Type highlighted in bold and underlined. This is the value you want to copy and paste into your filterRequest constant:
																<wfs:FeatureType>
																	<wfs:Name>osfeatures:Sites_FunctionalSite</wfs:Name>
																	<wfs:Title>Sites_FunctionalSite</wfs:Title>
																	<wfs:DefaultCRS>urn:ogc:def:crs:EPSG::27700</wfs:DefaultCRS>
																	<ows:WGS84BoundingBox>
																		<ows:LowerCorner>-8.114934309622171 49.88031284204585</ows:LowerCorner>
																		<ows:UpperCorner>2.678360052493208 60.7648749882926</ows:UpperCorner>
																	</ows:WGS84BoundingBox>
																</wfs:FeatureType>

			This results in the filterRequest value being: filterRequest = "&typenames=osfeatures:Sites_FunctionalSite&outputformat=geoJSON”.


	•	There is an additional constant called newUrl. The GeoJSON outputformat only works when the request is GetFeature. Therefore, the newURl does a str.replace, replacing the GetCapabilities request with a GetFeature request, and adds the filterRequest string to the url too, which returns in GeoJSON format.


How to use the function?
 
	1.	On your terminal, type “./local.sh”
	2.	On your browser, type http://127.0.0.1:5000/ This is where your output will be returned in geoJSON format.
	3.	If you want a different feature, copy and paste the value of the initial url parameter, and select your chosen feature type, in the way described above.


Count:

Count will return to you the first x number of features from the WFS. In older WFS features, this was called MaxFeatures. For example, if x = 10, then the query "&count=10" will return the first 10 features of the WFS. 

Filter Request:

You can also do filter requests with WFS based on properties, and property value. To do this, you can add the query string, "&filter=" and add the following GML style code below as the filter value.

```<Filter>
    <PropertyIsEqualTo>
        <PropertyName>
        *Property Name goes here, which is property constant in the function*
        </PropertyName>
        <Literal>
        *Property Value goes here, which is the constant, PropertyValue, in the function*
        </Literal>
    </PropertyIsEqualTo>
</Filter>```

With the function, you can change the value and name of the properties based on your WFS and filter accordingly. 
