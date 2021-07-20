from .scripts.utils import *




class ConcurrentRunner:
    def __init__(self):
        self.results = {}
        
        
    def run_concurrent_noargs_single(self, func, parallel=True, number_of_threads=5):
        threads = {}
        results = {}

        for i in range(number_of_threads):
            threads[f"{func.__name__}_{i}"] = ThreadWithResult(target=func, args=())

        for func_name, thread in threads.items():
            thread.start()

            if not parallel:
                thread.join()
                results[func_name] = thread.result

        if parallel:
            for func_name, thread in threads.items():
                thread.join()
                results[func_name] = thread.result

        return results

    def run_concurrent_noargs_multiple(self, funcs, parallel=True, number_of_threads=5):        
        results = {}

        for func in funcs:
            results[func.__name__] = self.run_concurrent_noargs_single(func, 
            parallel=parallel, 
            number_of_threads=number_of_threads)

        return results
        

    def run_concurrent_args_single(self, func, args, parallel=True, number_of_threads=5):
        threads = {}
        results = {}

        for i in range(number_of_threads):
            threads[f"{func.__name__}_{i}"] = ThreadWithResult(target=func, args=(*args, ))

        for func_name, thread in threads.items():
            thread.start()

            if not parallel:
                thread.join()
                results[func_name] = thread.result

        if parallel:
            for func_name, thread in threads.items():
                thread.join()
                results[func_name] = thread.result

        return results

    def run_concurrent_args_multiple(self, funcs, args, parallel=True, number_of_threads=5):        
        results = {}

        for func in funcs:
            results[func.__name__] = self.run_concurrent_noargs_single(func, args,
            parallel=parallel, 
            number_of_threads=number_of_threads)

        return results


