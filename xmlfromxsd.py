import uuid

from scripts.xsd2xmlgenerator import Xsd2XmlGenerator

xml_name = str(uuid.uuid4())


def main(src_dir, dst_dir, file):
    f_name = src_dir.joinpath(file).resolve()
    generator = Xsd2XmlGenerator(xsd_path=f_name)
    generator.generate()
    out_file = str(dst_dir.joinpath(f"{file}_generated.xml").resolve())
    generator.write(xml_path=out_file)
    types_file = dst_dir.joinpath(f"{file}_types.txt").resolve()
    with open(types_file, "wt") as f:
        out = "\n".join([f"{t}" for t in generator.all_types if t is not None])
        f.write(out)

    attr_file = dst_dir.joinpath(f"{file}_attr.txt").resolve()
    with open(attr_file, "wt") as f:
        out = "\n".join([f"{t}" for t in generator.all_attr if t is not None])
        f.write(out)


if __name__ == "__main__":
    import argparse
    import os
    import sys
    import subprocess
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Генерация xml из xsd")
    parser.add_argument(
        '-s', '--srcdir', metavar='SRC-DIR', type=str, default="data",
        help="папка с исходным файлом (по умолчанию data)"
    )
    parser.add_argument(
        '-t', '--targetdir', metavar='TARGET-DIR', type=str,
        help="папка для результата (по умолчанию совпадает с исходной), при отсутствии папки, она будет создана."
    )
    parser.add_argument(
        '-f', '--file', required=True,
        help="файл со схемой", type=str
    )
    args = parser.parse_args()

    if args.srcdir is not None:
        src_dir = Path(args.srcdir).resolve()
    else:
        os.chdir(Path(__file__).parent.parent)
        src_dir = Path('tests/data')
    assert src_dir.is_dir(), 'Папка с исходными файлами не найдена!'

    if args.targetdir is not None:
        dst_dir = Path(args.targetdir).resolve()
    else:
        dst_dir = Path(args.srcdir).resolve()

    if not dst_dir.is_dir():
        dst_dir.mkdir(exist_ok=True)

    if args.file is not None:
        file = Path(args.srcdir).joinpath(args.file).resolve()
    else:
        print('Не задан файл со схемой!')
        sys.exit(1)

    if not file.is_file():
        print(f'Не задан файл со схемой: {file}!')
        sys.exit(2)

    main(src_dir, dst_dir, args.file)