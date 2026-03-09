import subprocess

def execute_experiment(state):

    file = state["experiment_file"]

    result = subprocess.run(
        ["python", file],
        capture_output=True,
        text=True
    )

    state["experiment_output"] = result.stdout

    return state