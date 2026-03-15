import os
out = r"E:\YAPPYVERSE-FACTORY\status2.txt"
with open(out, "w") as f:
    f.write(f"init_result={os.path.exists(r'E:\YAPPYVERSE-FACTORY\init_result.txt')}\n")
    f.write(f"lock={os.path.exists(r'E:\YAPPYVERSE-FACTORY\.git\index.lock')}\n")
    # Check git objects size
    obj_dir = r"E:\YAPPYVERSE-FACTORY\.git\objects"
    if os.path.isdir(obj_dir):
        total = 0
        for root, dirs, files in os.walk(obj_dir):
            for fn in files:
                total += os.path.getsize(os.path.join(root, fn))
        f.write(f"git_objects_MB={total/1024/1024:.1f}\n")
    # Check COMMIT_EDITMSG
    ce = r"E:\YAPPYVERSE-FACTORY\.git\COMMIT_EDITMSG"
    f.write(f"commit_msg_exists={os.path.exists(ce)}\n")
    # Check refs
    heads = r"E:\YAPPYVERSE-FACTORY\.git\refs\heads"
    if os.path.isdir(heads):
        f.write(f"branches={os.listdir(heads)}\n")
    # Check packed-refs
    pr = r"E:\YAPPYVERSE-FACTORY\.git\packed-refs"
    f.write(f"packed_refs={os.path.exists(pr)}\n")
