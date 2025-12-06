<?php
require_once 'database.php';

try {
    // Get JSON input
    $input = json_decode(file_get_contents('php://input'), true);
    
    if (!$input) {
        throw new Exception('Invalid JSON input');
    }
    
    $action = $input['action'] ?? '';
    $db = new ResearchDatabase();
    
    switch ($action) {
        case 'save_research_data':
            $result = $db->saveResearchData(
                $input['sessionId'],
                $input['metrics']['participantInfo']['participantId'],
                $input['metrics']['participantInfo']['experienceLevel'],
                $input['metrics']
            );
            break;
            
        case 'get_research_data':
            $result = $db->getResearchData();
            break;
            
        default:
            throw new Exception('Unknown action: ' . $action);
    }
    
    echo json_encode(['success' => true, 'data' => $result]);
    
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => $e->getMessage()]);
}
?>