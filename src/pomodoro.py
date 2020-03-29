
def pomodoro(pomodoros_to_run: int = 5, work_minutes: int = 25,
             short_break: int = 5, long_break: int = 30, set_size: int = 4):
    session_stats = {"total": pomodoros_to_run, "done": 0, "todo": pomodoros_to_run}
    stats = update_session_stats(session_stats)
