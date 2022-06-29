import sys
from loguru import logger
from pathlib import Path
import uuid
from datetime import date
from time import localtime, strftime

from scripts.xsd2xmlgenerator import Xsd2XmlGenerator

xml_name = str(uuid.uuid4())

src_path = Path.cwd()
d = date.today().strftime('%Y%m%d')
t = strftime("%H%M%S", localtime())
log_file_name = f"xmlgenerator_{d}_{t}.logs"
log_level = "TRACE"
log_level = "DEBUG"
log_level_file = "DEBUG"
serialize = True
path_file = src_path.joinpath("logs").joinpath(log_file_name)
fmt = "{time} | {level: <8} | {name: ^15} | {function: ^15} | {line: >3} | {message}"

logger.add(path_file, level=log_level_file, serialize=serialize, format=fmt)
logger.add(sys.stderr, level=log_level)


def main(src_dir_, dst_dir_, file_, count=1, recurs=False):
    if recurs:
        scan_dirs(count, src_dir_)
    else:
        generate_xml(count, dst_dir_, file_, src_dir_)


def scan_dirs(count, src_dir_):
    all_xsd = list(src_dir_.glob('**/*.xsd'))
    logger.trace(f"ll: {all_xsd}")
    for i, file_ in enumerate(all_xsd):
        if file_.suffix != ".xsd":
            continue
        if "csv" in file_.name:
            logger.warning(f"Не обработан файл {file_}")
            continue
        if "types" in file_.name:
            logger.warning(f"Не обработан файл {file_}")
            continue
        logger.trace(f"START ({i+1}/{len(all_xsd)}): {file_}")
        file_name = file_.name
        path = file_.parent
        generate_xml(count, path, file_name, path)


def generate_xml(count, dst_dir_, file_, src_dir_):
    f_name = src_dir_.joinpath(file_).resolve()
    try:
        generator = Xsd2XmlGenerator(xsd_path=f_name, count=count, src_dir=src_dir_)
        # generator.validate(str(f_name))
        generator.generate()
    except Exception as err:
        logger.error(f"ERR: {err}   f_name: {f_name}")
        return
    out_file = str(dst_dir_.joinpath(f"{file_}_generated.xml").resolve())
    generator.write(xml_path=out_file)
    types_file = dst_dir_.joinpath(f"{file_}_types.txt").resolve()
    with open(types_file, "wt") as f:
        out = "\n".join([f"{t}" for t in generator.all_types if t is not None])
        f.write(out)
    attr_file = dst_dir_.joinpath(f"{file_}_attr.txt").resolve()
    with open(attr_file, "wt") as f:
        out = "\n".join([f"{t}" for t in generator.all_attr if t is not None])
        f.write(out)


if __name__ == "__main__":
    import argparse
    import os
    import sys
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
        '-f', '--file', required=False,
        help="файл со схемой", type=str
    )
    parser.add_argument(
        '-с', '--count', required=False, default=1,
        help="Количество генерируемых документов", type=int
    )
    # parser.add_argument(
    #     '-r', '--recurs', dest='now', action='store_true', required=False, default=True,
    #     help="Генерация всех xsd во вложенных папках", type=int
    # )
    parser.add_argument('-r', dest='recursive_dirs', action='store_true', required=False,
                        help="Генерация всех xsd во вложенных папках.")
    args = parser.parse_args()

    dst_dir = None
    if args.recursive_dirs:
        if args.srcdir is not None:
            src_dir = Path(args.srcdir).resolve()
            assert src_dir.is_dir(), 'Папка с исходными файлами не найдена!'
        else:
            print('Не задана папка  со схемами!')
            sys.exit(1)
    else:

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

    main(src_dir, dst_dir, args.file, args.count, args.recursive_dirs)
