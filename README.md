# snooper-ai 🔍

**snooper-ai** is a simple fork of [PySnooper](https://github.com/cool-RR/PySnooper). It simply sends the entire execution trace to an LLM for debugging, so it fully understands what happened in your code.

Disclaimer: This was implemented simply and may not be very robust. Feel free to submit issues. 


## Usage:
1. Store your LLM api key (either claude or openai):
```
ANTHROPIC_API_KEY=xxx
OPENAI_API_KEY=xxx
```
2. Add a decorator to the function you want to inquire:
```python
from snooper_ai import snoop

@snoop()
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]

number_to_bits(6)
```
3. Run the file

```
snoop run file.py
```
4. Tell the LLM what you're confused about:
```bash
╭─────────────────────────────────────────────────╮
│  🔍 snooper-ai: Debug your Python code with AI  │
╰─────────────────────────────────────────────────╯

What would you like to know about the code execution? (e.g. Error messages, unexpected behavior, etc.):
```

5. Run it and get a detailed explanation!

6. To choose which model you're using (This will be saved in your pyproject.toml):
```
snoop config
```

## More info

This is what gets sent to the LLM. Refer to the original PySnooper for more details


```
New var:....... i = 9
New var:....... lst = [681, 267, 74, 832, 284, 678, ...]
09:37:35.881721 line        10         lower = min(lst)
New var:....... lower = 74
09:37:35.882137 line        11         upper = max(lst)
New var:....... upper = 832
09:37:35.882304 line        12         mid = (lower + upper) / 2
74 453.0 832
New var:....... mid = 453.0
09:37:35.882486 line        13         print(lower, mid, upper)
Elapsed time: 00:00:00.000344
```


## Installation with Pip

The best way to install **snooper-ai** is with Pip:

```console
$ pip install snooper-ai
```
