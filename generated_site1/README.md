# VibrantTodo

**VibrantTodo** is a lightweight, browser‑only todo‑list application that feels snappy and modern. It runs entirely on the client side – no server, no build step – and stores your tasks in `localStorage` so they survive page reloads.

---

## Screenshot

![VibrantTodo screenshot](./screenshot.png)
> *Replace `screenshot.png` with an actual screenshot of the app.*

---

## Features

- **Add tasks** via the input field or `Ctrl+Enter` shortcut.
- **Edit tasks inline** by clicking the task label.
- **Delete tasks** with a dedicated delete button or the `Delete` key when a task is focused.
- **Toggle completion** using the checkbox.
- **Filter view** – *All*, *Active*, *Completed* – via the navigation buttons.
- **Drag‑and‑drop reordering** using the ☰ handle.
- **Keyboard shortcuts** for fast workflow (`Ctrl+Enter`, `Delete`, `Escape`).
- **Persistent storage** – tasks are saved in `localStorage` and restored on page load.
- **Responsive UI** built with plain HTML, CSS, and JavaScript.

---

## Tech Stack

- **HTML** – structure and semantic markup (`index.html`).
- **CSS** – styling (`style.css`).
- **JavaScript** – core logic, DOM manipulation, persistence, and interactions (`script.js`).

---

## Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/vibranttodo.git
   cd vibranttodo
   ```
2. **Open the app**
   - Simply double‑click `index.html` or open it in any modern browser.
   - No build tools, package managers, or servers are required.

---

## Keyboard Shortcuts & Drag‑and‑Drop

| Shortcut / Action | Description |
|-------------------|-------------|
| `Enter` (while typing in the **new‑task** input) | Adds the task. |
| `Ctrl+Enter` (while the **new‑task** input is focused) | Adds the task (alternative shortcut). |
| `Delete` (when a **task item** `<li>` has focus) | Deletes the selected task. |
| `Escape` (while editing a task) | Cancels the edit and restores the original text. |
| **Drag‑and‑Drop** – grab the **☰** handle (`.drag-handle`) and move the task to a new position. The list updates instantly and the new order is saved. |

---

## Folder Structure

```
├─ index.html        # Main markup – defines IDs and classes used by the script
├─ style.css         # Visual styling for the app (layout, colors, drag cues)
├─ script.js         # Core JavaScript – data model, persistence, UI logic
└─ README.md         # Documentation (you are reading it!)
```

### File purpose details

- **`index.html`**
  - Contains the root elements: `#new-task`, `#add-task-btn`, `#filter-nav`, `#task-list`.
  - Each task rendered by the script receives the following classes/attributes:
    - `.task-item` – the `<li>` wrapper.
    - `.completed` – added when a task is marked complete.
    - `.drag-handle` – the draggable handle (☰).
    - `.toggle-complete` – the checkbox.
    - `.task-label` – the visible label.
    - `.edit-input` – hidden text input for inline editing.
    - `.delete-btn` – the delete button.

- **`style.css`**
  - Styles the layout, colors, and visual feedback for drag‑over/dragging states.

- **`script.js`**
  - Implements the `Task` class, CRUD operations, filtering, drag‑and‑drop, keyboard shortcuts, and `localStorage` persistence.
  - Exposes a global `window.todoApp` object for debugging or automated tests.

---

## Persistence & Data Management

- Tasks are stored under the key **`vibrantTodoTasks`** in `localStorage` as a JSON array.
- On every change (add, edit, delete, toggle, reorder) the array is re‑saved, preserving order via the `order` property.
- **Clearing data**: open the browser’s developer tools, go to the *Application* (or *Storage*) tab, locate `localStorage → vibrantTodoTasks`, and delete the entry. Alternatively, run:
  ```javascript
  localStorage.removeItem('vibrantTodoTasks');
  location.reload();
  ```
  to reset the app.

---

## License

*Add your license information here (e.g., MIT, Apache 2.0, etc.).*
