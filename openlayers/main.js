window.onload = init;
let dataset = []

// async function loadJSONData() {
//     return new Promise(async (resolve, reject) => {
//         try {
//             const response = await fetch('../dataset.json');

//             if (!response.ok) {
//                 throw new Error('JSON file not found ' + response.statusText);
//             }

//             const jsonData = await response.json();

//             resolve(jsonData);
//         } catch (error) {
//             reject(error);
//         }
//     });
// }
function waitForDataset() {
    const checkInterval = setInterval(() => {
        if (dataset.length > 0) {
            console.log(dataset);
            clearInterval(checkInterval);
        }
    }, 1000);
}

function init() {
    waitForDataset()
    console.log(dataset)

    // Styles
    const fillStyle = new ol.style.Fill({
        color: [255, 0, 0, 0.2]
    });

    const strokeStyle = new ol.style.Stroke({
        color: [255, 0, 0, 1],
        width: 1.2
    });

    // Data
    document.addEventListener('DOMContentLoaded', function () {
        fetch('../dataset.json')
            .then(response => response.json())
            .then(data => {
                dataset = data.data;
                console.log(dataset)
            });
    });


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

    const data2 = {
        Nombre: 'Anchuelo'
    }
    const municipiosPoblacionSource = MunicipiosPoblacion.getSource();

    municipiosPoblacionSource.on('change', function () {
        if (municipiosPoblacionSource.getState() === 'ready') {
            const features = municipiosPoblacionSource.getFeatures();
            features.forEach(feature => {
                const name = feature.get('NAMEUNIT');
                console.log(name);
                const matchingData = data2.find(entry => entry.Nombre === name);
                // if (matchingData) {
                // Aquí puedes hacer algo con los datos coincidentes
                // } else {
                //     console.log('No matching data found for:', name);
                // }
                // console.log(matchingData);

                // if (matchingData) {
                //     const population = matchingData.population;
                //     console.log(`Población total de ${name}: ${population}`);
                //     // feature.set('population', population); 
                // }
            });
        }
    });

}
