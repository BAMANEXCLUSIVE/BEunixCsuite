# Complete Microweber Dropshipping Implementation Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Configuration](#basic-configuration)
4. [Dropshipping Customizations](#dropshipping-customizations)
5. [Supplier Integration](#supplier-integration)
6. [Payment Gateway Setup](#payment-gateway-setup)
7. [Shipping Configuration](#shipping-configuration)
8. [Order Management System](#order-management-system)
9. [Performance Optimization](#performance-optimization)
10. [Marketing Tools](#marketing-tools)

## Introduction

This guide provides step-by-step instructions for setting up a complete dropshipping e-commerce platform using Microweber. The solution will enable you to:
- Import products from suppliers
- Automatically forward orders to suppliers
- Process payments
- Track inventory
- Manage customer relationships
- Scale your business efficiently

## Installation

### Prerequisites
- Web hosting with PHP 7.4+ and MySQL 5.7+
- Composer
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/microweber/microweber.git
cd microweber
```

### Step 2: Install Dependencies
```bash
composer install
```

### Step 3: Configuration
Create a `.env` file with your database information:
```
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=your_database
DB_USERNAME=your_username
DB_PASSWORD=your_password
APP_URL=https://your-domain.com
```

### Step 4: Run the Installer
```bash
php artisan microweber:install
```

Or visit your domain in a browser to complete the installation wizard.

## Basic Configuration

### Admin Setup
1. Access the admin panel at `yourdomain.com/admin`
2. Configure basic store settings:
   - Store name and contact information
   - Currency and tax settings
   - Email templates
   - User roles and permissions

### Theme Selection
1. Navigate to `Templates` in the admin panel
2. Choose a responsive e-commerce theme
3. Customize the theme to match your brand:
   - Colors and typography
   - Logo and favicon
   - Homepage layout
   - Product page design

## Dropshipping Customizations

### Create a Custom Module

Create a dropshipping module to extend Microweber's functionality:

1. Create the module structure:
```bash
mkdir -p userfiles/modules/dropshipping
```

2. Create a module.json file:
```json
{
  "name": "Dropshipping",
  "description": "Dropshipping module for Microweber",
  "version": 1.0,
  "author": "Your Name",
  "categories": ["e-commerce"]
}
```

3. Create a main PHP file (index.php) for the module:
```php
<?php
/**
 * Dropshipping Module for Microweber
 */

// Admin configuration
function dropshipping_admin() {
    $module_template = get_option('template', 'dropshipping');
    if ($module_template == false) {
        $module_template = 'default';
    }
    
    $template_file = module_dir('dropshipping') . 'templates/' . $module_template . '.php';
    $settings = get_option('settings', 'dropshipping');
    
    $defaults = array(
        'supplier_api_key' => '',
        'auto_order_forwarding' => 'yes',
        'sync_interval' => '24', // hours
        'markup_percentage' => '30',
        'low_stock_threshold' => '5'
    );
    
    $settings = array_merge($defaults, (array) $settings);
    
    $view = new \Microweber\View($template_file);
    $view->assign('settings', $settings);
    return $view->display();
}

// Register module
$modules['dropshipping'] = array(
    'name' => 'Dropshipping',
    'description' => 'Dropshipping module for Microweber',
    'author' => 'Your Name',
    'ui' => true,
    'ui_admin' => true,
    'categories' => ['e-commerce'],
    'position' => 99,
    'version' => 1.0
);
```

4. Create templates directory and default template:
```bash
mkdir -p userfiles/modules/dropshipping/templates
touch userfiles/modules/dropshipping/templates/default.php
```

5. Create the template file with configuration options:
```php
<div class="module-dropshipping-settings">
    <h2>Dropshipping Settings</h2>
    
    <form method="post" class="mw_option_form" action="<?php echo api_url('save_option'); ?>">
        <input type="hidden" name="option_group" value="dropshipping" />
        <input type="hidden" name="option_key" value="settings" />
        
        <div class="form-group">
            <label>Supplier API Key</label>
            <input type="text" name="supplier_api_key" class="form-control" value="<?php echo $settings['supplier_api_key']; ?>" />
        </div>
        
        <div class="form-group">
            <label>Auto-Forward Orders to Supplier</label>
            <select name="auto_order_forwarding" class="form-control">
                <option value="yes" <?php if($settings['auto_order_forwarding'] == 'yes'): ?>selected<?php endif; ?>>Yes</option>
                <option value="no" <?php if($settings['auto_order_forwarding'] == 'no'): ?>selected<?php endif; ?>>No</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>Inventory Sync Interval (hours)</label>
            <input type="number" name="sync_interval" class="form-control" value="<?php echo $settings['sync_interval']; ?>" />
        </div>
        
        <div class="form-group">
            <label>Default Markup Percentage</label>
            <input type="number" name="markup_percentage" class="form-control" value="<?php echo $settings['markup_percentage']; ?>" />
        </div>
        
        <div class="form-group">
            <label>Low Stock Threshold</label>
            <input type="number" name="low_stock_threshold" class="form-control" value="<?php echo $settings['low_stock_threshold']; ?>" />
        </div>
        
        <button type="submit" class="btn btn-success">Save Settings</button>
    </form>
</div>
```

### Product Import System

Create a product import functionality:

1. Create an import controller:
```php
<?php
// userfiles/modules/dropshipping/controllers/ImportController.php

namespace Modules\Dropshipping\Controllers;

class ImportController {
    
    private $apiKey;
    private $markupPercentage;
    
    public function __construct() {
        $settings = get_option('settings', 'dropshipping');
        $this->apiKey = $settings['supplier_api_key'];
        $this->markupPercentage = $settings['markup_percentage'];
    }
    
    public function importProducts($supplier = 'default', $category = null) {
        // Implementation depends on supplier API
        switch($supplier) {
            case 'aliexpress':
                return $this->importFromAliExpress($category);
            case 'oberlo':
                return $this->importFromOberlo($category);
            default:
                return $this->importFromDefaultSupplier($category);
        }
    }
    
    private function importFromDefaultSupplier($category) {
        // Example implementation
        $apiEndpoint = "https://supplier-api.example.com/products";
        if ($category) {
            $apiEndpoint .= "?category=" . urlencode($category);
        }
        
        $ch = curl_init($apiEndpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $this->apiKey,
            'Accept: application/json'
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        $products = json_decode($response, true);
        $importCount = 0;
        
        foreach ($products as $product) {
            // Calculate price with markup
            $costPrice = $product['price'];
            $sellingPrice = $costPrice * (1 + ($this->markupPercentage / 100));
            
            // Prepare product data
            $productData = [
                'title' => $product['name'],
                'content' => $product['description'],
                'price' => $sellingPrice,
                'content_data' => [
                    'cost_price' => $costPrice,
                    'supplier_id' => $product['id'],
                    'supplier' => 'default'
                ],
                'is_active' => 1
            ];
            
            // Save product
            $saved = save_content($productData);
            
            if ($saved) {
                $importCount++;
                
                // Save product images
                if (isset($product['images']) && is_array($product['images'])) {
                    foreach ($product['images'] as $imageUrl) {
                        // Download and attach image
                        $this->downloadAndAttachImage($saved, $imageUrl);
                    }
                }
                
                // Save product variants if any
                if (isset($product['variants']) && is_array($product['variants'])) {
                    foreach ($product['variants'] as $variant) {
                        $this->saveProductVariant($saved, $variant);
                    }
                }
            }
        }
        
        return [
            'success' => true,
            'imported' => $importCount
        ];
    }
    
    private function downloadAndAttachImage($productId, $imageUrl) {
        // Download image to temporary location
        $tempImage = tempnam(sys_get_temp_dir(), 'download');
        file_put_contents($tempImage, file_get_contents($imageUrl));
        
        // Attach image to product
        $mediaId = save_media($tempImage, [
            'rel_type' => 'content',
            'rel_id' => $productId
        ]);
        
        // Clean up
        @unlink($tempImage);
        
        return $mediaId;
    }
    
    private function saveProductVariant($productId, $variant) {
        // Implementation depends on how variants are structured in Microweber
        // This is a simplified example
        $variantData = [
            'product_id' => $productId,
            'title' => $variant['title'],
            'price' => $variant['price'] * (1 + ($this->markupPercentage / 100)),
            'sku' => $variant['sku'],
            'stock' => $variant['stock']
        ];
        
        // Save variant using the appropriate Microweber function
        // This will depend on how variants are implemented in your version
        db_save('custom_fields', $variantData);
    }
}
```

2. Create an import interface in the admin panel:
```php
// userfiles/modules/dropshipping/admin.php

<div class="module-admin-wrapper">
    <div class="card style-1 mb-3">
        <div class="card-header">
            <h5>Product Import</h5>
        </div>
        <div class="card-body pt-3">
            <form method="post" id="dropshipping-import-form">
                <div class="form-group">
                    <label>Supplier</label>
                    <select name="supplier" class="form-control">
                        <option value="default">Default Supplier</option>
                        <option value="aliexpress">AliExpress</option>
                        <option value="oberlo">Oberlo</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Category (optional)</label>
                    <input type="text" name="category" class="form-control" placeholder="Leave empty to import all" />
                </div>
                
                <button type="button" id="start-import" class="btn btn-primary">Start Import</button>
                
                <div id="import-progress" class="mt-3 d-none">
                    <div class="progress">
                        <div class="progress-bar" role="progressbar" style="width: 0%"></div>
                    </div>
                    <div id="import-status" class="mt-2"></div>
                </div>
            </form>
        </div>
    </div>
</div>

<script>
$(document).ready(function() {
    $('#start-import').on('click', function() {
        var supplier = $('select[name="supplier"]').val();
        var category = $('input[name="category"]').val();
        
        $('#import-progress').removeClass('d-none');
        $('#import-status').html('Starting import...');
        
        $.ajax({
            url: mw.settings.api_url + 'dropshipping/import',
            type: 'POST',
            data: {
                supplier: supplier,
                category: category
            },
            success: function(response) {
                if (response.success) {
                    $('#import-status').html('Import completed. ' + response.imported + ' products were imported.');
                    $('.progress-bar').css('width', '100%');
                } else {
                    $('#import-status').html('Import failed: ' + response.message);
                }
            },
            error: function() {
                $('#import-status').html('Error occurred during import.');
            }
        });
    });
});
</script>
```

## Supplier Integration

Integrate with popular dropshipping suppliers:

### AliExpress Integration

1. Create a specific adapter for AliExpress:
```php
<?php
// userfiles/modules/dropshipping/suppliers/AliExpressAdapter.php

namespace Modules\Dropshipping\Suppliers;

class AliExpressAdapter {
    
    private $apiKey;
    
    public function __construct($apiKey) {
        $this->apiKey = $apiKey;
    }
    
    public function getProducts($category = null, $page = 1, $limit = 100) {
        // Implementation specific to AliExpress API
        $apiEndpoint = "https://aliexpress-api.example.com/products";
        $queryParams = [
            'page' => $page,
            'limit' => $limit
        ];
        
        if ($category) {
            $queryParams['category'] = $category;
        }
        
        $apiEndpoint .= '?' . http_build_query($queryParams);
        
        $ch = curl_init($apiEndpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $this->apiKey,
            'Accept: application/json'
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    public function placeOrder($orderData) {
        $apiEndpoint = "https://aliexpress-api.example.com/orders";
        
        $ch = curl_init($apiEndpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($orderData));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $this->apiKey,
            'Content-Type: application/json',
            'Accept: application/json'
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    public function getOrderStatus($orderId) {
        $apiEndpoint = "https://aliexpress-api.example.com/orders/" . $orderId;
        
        $ch = curl_init($apiEndpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $this->apiKey,
            'Accept: application/json'
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    public function getTracking($orderId) {
        $apiEndpoint = "https://aliexpress-api.example.com/orders/" . $orderId . "/tracking";
        
        $ch = curl_init($apiEndpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Authorization: Bearer ' . $this->apiKey,
            'Accept: application/json'
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
}
```

### Generic Supplier Integration

Create a factory pattern to handle multiple suppliers:

```php
<?php
// userfiles/modules/dropshipping/suppliers/SupplierFactory.php

namespace Modules\Dropshipping\Suppliers;

class SupplierFactory {
    
    public static function create($supplier) {
        $settings = get_option('settings', 'dropshipping');
        $apiKey = $settings['supplier_api_key'];
        
        switch($supplier) {
            case 'aliexpress':
                return new AliExpressAdapter($apiKey);
            case 'oberlo':
                return new OberloAdapter($apiKey);
            default:
                return new DefaultSupplier($apiKey);
        }
    }
}
```

## Payment Gateway Setup

Configure multiple payment gateways:

### Stripe Integration

1. Add Stripe as a payment option:
```php
<?php
// userfiles/modules/dropshipping/payments/StripePayment.php

namespace Modules\Dropshipping\Payments;

class StripePayment {
    
    private $apiKey;
    private $secretKey;
    
    public function __construct($apiKey, $secretKey) {
        $this->apiKey = $apiKey;
        $this->secretKey = $secretKey;
    }
    
    public function processPayment($amount, $currency, $cardDetails) {
        // Stripe API implementation
        \Stripe\Stripe::setApiKey($this->secretKey);
        
        try {
            $charge = \Stripe\Charge::create([
                'amount' => $amount * 100, // Stripe requires amount in cents
                'currency' => $currency,
                'source' => $cardDetails['token'],
                'description' => 'Order payment'
            ]);
            
            return [
                'success' => true,
                'transaction_id' => $charge->id
            ];
        } catch (\Exception $e) {
            return [
                'success' => false,
                'message' => $e->getMessage()
            ];
        }
    }
}
```

### PayPal Integration

```php
<?php
// userfiles/modules/dropshipping/payments/PayPalPayment.php

namespace Modules\Dropshipping\Payments;

class PayPalPayment {
    
    private $clientId;
    private $clientSecret;
    private $isSandbox;
    
    public function __construct($clientId, $clientSecret, $isSandbox = false) {
        $this->clientId = $clientId;
        $this->clientSecret = $clientSecret;
        $this->isSandbox = $isSandbox;
    }
    
    public function getApiUrl() {
        return $this->isSandbox 
            ? 'https://api-m.sandbox.paypal.com' 
            : 'https://api-m.paypal.com';
    }
    
    public function getAccessToken() {
        $ch = curl_init($this->getApiUrl() . '/v1/oauth2/token');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_USERPWD, $this->clientId . ":" . $this->clientSecret);
        curl_setopt($ch, CURLOPT_POSTFIELDS, "grant_type=client_credentials");
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Accept: application/json',
            'Accept-Language: en_US'
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        $data = json_decode($response, true);
        return $data['access_token'] ?? null;
    }
    
    public function createOrder($amount, $currency) {
        $accessToken = $this->getAccessToken();
        
        $payload = [
            'intent' => 'CAPTURE',
            'purchase_units' => [
                [
                    'amount' => [
                        'currency_code' => $currency,
                        'value' => number_format($amount, 2, '.', '')
                    ]
                ]
            ],
            'application_context' => [
                'return_url' => url_to_module('dropshipping') . 'payments/paypal/success',
                'cancel_url' => url_to_module('dropshipping') . 'payments/paypal/cancel'
            ]
        ];
        
        $ch = curl_init($this->getApiUrl() . '/v2/checkout/orders');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $accessToken
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
    
    public function captureOrder($orderId) {
        $accessToken = $this->getAccessToken();
        
        $ch = curl_init($this->getApiUrl() . '/v2/checkout/orders/' . $orderId . '/capture');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $accessToken
        ]);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
}
```

## Shipping Configuration

Set up automated shipping rate calculation:

```php
<?php
// userfiles/modules/dropshipping/shipping/ShippingCalculator.php

namespace Modules\Dropshipping\Shipping;

class ShippingCalculator {
    
    private $shippingZones;
    private $methods;
    
    public function __construct() {
        // Load shipping zones and methods from database
        $this->shippingZones = db_get('shipping_zones');
        $this->methods = db_get('shipping_methods');
    }
    
    public function calculateRates($address, $products) {
        $zone = $this->findShippingZone($address);
        
        if (!$zone) {
            return [
                'success' => false,
                'message' => 'No shipping available to this location'
            ];
        }
        
        $availableMethods = [];
        $totalWeight = $this->calculateTotalWeight($products);
        
        foreach ($this->methods as $method) {
            if ($method['zone_id'] == $zone['id']) {
                $rate = $this->calculateRate($method, $totalWeight);
                
                $availableMethods[] = [
                    'id' => $method['id'],
                    'name' => $method['name'],
                    'rate' => $rate,
                    'estimated_days' => $method['estimated_days']
                ];
            }
        }
        
        return [
            'success' => true,
            'methods' => $availableMethods
        ];
    }
    
    private function findShippingZone($address) {
        foreach ($this->shippingZones as $zone) {
            $countries = json_decode($zone['countries'], true);
            
            if (in_array($address['country'], $countries)) {
                return $zone;
            }
        }
        
        return null;
    }
    
    private function calculateTotalWeight($products) {
        $weight = 0;
        
        foreach ($products as $product) {
            $productWeight = $product['weight'] ?? 0;
            $quantity = $product['quantity'] ?? 1;
            
            $weight += ($productWeight * $quantity);
        }
        
        return $weight;
    }
    
    private function calculateRate($method, $weight) {
        $baseRate = $method['base_rate'];
        $perWeightRate = $method['per_weight_rate'];
        
        return $baseRate + ($weight * $perWeightRate);
    }
}
```

## Order Management System

Create an order management system to handle the dropshipping workflow:

```php
<?php
// userfiles/modules/dropshipping/orders/OrderManager.php

namespace Modules\Dropshipping\Orders;

use Modules\Dropshipping\Suppliers\SupplierFactory;

class OrderManager {
    
    private $settings;
    
    public function __construct() {
        $this->settings = get_option('settings', 'dropshipping');
    }
    
    public function processNewOrder($orderId) {
        // Get order details
        $order = get_order($orderId);
        
        if (!$order) {
            return [
                'success' => false,
                'message' => 'Order not found'
            ];
        }
        
        // Extract order items
        $items = get_order_items($orderId);
        
        // Group items by supplier
        $supplierItems = [];
        
        foreach ($items as $item) {
            $productId = $item['product_id'];
            $product = get_content_by_id($productId);
            
            $supplier = $product['content_data']['supplier'] ?? 'default';
            
            if (!isset($supplierItems[$supplier])) {
                $supplierItems[$supplier] = [];
            }
            
            $supplierItems[$supplier][] = [
                'supplier_id' => $product['content_data']['supplier_id'],
                'quantity' => $item['qty'],
                'options' => $item['options'] ?? []
            ];
        }
        
        // Process each supplier's items
        $results = [];
        
        foreach ($supplierItems as $supplier => $items) {
            $supplierAdapter = SupplierFactory::create($supplier);
            
            $supplierOrder = [
                'items' => $items,
                'shipping_address' => [
                    'name' => $order['first_name'] . ' ' . $order['last_name'],
                    'address1' => $order['address'],
                    'address2' => $order['address2'] ?? '',
                    'city' => $order['city'],
                    'state' => $order['state'],
                    'country' => $order['country'],
                    'zip' => $order['zip'],
                    'phone' => $order['phone']
                ]
            ];
            
            $result = $supplierAdapter->placeOrder($supplierOrder);
            
            if ($result['success']) {
                // Save supplier order reference
                db_save('dropshipping_orders', [
                    'order_id' => $orderId,
                    'supplier' => $supplier,
                    'supplier_order_id' => $result['order_id'],
                    'status' => 'processing'
                ]);
            }
            
            $results[$supplier] = $result;
        }
        
        return [
            'success' => true,
            'results' => $results
        ];
    }
    
    public function syncOrderStatuses() {
        // Get all processing dropshipping orders
        $orders = db_get('dropshipping_orders', [
            'status' => 'processing'
        ]);
        
        foreach ($orders as $order) {
            $supplier = $order['supplier'];
            $supplierOrderId = $order['supplier_order_id'];
            
            $supplierAdapter = SupplierFactory::create($supplier);
            $status = $supplierAdapter->getOrderStatus($supplierOrderId);
            
            if ($status['status'] != $order['status']) {
                // Update status
                db_save('dropshipping_orders', [
                    'id' => $order['id'],
                    'status' => $status['status']
                ]);
                
                // If shipped, get tracking
                if ($status['status'] == 'shipped') {
                    $tracking = $supplierAdapter->getTracking($supplierOrderId);
                    
                    if ($tracking) {
                        db_save('dropshipping_orders', [
                            'id' => $order['id'],
                            'tracking_number' => $tracking['number'],
                            'tracking_url' => $tracking['url'],
                            'carrier' => $tracking['carrier']
                        ]);
                        
                        // Send tracking notification to customer
                        $this->sendTrackingNotification($order['order_id'], $tracking);
                    }
                }
            }
        }
    }
    
    private function sendTrackingNotification($orderId, $tracking) {
        $order = get_order($orderId);
        
        if (!$order) {
            return false;
        }
        
        $email = $order['email'];
        $customerName = $order['first_name'];
        
        $emailTemplate = 'Your order #' . $orderId . ' has been shipped!<br><br>';
        $emailTemplate .= 'You can track your package with ' . $tracking['carrier'] . ' using tracking number: ' . $tracking['number'] . '<br><br>';
        $emailTemplate .= 'Tracking link: <a href="' . $tracking['url'] . '">' . $tracking['url'] . '</a><br><br>';
        $emailTemplate .= 'Thank you for your order!';
        
        return send_mail([
            'to' => $email,
            'subject' => 'Your order has been shipped! Track your package',
            'message' => $emailTemplate,
            'from' => get_option('email_from', 'website')
        ]);
    }
}
```

### Order