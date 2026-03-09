class TokenLogger:

    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def log(self, usage):

        self.prompt_tokens += usage.prompt_tokens
        self.completion_tokens += usage.completion_tokens

    def report(self):

        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens
        }