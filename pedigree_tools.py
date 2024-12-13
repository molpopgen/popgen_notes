import argparse
from dataclasses import dataclass
import pickle
import typing

import msprime
import numpy as np
import tskit


@dataclass
class PedigreeRecord:
    id: int
    parents: list[int]
    time: int
    sex: typing.Optional[int]


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help="subcommand help")

    simulate = subparsers.add_parser("simulate", help="simulate a random pedigree")
    simulate.add_argument("--individuals", "-i", type=int, help="number of individuals")
    simulate.add_argument("--generations", "-g", type=int, help="number of generations")
    simulate.add_argument("--outfile", "-o", type=str, help="output file name")
    simulate.add_argument("--seed", "-s", type=int, help="random number seed")

    tables = subparsers.add_parser(
        "make_tables", help="make table collection from pedigree records"
    )
    tables.add_argument("--infile", "-i", type=str, help="pedigree records file")
    tables.add_argument(
        "--tables", "-t", type=str, help="output file for a tskit.TableCollection"
    )
    tables.add_argument("--sequence_length", "-l", type=float, help="genome_length")

    dataframe = subparsers.add_parser(
        "make_dataframe", help="make table collection from pedigree records"
    )
    dataframe.add_argument("--infile", "-i", type=str, help="pedigree records file")
    dataframe.add_argument(
        "--dataframe", "-d", type=str, help="output file for data frame"
    )

    return parser


def main():
    parser = make_parser()
    parsed = parser.parse_args()

    if "individuals" in parsed:
        records = strict_monogamy(
            parsed.individuals,
            parsed.generations,
            parsed.seed,
        )
        with open(parsed.outfile, "wb") as f:
            pickle.dump(records, f)
    elif "tables" in parsed:
        with open(parsed.infile, "rb") as f:
            records = pickle.load(f)
            tables = records_to_pedigree(records, parsed.sequence_length)
            tables.dump(parsed.tables)
    elif "dataframe" in parsed:
        with open(parsed.infile, "rb") as f:
            records = pickle.load(f)
            df = records_to_dataframe(records)
            with open(parsed.dataframe, "w") as f:
                f.write(df)


def strict_monogamy(
    num_individuals, num_generations, seed=None
) -> list[PedigreeRecord]:
    assert num_individuals % 2 == 0.0
    assert num_generations > 1
    rv = []

    if seed is None:
        rng_seed = 0
    else:
        rng_seed = seed
    np.random.seed(rng_seed)
    current_parents = []
    for i in range(num_individuals):
        current_parents.append(i)
        rv.append(
            PedigreeRecord(
                id=i, parents=[None, None], time=num_generations - 1, sex=None
            )
        )
    current_time = num_generations - 1
    next_parents = []
    next_id = len(current_parents)
    while current_time > 0:
        shuffled_parents = np.random.choice(
            current_parents, size=len(current_parents), replace=False
        )
        for i in range(len(current_parents) // 2):
            s = shuffled_parents[2 * i : 2 * i + 2]
            assert len(s) == 2
            rv[min(s)].sex = 0
            rv[max(s)].sex = 1
        p = 1.0 / float(len(current_parents) // 2)
        num_offspring = np.random.multinomial(
            num_individuals, pvals=[p] * (len(current_parents) // 2), size=1
        )[0]
        for i, n in enumerate(num_offspring):
            for _ in range(n):
                rv.append(
                    PedigreeRecord(
                        id=next_id,
                        parents=[
                            int(shuffled_parents[2 * i]),
                            int(shuffled_parents[2 * i + 1]),
                        ],
                        time=current_time - 1,
                        sex=None,
                    )
                )
                next_parents.append(next_id)
                next_id += 1
        current_parents, next_parents = next_parents, current_parents
        next_parents.clear()
        current_time -= 1

    # randomise sex ratio of final generation
    for i in current_parents:
        rv[i].sex = int(np.random.choice([0, 1], 1)[0])

    return rv


def strict_monogamy_random_sex_ratio(
    num_individuals, num_generations, seed=None
) -> list[PedigreeRecord]:
    raise NotImplementedError("not sure this is up to date")
    assert num_individuals % 2 == 0.0
    assert num_generations > 1
    rv = []

    if seed is None:
        rng_seed = 0
    else:
        rng_seed = seed
    np.random.seed(rng_seed)
    current_parents = []
    sex = [0, 1]
    for i in range(num_individuals):
        current_parents.append(i)
        rv.append(
            PedigreeRecord(
                id=i,
                parents=[None, None],
                time=num_generations - 1,
                sex=int(np.random.choice(sex, 1)[0]),
            )
        )
    if all([rv[i].sex == 0 for i in current_parents]):
        rv[-1].sex = 1
    if all([rv[i].sex == 1 for i in current_parents]):
        rv[-1].sex = 0
    current_time = num_generations - 1
    next_parents = []
    next_id = len(current_parents)
    while current_time > 0:
        male_parents = [
            rv[j].id for i, j in enumerate(current_parents) if rv[j].sex == 0
        ]
        female_parents = [
            rv[j].id for i, j in enumerate(current_parents) if rv[j].sex == 1
        ]
        pairs = min(len(male_parents), len(female_parents))
        assert pairs > 0
        p = 1.0 / float(pairs)
        num_offspring = np.random.multinomial(
            num_individuals, pvals=[p] * pairs, size=1
        )[0]
        for i, n in enumerate(num_offspring):
            for _ in range(n):
                rv.append(
                    PedigreeRecord(
                        id=next_id,
                        parents=[
                            male_parents[i],
                            female_parents[i],
                        ],
                        time=current_time - 1,
                        sex=np.random.choice(sex, 1)[0],
                    )
                )
                next_parents.append(next_id)
                next_id += 1
        current_parents, next_parents = next_parents, current_parents
        next_parents.clear()
        current_time -= 1

    return rv


def records_to_pedigree(
    records: list[PedigreeRecord], sequence_length: float
) -> tskit.TableCollection:
    pb = msprime.PedigreeBuilder()
    records = sorted(records, key=lambda x: x.id)
    for r in records:
        sample = False
        if r.time == 0:
            sample = True
        if all([i is not None for i in r.parents]):
            id = pb.add_individual(time=r.time, parents=r.parents, is_sample=sample)
        else:
            id = pb.add_individual(time=r.time, is_sample=sample)
        assert id == r.id
    return pb.finalise(sequence_length)


def records_to_dataframe(records: list[PedigreeRecord]) -> str:
    rv = "id momid dadid sex\n"
    for r in records:
        momid = "NA"
        dadid = "NA"
        for p in r.parents:
            if p is not None:
                if records[p].sex == 0:
                    dadid = p
                if records[p].sex == 1:
                    momid = p
        rv += f"{r.id} {momid} {dadid} {r.sex}\n"
    return rv


if __name__ == "__main__":
    main()
