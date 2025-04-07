# snooper-ai 🔍

**snooper-ai** is a simple fork of [PySnooper](https://github.com/cool-RR/PySnooper). It sends the entire execution trace (variable values you'll typically examine in a debugger) to an LLM for debugging, so it fully understands what happened in your code.

Disclaimer: This was implemented simply and may not be very robust. Feel free to submit issues. 


## Usage:
1. Install
```
pip install snooper-ai
```
2. Store your LLM api key (either anthropic or openai):
```
ANTHROPIC_API_KEY=xxx
OPENAI_API_KEY=xxx
```
3. Add a decorator to the function you want to inquire:
```python
from snooper_ai import snoop

@snoop()
def loop_index_error():
    items = ['apple', 'banana', 'cherry']
    total = 0
    for i in range(5):
        total += len(items[i])
    return total

loop_index_error()

```
4. Run the file

```
snoop run file.py
```
5. Tell the LLM what you're confused about:
```bash
╭─────────────────────────────────────────────────╮
│  🔍 snooper-ai: Debug your Python code with AI  │
╰─────────────────────────────────────────────────╯

What would you like to know about the code execution? (e.g. Error messages, unexpected behavior, etc.):
```

6. Run it to get a detailed explanation! If your code errors out, the execution trace and the error message will be sent to the LLM.

7. To choose which model you're using (This will be saved in your pyproject.toml):
```
snoop config
```
## What's sent to the LLM:

Previous example:
```
17:15:51.845171 call         5 def loop_index_error():
17:15:51.845285 line         6     items = ['apple', 'banana', 'cherry']
New var:....... items = ['apple', 'banana', 'cherry']
17:15:51.845298 line         7     total = 0
New var:....... total = 0
17:15:51.845320 line         8     for i in range(5):
New var:....... i = 0
17:15:51.845335 line         9         total += len(items[i])
Modified var:.. total = 5
17:15:51.845347 line         8     for i in range(5):
Modified var:.. i = 1
17:15:51.845358 line         9         total += len(items[i])
Modified var:.. total = 11
17:15:51.845368 line         8     for i in range(5):
Modified var:.. i = 2
17:15:51.845377 line         9         total += len(items[i])
Modified var:.. total = 17
17:15:51.845386 line         8     for i in range(5):
Modified var:.. i = 3
17:15:51.845395 line         9         total += len(items[i])
17:15:51.845404 exception    9         total += len(items[i])
Exception:..... IndexError: list index out of range
Call ended by exception
Elapsed time: 00:00:00.000450

Error occurred:
Traceback (most recent call last):
  File "/path/to/file.py", line 117, in run_file
    spec.loader.exec_module(module)
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/path/to/file.py", line 12, in <module>
    loop_index_error()
  File "/path/to/snooper-ai/snooper_ai/tracer.py", line 319, in simple_wrapper
    return function(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/path/to/file.py", line 9, in loop_index_error
    total += len(items[i])
                 ~~~~~^^^
IndexError: list index out of range
```
Example response from LLM:
```
Analysis from Claude:
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ # IndexError Analysis                                                                                                       │
│                                                                                                                             │
│ The problem is that your code is trying to access elements from the `items` list that don't exist. Here's what's happening: │
│                                                                                                                             │
│ 1. You define `items = ['apple', 'banana', 'cherry']` which has 3 elements (at indices 0, 1, and 2)                         │
│ 2. Then you loop `for i in range(5)` which tries to iterate through indices 0, 1, 2, 3, and 4                               │
│ 3. The trace shows successful iterations for:                                                                               │
│    - i=0: Accessed 'apple', total becomes 5                                                                                 │
│    - i=1: Accessed 'banana', total becomes 11                                                                               │
│    - i=2: Accessed 'cherry', total becomes 17                                                                               │
│ 4. When i=3, the code tries to access `items[3]`, but the list only has elements at indices 0, 1, and 2                     │
│ 5. This causes the `IndexError: list index out of range` exception                                                          │
│                                                                                                                             │
│ To fix this, you should either:                                                                                             │
│ 1. Make your loop match the length of your list: `for i in range(len(items))`                                               │
│ 2. Or use a try/except block to handle cases where the index might be out of range                                          │
│ 3. Or simply iterate over the items directly: `for item in items:`                                                          │
│                                                                                                                             │
│ The error occurs because you're trying to access more elements than exist in your list.                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Other usage options:

1. Display execution trace

```
snoop run file.py --show-trace
```

2. View command options:
```
snoop run --help
```

```
snoop --help
```
