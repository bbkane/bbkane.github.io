class DelayedFunction:
    def __init__(self,function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self):
        self.function(*self.args, **self.kwargs)
    
    def __repr__(self):
        format_str = "{class_name}({fun_name}({args}, {kwargs}))"
        class_name = type(self).__name__
        fun_name = self.function.__name__
        return format_str.format(class_name=class_name, fun_name=fun_name, args=self.args, kwargs=self.kwargs)