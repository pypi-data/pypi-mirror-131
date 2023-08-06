
def gen_fire_argv(*args,**kwargs):
    argv=[]
    for arg in args:
        argv.append(arg)
    for k,v in kwargs.items():
        argv.append('--%s=%s'%(k,v))
    return argv