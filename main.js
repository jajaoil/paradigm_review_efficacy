let researchMetrics = new ResearchMetrics();
let reviewedParadigms = new Set();
let sessionTimer = null;
let sessionStartTime = null;

function startResearchSession() {
    const participantId = document.getElementById('participant-id').value;
    const experienceLevel = document.getElementById('experience-level').value;
    
    if (!participantId) {
        alert('Please enter a Participant ID');
        return;
    }
    
    researchMetrics.startSession({
        participantId: participantId,
        experienceLevel: experienceLevel,
        startTime: new Date().toISOString()
    });
    
    document.getElementById('participant-form').classList.add('hidden');
    document.getElementById('research-interface').classList.remove('hidden');
    
    startSessionTimer();
}

function startSessionTimer() {
    sessionStartTime = Date.now();
    sessionTimer = setInterval(() => {
        const elapsed = Math.floor((Date.now() - sessionStartTime) / 1000);
        document.getElementById('timer').textContent = `Time: ${elapsed}s`;
    }, 1000);
}

function loadCodeSample(paradigm) {
    const sample = codeSamples[paradigm];
    if (!sample) return;
    
    researchMetrics.startParadigmReview(paradigm);
    
    document.getElementById('code-title').textContent = sample.title;
    document.getElementById('current-paradigm').textContent = paradigm.toUpperCase();
    document.getElementById('code-content').textContent = sample.code;
    
    // Add syntax highlighting
    highlightCode(paradigm);
    
    // Setup defect checkboxes
    setupDefectCheckboxes(sample.defects);
    
    // Setup comprehension questions
    setupComprehensionQuestions(sample.questions);
    
    // Track when user starts reviewing (moves away from code)
    setTimeout(() => researchMetrics.trackCodeViewTime(), 1000);
}

function highlightCode(paradigm) {
    const codeElement = document.getElementById('code-content');
    let code = codeElement.textContent;
    
    // Simple syntax highlighting
    if (paradigm === 'java' || paradigm === 'oop') {
        code = code.replace(/\b(public|private|class|void|double|int|if|else|return)\b/g, '<span class="keyword">$1</span>');
        code = code.replace(/\b(deposit|withdraw|transfer|getBalance)\b/g, '<span class="function">$1</span>');
    } else if (paradigm === 'javascript' || paradigm === 'functional') {
        code = code.replace(/\b(const|let|function|return|if|else)\b/g, '<span class="keyword">$1</span>');
        code = code.replace(/\b(createAccount|deposit|withdraw|transfer|processTransactions)\b/g, '<span class="function">$1</span>');
    } else if (paradigm === 'c' || paradigm === 'procedural') {
        code = code.replace(/\b(#include|#define|struct|void|int|double|char|if|else|for|return)\b/g, '<span class="keyword">$1</span>');
        code = code.replace(/\b(createAccount|deposit|withdraw|transfer|findAccount|printf|strcpy|strcmp)\b/g, '<span class="function">$1</span>');
    }
    
    code = code.replace(/(".*?"|'.*?')/g, '<span class="string">$1</span>');
    code = code.replace(/\/\/.*$/gm, '<span class="comment">$&</span>');
    code = code.replace(/\b\d+\b/g, '<span class="number">$&</span>');
    
    // Add line numbers
    const lines = code.split('\n');
    const numberedCode = lines.map((line, index) => 
        `<div class="code-line"><span class="line-number">${index + 1}</span>${line}</div>`
    ).join('');
    
    codeElement.innerHTML = numberedCode;
}

function setupDefectCheckboxes(defects) {
    const container = document.getElementById('defect-checkboxes');
    container.innerHTML = '';
    
    defects.forEach((defect, index) => {
        const div = document.createElement('div');
        div.className = 'defect-option flex items-center space-x-3 p-2 rounded hover:bg-gray-50';
        div.innerHTML = `
            <input type="checkbox" id="defect-${index}" value="${defect}" 
                   onchange="trackDefectSelection('${defect}', this.checked)"
                   class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500">
            <label for="defect-${index}" class="text-sm text-gray-700">${defect}</label>
        `;
        container.appendChild(div);
    });
}

function setupComprehensionQuestions(questions) {
    const container = document.getElementById('comprehension-questions');
    container.innerHTML = '';
    
    questions.forEach((q, qIndex) => {
        const div = document.createElement('div');
        div.className = 'bg-gray-50 p-4 rounded-lg';
        div.innerHTML = `
            <p class="font-medium mb-2">${q.question}</p>
            <div class="space-y-1">
                ${q.options.map((option, oIndex) => `
                    <label class="flex items-center space-x-2">
                        <input type="radio" name="question-${qIndex}" value="${option}" 
                               onchange="recordComprehensionAnswer('${q.question}', '${option}')"
                               class="w-4 h-4 text-blue-600">
                        <span class="text-sm">${option}</span>
                    </label>
                `).join('')}
            </div>
        `;
        container.appendChild(div);
    });
}

function trackDefectSelection(defect, isSelected) {
    researchMetrics.recordDefectSelection(defect, isSelected);
}

function recordComprehensionAnswer(question, answer) {
    researchMetrics.recordComprehensionAnswer(question, answer);
}

function submitReview() {
    const comments = document.getElementById('review-comments').value;
    const currentParadigm = researchMetrics.currentParadigm;
    
    researchMetrics.completeParadigmReview(comments);
    reviewedParadigms.add(currentParadigm);
    
    // Update progress
    const progress = researchMetrics.getProgress();
    document.getElementById('progress-bar').style.width = `${progress.percentage}%`;
    document.getElementById('progress-text').textContent = 
        `${progress.completed} of ${progress.total} paradigms completed`;
    
    // Clear form
    document.getElementById('review-comments').value = '';
    document.getElementById('defect-checkboxes').innerHTML = '';
    document.getElementById('comprehension-questions').innerHTML = '';
    document.getElementById('code-content').textContent = '';
    document.getElementById('current-paradigm').textContent = '';
    
    // Check if session is complete
    if (progress.completed >= progress.total) {
        completeResearchSession();
    } else {
        alert(`Thank you! ${currentParadigm.toUpperCase()} review submitted. Please select another paradigm.`);
    }
}

function completeResearchSession() {
    clearInterval(sessionTimer);
    
    const results = researchMetrics.completeSession();
    
    document.getElementById('research-interface').classList.add('hidden');
    document.getElementById('completion-screen').classList.remove('hidden');
    
    // Display results summary
    displaySessionResults(results);
}

function displaySessionResults(results) {
    const container = document.getElementById('session-results');
    let html = `
        <h3 class="font-semibold mb-3">Session Summary</h3>
        <div class="space-y-2 text-sm">
            <p><strong>Session ID:</strong> ${results.participantInfo.participantId}</p>
            <p><strong>Experience Level:</strong> ${results.participantInfo.experienceLevel}</p>
            <p><strong>Total Duration:</strong> ${Math.round(results.sessionDuration / 1000)} seconds</p>
        </div>
        <div class="mt-4">
            <h4 class="font-medium mb-2">Paradigm Reviews Completed:</h4>
            <ul class="list-disc list-inside space-y-1 text-sm">
    `;
    
    Object.keys(results.paradigms).forEach(paradigm => {
        const data = results.paradigms[paradigm];
        html += `
            <li>${paradigm.toUpperCase()}:
                <span class="text-gray-600">
                    ${Math.round(data.reviewTime / 1000)}s, 
                    ${data.defectsIdentified.length} defects identified
                </span>
            </li>
        `;
    });
    
    html += `</ul></div>`;
    container.innerHTML = html;
}