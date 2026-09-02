from pathlib import Path

import piexif


# ============================================================
# CONFIGURAÇÃO
# ============================================================

# /home/henry/projetos/horus/mvp
MVP_DIR = Path(__file__).resolve().parent.parent

# /home/henry/projetos/horus
PROJECT_DIR = MVP_DIR.parent

# Imagens de teste do Horus
TARGET_DIR = (
    MVP_DIR
    / "tests"
    / "mission_001"
    / "images"
)

# Imagens reais da USGS que possuem GPS no EXIF
SOURCE_DIR = (
    PROJECT_DIR
    / "datasets"
    / "2017042FA_U35_F1toF6_BraddockBay"
    / "f1"
)

NUMBER_OF_IMAGES = 20


# ============================================================
# FUNÇÕES
# ============================================================

def find_images(directory: Path) -> list[Path]:
    """
    Procura imagens JPEG em uma pasta.
    """

    if not directory.exists():
        raise FileNotFoundError(
            f"Pasta não encontrada:\n{directory}"
        )

    extensions = {
        ".jpg",
        ".jpeg",
    }

    return sorted(
        [
            path
            for path in directory.iterdir()
            if path.is_file()
            and path.suffix.lower() in extensions
        ]
    )


def copy_gps_exif(
    source_image: Path,
    target_image: Path,
):
    """
    Copia somente o GPS do EXIF da imagem fonte
    para a imagem de destino.

    Os pixels da imagem de destino permanecem
    sendo os pixels originais da imagem de dengue.
    """

    source_exif = piexif.load(
        str(source_image)
    )

    source_gps = source_exif.get(
        "GPS",
        {}
    )

    if not source_gps:
        raise ValueError(
            f"A imagem fonte não possui GPS:\n"
            f"{source_image}"
        )

    target_exif = piexif.load(
        str(target_image)
    )

    # Mantém todo o EXIF existente da imagem alvo
    # e substitui somente o bloco GPS.
    target_exif["GPS"] = source_gps

    exif_bytes = piexif.dump(
        target_exif
    )

    piexif.insert(
        exif_bytes,
        str(target_image),
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("HORUS - INJEÇÃO DE GPS NAS IMAGENS DE TESTE")
    print("=" * 70)

    print(
        f"\nPasta das imagens de teste:\n"
        f"{TARGET_DIR}"
    )

    print(
        f"\nPasta das imagens USGS:\n"
        f"{SOURCE_DIR}"
    )

    # --------------------------------------------------------
    # Verificações
    # --------------------------------------------------------

    if not TARGET_DIR.exists():
        raise FileNotFoundError(
            f"\nPasta das imagens de teste não encontrada:\n"
            f"{TARGET_DIR}"
        )

    if not SOURCE_DIR.exists():
        raise FileNotFoundError(
            f"\nPasta fonte da USGS não encontrada:\n"
            f"{SOURCE_DIR}"
        )

    # --------------------------------------------------------
    # Encontrar imagens
    # --------------------------------------------------------

    target_images = find_images(
        TARGET_DIR
    )

    source_images = find_images(
        SOURCE_DIR
    )

    print(
        f"\nImagens de teste encontradas: "
        f"{len(target_images)}"
    )

    print(
        f"Imagens USGS encontradas: "
        f"{len(source_images)}"
    )

    if len(target_images) < NUMBER_OF_IMAGES:
        raise RuntimeError(
            f"São necessárias pelo menos "
            f"{NUMBER_OF_IMAGES} imagens de teste."
        )

    if len(source_images) < NUMBER_OF_IMAGES:
        raise RuntimeError(
            f"São necessárias pelo menos "
            f"{NUMBER_OF_IMAGES} imagens USGS."
        )

    # Pegamos somente as primeiras 20
    target_images = target_images[
        :NUMBER_OF_IMAGES
    ]

    source_images = source_images[
        :NUMBER_OF_IMAGES
    ]

    # --------------------------------------------------------
    # Copiar GPS
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("COPIANDO GPS")
    print("=" * 70)

    for index, (
        source_image,
        target_image,
    ) in enumerate(
        zip(
            source_images,
            target_images,
        ),
        start=1,
    ):

        print(
            f"\n[{index}/{NUMBER_OF_IMAGES}]"
        )

        print(
            f"USGS   : {source_image.name}"
        )

        print(
            f"Destino: {target_image.name}"
        )

        copy_gps_exif(
            source_image,
            target_image,
        )

        print(
            "GPS copiado com sucesso."
        )

    print("\n")
    print("=" * 70)
    print("CONCLUÍDO")
    print("=" * 70)

    print(
        f"{NUMBER_OF_IMAGES} imagens receberam "
        f"GPS no EXIF."
    )


if __name__ == "__main__":
    main()
