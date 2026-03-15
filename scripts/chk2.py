import os
with open(r"E:\chk2.txt", "w") as f:
    f.write(f"lock={os.path.exists(r'E:\YAPPYVERSE-FACTORY\.git\index.lock')}\n")
    f.write(f"result={os.path.exists(r'E:\YAPPYVERSE-FACTORY\init_result.txt')}\n")
    f.write("OK\n")
