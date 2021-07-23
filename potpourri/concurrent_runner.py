from .scripts.utils import *




class ConcurrentRunner:
    def __init__(self):
        self.results = {}
        
        
    def run_funcs_parallel(self, funcs_and_args):
        threads = {}
        results = {}

        for func, args in funcs_and_args.items():
            threads[f"{func.__name__}"] = ThreadWithResult(target=func, args=(*args, ))

        for func_name, thread in threads.items():
            thread.start()


        for func_name, thread in threads.items():
            thread.join()
            results[func_name] = thread.result
            self.results[func_name] = thread.result

        return results

    def run_funcs_concurrent(self, funcs_and_args):
        threads = {}
        results = {}

        for func, args in funcs_and_args.items():
            threads[f"{func.__name__}"] = ThreadWithResult(target=func, args=(*args, ))

        for func_name, thread in threads.items():
            thread.start()
            thread.join()
            results[func_name] = thread.result

      
        return results

    

