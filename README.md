# 🛠️ Coder Uncle

**Coder Uncle** is an AI-powered coding assistant built with [LangGraph](https://github.com/langchain-ai/langgraph).  
It works like a multi-agent development team that can take a natural language request and transform it into a complete, working project — file by file — using real developer workflows.

---

## How to use
1. Enter a prompt.
2. Click **Generate**.
3. Watch logs & preview.
4. Click **Download ZIP** to get the generated site.

## Notes
- If the model is rate-limited or no API key is set, the demo falls back to MOCK mode so you still see a working preview + ZIP.

## 使い方
1. プロンプトを入力します。  
2. **Generate** をクリックします。  
3. ログとプレビューを確認します。  
4. **Download ZIP** をクリックして生成されたサイトを取得します。  

## 注意事項
- モデルがレート制限されている場合、または API キーが設定されていない場合、デモは MOCK モードに切り替わります。そのため、プレビューと ZIP を引き続き利用できます。  


## 🏗️ Architecture

- **Planner Agent** – Analyzes your request and generates a detailed project plan.
- **Architect Agent** – Breaks down the plan into specific engineering tasks with explicit context for each file.
- **Coder Agent** – Implements each task, writes directly into files, and uses available tools like a real developer.

<div style="text-align: center;">
    <img src="resources/coder_buddy_diagram.png" alt="Coder Agent Architecture" width="90%"/>
</div>

---

## 🚀 Getting Started

### Prerequisites

- Make sure you have uv installed, follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/) to install it.
- Ensure that you have created a groq account and have your API key ready. Create an API key [here](https://console.groq.com/keys).

### ⚙️ **Instsllstion and Startup**

- Create a virtual environment using: `uv venv` and activate it using `source .venv/bin/activate`
- Install the dependencies using: `uv pip install -r pyproject.toml`
- Create a `.env` file and add the variables and their respective values mentioned in the `.sample_env` file

Now that we are done with all the set-up & installation steps we can start the application using the following command:

```bash
  python app.py
```

### 🧪 Example Prompts

- Create a to-do list application using html, css, and javascript.
- Create a simple calculator web application.

---

Copyright©️ Norul islam. All rights reserved.
