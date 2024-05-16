import chardet
import pandas as pd

def detect_encoding(file_path):
    with open(file_path, 'rb', ) as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        return encoding, confidence


def convert_encoding(input_file, output_file, encoding):
    with open(input_file, 'r', encoding=encoding, errors='backslashreplace') as f:
        data = f.read()

    with open(output_file, 'w', encoding='utf-8', errors='backslashreplace') as f:
        f.write(data)

def xls_to_csv(input_file):
    archivo_xls = pd.read_excel(input_file)
    output_file = input_file[:-4] + '.csv'
    archivo_xls.iloc[8:].to_csv(output_file, index=False, sep=';')
    return output_file