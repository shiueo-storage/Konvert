from PIL import Image


def convert(in_format, out_format, loc, save_loc):
    if in_format == "png":
        if out_format == "jpg":
            file = Image.open(f"{loc}.png").convert("RGB")
            file.save(f"{save_loc}.jpg", "JPEG")
            return True
        else:
            return False
    else:
        return False
