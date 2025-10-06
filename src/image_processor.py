# src/image_processor.py
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import os

def load_and_preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocesa una imagen para adaptarla al formato MNIST:
    - Escala de grises
    - Inversión (si procede) para que el dígito sea blanco sobre fondo negro
    - Autocontraste
    - Binarización adaptativa simple (umbral por la media)
    - Recorte del dígito (bbox)
    - Escalado proporcional para que el dígito ocupe ~20x20
    - Centrado usando centro de masa (centroid)
    - Ligera dilatación para engrosar trazos finos
    - Normalización y reshape a (1, 28, 28, 1)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"La imagen no existe: {image_path}")

    try:
        # 1) Abrir como L (grises)
        img = Image.open(image_path).convert('L')

        # 2) Invertir colores: asumimos input fondo blanco / trazo negro.
        #    Después de invertir, dígito = blanco (255), fondo = negro (0).
        img = ImageOps.invert(img)

        # 3) Mejorar contraste automático (ayuda con JPG y antialiasing)
        img = ImageOps.autocontrast(img)

        # 4) Convertir a numpy para umbral adaptativo simple
        arr = np.array(img).astype(np.uint8)

        # Si la imagen está casi toda negra/negra tras invertir, intenta no romper
        if arr.max() == 0:
            # nada: conservar la imagen original invertida
            bin_arr = arr
        else:
            # Umbral: usar la media como punto de corte (robusto para dibujos simples)
            th = arr.mean()
            bin_arr = (arr > th).astype(np.uint8) * 255

        # 5) Convertir a PIL y aplicar una pequeña dilatación (MaxFilter) para engrosar trazos finos
        bin_img = Image.fromarray(bin_arr).convert('L')
        bin_img = bin_img.filter(ImageFilter.MaxFilter(3))  # engrosa 1 píxel alrededor

        # 6) Recortar al bounding box del dígito
        bbox = bin_img.getbbox()
        if bbox:
            digit = bin_img.crop(bbox)
        else:
            digit = bin_img  # caso raro: sin bbox, usar imagen tal cual

        # 7) Redimensionar proporcionalmente para que el dígito ocupe ~20px en su mayor lado
        max_side = max(digit.size)
        if max_side == 0:
            # imagen vacía: crear lienzo 28x28 en negro
            canvas = Image.new('L', (28, 28), 0)
        else:
            scale = 20.0 / max_side
            new_size = (max(1, int(round(digit.size[0] * scale))),
                        max(1, int(round(digit.size[1] * scale))))
            digit_resized = digit.resize(new_size, resample=Image.Resampling.LANCZOS)

            # 8) Pegar centrado en un canvas 28x28
            canvas = Image.new('L', (28, 28), 0)
            paste_xy = ((28 - new_size[0]) // 2, (28 - new_size[1]) // 2)
            canvas.paste(digit_resized, paste_xy)

            # 9) Centrar por centro de masa (mejor que bounding-box centering)
            arr_canvas = np.array(canvas)
            ys, xs = np.where(arr_canvas > 0)
            if ys.size > 0:
                cy = ys.mean()
                cx = xs.mean()
                target = 13.5  # centro del lienzo 28x28 (0-index)
                shift_y = int(round(target - cy))
                shift_x = int(round(target - cx))

                # Crear nueva matriz y pegar sin wrap (clamping)
                new_arr = np.zeros_like(arr_canvas)
                # Rango origen
                src_y1 = max(0, -shift_y)
                src_y2 = min(28, 28 - shift_y)
                src_x1 = max(0, -shift_x)
                src_x2 = min(28, 28 - shift_x)
                # Rango destino
                dst_y1 = max(0, shift_y)
                dst_y2 = dst_y1 + (src_y2 - src_y1)
                dst_x1 = max(0, shift_x)
                dst_x2 = dst_x1 + (src_x2 - src_x1)

                new_arr[dst_y1:dst_y2, dst_x1:dst_x2] = arr_canvas[src_y1:src_y2, src_x1:src_x2]
                canvas = Image.fromarray(new_arr)

        # 10) Convertir a array float normalizado 0..1 (ya: 0 fondo, 255 dígito)
        final_arr = np.array(canvas).astype('float32') / 255.0

        # 11) Asegurarnos que el dígito es blanco (1.0) y fondo negro (0.0) — esto ya se cumple por la inversión
        #     pero en caso de dudas, no invertimos otra vez aquí.

        # 12) Añadir dimensiones (1, 28, 28, 1)
        final_arr = np.expand_dims(final_arr, axis=(0, -1))

        return final_arr

    except Exception as e:
        raise ValueError(f"No se pudo procesar la imagen: {e}")

# alias
preprocess_image = load_and_preprocess_image
