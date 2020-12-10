from lxml import etree
import pathlib


def validate(file, schema):
    relaxng_doc = etree.parse(schema)
    relaxng = etree.RelaxNG(relaxng_doc)
    doc = etree.parse(file)
    return relaxng.validate(doc)


def validate_all(path_to_tei_files):
    files = pathlib.Path(path_to_tei_files).glob('*rv_book*')
    for f in files:
        valid = validate(str(f), path_to_tei_files + '/vedaweb.rng')
        if not valid:
            print(f, valid)
