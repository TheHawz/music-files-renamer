from pathlib import Path
from get_metadata import get_metadata_from_file, is_music
import shutil
import click
import pandas as pd

pd.set_option('max_colwidth', None)


@click.command()
@click.option('--input-folder', '-i', prompt='Input folder')
@click.option('--output-folder', '-o', prompt='Output folder')
def main(input_folder, output_folder):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    assert input_folder.exists()

    print('Input folder: ', input_folder.resolve())
    print('Output folder: ', output_folder.resolve())

    output_folder.mkdir(parents=True, exist_ok=True)

    files = [path.resolve().as_posix() for path in input_folder.glob('*')]
    files.sort()

    input_files = []
    renamed_files = []
    for ii, file in enumerate(files):
        if not file.endswith('.mp3') or not is_music(input_folder / file):
            print(f"Skipping file: {file}")
            continue

        try:
            md = get_metadata_from_file(file)
            artist, title = md['artist'], md['title']
            title = f'{artist} - {title}.mp3'
        except Exception:
            title = Path(file).name

        title = title.lower().replace(' ', '_')

        input_files.append(Path(file).name)
        renamed_files.append(title)

    assert len(input_files) == len(renamed_files)

    df = pd.DataFrame(input_files, columns=['input']).assign(output=renamed_files)

    print(df)
    response = input("Confirm changes? (y / N): ")
    procede_with_rename = response == 'y'

    if not procede_with_rename:
        return
    
    print("Renaming...")
    
    for file, title in zip(input_files, renamed_files):
        if not file.endswith('.mp3') or not is_music(input_folder / file):
            print(f"Skipping file: {file}")
            continue

        try:
            print(f"Renaming: {file} -> {title}")
            shutil.copy(
                src=input_folder / file,
                dst=output_folder / title,
            )
        except Exception as e:
            print(e)


if __name__ == '__main__':
    
    main()
