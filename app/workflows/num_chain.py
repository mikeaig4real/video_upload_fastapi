from celery import chain
from app.tasks.to_decimal import to_decimal
from app.tasks.square import square
from app.tasks.sum_nums import sum_nums
from app.tasks.half import half
from celery.canvas import Signature, group


def num_workflow(x: int) -> Signature:
    print("Starting number workflow")
    num_chain = chain(
        to_decimal.s(x),  # type: ignore
        group(half.s(), square.s()),  # pyright: ignore[reportFunctionMemberAccess]
        sum_nums.s(),  # type: ignore
    )
    return num_chain.apply_async()  # type: ignore
