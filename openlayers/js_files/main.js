window.onload = init;

let data = null;
let ratio = null;
let standardValue = null;
let minRatio = Infinity;
let maxRatio = -Infinity;
let selectedRatio = null;
let municipiosSeleccionados = [];
let sumRatios = 0;
let countRatios = 0;

let indicadores = {
    'Índice de contratación': 'ratio_contratos',
    'Índice de empleabilidad': 'ratio_empleo',
    'Índice de paro': 'ratio_paro',
    'Índice de empleabilidad vs paro': 'ratio_empleo_por_paro',
    'Índice de disponibilidad empresarial': 'ratio_up',
    'Índice de contratación empresarial': 'ratio_contratos_por_up'
}

let subIndicadores = {
    'Total': 'por_poblacion_activa',
    'Sector primario': 'primario_por_poblacion_activa',
    'Sector secundario': 'secundario_por_poblacion_activa',
    'Sector terciario': 'terciario_por_poblacion_activa',
};

function defineAgeIntervals() {
    const startAge = 15;
    const endAge = 64;
    const interval = 5;
    const ageIntervals = {};

    for (let age = startAge; age <= endAge; age += interval) {
        const nextAge = age + interval - 1;
        const key = `${age}-${nextAge} años`;
        const value = `por_poblacion_censada_${age}a${nextAge}`;
        ageIntervals[key] = value;
    }

    return ageIntervals;
}

subIndicadores = { ...subIndicadores, ...defineAgeIntervals() };

let clusterVariables = {
    'Densidad de población': 'cluster_densidad_poblacion',
    'Distancia a la capital': 'cluster_distancia_capital',
    'Población censada': 'cluster_poblacion_censada',
    'Zona estadística': 'cluster_zona_estadistica'
};

let clusterNumbers = {
    'Clúster 0': '0.0',
    'Clúster 1': '1.0',
    'Clúster 2': '2.0'
};

function loadData() {
    return fetch('../dataset.json')
        .then(response => response.json())
        .then(jsonData => {
            data = jsonData;
            console.log('Datos cargados:', data);
        })
        .catch(error => console.error('Error al cargar el JSON:', error));
}

function init() {
    loadData().then(initializeMap).catch(error => console.error('Error durante la inicialización:', error));
}

// Reglas de normalización basadas en expresiones regulares
function nameTransform(nombre) {
    const patron = /^(La|Las|El|Los)\s(.+)$/;

    if (patron.test(nombre)) {
        const reemplazo = '$2 ($1)';
        return nombre.replace(patron, reemplazo);
    } else {
        return nombre;
    }
}

function maxMinRatios() {
    let municipios = municipiosSeleccionados.length > 0 ? municipiosSeleccionados : data;
    municipios.forEach(entry => {
        const ratio = parseFloat(entry[selectedRatio]);
        if (!isNaN(ratio)) {
            if (ratio < minRatio) minRatio = ratio;
            if (ratio > maxRatio) maxRatio = ratio;
            // sumRatios += ratio;
            // countRatios++;
        }
    });
    if (!standardValue) {
        if (countRatios > 0) {
            standardValue = sumRatios / countRatios;
        } else {
            standardValue = 1;
        }
    }
    return maxRatio, minRatio, standardValue
    sumRatios = 0;
    countRatios = 0;
}

function getFeatureStyle(ratio, standardValue) {
    if (!ratio || isNaN(ratio) || isNaN(maxRatio) || isNaN(minRatio)) {
        return new ol.style.Style({
            fill: new ol.style.Fill({
                color: [255, 255, 255, 0.2]
            }),
            stroke: new ol.style.Stroke({
                color: [0, 0, 0, 1],
                width: 1.2
            })
        });
    }

    if (ratio && minRatio && maxRatio && standardValue) {
        console.log(ratio, standardValue, minRatio, maxRatio);
        const scale = chroma.scale(['#f00', '#ff0', '#0f0']).domain([minRatio, standardValue, maxRatio]);
        let fillColor = scale(ratio).rgba();
        fillColor[3] = 0.5;

        return new ol.style.Style({
            fill: new ol.style.Fill({
                color: fillColor
            }),
            stroke: new ol.style.Stroke({
                color: [0, 0, 0, 1],
                width: 1.2
            })
        });
    }
}

function isSelectedMunicipio(nombre) {
    const nombreNormalizado = nameTransform(nombre);
    return municipiosSeleccionados.some(entry => entry.Nombre === nombreNormalizado);
}

function updateSelectedMunicipios() {
    const cluster_dict = getSelectedCluster();
    console.log('cluster_dict:', cluster_dict);
    const clusterVariable = clusterVariables[cluster_dict['cluster']];
    const clusterNumber = clusterNumbers[cluster_dict['subCluster']];
    municipiosSeleccionados = data.filter(municipio => municipio[clusterVariable] === clusterNumber);
}


function updateStyles(MunicipiosDelimiter) {
    MunicipiosDelimiter.setStyle(function (feature) {
        const name = feature.get('NAMEUNIT');
        const nombreNormalizado = nameTransform(name);
        const municipio = data.find(entry => entry.Nombre === nombreNormalizado);
        const ratio = municipio ? parseFloat(municipio[selectedRatio]) : null;

        // Verificar si el municipio está en la lista de selectedMunicipios
        const selectedMunicipio = municipiosSeleccionados.find(entry => entry.Nombre === nombreNormalizado);

        // Obtener las variables de clúster seleccionadas
        const cluster_dict = getSelectedCluster();
        const clusterVariable = clusterVariables[cluster_dict['cluster']];
        const clusterNumber = clusterNumbers[cluster_dict['subCluster']];

        if (selectedMunicipio && municipio && !isNaN(ratio) && ratio) {
            if (clusterVariable && selectedRatio) {
                standardValue = parseFloat(municipio[`${selectedRatio}_mean_${clusterVariable}`]);
            }
            maxMinRatios();
            return getFeatureStyle(ratio, standardValue);
        } else {
            maxMinRatios();
            return getFeatureStyle(null);
        }
    });
}


// Define la función updateSelectedIndicator
function updateSelectedIndicator() {
    const indicator_dict = getSelectedIndicator();
    console.log('municipiosSeleccionados:', municipiosSeleccionados);
    ratioIndicator = indicator_dict['indicator'];
    ratioSubIndicator = indicator_dict['subIndicator']
    if (ratioIndicator === 'Índice de contratación'
        || ratioIndicator === 'Índice de empleabilidad'
        || ratioIndicator === 'Índice de paro'
        || ratioIndicator === 'Índice de disponibilidad empresarial') {
        selectedRatio = `${indicadores[ratioIndicator]}_${subIndicadores[ratioSubIndicator]}`;
        console.log(selectedRatio);
    } else if (ratioIndicator === 'Índice de contratación empresarial'
        || ratioIndicator === 'Índice de empleabilidad vs paro') {
        selectedRatio = `${indicadores[ratioIndicator]}`;
    }
}


