#!/usr/bin/env python3
"""
Convertidor de imágenes HEIC/HEIF a JPG.

Requiere: pillow-heif (registra el plugin HEIC para Pillow)
Instalación:
    pip install pillow-heif pillow

Uso:
    python heic_a_jpg.py                              # abre un diálogo para elegir archivos
    python heic_a_jpg.py archivo.heic
    python heic_a_jpg.py carpeta_con_heic/
    python heic_a_jpg.py carpeta_con_heic/ -o carpeta_salida/ -q 90
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
    import pillow_heif
except ImportError:
    print("Faltan dependencias. Instala con:")
    print("    pip install pillow-heif pillow")
    sys.exit(1)

pillow_heif.register_heif_opener()

EXTENSIONES_HEIC = {".heic", ".heif"}


def elegir_archivos_gui():
    """Abre un diálogo gráfico para elegir uno o varios archivos .heic/.heif."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        print("No se pudo abrir el selector gráfico (tkinter no disponible).")
        print("Pasa la ruta como argumento: python heic_a_jpg.py archivo.heic")
        sys.exit(1)

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    rutas = filedialog.askopenfilenames(
        title="Selecciona archivos HEIC/HEIF",
        filetypes=[("Imágenes HEIC/HEIF", "*.heic *.heif"), ("Todos los archivos", "*.*")],
    )
    root.destroy()

    if not rutas:
        print("No se seleccionó ningún archivo.")
        sys.exit(0)

    return [Path(r) for r in rutas]


def convertir_archivo(ruta_entrada: Path, ruta_salida: Path, calidad: int = 95) -> bool:
    """Convierte un único archivo HEIC/HEIF a JPG."""
    try:
        img = Image.open(ruta_entrada)
        # HEIC puede venir en modo RGBA o con perfil de color especial;
        # JPG no soporta canal alfa, así que convertimos a RGB.
        if img.mode != "RGB":
            img = img.convert("RGB")
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        img.save(ruta_salida, "JPEG", quality=calidad)
        print(f"✓ {ruta_entrada.name} -> {ruta_salida}")
        return True
    except Exception as e:
        print(f"✗ Error convirtiendo {ruta_entrada.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Convierte imágenes HEIC/HEIF a JPG")
    parser.add_argument(
        "entrada",
        nargs="?",
        default=None,
        help="Archivo .heic o carpeta con archivos .heic (si se omite, abre un selector gráfico)",
    )
    parser.add_argument(
        "-o", "--salida",
        help="Carpeta de salida (por defecto: misma carpeta que la entrada)",
        default=None,
    )
    parser.add_argument(
        "-q", "--calidad",
        type=int,
        default=95,
        help="Calidad JPG 1-100 (por defecto: 95)",
    )
    args = parser.parse_args()

    exitosos = 0
    fallidos = 0

    # Sin argumento: abrir selector gráfico y permitir elegir varios archivos
    if args.entrada is None:
        archivos = elegir_archivos_gui()
        carpeta_salida = Path(args.salida) if args.salida else None

        for archivo in archivos:
            if archivo.suffix.lower() not in EXTENSIONES_HEIC:
                print(f"⚠ Saltando '{archivo.name}' (no es .heic/.heif)")
                continue
            destino = carpeta_salida if carpeta_salida else archivo.parent
            ruta_salida = destino / (archivo.stem + ".jpg")
            if convertir_archivo(archivo, ruta_salida, args.calidad):
                exitosos += 1
            else:
                fallidos += 1

        print(f"\nCompletado: {exitosos} convertidos, {fallidos} fallidos")
        return

    ruta_entrada = Path(args.entrada)

    if not ruta_entrada.exists():
        print(f"No existe: {ruta_entrada}")
        sys.exit(1)

    if ruta_entrada.is_file():
        if ruta_entrada.suffix.lower() not in EXTENSIONES_HEIC:
            print(f"'{ruta_entrada}' no parece un archivo HEIC/HEIF")
            sys.exit(1)
        carpeta_salida = Path(args.salida) if args.salida else ruta_entrada.parent
        ruta_salida = carpeta_salida / (ruta_entrada.stem + ".jpg")
        if convertir_archivo(ruta_entrada, ruta_salida, args.calidad):
            exitosos += 1
        else:
            fallidos += 1

    elif ruta_entrada.is_dir():
        archivos = [
            f for f in ruta_entrada.iterdir()
            if f.is_file() and f.suffix.lower() in EXTENSIONES_HEIC
        ]
        if not archivos:
            print(f"No se encontraron archivos .heic/.heif en {ruta_entrada}")
            sys.exit(0)

        carpeta_salida = Path(args.salida) if args.salida else ruta_entrada

        for archivo in archivos:
            ruta_salida = carpeta_salida / (archivo.stem + ".jpg")
            if convertir_archivo(archivo, ruta_salida, args.calidad):
                exitosos += 1
            else:
                fallidos += 1

    print(f"\nCompletado: {exitosos} convertidos, {fallidos} fallidos")


if __name__ == "__main__":
    main()
