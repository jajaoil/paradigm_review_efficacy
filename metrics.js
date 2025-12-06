class ResearchMetrics {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.startTime = null;
        this.currentParadigm = null;
        this.metrics = {
            participantInfo: {},
            paradigms: {},
            sessionDuration: 0,
            completionTime: null
        };
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    startSession(participantInfo) {
        this.startTime = Date.now();
        this.metrics.participantInfo = participantInfo;
        this.metrics.sessionStart = new Date().toISOString();
        
        console.log('Research session started:', this.sessionId);
    }

    startParadigmReview(paradigm) {
        this.currentParadigm = paradigm;
        this.metrics.paradigms[paradigm] = {
            startTime: Date.now(),
            codeViewTime: 0,
            reviewTime: 0,
            defectsIdentified: [],
            comments: '',
            comprehensionAnswers: {},
            completionTime: null
        };
    }

    trackCodeViewTime() {
        if (this.currentParadigm && this.metrics.paradigms[this.currentParadigm]) {
            this.metrics.paradigms[this.currentParadigm].codeViewTime = 
                Date.now() - this.metrics.paradigms[this.currentParadigm].startTime;
        }
    }

    recordDefectSelection(defect, isSelected) {
        if (this.currentParadigm) {
            if (isSelected) {
                this.metrics.paradigms[this.currentParadigm].defectsIdentified.push(defect);
            } else {
                const index = this.metrics.paradigms[this.currentParadigm].defectsIdentified.indexOf(defect);
                if (index > -1) {
                    this.metrics.paradigms[this.currentParadigm].defectsIdentified.splice(index, 1);
                }
            }
        }
    }

    recordComprehensionAnswer(question, answer) {
        if (this.currentParadigm) {
            this.metrics.paradigms[this.currentParadigm].comprehensionAnswers[question] = answer;
        }
    }

    completeParadigmReview(comments) {
        if (this.currentParadigm) {
            this.metrics.paradigms[this.currentParadigm].reviewTime = 
                Date.now() - this.metrics.paradigms[this.currentParadigm].startTime - 
                this.metrics.paradigms[this.currentParadigm].codeViewTime;
            
            this.metrics.paradigms[this.currentParadigm].comments = comments;
            this.metrics.paradigms[this.currentParadigm].completionTime = Date.now();
        }
    }

    completeSession() {
        this.metrics.sessionDuration = Date.now() - this.startTime;
        this.metrics.completionTime = new Date().toISOString();
        
        this.saveToDatabase();
        return this.metrics;
    }

    async saveToDatabase() {
        try {
            const response = await fetch('php/api.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'save_research_data',
                    sessionId: this.sessionId,
                    metrics: this.metrics
                })
            });

            const result = await response.json();
            console.log('Data saved:', result);
        } catch (error) {
            console.error('Error saving data:', error);
        }
    }

    getProgress() {
        const completed = Object.keys(this.metrics.paradigms).length;
        return {
            completed: completed,
            total: 3,
            percentage: (completed / 3) * 100
        };
    }
}