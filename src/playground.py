class PlaygroundWorker:
    def __init__(self, progress_callback, status_callback):
        self.progress_callback = progress_callback
        self.status_callback = status_callback

    def run(self):
        raise NotImplementedError("PlaygroundWorker.run() is not implemented yet.")