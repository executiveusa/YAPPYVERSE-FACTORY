"""Wire .env from master.env for YAPPYVERSE Factory."""
import os, re

MASTER_ENV = r"E:\THE PAULI FILES\master.env"
OUTPUT_ENV = os.path.join(os.path.dirname(__file__), "..", ".env")

# Map master.env keys to what the factory needs
KEY_MAP = {
    "ANTHROPIC_API_KEY": "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY": "OPENAI_API_KEY",
    "GOOGLE_API_KEY": "GOOGLE_API_KEY",
    "OPEN_ROUTER_API": "OPEN_ROUTER_API",
    "HUGGINGFACE_TOKEN": "HUGGINGFACE_TOKEN",
    "READYPLAYERME_TOKEN": "READYPLAYERME_TOKEN",
    "REPLICATE_API_KEY": "REPLICATE_API_KEY",
    "VERCEL_TOKEN": "VERCEL_TOKEN",
    "GH_PAT": "GH_PAT",
    "SUPABASE_URL": "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY_2": "SUPABASE_SERVICE_ROLE_KEY",
}

def load_env(path):
    env = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

if __name__ == "__main__":
    if not os.path.exists(MASTER_ENV):
        print(f"ERROR: {MASTER_ENV} not found")
        exit(1)
    
    master = load_env(MASTER_ENV)
    lines = [
        "# Auto-generated from master.env",
        f"# Source: {MASTER_ENV}",
        f"BLENDER_PATH=C:\\Program Files\\Blender Foundation\\Blender 5.0\\blender.exe",
        "",
    ]
    
    for src_key, dst_key in KEY_MAP.items():
        val = master.get(src_key, "")
        if val:
            lines.append(f"{dst_key}={val}")
        else:
            lines.append(f"# {dst_key}= (not found in master.env)")
    
    with open(OUTPUT_ENV, "w") as f:
        f.write("\n".join(lines) + "\n")
    
    print(f"Written {OUTPUT_ENV} with {sum(1 for l in lines if '=' in l and not l.startswith('#'))} keys")
