window.onload = init;

function init() {

    // Styles
    const fillStyle = new ol.style.Fill({
        color: [255, 0, 0, 0.2]
    });

    const strokeStyle = new ol.style.Stroke({
        color: [255, 0, 0, 1],
        width: 1.2
    });

    const response = fetch('dataset.csv')
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }

    const data = response.json();
    console.log(response)

    // Map
    const map = new ol.Map({
        view: new ol.View({
            center: [-412791.8169733428, 4927179.319627684],
            zoom: 11,
            maxZoom: 20,
            minZoom: 4,
        }),
        target: "js-map"
    });

    const openStreetMapStandard = new ol.layer.Tile({
        source: new ol.source.OSM(),
        visible: true,
        title: 'Standard'
    });


    // Layer Switcher Logic for Basemaps
    const vectorLayerElements = document.querySelectorAll('.sidebar > input[type=radio]');
    for (let vectorLayerElement of vectorLayerElements) {
        vectorLayerElement.addEventListener('change', function () {
            let vectorLayerElementValue = this.value;
            baseLayerGroup.getLayers().forEach(function (element, index, array) {
                let vectorLayerTitle = element.get('title');
                if (vectorLayerTitle !== 'Standard') {
                    element.setVisible(vectorLayerTitle === vectorLayerElementValue);
                    // console.log('vectorLayerTitle:' + vectorLayerTitle, 'vectorLayerElementValue:' + vectorLayerElementValue)
                }
            });
        });
    }


    // Vector layers
    const ComunidadDeMadridDelimiter = new ol.layer.VectorImage({
        source: new ol.source.Vector({
            url: './geo_data/delimiter.geojson',
            format: new ol.format.GeoJSON()
        }),
        visible: false,
        title: 'ComunidadDeMadridDelimiter',
        style: new ol.style.Style({
            fill: fillStyle,
            stroke: strokeStyle,
        })
    });
    const MunicipiosVector = new ol.source.Vector({
        url: './geo_data/municipios.geojson',
        format: new ol.format.GeoJSON()
    });

    const MunicipiosDelimiter = new ol.layer.VectorImage({
        source: new ol.source.Vector({
            url: './geo_data/municipios.geojson',
            format: new ol.format.GeoJSON()
        }),
        visible: false,
        title: 'MunicipiosDelimiter'
    });

    const MunicipiosColor = new ol.layer.VectorImage({
        source: new ol.source.Vector({
            url: './geo_data/municipios.geojson',
            format: new ol.format.GeoJSON()
        }),
        visible: false,
        title: 'MunicipiosColor',
        style: function (feature) {
            const name = feature.get('NAMEUNIT');
            const firstLetter = name.charAt(0).toUpperCase();
            return getFeatureStyle(firstLetter);
        }
    });

    const MunicipiosPoblacion = new ol.layer.VectorImage({
        source: new ol.source.Vector({
            url: './geo_data/municipios.geojson',
            format: new ol.format.GeoJSON()
        }),
        visible: false,
        title: 'MunicipiosPoblacion'
    })

    // Layer group
    const baseLayerGroup = new ol.layer.Group({
        layers: [
            openStreetMapStandard, ComunidadDeMadridDelimiter, MunicipiosDelimiter, MunicipiosColor, MunicipiosPoblacion
        ]
    });

    map.addLayer(baseLayerGroup);

    // Vector feature click
    const overlayContainerElement = document.querySelector('.overlay-container');
    const overlayLayer = new ol.Overlay({
        element: overlayContainerElement
    })
    map.addOverlay(overlayLayer);
    const overlayFeatureName = document.getElementById('feature-name');
    const overlayFeatureData = document.getElementById('feature-data');
    map.on('click', function (e) {
        overlayLayer.setPosition(undefined);
        map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
            let clickCoordinate = e.coordinate;
            let clickFeatureName = feature.get('NAMEUNIT');
            let clickFeatureData = feature.get('NATLEVNAME');
            overlayLayer.setPosition(clickCoordinate);
            overlayFeatureName.innerHTML = clickFeatureName;
            overlayFeatureData.innerHTML = clickFeatureData;
        },
            {
                layerFilter: function (layerCandidate) {
                    return layerCandidate.get('title') == 'MunicipiosDelimiter'
                }
            }
        )

    })

    // Municipios color
    function getFeatureStyle(firstLetter) {
        let fillColor;
        switch (firstLetter) {
            case 'A':
                fillColor = [255, 0, 0, 0.2]; // Rojo
                break;
            case 'B':
                fillColor = '#330099'; // Verde
                break;
            case 'C':
                fillColor = [0, 0, 255, 0.2]; // Azul
                break;
            default:
                fillColor = [0, 128, 128, 0.2]; // Gris por defecto
                break;
        }
        return new ol.style.Style({
            fill: new ol.style.Fill({
                color: fillColor
            }),
            stroke: new ol.style.Stroke({
                color: [255, 0, 0, 1],
                width: 1.2
            })
        });
    }

    async function loadAndAddData() {
        try {
            // Fetch the JSON file
            const response = await fetch('data.json');

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            const data = await response.json();

            // Create a vector source and add features to it
            const vectorSource = new ol.source.Vector();
            data.forEach(item => {
                const feature = new ol.Feature({
                    geometry: new ol.geom.Point(ol.proj.fromLonLat([/* longitude */, /* latitude */])),
                    name: item.name,
                    population: item.population
                });

                vectorSource.addFeature(feature);
            });

            // Create a vector layer and add it to the map
            const vectorLayer = new ol.layer.Vector({
                source: vectorSource
            });

            map.addLayer(vectorLayer);
        } catch (error) {
            console.error('Error loading or processing data:', error);
        }
    }

    loadAndAddData
    const municipiosPoblacionSource = MunicipiosPoblacion.getSource();

    // municipios

}
