let selectedCluster = null;
let selectedSubCluster = null;

function getSelectedCluster() {
    return { cluster: selectedCluster, subCluster: selectedSubCluster };
}

document.addEventListener('DOMContentLoaded', function () {
    const clusters = [
        { label: "Densidad de población", className: "cluster-dp" },
        { label: "Distancia a la capital", className: "cluster-dc" },
        { label: "Población censada", className: "cluster-pc" },
        { label: "Zona estadística", className: "cluster-ze" }
    ];


    function createClusterElements() {
        const container = document.getElementById('cluster-container');

        clusters.forEach(cluster => {
            const clusterDiv = document.createElement('div');
            clusterDiv.className = cluster.className;

            const label = document.createElement('label');
            label.className = 'cluster-label';

            const input = document.createElement('input');
            input.type = 'radio';
            input.className = 'clusterSelect';
            input.name = 'clusterRadioButton';
            input.value = cluster.label;
            input.style.display = 'none';

            const icon = document.createElement('i');
            icon.className = 'ph ph-caret-double-right';

            const text = document.createTextNode(` ${cluster.label}`);

            label.appendChild(input);
            label.appendChild(icon);
            label.appendChild(text);

            const subClustersDiv = document.createElement('div');
            subClustersDiv.className = 'sub-clusters';

            const subOptions = ['Clúster 0', 'Clúster 1', 'Clúster 2'];

            subOptions.forEach(option => {
                const subOptionDiv = document.createElement('div');
                subOptionDiv.className = 'sub-cluster';
                const subLabel = document.createElement('label');
                subLabel.className = 'sub-label';

                const subInput = document.createElement('input');
                subInput.type = 'radio';
                subInput.className = 'subClusterSelect';
                subInput.name = `subClusterRadioButton`;
                subInput.value = option;
                subInput.style.display = 'none';

                const subIcon = document.createElement('i');
                subIcon.className = 'ph ph-circle';

                const subText = document.createTextNode(` ${option}`);

                subLabel.appendChild(subInput);
                subLabel.appendChild(subIcon);
                subLabel.appendChild(subText);

                subLabel.addEventListener('click', () => {
                    const groupName = `subClusterRadioButton`;
                    const allSameGroupInputs = document.querySelectorAll(`input[name='${groupName}']`);
                    allSameGroupInputs.forEach(input => {
                        const icon = input.nextElementSibling;
                        if (icon.classList.contains('ph-x-circle')) {
                            icon.className = 'ph ph-circle';
                        }
                    });

                    if (subIcon.classList.contains('ph-circle')) {
                        subIcon.className = 'ph ph-x-circle';
                        selectedSubCluster = option;
                        selectedCluster = cluster.label;
                    } else {
                        subIcon.className = 'ph ph-circle';
                        selectedSubCluster = null;
                        selectedCluster = null;
                    }

                });

                subOptionDiv.appendChild(subLabel);
                subClustersDiv.appendChild(subOptionDiv);
                subClustersDiv.appendChild(document.createElement('br'));
            });

            clusterDiv.appendChild(label);
            clusterDiv.appendChild(subClustersDiv);
            container.appendChild(clusterDiv);
        });
    }

    createClusterElements();

    const clusterSelects = document.querySelectorAll('.clusterSelect');

    clusterSelects.forEach(clusterSelect => {
        clusterSelect.addEventListener('click', function () {
            selectedCluster = this.value;
            const subClusters = this.parentElement.nextElementSibling;
            const icon = this.parentElement.querySelector('.ph-caret-double-right, .ph-caret-double-down');

            if (subClusters && subClusters.classList.contains('sub-clusters')) {
                if (subClusters.style.display === 'none' || subClusters.style.display === '') {
                    subClusters.style.display = 'block';
                    icon.classList.remove('ph-caret-double-right');
                    icon.classList.add('ph-caret-double-down');
                } else {
                    subClusters.style.display = 'none';
                    icon.classList.remove('ph-caret-double-down');
                    icon.classList.add('ph-caret-double-right');
                }
            }
        });
    });
});
