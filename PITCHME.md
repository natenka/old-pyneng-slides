# Black

---?color=linear-gradient(90deg, white 50%, black 50%)

@snap[west span-40 text-center]

### GraphQL
@fa[quote-left quote-graphql](A query language for your API)

@snapend

@snap[north-east span-40 text-08]
@box[](Step 1. Schema # Define types using SDL)
@snapend

@snap[east span-40 text-08]
@box[](Step 2. Query # Fetch data with Queries)
@snapend

@snap[south-east span-40 text-08]
@box[](Step 3. Mutate # Modify data with Mutations)
@snapend


---?color=linear-gradient(90deg, white 50%, black 50%)

@snap[west]

```
@click.command()
@click.option("--pomodoros_to_run", "-r", default=5, show_default=True, type=int)
@click.option("--work_minutes", "-w", default=25, show_default=True, type=int)
@click.option("--short_break", "-s", default=5, show_default=True, type=int)
@click.option("--long_break", "-l", default=30, show_default=True, type=int)
@click.option(
    "--set_size",
    "-p",
    default=4,
    show_default=True,
    type=int,
    help="Number of pomodoros before a long break",
)
def pomodoro(
    pomodoros_to_run: int = 5,
    work_minutes: int = 25,
    short_break: int = 5,
    long_break: int = 30,
    set_size: int = 4,
):
    session_stats = {"total": pomodoros_to_run, "done": 0, "todo": pomodoros_to_run}
    global stats
    stats = update_session_stats(session_stats)

    clearscreen()
    all_pomodoros = list(range(1, pomodoros_to_run + 1))
    pomodoro_sets = sets_of_pomodoros(all_pomodoros, set_size)
    for pomo_set in pomodoro_sets:
        run_pomodoro_set(pomo_set, work_minutes, short_break, long_break)
```

@snapend

@snap[east span-40 text-center]

```
for item in items:
    print(item)
```
@snapend


---
### Assignment expressions

+++
### Walrus operator

