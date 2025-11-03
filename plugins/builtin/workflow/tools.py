
def if_condition_met(condition: bool, then: str, else_: str) -> str:
    """Return 'then' if condition is True, otherwise return 'else_'."""
    return then if condition else else_

def case_condition_met(condition: str, cases: dict) -> str:
    """Return the value corresponding to the condition in cases, or None if not found."""
    return cases.get(condition, None)

def is_true(value: bool) -> bool:
    """Return True if value is True, otherwise return False."""
    return value is True

def is_false(value: bool) -> bool:
    """Return True if value is False, otherwise return False."""
    return value is False

def is_none(value) -> bool:
    """Return True if value is None, otherwise return False."""
    return value is None

def convert_to_string(value) -> str:
    """Convert value to string."""
    return str(value)


def convert_to_int(value) -> int:
    """Convert value to integer."""
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert {value} to int")
    

def concatenate_strings(*args) -> str:
    """Concatenate multiple strings into one."""
    return ''.join(str(arg) for arg in args)


def loop_until_condition_met(condition: callable, timeout: int = 10) -> bool:
    """Loop until the condition is met or timeout occurs."""
    import time
    start_time = time.time()
    while not condition():
        if time.time() - start_time > timeout:
            return False
        time.sleep(0.1)  # Sleep to avoid busy waiting
    return True


def iterate_over_list(lst: list, func: callable) -> list:
    """Apply a function to each item in the list and return a new list."""
    return [func(item) for item in lst]

def print_message(message: str) -> None:
    """Print a message to the console."""
    print(message)
    return message
