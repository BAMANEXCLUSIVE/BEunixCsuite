<?php
// index.php - Main entry point for BEunixCsuite

// Load the configuration file
$config = require __DIR__ . '/config/beunixcsuite.php';

// Display application information from the configuration
echo "Welcome to " . $config['app_name'] . " (version " . $config['version'] . ").<br>";

// Check if supplier sync is enabled and active
if ($config['suppliers']['enabled'] && $config['suppliers']['auto_sync']) {
    echo "Supplier auto-sync is active and will run every " . $config['suppliers']['sync_interval'] . " seconds.";
} else {
    echo "Supplier auto-sync is disabled.";
}
