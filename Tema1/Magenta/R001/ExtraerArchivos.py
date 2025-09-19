import os
import zipfile

# Firmas mágicas conocidas 
MAGIC_SIGNATURES = {
    b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46': "jpg",
    b'\xFF\xD8\xFF\xDB\x00\x43\x00\x04': "jpg",
    b'\xFF\xD8\xFF\xEE\x00\x10\x4A\x46': "jpg",
    b'\xFF\xD8\xFF\xE1\x00\x10\x4A\x46': "jpg",
    b'\x50\x4B\x03\x04\x14\x03\x00\x00': "zip",
    b'\x1A\x45\xDF\xA3\x01\x00\x00\x00': "webm",
    b'\x4F\x67\x67\x53': "ogv",                   # 'OggS'
    b'\x00\x00\x00\x18\x66\x74\x79\x70': "mp4",
    b'\x49\x44\x33\x02\x00\x00\x00\x00': "mp3",
    b'\x49\x44\x33\x03\x00\x00\x00\x00': "mp3",
    b'\x49\x44\x33\x04\x00\x00\x00\x00': "mp3",
    b'\xFF\xFB\x90\x64\x00\x00\x00\x00': "mp3",
    b'\xFF\xFA\x92\xC4\x00\x00\x00\x00': "mp3",
    b'\xFF\xF3\x40\xC4\x00\x00\x00\x00': "mp3",
    b'\xFF\xF2\x48\x80\x00\x00\x00\x00': "mp3",
    b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': "png",

}

def ensure_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def extract_zip(file_path, output_dir):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
            for f in zip_ref.namelist():
                print(f"Extracted from ZIP: {f}")
    except zipfile.BadZipFile:
        print(f"Failed to extract ZIP file (corrupted): {file_path}")

def find_next_magic_position(content, current_pos, magic_signatures):
  
    next_pos = len(content)
    for sequence in magic_signatures.keys():
        pos = content.find(sequence, current_pos + 1)
        if pos != -1 and pos < next_pos:
            next_pos = pos
    return next_pos

def parse_ogg_stream_end(content, start_pos):
    pos = start_pos
    length = len(content)
    while pos + 27 <= length:  # 27 bytes mínimos del header sin la tabla de segmentos
        if content[pos:pos+4] != b'OggS':
            # no es un encabezado Ogg válido aquí -> salir
            return pos
        # header_type está en offset pos+5
        try:
            header_type = content[pos + 5]
            page_segments = content[pos + 26]
        except IndexError:
            return length

        segment_table_start = pos + 27
        segment_table_end = segment_table_start + page_segments
        if segment_table_end > length:
            return length

        segments = content[segment_table_start:segment_table_end]
        payload_size = sum(segments)
        page_end = segment_table_end + payload_size
        if page_end > length:
            return length

        # Si la página tiene el flag EOS (0x04), la corriente Ogg termina en esta página.
        if header_type & 0x04:
            return page_end

        # avanzar a la siguiente página
        pos = page_end

    # Si salimos del while por falta de bytes, devolver EOF como fallback
    return length

def extract_files(content, magic_signatures, output_dir):
    pos = 0
    ogv_count = 0

    # Ordenamos las firmas por longitud descendente para evitar matches parciales
    sorted_sigs = sorted(magic_signatures.items(), key=lambda kv: len(kv[0]), reverse=True)

    while pos < len(content):
        found = False
        for sequence, file_type in sorted_sigs:
            if content.startswith(sequence, pos):
                # Tratamiento especial para OGV (OggS): parseamos páginas y buscamos EOS
                if file_type == "ogv":
                    end_pos = parse_ogg_stream_end(content, pos)
                    if end_pos <= pos:
                        # fallback: si parse falla, buscar el siguiente magic o EOF
                        end_pos = find_next_magic_position(content, pos, magic_signatures)
                    ogv_count += 1
                    file_name = f"{output_dir}/video_extraido_{ogv_count}.ogv"
                    with open(file_name, "wb") as out:
                        out.write(content[pos:end_pos])
                    print(f"Extracted OGV: {file_name} (bytes {pos}-{end_pos})")
                    pos = end_pos
                    found = True
                    break

                # Tratamiento general para los demás tipos
                next_pos = find_next_magic_position(content, pos, magic_signatures)
                if next_pos <= pos:
                    next_pos = len(content)
                file_name = f"{output_dir}/archivo_{pos}.{file_type}"
                with open(file_name, "wb") as out:
                    out.write(content[pos:next_pos])
                print(f"Extracted: {file_name} (bytes {pos}-{next_pos})")

                if file_type == "zip":
                    extract_zip(file_name, output_dir)

                pos = next_pos
                found = True
                break

        if not found:
            pos += 1

def main(input_file, output_dir):
    ensure_output_directory(output_dir)
    with open(input_file, "rb") as f:
        content = f.read()
    extract_files(content, MAGIC_SIGNATURES, output_dir)
    print("Done.")

if __name__ == "__main__":
    INPUT_FILE = "resultado10.jpg"  
    OUTPUT_DIR = "extraidos"
    main(INPUT_FILE, OUTPUT_DIR)
