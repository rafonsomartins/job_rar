import argparse
import re

def remove_multiple_nbsp(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='ISO-8859-1') as file:
            content = file.read()

        # Replace multiple &nbsp; with a single &nbsp;
        content = re.sub(r'(&nbsp;)+', '&nbsp;', content)

        with open(output_file, 'w', encoding='ISO-8859-1') as file:
            file.write(content)

        print(f"Os caracteres &nbsp; foram ajustados com sucesso e o resultado foi salvo em {output_file}.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove multiple &nbsp; characters from the input file.')
    parser.add_argument('-path', type=str, required=True, help='Path to the input HTML file')
    parser.add_argument('-output', type=str, required=True, help='Path to the output HTML file')
    args = parser.parse_args()

    remove_multiple_nbsp(args.path, args.output)
