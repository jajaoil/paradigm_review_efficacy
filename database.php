<?php
require_once 'config.php';

class ResearchDatabase {
    private $db;
    
    public function __construct() {
        $this->initializeDatabase();
    }
    
    private function initializeDatabase() {
        // Create data directory if it doesn't exist
        if (!file_exists(dirname(DB_PATH))) {
            mkdir(dirname(DB_PATH), 0777, true);
        }
        
        $this->db = new SQLite3(DB_PATH);
        $this->db->enableExceptions(true);
        
        // Create tables
        $this->createTables();
    }
    
    private function createTables() {
        $queries = [
            "CREATE TABLE IF NOT EXISTS research_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                participant_id TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                session_data TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )",
            
            "CREATE TABLE IF NOT EXISTS paradigm_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                paradigm TEXT NOT NULL,
                code_view_time INTEGER,
                review_time INTEGER,
                defects_identified TEXT,
                comments TEXT,
                comprehension_answers TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES research_sessions (session_id)
            )",
            
            "CREATE INDEX IF NOT EXISTS idx_session_id ON research_sessions(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_paradigm ON paradigm_reviews(paradigm)"
        ];
        
        foreach ($queries as $query) {
            $this->db->exec($query);
        }
    }
    
    public function saveResearchData($sessionId, $participantId, $experienceLevel, $metrics) {
        try {
            // Begin transaction
            $this->db->exec('BEGIN TRANSACTION');
            
            // Save main session data
            $stmt = $this->db->prepare("
                INSERT OR REPLACE INTO research_sessions 
                (session_id, participant_id, experience_level, session_data) 
                VALUES (:session_id, :participant_id, :experience_level, :session_data)
            ");
            
            $stmt->bindValue(':session_id', $sessionId);
            $stmt->bindValue(':participant_id', $participantId);
            $stmt->bindValue(':experience_level', $experienceLevel);
            $stmt->bindValue(':session_data', json_encode($metrics));
            $stmt->execute();
            
            // Save individual paradigm reviews
            if (isset($metrics['paradigms'])) {
                foreach ($metrics['paradigms'] as $paradigm => $data) {
                    $stmt = $this->db->prepare("
                        INSERT INTO paradigm_reviews 
                        (session_id, paradigm, code_view_time, review_time, defects_identified, comments, comprehension_answers)
                        VALUES (:session_id, :paradigm, :code_view_time, :review_time, :defects_identified, :comments, :comprehension_answers)
                    ");
                    
                    $stmt->bindValue(':session_id', $sessionId);
                    $stmt->bindValue(':paradigm', $paradigm);
                    $stmt->bindValue(':code_view_time', $data['codeViewTime'] ?? 0);
                    $stmt->bindValue(':review_time', $data['reviewTime'] ?? 0);
                    $stmt->bindValue(':defects_identified', json_encode($data['defectsIdentified'] ?? []));
                    $stmt->bindValue(':comments', $data['comments'] ?? '');
                    $stmt->bindValue(':comprehension_answers', json_encode($data['comprehensionAnswers'] ?? {}));
                    $stmt->execute();
                }
            }
            
            // Commit transaction
            $this->db->exec('COMMIT');
            return ['success' => true, 'message' => 'Data saved successfully'];
            
        } catch (Exception $e) {
            $this->db->exec('ROLLBACK');
            return ['success' => false, 'error' => $e->getMessage()];
        }
    }
    
    public function getResearchData() {
        $result = $this->db->query("
            SELECT rs.session_id, rs.participant_id, rs.experience_level, rs.session_data, rs.created_at,
                   pr.paradigm, pr.code_view_time, pr.review_time, pr.defects_identified, pr.comments
            FROM research_sessions rs
            LEFT JOIN paradigm_reviews pr ON rs.session_id = pr.session_id
            ORDER BY rs.created_at DESC
        ");
        
        $data = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $data[] = $row;
        }
        
        return $data;
    }
    
    public function __destruct() {
        if ($this->db) {
            $this->db->close();
        }
    }
}
?>