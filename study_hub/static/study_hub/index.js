document.addEventListener('DOMContentLoaded', function () {
    const topicCards = document.querySelectorAll('.topic-card');
    const topicView = document.querySelector('#topic-view');
    const topicContent = document.querySelector('#topic-content');
    const listTopics = document.querySelector('#topics-list');
    const backButton = document.querySelector('#back-button');

    function getCSRFToken() {
        const cookie = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    function highlightSQL(code) {
        const keywords = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'ON', 'UNION', 'DISTINCT', 'LIMIT', 'INSERT INTO', 'INSERT', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'ASC', 'DESC', 'AND', 'OR', 'NOT', 'IN', 'IS', 'NULL', 'LIKE', 'BETWEEN', 'AS'];
        const functions = ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX'];

        let html = code
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // Highlight strings in quotes
        html = html.replace(/('([^'\\]|\\.)*')/g, '<span class="sql-string">$1</span>');

        // Highlight keywords with word boundaries
        keywords.forEach(kw => {
            const regex = new RegExp(`\\b(${kw.replace(' ', '\\s+')})\\b`, 'gi');
            html = html.replace(regex, '<span class="sql-keyword">$1</span>');
        });

        // Highlight functions
        functions.forEach(fn => {
            const regex = new RegExp(`\\b(${fn})\\b(?=\\s*\\()`, 'gi');
            html = html.replace(regex, '<span class="sql-func">$1</span>');
        });

        return html;
    }

    function formatTheory(theoryText) {
        if (!theoryText) return '';
        
        const rawSections = theoryText.trim().split(/\n\s*\n/);
        let resultHTML = '';

        rawSections.forEach(section => {
            const trimmed = section.trim();
            if (!trimmed) return;

            const lines = trimmed.split('\n').map(l => l.trim()).filter(Boolean);

            // Header check (e.g. "Example:", "Basic syntax:", "Common operators:", "Often used with:")
            if (/^(Example|Examples|Basic syntax|Common operators|Often used with):?$/i.test(trimmed)) {
                resultHTML += `<h6 class="theory-section-header mt-4 mb-2"><i class="fa-solid fa-code-branch text-primary me-2"></i>${trimmed}</h6>`;
                return;
            }

            // Badge list check (e.g. COUNT(), SUM(), or =, !=, >, or ASC = Ascending)
            const isBadgeList = lines.length > 1 && lines.every(line => 
                /^[A-Z_]+\(\)$/i.test(line) || 
                /^[=!><]=?$/.test(line) || 
                /^[A-Z]+\s*=\s*.+$/i.test(line)
            );

            if (isBadgeList) {
                resultHTML += `<div class="operator-badges mb-3">`;
                lines.forEach(item => {
                    resultHTML += `<span class="operator-badge"><i class="fa-solid fa-terminal text-info me-2"></i>${item}</span>`;
                });
                resultHTML += `</div>`;
                return;
            }

            // Code block check
            const isCodeBlock = lines.some(line => 
                /^(SELECT|FROM|WHERE|GROUP BY\s+[a-z_0-9]+|HAVING\s+|ORDER BY\s+|INNER JOIN|LEFT JOIN|RIGHT JOIN|INSERT INTO|UPDATE\s+[a-z_0-9]+|DELETE FROM|LIMIT\s+\d+|DISTINCT\s+|UNION)/i.test(line)
            );

            const isExplanatorySentence = lines[0].toLowerCase().includes('statement') || 
                                         lines[0].toLowerCase().includes('combines') || 
                                         lines[0].toLowerCase().includes('returns') || 
                                         lines[0].toLowerCase().includes('clause') || 
                                         lines[0].toLowerCase().includes('removes') || 
                                         lines[0].toLowerCase().includes('changes') || 
                                         lines[0].toLowerCase().includes('used to');

            if (isCodeBlock && !isExplanatorySentence) {
                resultHTML += `
                    <div class="code-example-card mb-3">
                        <div class="code-example-header">
                            <div class="d-flex align-items-center gap-2">
                                <span class="dot dot-red"></span>
                                <span class="dot dot-yellow"></span>
                                <span class="dot dot-green"></span>
                            </div>
                            <span class="ms-2">SQL Syntax & Example</span>
                        </div>
                        <pre class="sql-code-snippet"><code>${highlightSQL(trimmed)}</code></pre>
                    </div>`;
                return;
            }

            // Default: Paragraph text
            resultHTML += `<p class="theory-paragraph mb-3">${trimmed.replace(/\n/g, '<br>')}</p>`;
        });

        return resultHTML;
    }

    topicCards.forEach((card) => {
        card.addEventListener('click', async () => {
            const topicId = card.dataset.topicId;
            try {
                const response = await fetch(`/topics/${topicId}/`);

                if (!response.ok) {
                    if (response.status === 403 || response.status === 401) {
                        throw new Error('login_required');
                    }
                    throw new Error('Error loading topic details!');
                }

                const topic = await response.json();
                const optionLabels = ['A', 'B', 'C', 'D'];

                topicContent.innerHTML = `
                <div class="topic-detail-wrapper">
                    <!-- Header -->
                    <div class="mb-4">
                        <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 rounded-pill mb-2">
                            <i class="fa-solid fa-graduation-cap me-1"></i> Module Theory
                        </span>
                        <h1 class="display-6 fw-bold mb-2">${topic.title}</h1>
                        <p class="lead text-muted">${topic.summary}</p>
                    </div>

                    <!-- Theory Container -->
                    <div class="theory-container mb-5">
                        <div class="d-flex align-items-center gap-2 mb-3 text-info fw-semibold border-bottom pb-2" style="border-color: rgba(255,255,255,0.08) !important;">
                            <i class="fa-solid fa-book-open"></i> Theory & Syntax Reference
                        </div>
                        <div class="theory-body">${formatTheory(topic.theory)}</div>
                    </div>

                    <!-- Questions Section -->
                    <div class="questions-section">
                        <div class="d-flex align-items-center justify-content-between mb-4">
                            <h3 class="h4 mb-0 text-white">
                                <i class="fa-solid fa-clipboard-question text-warning me-2"></i> Knowledge Check
                            </h3>
                            <span class="badge bg-dark border border-secondary text-muted">
                                ${topic.questions.length} Question${topic.questions.length === 1 ? '' : 's'}
                            </span>
                        </div>

                        ${topic.questions.map((question, qIdx) => `
                            <div class="card-glass mb-4 p-4">
                                <div class="d-flex align-items-start gap-3 mb-3">
                                    <div class="badge bg-primary rounded-circle p-2 px-3 fw-bold fs-6">
                                        ${qIdx + 1}
                                    </div>
                                    <h5 class="lh-base mb-0 pt-1 text-white">${question.statement}</h5>
                                </div>

                                <div id="feedback-${question.id}" class="mb-3"></div>

                                <div class="quiz-options-group">
                                    ${question.choices.map((choice, index) => `
                                        <div>
                                            <input
                                                class="btn-check"
                                                type="radio"
                                                name="question-${question.id}"
                                                id="choice-${choice.id}"
                                                value="${choice.id}"
                                                autocomplete="off"
                                            >
                                            <label class="quiz-option-card" for="choice-${choice.id}">
                                                <span class="option-badge">${optionLabels[index] || index + 1}</span>
                                                <span class="flex-grow-1">${choice.text}</span>
                                            </label>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                `;

                listTopics.style.display = 'none';
                topicContent.classList.remove('d-none');
                backButton.classList.remove('d-none');
                window.scrollTo({ top: 0, behavior: 'smooth' });

            } catch (error) {
                if (error.message === 'login_required') {
                    topicContent.innerHTML = `
                        <div class="alert alert-custom-warning my-4">
                            <i class="fa-solid fa-lock me-2"></i> You need to log in first to view topic details and complete quizzes.
                            <a href="/login/" class="btn btn-primary-custom btn-sm ms-3">Log In</a>
                        </div>
                    `;
                } else {
                    topicContent.innerHTML = `
                        <div class="alert alert-custom-danger my-4">
                            <i class="fa-solid fa-triangle-exclamation me-2"></i> Failed to load this topic. ${error.message}
                        </div>
                    `;
                }
                listTopics.style.display = 'none';
                topicContent.classList.remove('d-none');
                backButton.classList.remove('d-none');
            }
        });
    });

    topicContent.addEventListener('change', async (event) => {
        const input = event.target;

        if (!input.matches('input[type="radio"]')) {
            return;
        }
        const questionId = input.name.replace('question-', '');
        const choiceId = input.value;
        const feedback = document.querySelector(`#feedback-${questionId}`);

        const body = new URLSearchParams();
        body.append('question_id', questionId);
        body.append('choice_id', choiceId);

        try {
            const response = await fetch(`/submit-answer/${questionId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken()
                },
                body: body.toString()
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to submit answer');
            }

            feedback.innerHTML = data.correct
                ? `
                    <div class="alert alert-custom-success d-flex align-items-start gap-2">
                        <i class="fa-solid fa-circle-check fs-5 mt-1"></i>
                        <div>
                            <strong>Correct!</strong> ${data.explanation}
                        </div>
                    </div>
                `
                : `
                    <div class="alert alert-custom-danger d-flex align-items-start gap-2">
                        <i class="fa-solid fa-circle-xmark fs-5 mt-1"></i>
                        <div>
                            <strong>Incorrect.</strong> ${data.explanation}
                        </div>
                    </div>
                `;

            document
                .querySelectorAll(`input[name="question-${questionId}"]`)
                .forEach((radio) => {
                    radio.disabled = true;
                });
        } catch (error) {
            feedback.innerHTML = `
                <div class="alert alert-custom-warning d-flex align-items-center gap-2">
                    <i class="fa-solid fa-triangle-exclamation fs-5"></i>
                    <div>${error.message}</div>
                </div>
            `;
        }
    });

    backButton.addEventListener('click', () => {
        topicContent.classList.add('d-none');
        backButton.classList.add('d-none');
        listTopics.style.display = 'block';
        topicContent.innerHTML = '';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});