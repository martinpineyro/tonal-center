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

    const drawCircleOfFifths = (tonalCenter, progression) => {
        const notesGroup = document.getElementById('circle-notes');
        const connectionsGroup = document.getElementById('circle-connections');
        notesGroup.innerHTML = '';
        connectionsGroup.innerHTML = '';

        // Circle of Fifths order
        const circleNotes = ['C', 'G', 'D', 'A', 'E', 'B', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'];
        const centerX = 200;
        const centerY = 200;
        const radius = 150;

        // Map notes from progression/tonal center to variants used in circle
        const normalizeNote = (n) => {
            if (!n) return '';
            let root = n.split(' ')[0].toUpperCase();
            // Map common synonyms
            const mappings = {
                'C#': 'Db',
                'F#': 'Gb',
                'G#': 'Ab',
                'D#': 'Eb',
                'A#': 'Bb'
            };
            return mappings[root] || root;
        };

        const targetTonalCenter = normalizeNote(tonalCenter);
        const uniqueProgression = [...new Set(progression.map(normalizeNote))];

        const notePositions = [];

        circleNotes.forEach((note, i) => {
            const angle = (i * 30 - 90) * (Math.PI / 180);
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);

            notePositions.push({ x, y, note });

            const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            group.setAttribute('class', 'note-group');

            const isTonal = (note === targetTonalCenter);
            const inProg = uniqueProgression.includes(note);

            if (isTonal) group.classList.add('is-tonal-center');
            if (inProg) group.classList.add('in-progression');

            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('class', 'note-circle');
            circle.setAttribute('cx', x);
            circle.setAttribute('cy', y);
            circle.setAttribute('r', '22');

            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('class', 'note-text');
            text.setAttribute('x', x);
            text.setAttribute('y', y);
            text.textContent = note;

            group.appendChild(circle);
            group.appendChild(text);
            notesGroup.appendChild(group);
        });

        // Draw connections for the progression
        if (uniqueProgression.length > 1) {
            let pathData = '';
            uniqueProgression.forEach((note, i) => {
                const pos = notePositions.find(p => p.note === note);
                if (pos) {
                    pathData += (i === 0 ? 'M' : 'L') + ` ${pos.x},${pos.y}`;
                }
            });

            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('class', 'progression-line');
            path.setAttribute('d', pathData);
            connectionsGroup.appendChild(path);
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

        // Visualize Circle of Fifths
        drawCircleOfFifths(data.tonal_center, uniqueSequence);

        // Show results
        resultsContainer.classList.remove('hidden');
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    };

    analyzeBtn.addEventListener('click', performAnalysis);

    songInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performAnalysis();
    });
});
