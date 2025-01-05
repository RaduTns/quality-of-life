import easyocr
import pandas as pd
import pdf2image
import os
import re
from constants import PDF_PATH, IMG_PATH, OUTPUT_FOLDER

reader = easyocr.Reader(['en'], gpu=False)

pd.set_option("display.max_columns", None)

def pdf_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = pdf2image.convert_from_path(pdf_path, fmt="jpeg", output_folder=output_folder)
    print(f"Converted {len(images)} pages to images in {output_folder}.")


def extract_text_from_image(img_path):
    print(f"Processing image: {img_path}")
    results = reader.readtext(image=img_path, paragraph=True, detail=0, y_ths=1.5)
    print("Extracted Text:", results)
    return results


def parse_products(results, keywords):
    matched_products = []
    for result in results:
        if any(keyword.lower() in result.lower() for keyword in keywords):
            print(f"Match found: {result}")
            matched_products.append(result)
        else:
            print("No match in:", result)
    return matched_products


def extract_price_details(text):
    pattern = r"(\d{1,2}%)\s([\d.,]+)\s([\d.,]+)"
    match = re.search(pattern, text)

    if match:
        sale_percentage = match.group(1)
        before_sale_price = match.group(2).replace(",", ".")
        sale_price = match.group(3).replace(",", ".")

        return {
            "sale_percentage": sale_percentage,
            "before_sale_price": float(before_sale_price),
            "sale_price": float(sale_price)
        }
    else:
        print(f"No price details found in: {text}")
        return None


def main():
    results = extract_text_from_image(IMG_PATH)

    keywords = ["salam", "pulpe", "sparanghel"]

    matched_products = parse_products(results, keywords)

    print("\nProducts on Sale:")
    for product in matched_products:
        price_details = extract_price_details(product)
        if price_details:
            print(f"- Product: {product}")
            print(f"  Sale Percentage: {price_details['sale_percentage']}")
            print(f"  Price Before Sale: {price_details['before_sale_price']}")
            print(f"  Sale Price: {price_details['sale_price']}")
        else:
            print(f"- Product: {product}")
            print("  No price details found.")


if __name__ == "__main__":
    main()
