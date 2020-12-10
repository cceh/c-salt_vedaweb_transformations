import argparse
import unicodedata
from pathlib import Path
from lxml import etree
from titlecase import titlecase

import utils


def set_addressees(current_dedic, hymn_node):
    if current_dedic:
        poets_addressees_node = etree.SubElement(hymn_node, 'div')
        poets_addressees_node.attrib['type'] = 'dedication'

        topic_node = etree.SubElement(poets_addressees_node, 'div')
        topic_node.attrib['type'] = 'addressee'
        p_topic_node_de = etree.SubElement(topic_node, 'p')
        p_topic_node_en = etree.SubElement(topic_node, 'p')

        addr = current_dedic[0]
        group = current_dedic[1]

        topic_de = addr[0].strip()
        topic_en = addr[1].strip()
        group_de = group[0].split(':')[0].split('.')[0].strip()
        classif_de = group[0].split(':')[1].strip()

        classif_en = group[1].split(':')[1].strip()

        # print(topic, group, classif)
        p_topic_node_de.text = topic_de
        p_topic_node_de.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'deu'
        p_topic_node_en.text = titlecase(topic_en)
        p_topic_node_en.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'eng'

        group_node = etree.SubElement(poets_addressees_node, 'div')
        group_node.attrib['type'] = 'group'
        group_node.attrib['n'] = group_de

        p_group_node_de = etree.SubElement(group_node, 'p')
        p_group_node_de.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'deu'
        p_group_node_de.text = classif_de

        p_group_node_en = etree.SubElement(group_node, 'p')
        p_group_node_en.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'eng'
        p_group_node_en.text = titlecase(classif_en)

    return hymn_node


