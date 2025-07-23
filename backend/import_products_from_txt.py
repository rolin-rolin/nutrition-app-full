import sys
import os
from pathlib import Path
import re

# Field order as per JSON schema
FIELD_ORDER = [
    "name", "brand", "description", "serving_size", "calories", "protein", "carbs", "fat", "fiber", "sugar", "electrolytes_mg", "flavor", "texture", "form", "price_usd", "categories", "dietary_flags", "timing_suitability", "tags", "allergens", "diet", "link", "image_url", "source", "verified"
]

LIST_FIELDS = {"categories", "dietary_flags", "timing_suitability", "tags", "allergens", "diet"}
FLOAT_FIELDS = {"calories", "protein", "carbs", "fat", "fiber", "sugar", "electrolytes_mg", "price_usd"}
BOOL_FIELDS = {"verified"}

PRODUCTS_START_MARKER = "sample_products = ["
PRODUCTS_END_MARKER = "]"


def parse_product(lines):
    product = {}
    for i, field in enumerate(FIELD_ORDER):
        if i >= len(lines):
            value = "N"
        else:
            value = lines[i].strip()
        if value == "N":
            if field in FLOAT_FIELDS:
                product[field] = 0.0
            elif field in BOOL_FIELDS:
                product[field] = False
            else:
                product[field] = None
        elif field in LIST_FIELDS:
            product[field] = [v.strip() for v in value.split(",") if v.strip()] if value else []
        elif field in FLOAT_FIELDS:
            try:
                product[field] = float(value)
            except ValueError:
                product[field] = 0.0
        elif field in BOOL_FIELDS:
            product[field] = value.lower() == "t"
        else:
            product[field] = value
    return product


def product_to_python(product):
    # Convert dict to Product(...) Python code
    fields = []
    for field in FIELD_ORDER:
        val = product[field]
        if val is None:
            continue
        if field in LIST_FIELDS:
            fields.append(f"{field}={val}")
        elif field in FLOAT_FIELDS:
            fields.append(f"{field}={val}")
        elif field in BOOL_FIELDS:
            fields.append(f"{field}={val}")
        else:
            fields.append(f'{field}="{val}"')
    return f"Product(\n    {',\n    '.join(fields)}\n)"


def main():
    if len(sys.argv) != 2:
        print("Usage: python import_products_from_txt.py products_input.txt")
        sys.exit(1)
    input_path = sys.argv[1]
    with open(input_path, "r") as f:
        content = f.read()
    
    # Split products by "PRODUCT <number>" markers
    product_blocks = re.split(r"# PRODUCT \d+", content)
    
    # Filter out empty blocks and the first block (before any PRODUCT marker)
    raw_products = []
    for block in product_blocks[1:]:  # Skip the first block (before any PRODUCT marker)
        if block.strip():
            # Filter out comment lines (lines starting with #) and empty lines
            lines = [line.strip() for line in block.splitlines() 
                    if line.strip() and not line.strip().startswith('#')]
            if lines:  # Only add if there are non-comment, non-empty lines
                raw_products.append(lines)
    
    products = []
    for lines in raw_products:
        product = parse_product(lines)
        products.append(product)
    
    # Convert to Product(...) code
    product_codes = [product_to_python(p) for p in products]
    
    # Read init_db.py
    init_db_path = Path(__file__).parent / "init_db.py"
    with open(init_db_path, "r") as f:
        init_db_code = f.read()
    
    # Find sample_products = [ ... ]
    marker = PRODUCTS_START_MARKER
    idx = init_db_code.find(marker)
    if idx == -1:
        print("Could not find sample_products list in init_db.py!")
        sys.exit(1)
    
    # Find the closing bracket of the list
    start_idx = idx + len(marker)
    end_idx = init_db_code.find("]", start_idx)
    if end_idx == -1:
        print("Could not find end of sample_products list in init_db.py!")
        sys.exit(1)
    
    # Insert new products before the closing bracket
    before = init_db_code[:end_idx]
    after = init_db_code[end_idx:]
    
    # Add comma if needed
    if before.rstrip()[-1] != "[":
        before = before.rstrip() + ",\n"
    
    new_code = before + "\n    " + ",\n    ".join(product_codes) + after
    
    # Write back to init_db.py
    with open(init_db_path, "w") as f:
        f.write(new_code)
    
    print(f"Appended {len(products)} products to sample_products in init_db.py.")

if __name__ == "__main__":
    main() 