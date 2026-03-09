def evaluate(state):

    output = state["experiment_output"]

    state["evaluation"] = f"""
    Experiment Results:

    {output}
    """

    return state