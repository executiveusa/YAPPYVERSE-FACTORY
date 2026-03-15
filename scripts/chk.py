import os
t = 0
g = r"E:\YAPPYVERSE-FACTORY\.git\objects"
for root, dirs, files in os.walk(g):
    for f in files:
        t += os.path.getsize(os.path.join(root, f))
with open(r"E:\chk.txt", "w") as out:
    out.write(f"git_obj_MB={t/1024/1024:.1f}\n")
    out.write(f"lock={os.path.exists(r'E:\YAPPYVERSE-FACTORY\.git\index.lock')}\n")
    out.write(f"result={os.path.exists(r'E:\YAPPYVERSE-FACTORY\init_result.txt')}\n")
