import consul
import os
import json
import time
from functools import wraps

mute = False
env = {'proto': None, 'values': {}}
runstep = {'current': {}, 'next': {}}
calls = []
current_call_limit = 0
next_call_limit = 0
stdio = {'out': [], 'error': []}
task_id = ''

c = consul.Consul(host=os.getenv('CONSUL_HOST') or 'consul-b2c-dev01.shein.com',
                  port=os.getenv('CONSUL_PORT') or '8500')


def init(_mute, _env, _runstep, _task_id):
    global mute
    mute = _mute
    global env
    env = _env
    global runstep
    runstep = _runstep
    global task_id
    task_id = _task_id


def get_state():
    return {'env': env, 'calls': calls, 'stdio': stdio}


def check(assertion, msg):
    calls.append({'method': 'check', 'args': [bool(assertion), msg]})


def stdio_write_out(s):
    stdio['out'].append(str(s))


def stdio_write_error(s):
    stdio['error'].append((str(s)))


def context_set_value(k, v, root=False):
    if not mute:
        raise Exception('You could only call setValue on an mute fn!')
    if not root:
        env['values'][k] = v
    else:
        node = env
        while bool(node['proto']):
            node = node['proto']
        node['values'][k] = v


def context_get_value(k):
    node = env
    while bool(node['proto']):
        if k in node['values']:
            return node['values'][k]
        node = node['proto']
    return None


def mutex(key='', ttl=30):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key_prefix = f'sotest_function_python_{task_id}'
            key_full = f'{key_prefix}_{key}' if key else key_prefix
            value = c.kv.get(key_full)[1]
            if value and value.get('Value'):
                return json.loads(value['Value'])
            session_id = c.session.create(lock_delay=0,
                                          name='sotest-utils-python',
                                          ttl=ttl,
                                          behavior='delete')
            set_result = c.kv.put(key=key_full,
                                  value=None,
                                  acquire=session_id)
            if set_result:
                fn_result = func()
                set_result2 = c.kv.put(key=key_full,
                                       value=json.dumps(fn_result),
                                       acquire=session_id)
                if set_result2:
                    return fn_result
            time.sleep(1)
            return wrapper(*args, **kwargs)
        return wrapper
    return decorator


def check_equal(a, b, msg):
    calls.extend(['checkEqual', [a, b, msg]])


def check_lt(a, b, msg):
    calls.extend(['checkLt', [a, b, msg]])


def check_gt(a, b, msg):
    calls.extend((['checkGt', [a, b, msg]]))
