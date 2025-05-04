<?php
// config/beunixcsuite.php

return [
    'app_name' => 'BEunixCsuite Ecommerce',
    'version' => '1.0.0',
    'suppliers' => [
        'enabled' => true,
        'auto_sync' => true,
        'sync_interval' => 3600, // hourly interval (3600 seconds)
    ],
    'project_management' => [
        'enabled' => true,
        'api_endpoint' => 'http://localhost:8000/api',
        'token_refresh_interval' => 86400, // daily interval (86400 seconds)
    ],
    'integrations' => [
        'payment_gateways' => ['stripe', 'paypal', 'square'],
        'shipping_providers' => ['fedex', 'ups', 'usps', 'dhl'],
        'analytics' => ['google', 'matomo', 'custom']
    ]
];
