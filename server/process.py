from base_process import BaseProcess
import time

class Process(BaseProcess):

    def __init__(self, job):
        self.job = job

    def run(self):
        """Run waiting stub for this process"""
        print(f"Current job is\n{self.job}")
        time.sleep(10)
        return {'00': 0.5, '11': 0.5}


