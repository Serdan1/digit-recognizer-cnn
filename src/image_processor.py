# src/image_processor.py
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import os

def otsu_threshold(arr: np.ndarray) -> int:
    """Calcula umbral Otsu para una imagen en escala 0..255."""
    hist, _ = np.histogram(arr.flatten(), bins=256, range=(0, 256))
    total = arr.size
    sum_total = (np.arange(256) * hist).sum()
    sumB = 0
    wB = 0
    max_var = 0
    threshold = 0
    for t in range(256):
        wB += hist[t]
        if wB == 0:
            continue
        wF = total - wB
        if wF == 0:
            break
        sumB += t * hist[t]
        mB = sumB / wB
        mF = (sum_total - sumB) / wF
        var_between = wB * wF * (mB - mF) ** 2
        if var_between > max_var:
            max_var = var_between
            threshold = t
    return int(threshold)

def load_and_preprocess_image(image_path: str, debug_save_path: str = None) -> np.ndarray:
    """
    Preprocesa una imagen para el modelo MNIST y devuelve array (1,28,28,1).
    debug_save_path: si se proporciona, guarda la imagen final que verá la red.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"La imagen no existe: {image_path}")

    try:
        # 1) Abrir y convertir a L (0..255)
        img = Image.open(image_path).convert('L')
        arr_orig = np.array(img).astype(np.uint8)

        # 2) Decidir si invertir: si fondo claro (media alta) invertimos,
        #    si ya fondo oscuro no invertimos. Esto evita invertir dos veces.
        mean = arr_orig.mean()
        if mean > 127:
            img = ImageOps.invert(img)

        # 3) Autocontrast para mejorar separación
        img = ImageOps.autocontrast(img)

        # 4) Suavizado leve para reducir artefactos al redimensionar (radio pequeño)
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

        # 5) Otsu para binarizar
        arr = np.array(img).astype(np.uint8)
        th = otsu_threshold(arr)
        bin_arr = (arr > th).astype(np.uint8) * 255
        bin_img = Image.fromarray(bin_arr).convert('L')

        # 6) Engrosar trazos finos (dilatación simple)
        bin_img = bin_img.filter(ImageFilter.MaxFilter(3))

        # 7) Recortar bounding box
        bbox = bin_img.getbbox()
        if bbox:
            digit = bin_img.crop(bbox)
        else:
            digit = bin_img

        # 8) Escalar proporcionalmente al max lado = 20
        max_side = max(digit.size)
        if max_side == 0:
            canvas = Image.new('L', (28, 28), 0)
        else:
            scale = 20.0 / max_side
            new_w = max(1, int(round(digit.size[0] * scale)))
            new_h = max(1, int(round(digit.size[1] * scale)))
            digit_resized = digit.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)

            # 9) Pegar en canvas 28x28 centrado inicialmente
            canvas = Image.new('L', (28, 28), 0)
            paste_xy = ((28 - new_w) // 2, (28 - new_h) // 2)
            canvas.paste(digit_resized, paste_xy)

            # 10) Centrar por centro de masa
            arr_canvas = np.array(canvas)
            ys, xs = np.where(arr_canvas > 0)
            if ys.size > 0:
                cy = ys.mean()
                cx = xs.mean()
                target = 13.5
                shift_y = int(round(target - cy))
                shift_x = int(round(target - cx))

                new_arr = np.zeros_like(arr_canvas)
                src_y1 = max(0, -shift_y)
                src_y2 = min(28, 28 - shift_y)
                src_x1 = max(0, -shift_x)
                src_x2 = min(28, 28 - shift_x)

                dst_y1 = max(0, shift_y)
                dst_y2 = dst_y1 + (src_y2 - src_y1)
                dst_x1 = max(0, shift_x)
                dst_x2 = dst_x1 + (src_x2 - src_x1)

                new_arr[dst_y1:dst_y2, dst_x1:dst_x2] = arr_canvas[src_y1:src_y2, src_x1:src_x2]
                canvas = Image.fromarray(new_arr)

        # 11) Resultado normalizado 0..1 y shape (1,28,28,1)
        final_arr = np.array(canvas).astype('float32') / 255.0
        final_arr = np.expand_dims(final_arr, axis=(0, -1))

        # 12) debug: guardar imagen procesada si se pidió
        if debug_save_path:
            save_arr = (final_arr[0, :, :, 0] * 255).astype(np.uint8)
            Image.fromarray(save_arr).save(debug_save_path)

        return final_arr

    except Exception as e:
        raise ValueError(f"No se pudo procesar la imagen: {e}")

# alias para compatibilidad
preprocess_image = load_and_preprocess_image
