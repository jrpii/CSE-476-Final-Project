## CSE-476 Final Project
General purpose reasoning agent from the provided course LLM API.

### Your goal

In this project, you will implement an inference-time agent to solve reasoning requests, as those provided in the development data. The grading of this project will be effort-based and you will get full credit if you produce the minimum deliverables below, with subject to the rules and requirements below.

#### Minimum Deliverables

1. A working agent loop (in the form of a Github project) that the TA can run, and implements *at least three* inference-time algorithms or techniques.
2. Outputs from your agent on the released test data (see important dates). 
3. A short one-page report on how your agent works, and pointer to important techniques (referece to code blocks).

### Setup
Create a conda environment:

```bash
conda create -n cse476-agent -c conda-forge python=3.12
conda activate cse476-agent
pip install -r requirements.txt
```

Create .env file:
The model chosen will be based on the API base, model name, and api key if provided. Below is the configuration to the projects model, accessible only locally via VPN connection to ASU. But should be configurable to any API or self hosted model in theory.
```
OPENAI_API_KEY=cse476
API_BASE=http://10.4.58.53:41701/v1
MODEL=bens_model
```

### Layout
- `src/` - all agent source code
- `data/` - datasets (dev/test)
- `notebooks/` - tutorial notebook
- `scripts/` - CLI scripts to run the agent
- `reports/` - the required report

### Project Requirements
From the project rules:
- Use only the provided API to call LLMs inside your agent loop.
- No AI-written code blocks longer than 3 lines.
- No hard coding tool calls.
- No paid services or direct calling of other LLMs.
- Efficient running, <20 LLM calls per question.

### Running the Project
Use this command to reproduce the 
```bash
 python main.py --input='data/cse_476_final_project_test_data.json' --max-reasoning-tokens=1024 --max-answer-tokens=128 --output='results/test_data_outputs'
```

### Implementation Details
Techniques Employed:
- Chain of Thought reasoning with answer extraction
- ReAct Agent Loop (Think -> Act -> Observe)
- Reasoning Effort Scaling (based on difficulty)
- Addaptive Prompting (based on domain)
- LLM-as-a-Judge (to infere domain and dicciculty)
-Tool Integration


### Submission files
Copy of report and json output run on test set will be in the submission folder.