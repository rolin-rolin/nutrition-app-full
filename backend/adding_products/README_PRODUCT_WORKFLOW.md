# Product Database Workflow

## **Clean Workflow for Adding Products**

### **Files:**

-   `products_input_template.txt` - Template for entering product data
-   `setup_database.py` - Creates database tables (run once)
-   `import_products.py` - Imports products from template to database

### **Step-by-Step Workflow:**

#### **1. First Time Setup (run once):**

```bash
python3 setup_database.py
```

#### **2. Add Products to Template:**

1. Open `products_input_template.txt`
2. Add your product data following the format:
    ```
    # PRODUCT X
    Product Name
    Brand
    Description
    Serving Size
    Calories
    Protein (g)
    Carbs (g)
    Fat (g)
    Fiber (g)
    Sugar (g)
    Electrolytes (mg)
    Flavor
    Texture
    Form
    Price (USD)
    Categories (comma-separated)
    Dietary Flags (comma-separated)
    Timing Suitability (comma-separated)
    Tags (comma-separated)
    Allergens (comma-separated)
    Diet (comma-separated)
    Link
    Image URL
    Source
    Verified (t/f)
    ```

#### **3. Import Products to Database:**

```bash
python3 import_products.py products_input_template.txt
```

#### **4. Verify Products:**

```bash
python3 -c "from app.db.session import SessionLocal; from app.db.models import Product; db = SessionLocal(); products = db.query(Product).all(); print(f'Total products: {len(products)}'); [print(f'{i+1}. {p.name}') for i, p in enumerate(products)]; db.close()"
```

### **Template Format Examples:**

#### **Categories:**

-   Product types: `protein bar`, `nuts`, `dairy`, `fruit`, `trail mix`
-   Taste: `sweet`, `savory`, `spicy`, `neutral`
-   Texture: `crunchy`, `chewy`, `smooth`, `soft`

#### **Dietary Flags:**

-   `high-protein`, `low-sugar`, `gluten-free`, `vegan`, `keto`, `paleo`

#### **Tags:**

-   `recovery`, `muscle-building`, `energy-boost`, `weight-loss`

#### **Source:**

-   `manual_entry`, `sample_data`, `web_scrape`, `api_import`

### **Notes:**

-   Use `N` for empty fields
-   Use `f` for False, `t` for True
-   Comma-separate multiple values
-   Script will skip products that already exist (by name)
