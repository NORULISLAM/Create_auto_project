// VibrantTodo - main application logic
// This script implements task management, persistence, UI rendering, CRUD operations,
// filtering, drag‑and‑drop reordering, and keyboard shortcuts.

(() => {
  // ----- Utility Functions -----
  const escapeHTML = (str) => {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  };

  // ----- Data Model -----
  class Task {
    /**
     * @param {string} id - UUID
     * @param {string} text - task description
     * @param {boolean} completed - completion status
     * @param {number} order - numeric order (timestamp or index)
     */
    constructor(id, text, completed = false, order = Date.now()) {
      this.id = id;
      this.text = text;
      this.completed = completed;
      this.order = order;
    }
  }

  // ----- Persistence -----
  const STORAGE_KEY = 'vibrantTodoTasks';

  const loadTasks = () => {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    try {
      const data = JSON.parse(raw);
      // Ensure we have Task instances and sort by order
      const tasks = data.map((obj) => new Task(obj.id, obj.text, obj.completed, obj.order));
      tasks.sort((a, b) => a.order - b.order);
      return tasks;
    } catch (e) {
      console.error('Failed to parse tasks from localStorage', e);
      return [];
    }
  };

  const saveTasks = (tasks) => {
    const data = JSON.stringify(tasks);
    localStorage.setItem(STORAGE_KEY, data);
  };

  // ----- State -----
  let tasks = [];
  let currentFilter = 'all'; // 'all' | 'active' | 'completed'

  // ----- Rendering -----
  const taskListEl = document.getElementById('task-list');

  const renderTasks = (filter = currentFilter) => {
    currentFilter = filter;
    // Clear list
    taskListEl.innerHTML = '';
    // Determine which tasks to show
    const filtered = tasks.filter((t) => {
      if (filter === 'active') return !t.completed;
      if (filter === 'completed') return t.completed;
      return true; // all
    });

    filtered.forEach((task) => {
      const li = document.createElement('li');
      li.className = 'task-item' + (task.completed ? ' completed' : '');
      li.setAttribute('draggable', 'true');
      li.dataset.id = task.id;
      li.tabIndex = 0; // make focusable for keyboard shortcuts

      // Drag handle
      const handle = document.createElement('span');
      handle.className = 'drag-handle';
      handle.textContent = '☰';
      li.appendChild(handle);

      // Checkbox
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'toggle-complete';
      checkbox.dataset.id = task.id;
      if (task.completed) checkbox.checked = true;
      li.appendChild(checkbox);

      // Label
      const label = document.createElement('label');
      label.className = 'task-label';
      label.dataset.id = task.id;
      label.textContent = escapeHTML(task.text);
      li.appendChild(label);

      // Edit input (hidden by default)
      const editInput = document.createElement('input');
      editInput.type = 'text';
      editInput.className = 'edit-input';
      editInput.dataset.id = task.id;
      editInput.value = task.text;
      editInput.style.display = 'none';
      li.appendChild(editInput);

      // Delete button
      const delBtn = document.createElement('button');
      delBtn.className = 'delete-btn';
      delBtn.dataset.id = task.id;
      delBtn.textContent = '✖';
      li.appendChild(delBtn);

      taskListEl.appendChild(li);
    });
  };

  // ----- CRUD Operations -----
  const addTask = (text) => {
    const id = crypto.randomUUID();
    const order = Date.now();
    const newTask = new Task(id, text, false, order);
    tasks.push(newTask);
    saveTasks(tasks);
    renderTasks();
  };

  const editTask = (id, newText) => {
    const task = tasks.find((t) => t.id === id);
    if (task) {
      task.text = newText;
      saveTasks(tasks);
      renderTasks();
    }
  };

  const deleteTask = (id) => {
    tasks = tasks.filter((t) => t.id !== id);
    saveTasks(tasks);
    renderTasks();
  };

  const toggleComplete = (id) => {
    const task = tasks.find((t) => t.id === id);
    if (task) {
      task.completed = !task.completed;
      saveTasks(tasks);
      renderTasks();
    }
  };

  const reorderTasks = (draggedId, targetId) => {
    const draggedIdx = tasks.findIndex((t) => t.id === draggedId);
    const targetIdx = tasks.findIndex((t) => t.id === targetId);
    if (draggedIdx === -1 || targetIdx === -1 || draggedIdx === targetIdx) return;
    const [draggedTask] = tasks.splice(draggedIdx, 1);
    // Insert before targetIdx if dragged comes from after, else after
    const insertIdx = draggedIdx < targetIdx ? targetIdx : targetIdx;
    tasks.splice(insertIdx, 0, draggedTask);
    // Reassign order values based on new index
    tasks.forEach((t, i) => (t.order = i));
    saveTasks(tasks);
    renderTasks();
  };

  // ----- Event Handlers -----
  const bindUIEvents = () => {
    // Add task via button
    const addBtn = document.getElementById('add-task-btn');
    const newTaskInput = document.getElementById('new-task');
    const handleAdd = () => {
      const text = newTaskInput.value.trim();
      if (text) {
        addTask(text);
        newTaskInput.value = '';
      }
    };
    addBtn.addEventListener('click', handleAdd);
    newTaskInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        handleAdd();
      }
    });

    // Filter navigation
    const filterNav = document.getElementById('filter-nav');
    if (filterNav) {
      filterNav.addEventListener('click', (e) => {
        const btn = e.target.closest('[data-filter]');
        if (!btn) return;
        const filter = btn.dataset.filter;
        // Update active class
        Array.from(filterNav.querySelectorAll('[data-filter]')).forEach((el) => el.classList.remove('active'));
        btn.classList.add('active');
        renderTasks(filter);
      });
    }

    // Delegate task list events
    taskListEl.addEventListener('click', (e) => {
      const id = e.target.dataset.id;
      if (!id) return;

      // Delete
      if (e.target.classList.contains('delete-btn')) {
        deleteTask(id);
        return;
      }

      // Toggle complete
      if (e.target.classList.contains('toggle-complete')) {
        toggleComplete(id);
        return;
      }

      // Start edit on label click
      if (e.target.classList.contains('task-label')) {
        const li = e.target.closest('li');
        const label = e.target;
        const input = li.querySelector('.edit-input');
        label.style.display = 'none';
        input.style.display = '';
        input.focus();
        input.select();
      }
    });

    // Edit input handling (blur & Enter)
    taskListEl.addEventListener('keydown', (e) => {
      if (e.target.classList.contains('edit-input')) {
        if (e.key === 'Enter') {
          e.preventDefault();
          e.target.blur();
        } else if (e.key === 'Escape') {
          // Cancel edit
          const li = e.target.closest('li');
          const label = li.querySelector('.task-label');
          e.target.value = label.textContent; // revert
          e.target.blur();
        }
      }
    });
    taskListEl.addEventListener('blur', (e) => {
      if (e.target.classList.contains('edit-input')) {
        const li = e.target.closest('li');
        const label = li.querySelector('.task-label');
        const newText = e.target.value.trim();
        const id = e.target.dataset.id;
        if (newText) {
          editTask(id, newText);
        } else {
          // If empty, delete task
          deleteTask(id);
        }
        // Reset UI (renderTasks already did this)
      }
    }, true);

    // Drag‑and‑Drop
    let dragSrcId = null;
    taskListEl.addEventListener('dragstart', (e) => {
      const li = e.target.closest('li');
      if (!li) return;
      // Only allow drag when started from handle
      if (!e.target.classList.contains('drag-handle')) return;
      dragSrcId = li.dataset.id;
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', dragSrcId);
      // Add dragging class for styling (optional)
      li.classList.add('dragging');
    });
    taskListEl.addEventListener('dragover', (e) => {
      e.preventDefault(); // Necessary to allow drop
      const li = e.target.closest('li');
      if (!li) return;
      li.classList.add('drag-over');
    });
    taskListEl.addEventListener('dragleave', (e) => {
      const li = e.target.closest('li');
      if (!li) return;
      li.classList.remove('drag-over');
    });
    taskListEl.addEventListener('drop', (e) => {
      e.preventDefault();
      const targetLi = e.target.closest('li');
      if (!targetLi) return;
      targetLi.classList.remove('drag-over');
      const targetId = targetLi.dataset.id;
      if (dragSrcId && targetId && dragSrcId !== targetId) {
        reorderTasks(dragSrcId, targetId);
      }
    });
    taskListEl.addEventListener('dragend', (e) => {
      const li = e.target.closest('li');
      if (li) li.classList.remove('dragging');
      // Clean any leftover visual cues
      taskListEl.querySelectorAll('.drag-over').forEach((el) => el.classList.remove('drag-over'));
    });

    // Global keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      // Ctrl+Enter to add task when #new-task focused
      if (e.key === 'Enter' && e.ctrlKey && document.activeElement === newTaskInput) {
        e.preventDefault();
        handleAdd();
        return;
      }
      // Delete key on focused task item
      if (e.key === 'Delete' && document.activeElement && document.activeElement.matches('li.task-item')) {
        const id = document.activeElement.dataset.id;
        if (id) deleteTask(id);
        return;
      }
    });
  };

  // ----- Initialization -----
  document.addEventListener('DOMContentLoaded', () => {
    tasks = loadTasks();
    renderTasks();
    bindUIEvents();
    // Expose API for testing / external use
    window.todoApp = {
      loadTasks,
      saveTasks,
      addTask,
      editTask,
      deleteTask,
      toggleComplete,
      reorderTasks,
      getTasks: () => tasks.slice(), // return copy
    };
  });
})();
