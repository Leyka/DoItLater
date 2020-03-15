from pathlib import Path


def print_console(data: {}):
    print(f'Message from PRINT_CONSOLE: "{data["message"]}"')


def write_quote_file(data: {}):
    txt_path = Path('quotes.txt')

    with open(txt_path.resolve(), 'a+') as f:
        body = f"{data['author']} \t {data['quote']}\n"
        f.write(body)
        f.close()
