"""
YAPPYVERSE Asset Scanner & Organizer
=====================================
Scans a character's source folder, classifies files, copies them
to canonical paths with canonical names, and writes .meta.json sidecars.

Usage:
  python scan_assets.py --character pauli
  python scan_assets.py --character pauli --dry-run
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone

FACTORY_ROOT = r"E:\YAPPYVERSE-FACTORY"
ASSETS_ROOT = os.path.join(FACTORY_ROOT, "assets")

# Classification rules: extension -> category
EXT_CATEGORIES = {
    ".png": "reference",
    ".jpg": "reference",
    ".jpeg": "reference",
    ".webp": "reference",
    ".bmp": "reference",
    ".tiff": "reference",
    ".gif": "reference",
    ".svg": "reference",
    ".obj": "mesh",
    ".fbx": "mesh",
    ".glb": "mesh",
    ".gltf": "mesh",
    ".stl": "mesh",
    ".blend": "rig",
    ".mp4": "animation",
    ".mov": "animation",
    ".avi": "animation",
    ".webm": "animation",
    ".mp3": "audio",
    ".wav": "audio",
    ".ogg": "audio",
    ".flac": "audio",
    ".m4a": "audio",
    ".pdf": "reference",
}

# Filename-based overrides (substring match, case-insensitive)
NAME_OVERRIDES = {
    "nft": "nft",
    "coin": "nft",
    "card": "nft",
    "render": "render",
    "turntable": "render",
    "texture": "texture",
    "material": "texture",
    "pbr": "texture",
    "normal": "texture",
    "roughness": "texture",
    "metallic": "texture",
    "albedo": "texture",
    "diffuse": "texture",
    "rig": "rig",
    "skeleton": "rig",
    "armature": "rig",
    "voice": "audio",
    "sound": "audio",
    "morph": "animation",
    "anim": "animation",
}

# Variant classification (substring match)
VARIANT_HINTS = {
    "full": "hero",
    "hero": "hero",
    "main": "hero",
    "mugshot": "mugshot",
    "profile": "profile",
    "thumbnail": "thumb",
    "thumb": "thumb",
    "icon": "icon",
    "logo": "logo",
    "plant": "plant",
    "cadillac": "cadillac",
    "cosmos": "cosmos",
    "coin": "coin",
    "funnel": "funnel",
    "effect": "effect",
    "bambu": "bambu",
    "morph": "morph",
}


def sha256_file(filepath):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def classify_file(filename, ext):
    """Determine category and variant for a file."""
    name_lower = filename.lower()

    # Check name overrides first
    category = None
    for keyword, cat in NAME_OVERRIDES.items():
        if keyword in name_lower:
            category = cat
            break

    # Fall back to extension
    if category is None:
        category = EXT_CATEGORIES.get(ext.lower(), "reference")

    # Determine variant
    variant = "v1"
    for keyword, var in VARIANT_HINTS.items():
        if keyword in name_lower:
            variant = var
            break

    return category, variant


def scan_folder(source_folder):
    """Recursively scan source folder and return file info list."""
    files = []
    for root, dirs, filenames in os.walk(source_folder):
        for fname in filenames:
            filepath = os.path.join(root, fname)
            ext = os.path.splitext(fname)[1].lower()

            # Skip system/hidden files
            if fname.startswith(".") or fname.startswith("~"):
                continue

            category, variant = classify_file(fname, ext)
            rel_path = os.path.relpath(filepath, source_folder)

            files.append({
                "source_path": filepath,
                "source_relative": rel_path,
                "original_name": fname,
                "extension": ext,
                "category": category,
                "variant": variant,
                "size_bytes": os.path.getsize(filepath),
            })

    return files


def generate_canonical_name(canonical_id, category, variant, version, ext):
    """Generate canonical filename: {id}_{category}_{variant}_v{NNN}.{ext}"""
    return f"{canonical_id}_{category}_{variant}_v{version:03d}{ext}"


def organize_files(canonical_id, files, dry_run=False):
    """Copy files to canonical locations and write .meta.json sidecars."""
    char_dir = os.path.join(ASSETS_ROOT, canonical_id)
    results = []

    # Track version numbers per category+variant combo
    version_counter = {}

    for finfo in files:
        cat = finfo["category"]
        var = finfo["variant"]
        ext = finfo["extension"]

        key = f"{cat}_{var}"
        version_counter[key] = version_counter.get(key, 0) + 1
        version = version_counter[key]

        canon_name = generate_canonical_name(canonical_id, cat, var, version, ext)
        dest_dir = os.path.join(char_dir, cat)
        dest_path = os.path.join(dest_dir, canon_name)
        meta_path = dest_path + ".meta.json"

        finfo["canonical_name"] = canon_name
        finfo["destination"] = dest_path
        finfo["label"] = f"{canonical_id}:{cat}:{var}:v{version}"

        if dry_run:
            finfo["action"] = "DRY_RUN"
        else:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy2(finfo["source_path"], dest_path)
            finfo["sha256"] = sha256_file(dest_path)
            finfo["action"] = "COPIED"

            # Write meta sidecar
            meta = {
                "canonical_name": canon_name,
                "label": finfo["label"],
                "category": cat,
                "variant": var,
                "version": version,
                "original_name": finfo["original_name"],
                "source_path": finfo["source_path"],
                "sha256": finfo["sha256"],
                "size_bytes": finfo["size_bytes"],
                "organized_at": datetime.now(timezone.utc).isoformat(),
            }
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)

        results.append(finfo)

    return results


def main():
    parser = argparse.ArgumentParser(description="YAPPYVERSE Asset Scanner")
    parser.add_argument("--character", required=True, help="Canonical character ID (e.g., pauli)")
    parser.add_argument("--dry-run", action="store_true", help="List files without copying")
    parser.add_argument("--source", default=None, help="Override source folder path")
    args = parser.parse_args()

    # Load registry
    registry_path = os.path.join(ASSETS_ROOT, "registry.json")
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    char_entry = registry["characters"].get(args.character)
    if char_entry is None:
        print(f"ERROR: Character '{args.character}' not found in registry")
        sys.exit(1)

    source_folder = args.source or char_entry.get("source_folder")
    if source_folder is None:
        # Try CHARACTER_CONFIG.json
        config_path = os.path.join(ASSETS_ROOT, args.character, "CHARACTER_CONFIG.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            source_folder = config.get("source_assets", {}).get("source_folder")

    if source_folder is None or not os.path.isdir(source_folder):
        print(f"ERROR: Source folder not found: {source_folder}")
        sys.exit(1)

    print(f"Scanning: {source_folder}")
    files = scan_folder(source_folder)
    print(f"Found {len(files)} files")

    # Classify summary
    categories = {}
    for f in files:
        cat = f["category"]
        categories[cat] = categories.get(cat, 0) + 1
    print("Classification summary:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    # Organize
    mode = "DRY RUN" if args.dry_run else "COPYING"
    print(f"\n--- {mode} ---")
    results = organize_files(args.character, files, dry_run=args.dry_run)

    # Write manifest
    manifest_path = os.path.join(ASSETS_ROOT, args.character, "manifest.json")
    manifest = {
        "character": args.character,
        "source_folder": source_folder,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "total_files": len(results),
        "files": results,
    }

    if not args.dry_run:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, default=str)
        print(f"\nManifest written: {manifest_path}")

    # Print results
    for r in results:
        print(f"  [{r['action']}] {r['original_name']} -> {r.get('canonical_name', '?')} ({r['label']})")

    # Write summary to output file
    summary_path = os.path.join(FACTORY_ROOT, f"scan_{args.character}.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"character={args.character}\n")
        f.write(f"source={source_folder}\n")
        f.write(f"total={len(results)}\n")
        f.write(f"dry_run={args.dry_run}\n")
        for r in results:
            f.write(f"{r['action']} | {r['original_name']} -> {r.get('canonical_name', '?')} | {r['label']}\n")

    print(f"\nDone! Summary: {summary_path}")


if __name__ == "__main__":
    main()