def set_strata(verse_container, verse_in_strata, verse_id_tei):
    if verse_in_strata:
        lg_strata = etree.SubElement(verse_container, "lg")
        lg_strata.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_strata'
        lg_strata.attrib['type'] = 'strata'

        for sub_verse in verse_in_strata:
            lg_strata_pada = etree.SubElement(lg_strata, "l")
            lg_strata_pada.attrib[
                '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_strata_' + sub_verse[0]
            strata_fs = etree.SubElement(lg_strata_pada, "fs")
            strata_fs.attrib['type'] = 'strata_info'
            strata_label = etree.SubElement(strata_fs, "f")
            strata_t = etree.SubElement(strata_fs, "f")
            strata_label.attrib['name'] = 'label'
            strata_label.text = sub_verse[1]
            strata_t.attrib['name'] = 'strata'
            strata_t.text = sub_verse[2]
    return verse_container


def set_stanza_properties(verse_container, verse_in_stanza_properties, verse_id_tei):
    # stanza_properties provided by gunkel+ryan
    # <fs xml:id="b_01_h_01_001_01_sp" type="stanza_properties">
    if verse_in_stanza_properties:
        fs_sp = etree.SubElement(verse_container, "fs")
        fs_sp.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_sp'
        fs_sp.attrib['type'] = 'stanza_properties'

        for k, v in verse_in_stanza_properties.items():
            fs_sp_f = etree.SubElement(fs_sp, "f")
            fs_sp_f.attrib['name'] = k
            fs_sp_f_s = etree.SubElement(fs_sp_f, "symbol")
            fs_sp_f_s.attrib['value'] = v
    return verse_container


def set_half_based_verse(verse_container, verse, verse_id_tei, lang, id):
    if verse:
        verse_gr = etree.SubElement(verse_container, "lg")
        verse_gr.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_{}'.format(id)

        verse_gr.attrib[
            '{http://www.w3.org/XML/1998/namespace}lang'] = lang
        verse_gr.attrib['source'] = id

        for sub_verse in verse:
            gr_pada = etree.SubElement(verse_gr, "l")
            gr_pada.attrib[
                '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_{}_'.format(id) + sub_verse[0]
            gr_pada.text = sub_verse[1]

    return verse_container


def set_verse(verse_container, verse, verse_id_tei, lang, id):
    if verse:
        geldner_container = etree.SubElement(verse_container, 'lg')
        geldner_de_id_tei = verse_id_tei + '_{}'.format(id)
        geldner_container.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = geldner_de_id_tei
        geldner_container.attrib[
            '{http://www.w3.org/XML/1998/namespace}lang'] = lang
        geldner_container.attrib['source'] = id

        geldner_de = etree.SubElement(geldner_container, 'l')
        geldner_de_id_tei_0 = verse_id_tei + '_{}_0'.format(id)
        geldner_de.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = geldner_de_id_tei_0
        geldner_de.attrib[
            '{http://www.w3.org/XML/1998/namespace}lang'] = lang
        geldner_de.text = verse

    return verse_container


def set_padapatha(verse_container, verse, verse_id_tei):
    if verse:

        padapatha_container = etree.SubElement(verse_container, "lg")
        padapatha_container.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_padapatha'
        padapatha_container.attrib[
            '{http://www.w3.org/XML/1998/namespace}lang'] = 'san-Latn-x-ISO-15919'
        padapatha_container.attrib['source'] = 'padapatha'

        verse_padapatha = etree.SubElement(padapatha_container, "l")
        verse_padapatha.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_padapatha_0'
        verse_padapatha.attrib[
            '{http://www.w3.org/XML/1998/namespace}lang'] = 'san-Latn-x-ISO-15919'

        papatha_tokens = verse.split('|')

        for i, token in enumerate(papatha_tokens):
            padapatha_token = etree.SubElement(verse_padapatha, "w")
            padapatha_token.attrib[
                '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_padapatha_0_' + str(i + 1).zfill(
                2)

            padapatha_token.text = token.strip()

    return verse_container


def set_eichler(verse_container, verse, verse_id_tei):
    if verse:
        # some verses have not subverses e.g. 07.034.01
        if isinstance(verse[0], list):
            verse_deva = etree.SubElement(verse_container, "lg")
            verse_deva.attrib[
                '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_eichler'
            verse_deva.attrib[
                '{http://www.w3.org/XML/1998/namespace}lang'] = 'san-Deva'
            verse_deva.attrib[
                'source'] = 'eichler'
            for sub_verse in verse:
                deva_pada = etree.SubElement(verse_deva, "l")
                deva_pada.attrib[
                    '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_eichler_' + sub_verse[0]
                deva_pada.text = sub_verse[1]
        else:
            verse_deva = etree.SubElement(verse_container, "lg")
            verse_deva.attrib[
                '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_eichler'
            verse_deva.attrib[
                '{http://www.w3.org/XML/1998/namespace}lang'] = 'san-Deva'
            verse_deva.attrib[
                'source'] = 'eichler'

            deva_pada = etree.SubElement(verse_deva, "l")
            verse_deva.attrib[
                '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_eichler_0'
            deva_pada.attrib[
                '{http://www.w3.org/XML/1998/namespace}lang'] = 'san-Deva'
            deva_pada.attrib[
                'source'] = 'eichler'
            deva_pada.text = verse[0]
    return verse_container


def clean_up_zur_text(to_clean):
    # normalize into NFC
    to_clean = unicodedata.normalize('NFC', to_clean)

    # remove verse boundaries
    to_clean = to_clean.replace('|', '')
    to_clean = to_clean.replace('‖', '')

    # ṃ -> ṁ
    to_clean = to_clean.replace('ṃ', 'ṁ')

    # issue #39
    to_clean = to_clean.replace('!', '')
    to_clean = to_clean.replace('+', '')

    # strip text
    to_clean = to_clean.strip()

    return to_clean


def set_zurich_info(pada_dict, verse_container, matched_lemmata, leipzig_mapping, verse_id_tei):
    # <lg xml:id="b_01_h_01_001_01_zur" xml:lang="san-Latn-x-ISO-15919" source="zurich">
    verse_zur = etree.SubElement(verse_container, "lg")
    verse_zur.attrib[
        '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_zur'

    verse_zur.attrib[
        '{http://www.w3.org/XML/1998/namespace}lang'] = 'san-Latn-x-ISO-15919'
    verse_zur.attrib[
        'source'] = 'zurich'

    # dirty solution for extracting this info from column 'Y'
    des = 'Des.'
    prek = 'Prek.'
    abs = 'Abs.'
    evim = set()
    evim.add(des)
    evim.add(prek)
    evim.add(abs)

    for pada_id in pada_dict:

        # print(pada, type(pada))
        # pada_str = str(pada)
        l_pada = etree.SubElement(verse_zur, "l")
        # xml: id = "01_001_02_zur_a"
        l_pada.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_zur_' + pada_id

        lubotsky_pada = pada_dict.get(pada_id)[0].get('belege::lubotskypada')

        lubotsky_pada = clean_up_zur_text(lubotsky_pada)

        # add
        l_pada.text = lubotsky_pada

        # print(pada_dict.get(pada))
        # <l xml:id="b_01_h_001_001_zur_a_tokens">
        l_tokens = etree.SubElement(verse_zur, "l")
        l_tokens.attrib[
            '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei + '_zur_' + pada_id + '_tokens'

        for token in pada_dict.get(pada_id):

            word = etree.SubElement(l_tokens, "fs")
            word.attrib['type'] = 'zurich_info'
            # get wortnummer pada (comes as string)
            rc_id = token.get('belege::wortnummer pada')
            # format it
            rc_id = '{:02d}'.format(int(str(rc_id).rstrip('.0')))
            fs_id = verse_id_tei + '_zur_' + pada_id + '_' + rc_id
            #  xml:id="01_001_02_zur_a_01"
            word.attrib['{http://www.w3.org/XML/1998/namespace}id'] = fs_id

            f_surface = etree.SubElement(word, "f")
            f_surface.attrib['name'] = 'surface'
            f_string = etree.SubElement(f_surface, "string")

            token_form = token.get('belege::form')
            token_form_src = token.get('belege::form')
            # token_form_src = unicodedata.normalize('NFC', token_form_src)

            # clean_up
            token_form = clean_up_zur_text(token_form)
            f_string.text = token_form

            lemma_form = token.get('lemmata klassisch::lemma')
            lemma_form = clean_up_zur_text(lemma_form)

            # add gra_lemma
            if lemma_form:
                f_grassmann_lemma = etree.SubElement(word, 'f')
                f_grassmann_lemma.attrib['name'] = 'gra_lemma'

                # automatically matched
                string_lemma_grassmann = etree.SubElement(
                    f_grassmann_lemma, 'string')
                string_lemma_grassmann.text = lemma_form
                matched_lemma = matched_lemmata.get(token_form_src)
                matches = matched_lemma['id_matched']
                if isinstance(matches, list):
                    gra_source = ' #'.join(matches)
                    gra_source = '#' + gra_source
                else:
                    gra_source = '#' + str(matches)
                string_lemma_grassmann.attrib['match'] = gra_source

                # correction?
                if matched_lemma.get('id_correction'):
                    corrections = matched_lemma['id_correction']
                    if isinstance(corrections, list):
                        gra_correction = ' #'.join(corrections)
                        gra_correction = '#' + gra_correction
                    else:
                        gra_correction = '#' + str(corrections)
                    string_lemma_grassmann.attrib['correction'] = gra_correction

            # add gra_gramm
            gra_gramm = token.get('lemmata klassisch::lemmatyp')
            if gra_gramm:
                f_grassmann_gramm = etree.SubElement(word, 'f')
                f_grassmann_gramm.attrib['name'] = 'gra_gramm'
                gra_gramm = token.get('lemmata klassisch::lemmatyp')
                gra_gramm = gra_gramm.strip()
                # add EN translation
                # gra_gramm = gra_gramm.lower()
                gra_gramm = unicodedata.normalize('NFC', gra_gramm)

                if gra_gramm == 'Invariabile':
                    gra_gramm = 'invariable'
                if gra_gramm == 'Nominalstamm':
                    gra_gramm = 'nominal stem'
                if gra_gramm == 'Pronomen':
                    gra_gramm = 'pronoun'
                if gra_gramm == 'Wurzel':
                    gra_gramm = 'root'

                symbol_gramm_grassmann = etree.SubElement(
                    f_grassmann_gramm, 'symbol')
                symbol_gramm_grassmann.attrib['value'] = gra_gramm

            # morphosyntaktische info

            basic = {}
            basic['kasus'] = token.get('belege::kasus')
            basic['genus'] = token.get('belege::genus')
            basic['numerus'] = token.get('belege::numerus')
            basic['person'] = token.get('belege::person')
            basic['modus'] = token.get('belege::modus')
            basic['tempus'] = token.get('belege::tempus')
            basic['diathese'] = token.get('belege::diathese')

            gramm_sum_info = token.get('belege::belegbestimmung summe simpel')
            if 'ta-Ptz.' in gramm_sum_info:
                basic['non-finite'] = 'ta-Ptz.'
            if 'na-Ptz.' in gramm_sum_info:
                basic['non-finite'] = 'na-Ptz.'

            extra_verb_info = token.get('formen::zusätzliche merkmale verb')
            nvi = ''

            if extra_verb_info is not None:
                for evi in evim:
                    if evi in extra_verb_info:
                        nvi = evi

            if nvi != '':
                basic['evi'] = nvi

            f_morphosyntax = etree.SubElement(word, 'f')
            f_morphosyntax.attrib['name'] = 'morphosyntax'

            fs_leipzig = etree.SubElement(f_morphosyntax, 'fs')
            fs_leipzig.attrib['type'] = 'leipzig_glossing_rules'

            for k, v in basic.items():
                try:
                    if v is not None and v != '':
                        mapping = leipzig_mapping.get(v)
                        if mapping:
                            if mapping[1] != '' and mapping[1] != ' ' and mapping[1] is not None:
                                # print('mapping[1]', mapping[1])
                                f_gloss = etree.SubElement(fs_leipzig, 'f')
                                f_gloss.attrib['name'] = mapping[1]
                                f_gloss_symbol = etree.SubElement(
                                    f_gloss, 'symbol')
                                f_gloss_symbol.attrib['value'] = mapping[0]
                            else:
                                print('no_mapping', verse_id_tei,
                                      token_form, k, v)
                    else:
                        if k == 'evi':
                            continue
                        searched_best_of = 'belege::{} bestof'.format(k)
                        bestof = token.get(searched_best_of)
                        bestof = bestof.split('/')
                        if len(bestof) == 1:
                            if bestof[0] != '':
                                mapping = leipzig_mapping.get(
                                    bestof[0].strip())
                                if mapping:
                                    f_gloss = etree.SubElement(fs_leipzig, 'f')
                                    f_gloss.attrib['name'] = mapping[1]
                                    f_gloss_symbol = etree.SubElement(
                                        f_gloss, 'symbol')
                                    f_gloss_symbol.attrib['value'] = mapping[0]

                        if len(bestof) > 1:
                            f_valt_container = etree.SubElement(
                                fs_leipzig, 'f')
                            f_valt = etree.SubElement(f_valt_container, 'vAlt')
                            map = leipzig_mapping.get(bestof[0].strip())
                            if map:
                                f_valt_container.attrib['name'] = map[1]
                                for b in bestof:
                                    mapping = leipzig_mapping.get(b.strip())
                                    if mapping:
                                        if mapping[1] != '' and mapping[1] is not None and mapping[1] != ' ':
                                            # f_gloss = etree.SubElement(f_valt_container, 'f')
                                            # f_gloss.attrib['name'] = mapping[1]
                                            f_gloss_symbol = etree.SubElement(
                                                f_valt, 'symbol')
                                            f_gloss_symbol.attrib['value'] = mapping[0]
                                        else:
                                            print('no_mapping', verse_id_tei,
                                                  token_form, k, v)

                except TypeError as e:
                    print(fs_id, e, mapping, k, v)


def set_header(root):
    # add header info
    header = etree.SubElement(root, "teiHeader")
    file_desc = etree.SubElement(header, 'fileDesc')

    title_stmt = etree.SubElement(file_desc, 'titleStmt')
    title = etree.SubElement(title_stmt, 'title')

    publication_stmt = etree.SubElement(file_desc, 'publicationStmt')
    p_publisher = etree.SubElement(publication_stmt, 'p')
    p_publisher.text = 'CCeH - Cologne Center for eHumanities - 2020'

    source_desc = etree.SubElement(file_desc, 'sourceDesc')
    p_source_desc = etree.SubElement(source_desc, 'p')
    p_source_desc.text = 'For more information regarding sources and their licences, please see: '
    # header_ptr = etree.SubElement(p_source_desc, 'ptr')
    # header_ptr.attrib['target'] = 'teiCorpus.tei#vedaweb_header'

    text_node = etree.SubElement(root, "text")
    body_node = etree.SubElement(text_node, "body")

    return body_node, title


def verses_into_tei(rv, grassmann_enum, leipzig_mapping, addresees, stanza_properties, strata, aufrecht, lubotsky,
                    vnh_texas, padapatha,
                    geldner, grassmann,
                    otto, griffith, macdonell, mueller, oldenberg, renou, eichler, elizarenkova, matched_lemmata,
                    output_dir):
    for book, v1 in rv.items():

        root = etree.Element(
            'TEI', attrib={"xmlns": 'http://www.tei-c.org/ns/1.0'})
        body_node, title = set_header(root)
        book_node = etree.SubElement(body_node, 'div')
        book_id_tei = 'b{}'.format(book)
        book_node.attrib['{http://www.w3.org/XML/1998/namespace}id'] = book_id_tei
        book_node.attrib['type'] = 'book'

        title.text = 'Rigveda - VedaWeb Version - Book {}'.format(book)

        ## TODO add schema URL

        print('processing book {}'.format(book))

        for hymn, v2 in v1.items():

            hymn_node = etree.SubElement(book_node, 'div')
            hymn_id_tei = book_id_tei + '_h{}'.format(hymn)
            hymn_node.attrib['{http://www.w3.org/XML/1998/namespace}id'] = hymn_id_tei
            # set grassmann's hymn notation
            hymn_node.attrib['ana'] = str(
                grassmann_enum.get(book + '.' + hymn))
            hymn_node.attrib['type'] = 'hymn'

            # addressees
            current_dedic = addresees.get(book + '.' + hymn)
            hymn_node = set_addressees(current_dedic, hymn_node)

            for verse, v3 in v2.items():
                # <div xml:id="01_001_001">
                verse_id_tei = hymn_id_tei + '_' + verse
                verse_id = book + '.' + hymn + '.' + verse
                verse_container = etree.SubElement(hymn_node, "div")
                verse_container.attrib[
                    '{http://www.w3.org/XML/1998/namespace}id'] = verse_id_tei
                verse_container.attrib['type'] = 'stanza'

                # INFO

                # stanza properties
                set_stanza_properties(verse_container=verse_container,
                                      verse_in_stanza_properties=stanza_properties.get(
                                          verse_id),
                                      verse_id_tei=verse_id_tei)

                # strata
                set_strata(verse_container=verse_container,
                           verse_in_strata=strata.get(verse_id),
                           verse_id_tei=verse_id_tei)

                # SANSKRIT
                # zurich
                set_zurich_info(pada_dict=v3, verse_container=verse_container,
                                matched_lemmata=matched_lemmata,
                                leipzig_mapping=leipzig_mapping,
                                verse_id_tei=verse_id_tei)

                # lubotsky
                set_half_based_verse(verse_container=verse_container, verse=lubotsky.get(verse_id),
                                     verse_id_tei=verse_id_tei, lang='san-Latn-x-ISO-15919',
                                     id='lubotsky')

                # vnh
                set_half_based_verse(verse_container=verse_container, verse=vnh_texas.get(verse_id),
                                     verse_id_tei=verse_id_tei, lang='san-Latn-x-ISO-15919',
                                     id='vnh')

                # aufrecht
                set_half_based_verse(verse_container=verse_container, verse=aufrecht.get(verse_id),
                                     verse_id_tei=verse_id_tei, lang='san-Latn-x-ISO-15919',
                                     id='aufrecht')

                # padapatha

                set_padapatha(verse_container=verse_container, verse=padapatha.get(verse_id),
                              verse_id_tei=verse_id_tei)

                # deva (eichler)
                set_eichler(verse_container=verse_container, verse=eichler.get(verse_id),
                            verse_id_tei=verse_id_tei)

                # TRANSLATIONS

                # DEU
                # geldner
                set_verse(verse_container=verse_container, verse=geldner.get(verse_id),
                          verse_id_tei=verse_id_tei, lang='deu', id='geldner')

                # grassmann
                set_verse(verse_container=verse_container, verse=grassmann.get(verse_id),
                          verse_id_tei=verse_id_tei, lang='deu', id='grassmann')
                # otto
                set_verse(verse_container=verse_container, verse=otto.get(verse_id),
                          verse_id_tei=verse_id_tei, lang='deu', id='otto')

                # ENG

                # griffith
                set_verse(verse_container=verse_container, verse=griffith.get(verse_id),
                          verse_id_tei=verse_id_tei, lang='eng', id='griffith')

                # macdonell
                set_verse(verse_container=verse_container, verse=macdonell.get(verse_id),
                          verse_id_tei=verse_id_tei, lang='eng', id='macdonell')

                # mueller
                set_verse(verse_container=verse_container, verse=mueller.get(verse_id),
                          verse_id_tei=verse_id_tei, lang='eng', id='mueller')

                # oldenberg
                set_verse(verse_container=verse_container, verse=oldenberg.get(verse_id),
                          verse_id_tei=verse_id_tei, lang='eng', id='oldenberg')

                # FRA

                # renou
                set_verse(verse_container=verse_container, verse=renou.get(verse_id),
                          verse_id_tei=verse_id_tei, lang='fra', id='renou')

                # RUS

                # elizarenkova
                set_half_based_verse(verse_container=verse_container,
                                     verse=elizarenkova.get(verse_id),
                                     verse_id_tei=verse_id_tei, lang='rus', id='elizarenkova')

        et = etree.ElementTree(root)
        et.write(output_dir + '/rv_book_{}.tei'.format(book),
                 pretty_print=True, xml_declaration=True, encoding="utf-8")


def rec_dd():
    return collections.defaultdict(rec_dd)


def transform_rv(args):
    sources_repo = args.sources_repo
    output_dir = args.output_dir
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    if sources_repo:
        sources_repo = sources_repo.rstrip("/")
        output_dir = output_dir.rstrip("/")
        print('sources_repo', sources_repo)
        print('output', output_dir)
        # info
        addressees = utils.read_json(sources_repo + '/rigveda/info/addressees.json')

        leipzig_mapping = utils.read_json(
            sources_repo + '/rigveda/info/leipzig_mapping.json')

        strata = utils.read_json(
            sources_repo + '/rigveda/info/strata.json')

        stanza_properties = utils.read_json(
            sources_repo + '/rigveda/info/stanza_properties.json')

        grassmann_enum = utils.read_json(
            sources_repo + '/rigveda/info/grassmann_enum.json')

        matched_lemmata = utils.read_json(
            sources_repo + '/rigveda/info/matched_lemmata.json')

        # zurich: lubotsky, morphosyntax, lemmata in GRA
        rv_zur = utils.read_zurich(
            sources_repo + '/rigveda/versions/zurich.xlsx')

        # aufrecht
        aufrecht = utils.read_json(
            sources_repo + '/rigveda/versions/aufrecht.json')

        # lubotsky
        lubostky = utils.read_json(
            sources_repo + '/rigveda/versions/lubostky.json')

        # padapatha
        padapatha = utils.read_json(
            sources_repo + '/rigveda/versions/padapatha.json')

        # vnh_texas
        vnh_texas = utils.read_json(
            sources_repo + '/rigveda/versions/vnh.json')

        # deva
        eichler = utils.read_json(
            sources_repo + '/rigveda/versions/eichler.json')

        # translations

        # german

        geldner = utils.read_json(
            sources_repo + '/rigveda/translations/deu/geldner.json')

        grassmann = utils.read_json(
            sources_repo + '/rigveda/translations/deu/grassmann.json')

        otto = utils.read_json(
            sources_repo + '/rigveda/translations/deu/otto.json')

        # english

        griffith = utils.read_json(
            sources_repo + '/rigveda/translations/eng/griffith.json')

        macdonell = utils.read_json(
            sources_repo + '/rigveda/translations/eng/macdonell.json')

        mueller = utils.read_json(
            sources_repo + '/rigveda/translations/eng/mueller.json')

        oldenberg = utils.read_json(
            sources_repo + '/rigveda/translations/eng/oldenberg.json')

        # french
        renou = utils.read_json(
            sources_repo + '/rigveda/translations/fra/renou.json')

        # russian
        elizarenkova = utils.read_json(
            sources_repo + '/rigveda/translations/rus/elizarenkova.json')

        verses_into_tei(rv=rv_zur, grassmann_enum=grassmann_enum, leipzig_mapping=leipzig_mapping,
                        addresees=addressees,
                        lubotsky=lubostky, aufrecht=aufrecht, vnh_texas=vnh_texas,
                        padapatha=padapatha, stanza_properties=stanza_properties, strata=strata,
                        geldner=geldner,
                        grassmann=grassmann, otto=otto, griffith=griffith, macdonell=macdonell,
                        mueller=mueller, oldenberg=oldenberg, renou=renou, eichler=eichler,
                        elizarenkova=elizarenkova,
                        matched_lemmata=matched_lemmata, output_dir=output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('sources_repo',
                        help='path to c-salt_vedaweb_sources')
    parser.add_argument('output_dir',
                        help='path to c-salt_vedaweb_tei or to desired output directory')

    args = parser.parse_args()
    transform_rv(args)
