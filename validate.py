from lxml import etree
import pathlib
import argparse


def validate(file, schema):
    relaxng_doc = etree.parse(schema)
    relaxng = etree.RelaxNG(relaxng_doc)
    doc = etree.parse(file)
    return relaxng.validate(doc)


def validate_all(args):
    path_to_tei_files = args.csalt_vedaweb_tei
    files = pathlib.Path(path_to_tei_files).glob('*rv_book*')
    for f in files:
        valid = validate(str(f), path_to_tei_files + '/vedaweb.rng')
        if valid:
            print(f, valid)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('csalt_vedaweb_tei',
                        help='path to c-salt_vedaweb_tei')
    args = parser.parse_args()
    validate_all(args)
