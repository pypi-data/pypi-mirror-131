from grimoire import s


def get_commit_hash():
    return s.run_with_result("(git rev-parse HEAD | head -c 10) ||  true")
