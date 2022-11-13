# invoke-task-exp

# How to setup

1. Install Pipenv `pip install pipenv` 
2. Install required modules `PIPENV_VENV_IN_PROJECT=1 pipenv install`, this will create a virtual env in the current directory.
3. Execute a working shell in the virtual env `pipenv shell`
4. Check if invoke runs `inv -l`
5. Run an arbitrary invoke task `inv doctor`

# What I am doing
I want my Invoke tasks to print something with some indents prepended to each print message.
So I made the multi_print function, which prints a message with some indent provided as kwarg (indent=0).

Variable indent is a multiplier, to define how many indent string(2*SPACE == "  ") to be prepended.

Inside a task I may or may not print messages with an arbitrary indent(multiplier) values.

```python
from task_util import multi_print as mp
@task
def taskA(c):
    mp("Print the 1st message with no indent", indent=0)
    mp("Print the 2nd message with 1 indent(2 white space)", indent=1)
    mp("Print the 3rd message with 2 indent(4 white space)", indent=2)
    mp("Print the 4th message with 1 indent(2 white space)", indent=1)
```

I may run multiple Tasks in a session, and they keep indent multiplier value along with a session scope.

This is not I want, (indent multiplier is reset to 0, in every task)

```python
@task
def taskB(c):
    indent=0
    mp("Print the 1st message with no indent", indent=indent)
    mp("Print the 2nd message with 1 indent(2 white space)", indent=indent+1)
    mp("Print the 3rd message with 2 indent(4 white space)", indent=indent+2)
```

This is something I want, but this code does not run because indent multiplier is not defined.
```python
@task
def taskC(c):
    # indent multiplier to survive/come from session scope object.
    # Let's assume indent==0 in this task
    mp("Print the 1st message with no indent", indent=indent)
    mp("Print the 2nd message with 1 indent(2 white space)", indent=indent+1)
    mp("Print the 3rd message with 2 indent(4 white space)", indent=indent+2)
    indent = indent + 1 # This means the next task starts with added indent

@task
def taskD(c):
    # indent multiplier survives and keeps value from previous taskC
    # So indent==1
    mp("Print the 1st message with 1 indent", indent=indent)
    mp("Print the 2nd message with 2 indent(4 white space)", indent=indent+1)
    indent=0 # This means the indent multiplier is reset, and start with 0 in the next task.
```

Invoke task requires a task function(with @task decorator) to have Context object as its 1st arg, and
that Context is a session scope object(survive until a session ends).

So I wanted to let the (Invoke) Context object to have indent multiplier as its attribute. 

```python
@task
def taskE(c):
    if not hasattr(c, 'indent'):
      c.indent = 0
    
    mp("Print the 1st message with no indent", indent=indent)
    mp("Print the 2nd message with 1 indent(2 white space)", indent=indent+1)
    mp("Print the 3rd message with 2 indent(4 white space)", indent=indent+2)
```

This should work, but the problem is, I need to put the 1st 2lines in every single task, so I decided to define
a decorator to do that job, @pre_task.

```python
@task
@pre_task
def taskF(c):
    mp("Print the 1st message with no indent", indent=indent)
    mp("Print the 2nd message with 1 indent(2 white space)", indent=indent+1)
    mp("Print the 3rd message with 2 indent(4 white space)", indent=indent+2)
```

This works.
But here comes the next(and the final) problems.

Problem 1. I do not want to write 2 decorator for every single task.
Problem 2. If a task takes argument(s), the following code does not work.


```python
@task()
@pre_task
def taskG(c, arg1):
    mp("Print the 1st message with no indent", indent=indent)
    mp("Print the 2nd message with 1 indent(2 white space)", indent=indent+1)
    mp("Print the 3rd message with 2 indent(4 white space)", indent=indent+2)
    # use arg1
```


```shell
$ inv doctor.all

```


# Problem


# Reference

- [Invoke](https://www.pyinvoke.org/)
  - [Github](https://github.com/pyinvoke/invoke)
  - [tasks](https://github.com/pyinvoke/invoke/blob/main/invoke/tasks.py)
    - [task decorator](https://github.com/pyinvoke/invoke/blob/main/invoke/tasks.py#L274)
  -[context](https://github.com/pyinvoke/invoke/blob/main/invoke/context.py)
