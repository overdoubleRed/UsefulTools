import re
import argparse

def extract_urls(file_path):
    url_regex = re.compile(
        r'((http|https)://[^\s/$.?#].[^\s]*)|(\bwww\.[a-z0-9.-]+\.[a-z]{2,}\b)',
        re.IGNORECASE
    )

    urls = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                urls.extend(re.findall(url_regex, line))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except PermissionError:
        print(f"Permission denied: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

    # Extract just the URLs from the tuples returned by re.findall
    urls = [url[0] if url[0] else url[2] for url in urls]

    return urls

def save_urls(urls, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for url in urls:
                file.write(url + '\n')
    except PermissionError:
        print(f"Permission denied: {output_file}")
    except Exception as e:
        print(f"Error writing to file {output_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract URLs from a file.')
    parser.add_argument('-i', '--input', required=True, help='Path to the input file.')
    parser.add_argument('-o', '--output', required=True, help='Path to the output file.')

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    urls = extract_urls(input_file)
    if urls:
        save_urls(urls, output_file)
        print(f"Extracted URLs have been saved to {output_file}")
    else:
        print("No URLs found.")
