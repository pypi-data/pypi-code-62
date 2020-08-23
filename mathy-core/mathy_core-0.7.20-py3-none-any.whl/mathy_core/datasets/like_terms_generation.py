"""Generate a dataset of expressions and their unique like terms as string outputs.

The challenge then is for the model to identify and extract the like terms from an
expression, e.g.

IN: 4x + x^3 - 7x
OUT: 4x[SEP]-7x
"""
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Set
from mathy.expressions import SubtractExpression
from collections import OrderedDict
from mathy.tree import LEFT, RIGHT
import numpy as np
import typer
from tqdm.auto import tqdm

from mathy import ExpressionParser, MathExpression, TermEx, get_term_ex, get_terms
from mathy.problems import gen_simplify_multiple_terms, mathy_term_string

parser = ExpressionParser()


def generate_newline_q_a(
    file_base: str,
    number: int,
    exclude: Optional[Set[str]] = None,
    eval: bool = False,
    max_len: int = 128,
):

    train_file = f"{file_base}.txt"
    if exclude is None:
        exclude = set()
    skips = 0
    skip_threshold = 100
    problems = 0
    min_like = 4 if eval else 2
    max_like = 12 if eval else 4
    min_noise = 1
    max_noise = 2
    with Path(train_file).open("w") as f:
        with tqdm(total=number, mininterval=0.25, desc=file_base) as pbar:
            while problems < number:
                text, complexity = gen_simplify_multiple_terms(
                    random.randint(min_like, max_like),
                    noise_probability=0.5,
                    noise_terms=random.randint(min_noise, max_noise),
                    op=["+", "-"],
                )

                if text in exclude or len(text) >= max_len:
                    skips += 1
                    if skips >= skip_threshold:
                        raise ValueError(
                            f"Failed to generate more unique problems after {skips} tries!"
                        )
                    continue

                skips = 0
                exclude.add(text)
                answer = list_like_terms(text, sep=",")
                f.write(f"{text}\n{answer}\n")
                pbar.update(1)
                problems += 1


def list_like_terms(input_problem: str, sep: str) -> str:
    expression: MathExpression = parser.parse(input_problem)
    term_nodes: List[MathExpression] = get_terms(expression)
    node_groups: OrderedDict[str, List[MathExpression]] = OrderedDict()
    for term_node in term_nodes:
        ex: Optional[TermEx] = get_term_ex(term_node)
        assert ex is not None, f"invalid expression {term_node}"
        key = mathy_term_string(variable=ex.variable, exponent=ex.exponent)
        if key == "":
            key = "const"
        if key not in node_groups:
            node_groups[key] = [term_node]
        else:
            node_groups[key].append(term_node)
    out_terms: List[str] = []
    for term_node in term_nodes:
        ex: Optional[TermEx] = get_term_ex(term_node)
        assert ex is not None, f"invalid expression {term_node}"
        key = mathy_term_string(variable=ex.variable, exponent=ex.exponent)
        if key == "":
            key = "const"
        assert key in node_groups
        if len(node_groups[key]) <= 1:
            continue
        is_parent_sub = isinstance(term_node.parent, SubtractExpression)
        is_right_side = term_node.parent.get_side(term_node) == RIGHT
        pre = "-" if is_parent_sub and is_right_side else ""
        out_terms.append(f"{pre}{term_node}")
    return sep.join(out_terms)


def main(
    name: str,
    train_size: int = 1000 * 1000,
    eval_size: int = 1000,
    max_len: int = 128,
    include_eval: bool = True,
    include_generalization: bool = True,
):
    current = os.path.dirname(__file__)
    train_file = os.path.join(current, f"{name}.train")
    eval_file = os.path.join(current, f"{name}.eval")
    generalization_file = os.path.join(current, f"{name}.generalization")

    seen_texts: Set[str] = set()

    print(f"Generating train dataset with {train_size} examples...")
    generate_newline_q_a(train_file, train_size, seen_texts, max_len=max_len)
    if include_eval:
        print(f"Generating eval dataset with {eval_size} examples...")
        generate_newline_q_a(eval_file, eval_size, seen_texts, max_len=max_len)

    if include_generalization:
        print(f"Generating generalization dataset with {eval_size} examples...")
        generate_newline_q_a(
            generalization_file, eval_size, seen_texts, max_len=max_len, eval=True,
        )


if __name__ == "__main__":
    typer.run(main)
