MIN_ITERATIONS = 2


def validate_iterations(iterations: int) -> None:
    if iterations < MIN_ITERATIONS:
        raise ValueError(f"iterations value {iterations} must be greater than {MIN_ITERATIONS}.")