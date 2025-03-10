import shopify

# Set your API credentials
API_KEY = 'your_api_key'
PASSWORD = 'your_api_password'
SHOP_NAME = 'your_shop_name'

# Authenticate with Shopify
shop_url = f"https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin"
shopify.ShopifyResource.set_site(shop_url)

# Create a new product
product = shopify.Product()
product.title = "My New Product"
product.body_html = "<strong>Good product!</strong>"
product.vendor = "My Vendor"
product.product_type = "Category"

if product.save():
    print("Product created:", product.title)
else:
    print("Failed to create product:", product.errors.full_messages())