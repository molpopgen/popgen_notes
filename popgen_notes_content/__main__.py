import click
import popgen_notes_content.human_chimp_gorilla


@click.group()
def _do_work():
    pass


def main():
    _do_work.add_command(popgen_notes_content.human_chimp_gorilla.human_chimp_gorilla)
    _do_work.add_command(
        popgen_notes_content.human_chimp_gorilla.human_chimp_gorilla_colored_edges
    )
    _do_work.add_command(
        popgen_notes_content.human_chimp_gorilla.human_chimp_gorilla_with_mutations
    )
    _do_work.add_command(popgen_notes_content.human_chimp_gorilla.human_chimp_gorilla_with_multiple_hits)
    _do_work()


if __name__ == "__main__":
    main()
