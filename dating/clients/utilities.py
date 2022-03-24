from PIL import Image, ImageEnhance


class ImageEditor():
    """An editor for editing image files.

    attributes:
    image_path: string - full path to edited image on local disk.
    methods:
    editor.put_watermark(watermark_path, opacity=0.1) - put an image as a
    watermask on edited image.
    """
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path

    def put_watermark(self, watermark_path, opacity=0.1) -> None:
        """Put an image as a watermask on edited image.
        Argiments:
        watermark_path: string - full path to image-watermark on local disk.
        opacity: float - degree of opacity from 0 to 1.
        """
        assert opacity >= 0 and opacity <= 1
        with Image.open(watermark_path) as watermark:
            if opacity < 1:
                if watermark.mode != 'RGBA':
                    watermark = watermark.convert('RGBA')
                else:
                    watermark = watermark.copy()
                alpha = watermark.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
                watermark.putalpha(alpha)
            with Image.open(self.image_path) as base_image:
                layer = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
                layer.paste(watermark, (0, 0))
                transparent = Image.composite(layer,  base_image,  layer)
                transparent_rgb = transparent.convert('RGB')
        transparent_rgb.save(self.image_path)
