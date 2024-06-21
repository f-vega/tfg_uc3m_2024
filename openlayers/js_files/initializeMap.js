function initializeMap() {
    console.log('Inicializando el mapa...');

    // Mapa base
    const map = new ol.Map({
        view: new ol.View({
            center: [-401991.8169733428, 4938199.319627684],
            zoom: 9,
            maxZoom: 20,
            minZoom: 4,
        }),
        target: "js-map"
    });

    const baseLayer = new ol.layer.Tile({
        source: new ol.source.OSM(),
        visible: true,
        title: 'Standard'
    });

    const MunicipiosDelimiter = new ol.layer.VectorImage({
        source: new ol.source.Vector({
            url: './geo_data/municipios.geojson',
            format: new ol.format.GeoJSON()
        }),
        visible: true,
        title: 'municipiosDelimiter',
        style: function (feature) {
            const name = feature.get('NAMEUNIT');
            return updateStyles(MunicipiosDelimiter);
        },
    });

    // Grupo de capas base
    const baseLayerGroup = new ol.layer.Group({
        layers: [baseLayer, MunicipiosDelimiter]
    });

    const overlayContainerElement = document.querySelector('.overlay-container');
    const overlayLayer = new ol.Overlay({
        element: overlayContainerElement
    });

    map.addOverlay(overlayLayer);
    const overlayFeatureName = document.getElementById('feature-name');
    const overlayFeatureData = document.getElementById('feature-data');
    map.on('click', function (e) {
        overlayLayer.setPosition(undefined);
        map.forEachFeatureAtPixel(e.pixel, function (feature, layer) {
            let clickCoordinate = e.coordinate;
            let clickFeatureName = feature.get('NAMEUNIT');
            let clickFeatureData = '';
            const matchingData = data.find(entry => entry.Nombre === nameTransform(clickFeatureName));
            if (matchingData && matchingData[selectedRatio] !== undefined) {
                clickFeatureData = matchingData[selectedRatio];
            } else if (matchingData && matchingData && matchingData[selectedRatio] === undefined) {
                clickFeatureData = '';
            } else {
                clickFeatureData = 'Datos no encontrados';
            }
            overlayLayer.setPosition(clickCoordinate);
            overlayFeatureName.innerHTML = clickFeatureName;
            overlayFeatureData.innerHTML = clickFeatureData;
        }, {
            layerFilter: function (layerCandidate) {
                return layerCandidate.get('title') == 'municipiosDelimiter';
            }
        });
    });

    function setupSelectListeners(MunicipiosDelimiter) {
        const clusterSelects = document.querySelectorAll('.subClusterSelect');
        const groupName = `subIndicatorRadioButton`;
        const subIndicatorSelects = document.querySelectorAll(`input[name='${groupName}']`)
        clusterSelects.forEach(clusterSelect => {
            clusterSelect.addEventListener('change', function () {
                updateSelectedMunicipios();
                updateStyles(MunicipiosDelimiter);
                try {
                    updateSelectedMunicipios();
                    updateStyles(MunicipiosDelimiter);
                } catch (error) {
                    console.error("Error al manejar el cambio del clúster:", error);
                    alert("Hubo un problema al cambiar el clúster. Verifique la consola para más detalles.");
                }
            });
        });
        subIndicatorSelects.forEach(subIndicatorSelects => {
            subIndicatorSelects.addEventListener('change', function () {
                try {
                    updateSelectedIndicator();
                    updateStyles(MunicipiosDelimiter);
                } catch (error) {
                    console.error("Error al manejar el cambio del indicador:", error);
                    alert("Hubo un problema al cambiar el indicador. Verifique la consola para más detalles.");
                }
            });
        });
    }

    map.addLayer(baseLayerGroup);

    setupSelectListeners(MunicipiosDelimiter);

    console.log('Capas añadidas al mapa.');
}



