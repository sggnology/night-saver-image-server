import re

from easyocr import easyocr
from fastapi import UploadFile


async def extract_car_plates_from_image(car_image: UploadFile):
    car_image_file = await car_image.read()

    reader = easyocr.Reader(['ko', 'en'], )
    raw_car_plates_candidates = reader.readtext(car_image_file, detail=0)

    car_plate_candidates = extract_car_plates_from_raw_value(raw_car_plates_candidates)

    print(f"car plate candidates : {car_plate_candidates}")
    return car_plate_candidates


def extract_car_plates_from_raw_value(raw_car_plates):
    raw_car_plates_join = "".join(raw_car_plates)

    filter_pattern = "[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]"

    filtered_text = re.sub(filter_pattern, '', raw_car_plates_join)

    car_plate_pattern = r"\d{2,3}[ㄱ-힣]\d{4}"

    match = re.findall(car_plate_pattern, filtered_text)

    return match
