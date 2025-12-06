<?php
// Research Platform Configuration
define('DB_PATH', __DIR__ . '/../data/research-data.db');
define('ALLOWED_ORIGINS', ['http://localhost', 'http://127.0.0.1', 'https://yourusername.github.io']);

// Set headers for CORS
header('Access-Control-Allow-Origin: ' . getAllowedOrigin());
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

function getAllowedOrigin() {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if (in_array($origin, ALLOWED_ORIGINS)) {
        return $origin;
    }
    return ALLOWED_ORIGINS[0];
}

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}
?>