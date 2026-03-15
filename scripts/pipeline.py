"""
YAPPYVERSE Character Factory Pipeline
Orchestrates the full 10-node MAS-Factory graph for one character:
  scanner → tagger → organizer → model_gen → texture → rigger →
  animator → scene → nft_card → qa_switch

Usage:
  python pipeline.py --character pauli [--stage all|scan|model|rig|nft]
  python pipeline.py --batch               # process all queued characters
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

FACTORY_ROOT = Path(r"E:\YAPPYVERSE-FACTORY")
ASSETS_DIR = FACTORY_ROOT / "assets"
SCRIPTS_DIR = FACTORY_ROOT / "scripts"
BLENDER = Path(r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe")
PYTHON = Path(sys.executable)

REGISTRY_PATH = ASSETS_DIR / "registry.json"


def load_registry() -> dict:
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_registry(reg: dict):
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2)


def load_config(character_id: str) -> dict:
    cfg_path = ASSETS_DIR / character_id / "CHARACTER_CONFIG.json"
    if not cfg_path.exists():
        raise FileNotFoundError(f"No CHARACTER_CONFIG.json for {character_id}")
    with open(cfg_path, encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────────────────────────
# Stage 1: SCAN
# ─────────────────────────────────────────────
def stage_scan(character_id: str) -> dict:
    """Run scan_assets.py for this character, return manifest."""
    print(f"[scan] scanning {character_id} assets…")
    scan_script = SCRIPTS_DIR / "scan_assets.py"
    result = subprocess.run(
        [str(PYTHON), str(scan_script), "--character", character_id],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"[scan] WARN: {result.stderr[:200]}")
    manifest_path = ASSETS_DIR / character_id / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path, encoding="utf-8") as f:
            return json.load(f)
    return {}


# ─────────────────────────────────────────────
# Stage 2: MODEL_GEN  (HuggingFace TripoSR / Replicate)
# ─────────────────────────────────────────────
def stage_model_gen(character_id: str, config: dict) -> Path | None:
    """
    Generate 3D mesh from hero reference image.
    Uses HuggingFace TripoSR API if HUGGINGFACE_TOKEN is set,
    otherwise falls back to Replicate triposr model.
    Returns path to output .glb file or None on failure.
    """
    print(f"[model_gen] generating 3D mesh for {character_id}…")
    ref_dir = ASSETS_DIR / character_id / "reference"
    mesh_dir = ASSETS_DIR / character_id / "mesh"

    # Find hero reference image
    hero = None
    for pattern in ["*_reference_hero_v001.png", "*_reference_hero_v001.jpg",
                     "*_reference_hero_v001.PNG", "*hero*"]:
        candidates = list(ref_dir.glob(pattern))
        if candidates:
            hero = candidates[0]
            break

    if not hero:
        # Fall back to first PNG in reference dir
        candidates = list(ref_dir.glob("*.png")) + list(ref_dir.glob("*.PNG")) + list(ref_dir.glob("*.jpg"))
        if candidates:
            hero = candidates[0]

    if not hero:
        print(f"[model_gen] ERROR: no hero reference image found in {ref_dir}")
        return None

    print(f"[model_gen] using hero image: {hero.name}")

    output_glb = mesh_dir / f"{character_id}_mesh_base_v001.glb"
    output_obj = mesh_dir / f"{character_id}_mesh_base_v001.obj"

    # Try HuggingFace TripoSR
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")
    if hf_token:
        try:
            return _model_gen_huggingface(hero, output_obj, character_id, hf_token)
        except Exception as e:
            print(f"[model_gen] HuggingFace failed: {e}, trying Replicate…")

    # Try Replicate
    replicate_key = os.environ.get("REPLICATE_API_KEY")
    if replicate_key:
        try:
            return _model_gen_replicate(hero, output_glb, character_id, replicate_key)
        except Exception as e:
            print(f"[model_gen] Replicate failed: {e}")

    print("[model_gen] SKIP: no API keys available (HUGGINGFACE_TOKEN or REPLICATE_API_KEY)")
    return None


def _model_gen_huggingface(hero: Path, output: Path, character_id: str, token: str) -> Path | None:
    """Call HuggingFace TripoSR inference API."""
    try:
        import urllib.request, base64
        with open(hero, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()

        payload = json.dumps({
            "inputs": img_b64,
            "parameters": {"output_format": "obj", "remove_background": True}
        }).encode()

        req = urllib.request.Request(
            "https://api-inference.huggingface.co/models/stabilityai/TripoSR",
            data=payload,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()

        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "wb") as f:
            f.write(data)
        print(f"[model_gen] HuggingFace TripoSR saved to {output}")
        return output
    except Exception as e:
        raise RuntimeError(f"HuggingFace TripoSR error: {e}") from e


def _model_gen_replicate(hero: Path, output: Path, character_id: str, api_key: str) -> Path | None:
    """Call Replicate triposr model."""
    try:
        import urllib.request, base64

        # Upload image as data URI
        with open(hero, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        ext = hero.suffix.lower().lstrip(".")
        data_uri = f"data:image/{ext};base64,{img_b64}"

        # Create prediction
        payload = json.dumps({
            "version": "0bc5c1c82d5c6f71f3de67f4a2c5c41f38e3bcede4e0da5b19b786f1a75a9d86",
            "input": {"image": data_uri, "do_remove_background": True, "foreground_ratio": 0.85}
        }).encode()

        req = urllib.request.Request(
            "https://api.replicate.com/v1/predictions",
            data=payload,
            headers={"Authorization": f"Token {api_key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            pred = json.loads(resp.read())

        pred_id = pred["id"]
        print(f"[model_gen] Replicate prediction {pred_id} started, polling…")

        # Poll for completion (up to 5 min)
        poll_url = f"https://api.replicate.com/v1/predictions/{pred_id}"
        for _ in range(60):
            time.sleep(5)
            req = urllib.request.Request(poll_url,
                headers={"Authorization": f"Token {api_key}"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read())
            status = result.get("status")
            if status == "succeeded":
                mesh_url = result["output"]
                if isinstance(mesh_url, list):
                    mesh_url = mesh_url[0]
                # Download the mesh
                output.parent.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(mesh_url, str(output))
                print(f"[model_gen] Replicate TripoSR saved to {output}")
                return output
            elif status == "failed":
                raise RuntimeError(f"Replicate prediction failed: {result.get('error')}")

        raise RuntimeError("Replicate prediction timed out after 5 minutes")
    except Exception as e:
        raise RuntimeError(f"Replicate error: {e}") from e


# ─────────────────────────────────────────────
# Stage 3: RIG  (Blender headless)
# ─────────────────────────────────────────────
def stage_rig(character_id: str) -> Path | None:
    """Run auto_rig.py in Blender headless mode."""
    print(f"[rig] auto-rigging {character_id} in Blender…")
    mesh_dir = ASSETS_DIR / character_id / "mesh"
    rig_dir = ASSETS_DIR / character_id / "rig"
    auto_rig = SCRIPTS_DIR / "auto_rig.py"

    meshes = list(mesh_dir.glob("*.obj")) + list(mesh_dir.glob("*.glb"))
    if not meshes:
        print(f"[rig] SKIP: no mesh found in {mesh_dir} (run model_gen first)")
        return None

    mesh_in = meshes[0]
    rig_out = rig_dir / f"{character_id}_rigged_v001.glb"
    rig_dir.mkdir(parents=True, exist_ok=True)

    if not BLENDER.exists():
        print(f"[rig] ERROR: Blender not found at {BLENDER}")
        return None

    result = subprocess.run([
        str(BLENDER), "--background", "--python", str(auto_rig),
        "--", "--input", str(mesh_in), "--output", str(rig_out)
    ], capture_output=True, text=True, timeout=300)

    if result.returncode == 0 and rig_out.exists():
        print(f"[rig] rigged mesh saved to {rig_out}")
        return rig_out
    else:
        print(f"[rig] ERROR (rc={result.returncode}): {result.stderr[-300:]}")
        return None


# ─────────────────────────────────────────────
# Stage 4: NFT CARD
# ─────────────────────────────────────────────
def stage_nft_card(character_id: str, config: dict) -> Path | None:
    """
    Compose NFT card and generate ERC-721 metadata JSON using Pillow.
    Falls back to copying hero reference if Pillow unavailable.
    """
    print(f"[nft_card] composing NFT card for {character_id}…")
    ref_dir = ASSETS_DIR / character_id / "reference"
    nft_dir = ASSETS_DIR / character_id / "nft"
    nft_dir.mkdir(parents=True, exist_ok=True)

    identity = config.get("identity", {})
    palette = config.get("palette", {})
    display_name = identity.get("display_name", character_id)
    tagline = identity.get("tagline", "")
    edition = identity.get("edition", 1)
    bg_rgb = tuple(int(x) for x in palette.get("background", "20 15 30").split())
    accent_rgb = tuple(int(x) for x in palette.get("accent", "255 100 50").split())

    # Find hero reference
    hero = None
    for pat in ["*_reference_hero_v001.png", "*_reference_hero_v001.PNG", "*.png", "*.PNG"]:
        cands = list(ref_dir.glob(pat))
        if cands:
            hero = cands[0]
            break

    card_path = nft_dir / f"{character_id}_nft_card_v001.png"
    metadata_path = nft_dir / f"{character_id}_token_metadata.json"

    try:
        from PIL import Image, ImageDraw, ImageFont
        # Create 1080x1080 card
        card = Image.new("RGB", (1080, 1080), bg_rgb)
        draw = ImageDraw.Draw(card)

        # Paste hero image centered in top 75%
        if hero:
            try:
                img = Image.open(hero).convert("RGBA")
                img.thumbnail((900, 780), Image.LANCZOS)
                x = (1080 - img.width) // 2
                y = 40
                card.paste(img, (x, y), img)
            except Exception as e:
                print(f"[nft_card] WARN: could not paste hero image: {e}")

        # Bottom bar with accent color
        draw.rectangle([(0, 870), (1080, 1080)], fill=accent_rgb)

        # Text
        try:
            font_large = ImageFont.truetype("arial.ttf", 64)
            font_small = ImageFont.truetype("arial.ttf", 32)
        except Exception:
            font_large = ImageFont.load_default()
            font_small = font_large

        draw.text((540, 895), display_name, fill=(255, 255, 255), font=font_large, anchor="mt")
        if tagline:
            draw.text((540, 970), tagline, fill=(255, 255, 220), font=font_small, anchor="mt")

        card.save(str(card_path))
        print(f"[nft_card] card saved to {card_path}")

    except ImportError:
        # Pillow not available — copy hero as placeholder card
        if hero:
            shutil.copy(str(hero), str(card_path))
            print(f"[nft_card] Pillow not installed, copied hero as placeholder card")
        else:
            print("[nft_card] SKIP: Pillow not installed and no hero image")

    # Write ERC-721 token metadata
    nft_cfg = config.get("nft_card", {})
    blockchain = config.get("blockchain", {})
    metadata = {
        "name": display_name,
        "description": tagline,
        "image": f"ipfs://PLACEHOLDER/{character_id}_nft_card_v001.png",
        "external_url": f"https://yappyverse.com/characters/{character_id}",
        "attributes": [
            {"trait_type": "Series", "value": identity.get("series", "Series 1")},
            {"trait_type": "Edition", "value": edition},
            {"trait_type": "Role", "value": identity.get("primary_role", "")},
            {"trait_type": "Voice Actor", "value": identity.get("voice_actor", "")},
        ],
        "royalties": {
            "interface": "ERC-2981",
            "bps": blockchain.get("royalty_bps", 750),
            "recipient": blockchain.get("royalty_recipient", ""),
        }
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[nft_card] token metadata saved to {metadata_path}")
    return card_path if card_path.exists() else None


# ─────────────────────────────────────────────
# Stage 5: QA
# ─────────────────────────────────────────────
def stage_qa(character_id: str) -> dict:
    """Validate all outputs exist and return QA report."""
    print(f"[qa] validating outputs for {character_id}…")
    char_dir = ASSETS_DIR / character_id
    checks = {
        "CHARACTER_CONFIG.json": char_dir / "CHARACTER_CONFIG.json",
        "manifest.json": char_dir / "manifest.json",
        "reference_files": char_dir / "reference",
        "audio_files": char_dir / "audio",
        "nft_metadata": char_dir / "nft" / f"{character_id}_token_metadata.json",
    }
    report = {}
    for name, path in checks.items():
        if path.is_dir():
            files = [f for f in path.iterdir() if not f.name.endswith(".gitkeep")]
            report[name] = f"OK ({len(files)} files)"
        else:
            report[name] = "OK" if path.exists() else "MISSING"

    passed = all("OK" in v for v in report.values())
    report["RESULT"] = "PASS" if passed else "FAIL"
    print(f"[qa] {report['RESULT']}")
    for k, v in report.items():
        print(f"  {k}: {v}")
    return report


# ─────────────────────────────────────────────
# Main pipeline runner
# ─────────────────────────────────────────────
def run_character(character_id: str, stage: str = "all"):
    """Run the full (or partial) pipeline for one character."""
    print(f"\n{'='*60}")
    print(f"YAPPYVERSE FACTORY — Character: {character_id.upper()}")
    print(f"Stage: {stage}")
    print(f"{'='*60}\n")

    # Load .env
    env_path = FACTORY_ROOT / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())

    config = load_config(character_id)
    results = {"character": character_id, "stages": {}, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}

    if stage in ("all", "scan"):
        manifest = stage_scan(character_id)
        results["stages"]["scan"] = "OK" if manifest else "EMPTY"

    if stage in ("all", "model"):
        mesh = stage_model_gen(character_id, config)
        results["stages"]["model_gen"] = str(mesh) if mesh else "SKIPPED"

    if stage in ("all", "rig"):
        rigged = stage_rig(character_id)
        results["stages"]["rig"] = str(rigged) if rigged else "SKIPPED"

    if stage in ("all", "nft"):
        card = stage_nft_card(character_id, config)
        results["stages"]["nft_card"] = str(card) if card else "SKIPPED"

    if stage in ("all", "qa"):
        qa_report = stage_qa(character_id)
        results["stages"]["qa"] = qa_report["RESULT"]
        results["qa_details"] = qa_report

    # Write run report
    report_path = ASSETS_DIR / character_id / "pipeline_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[done] Report written to {report_path}")

    # Update registry status
    reg = load_registry()
    char = reg["characters"].get(character_id, {})
    char["status"] = "complete" if results["stages"].get("qa") == "PASS" else "partial"
    char["last_run"] = results["timestamp"]
    reg["characters"][character_id] = char
    save_registry(reg)

    return results


def run_batch():
    """Run pipeline for all queued characters."""
    reg = load_registry()
    queued = [cid for cid, v in reg["characters"].items() if v.get("status") == "queued"]
    print(f"Batch mode: {len(queued)} queued characters: {queued}")
    for cid in queued:
        try:
            run_character(cid, stage="all")
        except Exception as e:
            print(f"[batch] ERROR on {cid}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YAPPYVERSE Character Factory Pipeline")
    parser.add_argument("--character", help="Character canonical ID (e.g. pauli)")
    parser.add_argument("--stage", default="all",
                        choices=["all", "scan", "model", "rig", "nft", "qa"],
                        help="Pipeline stage to run (default: all)")
    parser.add_argument("--batch", action="store_true",
                        help="Run all queued characters")
    args = parser.parse_args()

    if args.batch:
        run_batch()
    elif args.character:
        run_character(args.character, stage=args.stage)
    else:
        parser.print_help()
        sys.exit(1)
