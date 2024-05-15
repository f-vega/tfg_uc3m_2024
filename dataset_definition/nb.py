import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def ejecutar_notebook(path_to_notebook):
    # Leer el notebook
    with open(path_to_notebook, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Ejecutar el notebook
    execute_processor = ExecutePreprocessor(timeout=-1, kernel_name='python3')
    execute_processor.preprocess(notebook, {'metadata': {'path': '.'}})
    
    # Guardar el notebook con las celdas ejecutadas
    output_path = path_to_notebook.replace('.ipynb', '_ejecutado.ipynb')
    with open(output_path, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)
    
    print(f"El notebook se ha ejecutado exitosamente. Resultados guardados en: {output_path}")

if __name__ == "__main__":
    path_to_notebook = 'dataset_definition\clustering_zzee_dp.ipynb'
    ejecutar_notebook(path_to_notebook)
