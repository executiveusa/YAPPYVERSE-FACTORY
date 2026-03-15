import os
out = r"E:\YAPPYVERSE-FACTORY\status_check.txt"
with open(out, "w") as f:
    f.write(f"init_result_exists={os.path.exists(r'E:\YAPPYVERSE-FACTORY\init_result.txt')}\n")
    f.write(f"index_lock_exists={os.path.exists(r'E:\YAPPYVERSE-FACTORY\.git\index.lock')}\n")
    f.write(f"git_exists={os.path.isdir(r'E:\YAPPYVERSE-FACTORY\.git')}\n")
    if os.path.exists(r"E:\YAPPYVERSE-FACTORY\init_result.txt"):
        with open(r"E:\YAPPYVERSE-FACTORY\init_result.txt") as r:
            f.write("RESULT:\n" + r.read())
    # Check git log
    import subprocess
    r = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True, text=True, cwd=r"E:\YAPPYVERSE-FACTORY")
    f.write(f"git_log_rc={r.returncode}\n")
    f.write(f"git_log={r.stdout.strip()}\n{r.stderr.strip()}\n")
    r2 = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, cwd=r"E:\YAPPYVERSE-FACTORY")
    f.write(f"git_remote={r2.stdout.strip()}\n")
