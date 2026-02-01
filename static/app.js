document.addEventListener('DOMContentLoaded', () => {
    const songInput = document.getElementById('song-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const instrumentBtns = document.querySelectorAll('.instrument-btn');
    const resultsContainer = document.getElementById('results-container');
    const loadingOverlay = document.getElementById('loading');

    // UI Elements for results
    const trackTitle = document.getElementById('track-title');
    const trackArtist = document.getElementById('track-artist');
    const tonalCenterValue = document.getElementById('tonal-center-value');
    const chordSequenceValue = document.getElementById('chord-sequence-value');
    const scalesGrid = document.getElementById('scales-grid');

    let selectedInstrument = 'concert';

    // Instrument Selection
    instrumentBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            instrumentBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedInstrument = btn.dataset.value;

            // If already searching or searched, we might want to re-analyze or just update UI?
            // For now, let's keep it simple: it's an input for the NEXT analysis.
        });
    });

    // Analysis Logic
    const performAnalysis = async () => {
        const query = songInput.value.trim();
        if (!query) return;

        // Show loading
        loadingOverlay.classList.remove('hidden');
        resultsContainer.classList.add('hidden');

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: query,
                    instrument: selectedInstrument === 'concert' ? 'concert' : selectedInstrument
                })
            });

            const data = await response.json();

            if (data.error) {
                alert(`Error: ${data.error}`);
                return;
            }

            displayResults(data);
        } catch (error) {
            console.error('Analysis failed:', error);
            alert('A server error occurred. Please make sure the backend is running.');
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    };

    const displayResults = (data) => {
        // Track info
        trackTitle.textContent = data.track.title || 'Unknown Track';
        trackArtist.textContent = data.track.artist || 'Unknown Artist';

        // Tonal Center
        tonalCenterValue.textContent = data.tonal_center;

        // Chords (Simplified sequence for the UI chip display)
        chordSequenceValue.innerHTML = '';
        const sequence = data.progression.flat(); // Flatten bar structure if present

        // De-duplicate consecutive
        const uniqueSequence = [];
        if (sequence.length > 0) {
            uniqueSequence.push(sequence[0]);
            for (let i = 1; i < sequence.length; i++) {
                if (sequence[i] !== uniqueSequence[uniqueSequence.length - 1]) {
                    uniqueSequence.push(sequence[i]);
                }
            }
        }

        uniqueSequence.slice(0, 16).forEach((chord, index) => {
            const chip = document.createElement('div');
            chip.className = 'chord-chip';
            chip.textContent = chord;
            chordSequenceValue.appendChild(chip);

            if (index < uniqueSequence.length - 1 && index < 15) {
                const arrow = document.createElement('span');
                arrow.className = 'chord-arrow';
                arrow.textContent = '→';
                chordSequenceValue.appendChild(arrow);
            }
        });

        // Scales
        scalesGrid.innerHTML = '';
        const suggestions = data.suggestions;
        for (const [type, data] of Object.entries(suggestions)) {
            const card = document.createElement('div');
            card.className = 'scale-card';

            const nameEl = document.createElement('div');
            nameEl.className = 'scale-name';
            nameEl.textContent = `${type}: ${data.label}`;

            const valueEl = document.createElement('div');
            valueEl.className = 'scale-notes';
            valueEl.textContent = data.notes;

            card.appendChild(nameEl);
            card.appendChild(valueEl);
            scalesGrid.appendChild(card);
        }

        // Show results
        resultsContainer.classList.remove('hidden');
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    };

    analyzeBtn.addEventListener('click', performAnalysis);

    songInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performAnalysis();
    });
});
