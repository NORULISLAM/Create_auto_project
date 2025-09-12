/*
 * app.js – Core logic for SimpleNotebook
 * Implements Note model, Storage handling (localStorage), UI rendering and event handling.
 * All code is wrapped in an IIFE to avoid polluting the global scope.
 */
(() => {
    // ---------- Note Model ----------
    class Note {
        /**
         * @param {string} id - Unique identifier
         * @param {string} title - Note title
         * @param {string} content - Note body
         * @param {number} timestamp - Unix epoch ms when note was created/updated
         */
        constructor(id, title, content, timestamp) {
            this.id = id;
            this.title = title;
            this.content = content;
            this.timestamp = timestamp;
        }
        /**
         * Convert the note instance to a plain object suitable for JSON.stringify.
         * @returns {{id:string,title:string,content:string,timestamp:number}}
         */
        toJSON() {
            return {
                id: this.id,
                title: this.title,
                content: this.content,
                timestamp: this.timestamp,
            };
        }
        /**
         * Serialize the note to a JSON string.
         * @returns {string}
         */
        serialize() {
            return JSON.stringify(this);
        }
    }

    // ---------- Storage Module ----------
    const STORAGE_KEY = 'notes';
    const Storage = {
        /** Retrieve all notes from localStorage and return as Note instances */
        getAllNotes() {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return [];
            try {
                const arr = JSON.parse(raw);
                // Ensure each entry becomes a Note instance
                return arr.map(o => new Note(o.id, o.title, o.content, o.timestamp));
            } catch (e) {
                console.error('Failed to parse notes from localStorage', e);
                return [];
            }
        },
        /** Save a note (add new or update existing) */
        saveNote(note) {
            if (!(note instanceof Note)) {
                console.error('Storage.saveNote expects a Note instance');
                return;
            }
            const notes = this.getAllNotes();
            const idx = notes.findIndex(n => n.id === note.id);
            if (idx >= 0) {
                notes[idx] = note; // update
            } else {
                notes.push(note); // add new
            }
            localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
        },
        /** Delete a note by its id */
        deleteNote(id) {
            const notes = this.getAllNotes().filter(n => n.id !== id);
            localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
        },
        /** Generate a unique identifier for a note */
        generateId() {
            return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        },
    };

    // ---------- UI Module ----------
    const UI = (() => {
        // Cache DOM elements
        const $sidebar = document.getElementById('sidebar');
        const $noteList = document.getElementById('note-list');
        const $titleInput = document.getElementById('note-title');
        const $contentArea = document.getElementById('note-content');
        const $newBtn = document.getElementById('new-note-btn');
        const $saveBtn = document.getElementById('save-note-btn');
        const $deleteBtn = document.getElementById('delete-note-btn');

        // Currently selected note id (null when creating a new note)
        let selectedNoteId = null;

        /** Render the list of notes in the sidebar */
        function renderNoteList(notes) {
            // Clear existing list
            $noteList.innerHTML = '';
            notes.sort((a, b) => b.timestamp - a.timestamp); // newest first
            notes.forEach(note => {
                const li = document.createElement('li');
                li.textContent = note.title || '(Untitled)';
                li.dataset.id = note.id;
                if (note.id === selectedNoteId) {
                    li.classList.add('selected');
                }
                $noteList.appendChild(li);
            });
        }

        /** Load a note into the editor fields */
        function loadNoteIntoEditor(id) {
            const notes = Storage.getAllNotes();
            const note = notes.find(n => n.id === id);
            if (!note) return;
            selectedNoteId = note.id;
            $titleInput.value = note.title;
            $contentArea.value = note.content;
            // Update selected class in list
            const items = $noteList.querySelectorAll('li');
            items.forEach(li => {
                li.classList.toggle('selected', li.dataset.id === id);
            });
        }

        /** Clear editor fields for creating a new note */
        function clearEditor() {
            selectedNoteId = null;
            $titleInput.value = '';
            $contentArea.value = '';
            // Remove selection highlight
            const items = $noteList.querySelectorAll('li');
            items.forEach(li => li.classList.remove('selected'));
        }

        /** Attach event listeners for UI interactions */
        function bindEvents() {
            // New note button
            $newBtn.addEventListener('click', () => {
                clearEditor();
            });

            // Save note button
            $saveBtn.addEventListener('click', () => {
                const title = $titleInput.value.trim();
                const content = $contentArea.value.trim();
                const timestamp = Date.now();
                let note;
                if (selectedNoteId) {
                    // Update existing note
                    note = new Note(selectedNoteId, title, content, timestamp);
                } else {
                    // Create new note
                    const id = Storage.generateId();
                    note = new Note(id, title, content, timestamp);
                }
                Storage.saveNote(note);
                // Refresh UI
                const notes = Storage.getAllNotes();
                renderNoteList(notes);
                loadNoteIntoEditor(note.id);
            });

            // Delete note button
            $deleteBtn.addEventListener('click', () => {
                if (!selectedNoteId) return;
                Storage.deleteNote(selectedNoteId);
                clearEditor();
                const notes = Storage.getAllNotes();
                renderNoteList(notes);
                // Auto‑select first note if any
                if (notes.length) {
                    loadNoteIntoEditor(notes[0].id);
                }
            });

            // Click on a note in the list (event delegation)
            $noteList.addEventListener('click', (e) => {
                const li = e.target.closest('li');
                if (!li) return;
                const id = li.dataset.id;
                loadNoteIntoEditor(id);
            });
        }

        /** Initialize UI on page load */
        function init() {
            const notes = Storage.getAllNotes();
            renderNoteList(notes);
            if (notes.length) {
                loadNoteIntoEditor(notes[0].id);
            }
            bindEvents();
        }

        // Expose public methods (if needed elsewhere)
        return {
            init,
            renderNoteList,
            loadNoteIntoEditor,
            clearEditor,
        };
    })();

    // ---------- Bootstrap ----------
    document.addEventListener('DOMContentLoaded', () => {
        UI.init();
    });
})();
