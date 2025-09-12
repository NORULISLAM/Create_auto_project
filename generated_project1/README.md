# SimpleNotebook

## Overview
SimpleNotebook is a lightweight, client‑side note‑taking web application. It runs entirely in the browser, storing notes in **localStorage**, so no backend or database is required. Users can create, edit, and delete notes, and their data persists across sessions.

---

## Features
- **Create notes** with a title and content.
- **Edit existing notes** instantly.
- **Delete notes** with a single click.
- **Automatic persistence** using the browser's `localStorage` (notes survive page reloads and browser restarts).
- **Responsive UI** with a sidebar list of notes and an editor pane.
- **Real‑time UI updates** – the note list refreshes after every operation.
- **Unique identifiers** for each note to avoid collisions.

---

## Tech Stack
- **HTML** – structure of the application (`index.html`).
- **CSS** – styling (`styles.css`).
- **JavaScript** – core logic, model, storage handling, and UI interactions (`app.js`).

---

## Setup
1. Clone or download the repository.
2. Open the `index.html` file in any modern web browser (Chrome, Firefox, Edge, Safari, …).
   ```bash
   # From the project root (no server required)
   open index.html   # macOS
   start index.html  # Windows
   xdg-open index.html # Linux
   ```
   *Alternatively, you can serve the folder with a simple static server (e.g., `python -m http.server`).*

---

## Usage
1. **Create a new note** – click the **New Note** button, fill in the title and content, then press **Save**.
2. **Edit a note** – select a note from the sidebar, modify the fields, and click **Save**.
3. **Delete a note** – with a note selected, click the **Delete** button.
4. All changes are automatically saved to `localStorage`; reopening the app will show the same notes.

---

## Development
### Folder Structure
```
SimpleNotebook/
├─ index.html        # Main HTML page
├─ styles.css        # Application styling
├─ app.js            # Core JavaScript (model, storage, UI)
└─ README.md         # Documentation (this file)
```
- **`index.html`** – contains the markup and links to the CSS and JS files.
- **`styles.css`** – defines layout, colors, and responsive behavior.
- **`app.js`** – encapsulated in an IIFE; includes:
  - `Note` class (model)
  - `Storage` module (localStorage CRUD)
  - `UI` module (rendering and event handling)
  - Bootstrap code that runs on `DOMContentLoaded`.

To modify the application, edit the corresponding files. The code is written in vanilla JavaScript, so no build step is required.

---

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug‑fix:
   ```bash
   git checkout -b feature/awesome‑feature
   ```
3. Make your changes and test them locally.
4. Commit with clear messages:
   ```bash
   git commit -m "Add awesome feature"
   ```
5. Push to your fork and open a Pull Request against the `main` branch.
6. Ensure the PR description explains the purpose of the change and any relevant screenshots.

---

## License
This project is licensed under the **MIT License** – see the `LICENSE` file for details.
