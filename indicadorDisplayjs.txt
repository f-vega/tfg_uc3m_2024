
let indicators = [
    { label: "Índice de contratación", className: "ratio-contratos", options: ['Total', 'Por sector', 'Por edad'] },
    { label: "Índice de empleabilidad", className: "ratio-empleo", options: ['Total', 'Por sector', 'Por edad'] },
    { label: "Índice de paro", className: "ratio-paro", options: ['Total', 'Por edad'] },
    { label: "Índice de empleabilidad vs paro", className: "ratio-empleo-vs-paro", options: ['Total'] },
    { label: "Índice de contratación empresarial", className: "ratio-empresa", options: ['Total'] },
    { label: "Índice de disponibilidad empresarial", className: "ratio-disponibilidad", options: ['Total'] },
];

let selectedIndicator = null;
let selectedSubIndicator = null;

function getSelectedIndicator() {
    return { indicator: selectedIndicator, subIndicator: selectedSubIndicator };
}


document.addEventListener('DOMContentLoaded', function () {
    function createIndicatorElements() {
        const container = document.getElementById('indicator-container');

        indicators.forEach(indicator => {
            const indicatorDiv = document.createElement('div');
            indicatorDiv.className = indicator.className;

            const label = document.createElement('label');
            label.className = 'indicator-label';

            const input = document.createElement('input');
            input.type = 'radio';
            input.className = 'indicatorSelect';
            input.name = 'indicatorRadioButton';
            input.value = indicator.label;
            input.style.display = 'none';

            const icon = document.createElement('i');
            icon.className = 'ph ph-caret-double-right';

            const text = document.createTextNode(` ${indicator.label}`);

            label.appendChild(input);
            label.appendChild(icon);
            label.appendChild(text);

            label.style.display = 'grid';

            const subIndicatorsDiv = document.createElement('div');
            subIndicatorsDiv.className = 'sub-indicators';

            const subOptions = indicator['options'];

            subOptions.forEach(option => {
                const subOptionDiv = document.createElement('div');
                subOptionDiv.className = 'sub-option';
                if (option === 'Por sector' || option === 'Por edad') {
                    const dropdownToggle = document.createElement('div');
                    dropdownToggle.className = 'dropdown-toggle';

                    const dropdownIcon = document.createElement('i');
                    dropdownIcon.className = 'ph ph-caret-double-right';

                    const dropdownText = document.createTextNode(` ${option}`);

                    dropdownToggle.appendChild(dropdownIcon);
                    dropdownToggle.appendChild(dropdownText);

                    const nestedSubIndicatorsDiv = document.createElement('div');
                    nestedSubIndicatorsDiv.className = 'options';

                    let nestedOptions = [];
                    if (option === 'Por sector') {
                        nestedOptions = ['Sector primario', 'Sector secundario', 'Sector terciario'];
                    } else if (option === 'Por edad') {
                        nestedOptions = ['15-19 años', '20-24 años', '25-29 años', '30-34 años', '35-39 años',
                            '40-44 años', '45-49 años', '50-54 años', '55-59 años', '60-64 años'];
                    }

                    nestedOptions.forEach(nestedOption => {
                        const nestedSubOptionDiv = document.createElement('div');
                        nestedSubOptionDiv.className = 'nested-sub-option';

                        const nestedLabel = document.createElement('label');
                        nestedLabel.className = 'nested-label';

                        const nestedSubInput = document.createElement('input');
                        nestedSubInput.type = 'radio';
                        nestedSubInput.className = 'nestedSubIndicatorSelect';
                        nestedSubInput.name = `subIndicatorRadioButton`;
                        nestedSubInput.value = nestedOption;
                        nestedSubInput.style.display = 'none';

                        const nestedIcon = document.createElement('i');
                        nestedIcon.className = 'ph ph-circle';

                        const nestedSubText = document.createTextNode(` ${nestedOption}`);

                        nestedLabel.appendChild(nestedSubInput);
                        nestedLabel.appendChild(nestedIcon);
                        nestedLabel.appendChild(nestedSubText);

                        nestedLabel.addEventListener('click', () => {
                            const groupName = `subIndicatorRadioButton`;
                            const allSameGroupInputs = document.querySelectorAll(`input[name='${groupName}']`);
                            allSameGroupInputs.forEach(input => {
                                const icon = input.nextElementSibling;
                                if (icon.classList.contains('ph-x-circle')) {
                                    icon.className = 'ph ph-circle';
                                }
                            });

                            if (nestedIcon.classList.contains('ph-circle')) {
                                nestedIcon.className = 'ph ph-x-circle';
                                selectedSubIndicator = nestedOption;
                                selectedIndicator = indicator.label;
                            } else {
                                nestedIcon.className = 'ph ph-circle';
                            }
                        });

                        nestedSubOptionDiv.appendChild(nestedLabel);
                        nestedSubIndicatorsDiv.appendChild(nestedSubOptionDiv);
                        nestedSubIndicatorsDiv.style.display = 'none';
                    });

                    dropdownToggle.addEventListener('click', () => {
                        nestedSubIndicatorsDiv.style.display = nestedSubIndicatorsDiv.style.display === 'none' || nestedSubIndicatorsDiv.style.display === '' ? 'block' : 'none';
                        dropdownIcon.classList.toggle('ph-caret-double-down');
                        dropdownIcon.classList.toggle('ph-caret-double-right');
                    });

                    subOptionDiv.appendChild(dropdownToggle);
                    subOptionDiv.appendChild(nestedSubIndicatorsDiv);
                } else {
                    const subLabel = document.createElement('label');
                    subLabel.className = 'sub-label';

                    const subInput = document.createElement('input');
                    subInput.type = 'radio';
                    subInput.className = 'subIndicatorSelect';
                    subInput.name = `subIndicatorRadioButton`;
                    subInput.value = option;
                    subInput.style.display = 'none';

                    subLabel.addEventListener('click', () => {
                        const groupName = `subIndicatorRadioButton`;
                        const allSameGroupInputs = document.querySelectorAll(`input[name='${groupName}']`);
                        allSameGroupInputs.forEach(input => {
                            const icon = input.nextElementSibling;
                            if (icon.classList.contains('ph-x-circle')) {
                                icon.className = 'ph ph-circle';
                            }
                        });

                        if (subIcon.classList.contains('ph-circle')) {
                            subIcon.className = 'ph ph-x-circle';
                            selectedSubIndicator = option;
                            selectedIndicator = indicator.label;
                        } else {
                            subIcon.className = 'ph ph-circle';
                            selectedIndicator = null;
                            selectedSubIndicator = null;
                        }
                    });

                    const subIcon = document.createElement('i');
                    subIcon.className = 'ph ph-circle';

                    const subText = document.createTextNode(` ${option}`);

                    subLabel.appendChild(subInput);
                    subLabel.appendChild(subIcon);
                    subLabel.appendChild(subText);

                    subOptionDiv.appendChild(subLabel);
                }

                subIndicatorsDiv.appendChild(subOptionDiv);
                subIndicatorsDiv.appendChild(document.createElement('br'));
            });

            indicatorDiv.appendChild(label);
            indicatorDiv.appendChild(subIndicatorsDiv);
            container.appendChild(indicatorDiv);
        });
    }

    createIndicatorElements();

    const indicatorSelects = document.querySelectorAll('.indicatorSelect');

    indicatorSelects.forEach(indicatorSelect => {
        indicatorSelect.addEventListener('click', function () {
            const subIndicators = this.parentElement.nextElementSibling;
            const icon = this.parentElement.querySelector('.ph-caret-double-right, .ph-caret-double-down');

            if (subIndicators && subIndicators.classList.contains('sub-indicators')) {
                if (subIndicators.style.display === 'none' || subIndicators.style.display === '') {
                    subIndicators.style.display = 'block';
                    icon.classList.remove('ph-caret-double-right');
                    icon.classList.add('ph-caret-double-down');
                } else {
                    subIndicators.style.display = 'none';
                    icon.classList.remove('ph-caret-double-down');
                    icon.classList.add('ph-caret-double-right');
                }
            }
        });
    });
});
