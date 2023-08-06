import logging
import os
import re
from pathlib import Path, PurePosixPath

import click

logging.basicConfig(
    level=logging.DEBUG, format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--input", "-i", default="./", help="input text help", type=str)
@click.option("--output", "-o", default="./", help="output text help", type=str)
@click.option("--delimiter", "-d", default=",", help="delimiter text help", type=str)
@click.option(
    "--prefix",
    "-prefix",
    prompt=True,
    prompt_required=False,
    default="exp",
    help="prefix text help",
)
def converter(input: str = "./", output: str = "./", delimiter: str = ",", prefix: str = "exp"):
    in_path = Path(input)
    out_path = Path(output)
    logger.info("Input path: %s", in_path)
    logger.info("Output path: %s", out_path)

    if not (out_path.is_dir()):
        raise TypeError("Not a valid Output path name.")

    if not (in_path.is_file() or in_path.is_dir()):
        raise TypeError("Not a valid Input path or file name.")

    if in_path.is_file():
        tmp_nme = PurePosixPath(in_path).stem
        tmp_ext = PurePosixPath(in_path).suffix

        file_name = out_path.joinpath(f"{prefix}_{tmp_nme}")

        if str(tmp_ext).find("csv") > 0:
            process_csv(in_path, file_name, delimiter)
        else:
            if str(tmp_ext).find("json") > 0:
                process_json(in_path, file_name, delimiter)
            else:
                raise TypeError("Not a valid Input file name (csv/json).")

    else:
        for filename in in_path.iterdir():
            if filename.is_file():
                tmp_nme = PurePosixPath(filename).stem
                tmp_ext = PurePosixPath(filename).suffix

                file_name = out_path.joinpath(f"{prefix}_{tmp_nme}")

                if str(tmp_ext).find("csv") > 0:
                    process_csv(filename, file_name, delimiter)
                else:
                    if str(tmp_ext).find("json") > 0:
                        process_json(filename, file_name, delimiter)


def process_csv(fname, oname, dl):
    f = open(fname, "r")

    o = open(str(oname) + ".json", "w")

    ln = f.readline().rstrip()

    if ln.find(dl) == -1:
        o.close()
        f.close()
        return

    hdr = []
    hdr = ln.split(dl)
    o.write("[\n")

    ln = f.readline()

    while ln:
        o.write("\t{\n")
        tmp_fld = ln.rstrip().split(dl)
        i = 0
        while i < len(hdr):
            try:
                tmp_f = float(tmp_fld[i])
                tmp_out = tmp_fld[i]
            except ValueError:
                tmp_out = '"' + tmp_fld[i] + '"'

            if i < (len(hdr) - 1):
                o.write('\t\t"' + hdr[i] + '" : ' + tmp_out + ",\n")
            else:
                o.write('\t\t"' + hdr[i] + '" : ' + tmp_out + "\n")
            i = i + 1

        o.write("\t}")
        ln = f.readline()
        if ln:
            o.write(",\n")
        else:
            o.write("\n")
    o.write("]\n")

    o.close()
    f.close()


def process_json(fname, oname, dl):
    f = open(fname, "r")

    o = open(str(oname) + ".csv", "w")

    ln = f.readline().rstrip()

    hdr = []
    i = 0
    while (ln) and (i == 0):
        ln = f.readline().rstrip()
        if ln.find("}") > 0:
            i = 1
        else:
            x = re.findall("(.+)[:.+]", ln)
            if x:
                hdr.append(x[0].replace('"', "").strip())

    f.seek(0)

    i = 0
    while i < len(hdr):
        if i < (len(hdr) - 1):
            o.write(hdr[i] + dl)
        else:
            o.write(hdr[i] + "\n")
        i = i + 1

    ln = f.readline().rstrip()
    rec = []
    while ln:
        tmp_fld = ln.split(":")
        if len(tmp_fld) == 2:
            lst_fld = tmp_fld[1].strip()
            if lst_fld[-1] == ",":
                lst_fld = lst_fld[:-1]

            if (lst_fld[0] == '"') and (lst_fld[-1] == '"'):
                lst_fld = lst_fld[1:-1]

            rec.append(lst_fld)

        if ln.find("}") > 0:
            i = 0
            while i < len(rec):
                if i < (len(rec) - 1):
                    o.write(rec[i] + dl)
                else:
                    o.write(rec[i] + "\n")
                i = i + 1
            rec = []

        ln = f.readline().rstrip()

    o.close()
    f.close()
