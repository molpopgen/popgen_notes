from dataclasses import dataclass
import pickle
import typing

import click
import msprime
import numpy as np
import tskit


@dataclass
class PedigreeRecord:
    id: int
    parents: list[int]
    time: int
    sex: typing.Optional[int]


@click.command(
    help="""
Simulate a pedigree with a costant number of individuals each generation.
The simulation enforces strict monogamy.
For all generations except the last, the sex ratio is kept at exactly 50/50.
"""
)
@click.option("--individuals", "-i", type=int, help="Number of founder individuals")
@click.option("--generations", "-g", type=int, help="Number of generations to simulate")
@click.option(
    "--outfile",
    "-o",
    type=str,
    help="Output file name to write pedigree records."
    " The format is Python's pickle.",
)
@click.option("--seed", "-s", type=int, help="Random number seed.")
def simulate(individuals, generations, outfile, seed):
    records = strict_monogamy(
        individuals,
        generations,
        seed,
    )
    with open(outfile, "wb") as f:
        pickle.dump(records, f)


@click.command(help="Convert pedigree records to a tskit.TableCollection.")
@click.option(
    "--infile",
    "-i",
    help="Input file name." " Should be an output file from the 'simulate' subcommand.",
)
@click.option("--outfile", "-o", help="File name to write the TableCollection.")
@click.option("--sequence_length", "-l", type=int, help="Length of the genome (bp).")
def tables(infile, outfile, sequence_length):
    with open(infile, "rb") as f:
        records = pickle.load(f)
        tc = records_to_pedigree(records, sequence_length)
        tc.dump(outfile)


@click.command(help="Convert pedigree records into a text file.")
@click.option(
    "--infile",
    "-i",
    help="The input file name."
    " Should be an output file from the 'simulate' subcommand.",
)
@click.option(
    "--outfile",
    "-o",
    help="Output file name." " Format is compatible with R's kinship2 package.",
)
def dataframe(infile, outfile):
    with open(infile, "rb") as f:
        records = pickle.load(f)
        df = records_to_dataframe(records)
        with open(outfile, "w") as f:
            f.write(df)


@click.command(
    help="""
Make a tskit.TreeSequence from a tskit.TableCollection using msprime's
fixed pedigree model.
"""
)
@click.option(
    "--input", "-i", help="Input file name. Contents are the TableCollection."
)
@click.option("--outfile", "-o", help="Output file name.")
@click.option("--recombination", "-r", help="Recombination rate (per bp).")
@click.option("--seed", "-s", type=int, help="Random number seed.")
def treeseq(input, recombination, outfile, seed):
    tc = tskit.TableCollection.load(input)
    ts = msprime.sim_ancestry(
        initial_state=tc,
        model="fixed_pedigree",
        recombination_rate=recombination,
        additional_nodes=(
            msprime.NodeType.RECOMBINANT
            | msprime.NodeType.PASS_THROUGH
            | msprime.NodeType.COMMON_ANCESTOR
        ),
        coalescing_segments_only=False,
        random_seed=seed,
    )
    ts.dump(outfile)


@click.group()
def do_work():
    pass


def main():
    do_work.add_command(simulate)
    do_work.add_command(tables)
    do_work.add_command(dataframe)
    do_work.add_command(treeseq)
    do_work()


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
