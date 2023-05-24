from PIL import Image
from pydub import AudioSegment


def convert(in_format, out_format, loc, save_loc):
    if in_format == "png":
        if out_format == "jpg":
            file = Image.open(f"{loc}.png").convert("RGB")
            file.save(f"{save_loc}.jpg", "JPEG")
            return True

        elif out_format == "ico":
            file = Image.open(f"{loc}.png").convert("RGB")
            file.save(f"{save_loc}.ico", "ICO")
            return True
        else:
            return False

    elif in_format == "mp3":
        if out_format == "wav":
            sound = AudioSegment.from_mp3(f"{loc}.mp3")
            sound.export(f"{save_loc}.wav", format="wav")
            return True
        else:
            return False
    else:
        return False
