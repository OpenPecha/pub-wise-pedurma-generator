from pathlib import Path

from openpecha.core.pecha import OpenPechaFS


PUBLICATIONS = ["derge", "narthang", "chone", "peking"]

def get_base_names(opf_path):
    base_names = []
    for base_path in list((opf_path / "base").iterdir()):
        base_names.append(base_path.stem)
    return base_names

def get_diplomatic_text(base_text, durchen_layer, pub):
    diplomatic_text = ""
    char_walker = 0
    for _, ann in durchen_layer['annotations'].items():
        ann_start = ann['span']['start']
        ann_end = ann['span']['end']
        pub_note = ann['options'][pub]['note']
        diplomatic_text += f"{base_text[char_walker:ann_start]}{pub_note}"
        char_walker = ann_end
    diplomatic_text += base_text[char_walker:]
    return diplomatic_text

def save_pub_wise_text(base_text, durchen_layer, output_dir):
    for pub in PUBLICATIONS:
        diplomatic_text = get_diplomatic_text(base_text, durchen_layer, pub)
        (output_dir / f"{pub}.txt").write_text(diplomatic_text, encoding="utf-8")

def serialize_pub_wise_text(open_edition_opf_path, output_dir):
    open_edition_pecha_id = open_edition_opf_path.stem
    open_edition_pecha = OpenPechaFS(open_edition_pecha_id, open_edition_opf_path)
    open_edition_pecha_path = open_edition_pecha.opf_path
    base_names = get_base_names(open_edition_pecha_path)
    for base_name in base_names:
        base_text = open_edition_pecha.read_base_file(base_name)
        durchen_layer = open_edition_pecha.read_layers_file(base_name, "Durchen")
        save_pub_wise_text(base_text, durchen_layer, output_dir)



if __name__ == "__main__":
    open_edition_opf_path = Path('./data/opfs/O278336C8')
    output_dir = Path('./data/D3871')
    serialize_pub_wise_text(open_edition_opf_path, output_dir)