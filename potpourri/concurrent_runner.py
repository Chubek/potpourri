from .scripts.utils import *




class ConcurrentRunner:
    def __init__(self):
        self.results = {}
        
        
    def run_funcs_parallel(self, funcs_and_args):
        threads = {}
        results = {}

        i = 0
        for func, args in funcs_and_args.items():
            threads[f"{func.__name__}_{i}"] = ThreadWithResult(func, args)
            i += 1
            
        for func_name, thread in threads.items():
            thread.start()


        for func_name, thread in threads.items():
            res = thread.get_result()
            results[func_name] = res
            self.results[func_name] = res

        return results

    def run_funcs_concurrent(self, funcs_and_args):
        threads = {}
        results = {}
        
        i = 0
        for func, args in funcs_and_args.items():
            threads[f"{func.__name__}_{i}"] = ThreadWithResult(func, args)
            i += 1

        for func_name, thread in threads.items():
            thread.start()
            res = thread.get_result()
            results[func_name] = res

      
        return results

    

