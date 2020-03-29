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

@snap[west span-40 text-center]

```
for item in items:
    print(item)
```

@snapend

@snap[east span-40 text-center]

```
for item in items:
    print(item)
```
@snapend


---?color=linear-gradient(180deg, white 50%, black 50%)

@snap[north span-100]
@code[py code-max code-shadow](src/pomodoro.py)
@snapend

@snap[south span-100]
```
def pomodoro(
    pomodoros_to_run: int = 5,
    work_minutes: int = 25,
    short_break: int = 5,
    long_break: int = 30,
    set_size: int = 4,
):
    session_stats = {"total": pomodoros_to_run, "done": 0, "todo": pomodoros_to_run}
    stats = update_session_stats(session_stats)

```


@snapend



---
### Assignment expressions

+++
### Walrus operator

