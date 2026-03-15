"""
YAPPYVERSE Auto-Rig Script for Blender 5.0+
============================================
Headless Blender script that:
  1. Imports a mesh (.obj / .fbx / .glb)
  2. Auto-rigs with Rigify
  3. Adds custom spring bones (hat jiggle, chain dangle, cigar hold)
  4. Bakes idle bobbing animation
  5. Bakes finger-wag reaction animation
  6. Exports Draco-compressed .glb

Usage:
  blender --background --python auto_rig.py -- \
      --input mesh.obj \
      --config CHARACTER_CONFIG.json \
      --output pauli_rigged.glb

Requires: Blender 5.0+ with Rigify addon enabled
"""

import argparse
import json
import math
import os
import sys

# ---------------------------------------------------------------------------
# Blender imports (only available when run inside Blender)
# ---------------------------------------------------------------------------
try:
    import bpy
    import mathutils
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False
    print("ERROR: This script must be run inside Blender.")
    print("Usage: blender --background --python auto_rig.py -- --input mesh.obj --output out.glb")
    sys.exit(1)


def parse_args():
    """Parse CLI args passed after '--' in Blender command line."""
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    parser = argparse.ArgumentParser(description="YAPPYVERSE Auto-Rig")
    parser.add_argument("--input", required=True, help="Path to input mesh (.obj/.fbx/.glb)")
    parser.add_argument("--config", default=None, help="Path to CHARACTER_CONFIG.json")
    parser.add_argument("--output", required=True, help="Output .glb path")
    parser.add_argument("--skip-animation", action="store_true", help="Skip animation baking")
    parser.add_argument("--poly-limit", type=int, default=50000, help="Max polygon count (decimate if exceeded)")
    return parser.parse_args(argv)


def clear_scene():
    """Remove all objects from the default scene."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)


def import_mesh(filepath):
    """Import mesh file, auto-detecting format."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".obj":
        bpy.ops.wm.obj_import(filepath=filepath)
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=filepath)
    elif ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=filepath)
    else:
        raise ValueError(f"Unsupported mesh format: {ext}")

    # Find the imported mesh object
    mesh_obj = None
    for obj in bpy.context.selected_objects:
        if obj.type == "MESH":
            mesh_obj = obj
            break

    if mesh_obj is None:
        for obj in bpy.data.objects:
            if obj.type == "MESH":
                mesh_obj = obj
                break

    if mesh_obj is None:
        raise RuntimeError("No mesh object found after import")

    return mesh_obj


def decimate_if_needed(mesh_obj, poly_limit):
    """Add decimate modifier if polygon count exceeds limit."""
    poly_count = len(mesh_obj.data.polygons)
    if poly_count > poly_limit:
        ratio = poly_limit / poly_count
        mod = mesh_obj.modifiers.new(name="Decimate", type="DECIMATE")
        mod.ratio = ratio
        bpy.context.view_layer.objects.active = mesh_obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
        print(f"Decimated from {poly_count} to {len(mesh_obj.data.polygons)} polygons")
    else:
        print(f"Polygon count OK: {poly_count}")


def center_and_scale(mesh_obj):
    """Center mesh at origin, scale to ~2m height for Rigify compatibility."""
    bpy.context.view_layer.objects.active = mesh_obj
    mesh_obj.select_set(True)

    # Apply transforms
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Get bounding box
    bbox = [mesh_obj.matrix_world @ mathutils.Vector(corner) for corner in mesh_obj.bound_box]
    min_z = min(v.z for v in bbox)
    max_z = max(v.z for v in bbox)
    height = max_z - min_z

    # Center on XY, put feet at Z=0
    center_x = sum(v.x for v in bbox) / 8
    center_y = sum(v.y for v in bbox) / 8
    mesh_obj.location.x -= center_x
    mesh_obj.location.y -= center_y
    mesh_obj.location.z -= min_z

    # Scale to ~2m height if way off
    if height > 0:
        target_height = 2.0
        if height < 0.1 or height > 10:
            scale_factor = target_height / height
            mesh_obj.scale = (scale_factor, scale_factor, scale_factor)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            print(f"Scaled mesh from {height:.3f} to {target_height} units")

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def enable_rigify():
    """Enable the Rigify addon if not already enabled."""
    if "rigify" not in bpy.context.preferences.addons:
        bpy.ops.preferences.addon_enable(module="rigify")
    print("Rigify addon enabled")


def create_rigify_rig(mesh_obj):
    """Add Rigify metarig, fit to mesh, generate rig, and parent mesh."""
    # Add human metarig
    bpy.ops.object.armature_human_metarig_add()
    metarig = bpy.context.active_object
    metarig.name = "metarig"

    # Scale metarig to match mesh height
    bbox = [mesh_obj.matrix_world @ mathutils.Vector(corner) for corner in mesh_obj.bound_box]
    mesh_height = max(v.z for v in bbox) - min(v.z for v in bbox)
    metarig_bbox = [metarig.matrix_world @ mathutils.Vector(corner) for corner in metarig.bound_box]
    meta_height = max(v.z for v in metarig_bbox) - min(v.z for v in metarig_bbox)

    if meta_height > 0 and mesh_height > 0:
        scale_factor = mesh_height / meta_height
        metarig.scale = (scale_factor, scale_factor, scale_factor)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Generate Rigify rig
    bpy.context.view_layer.objects.active = metarig
    metarig.select_set(True)
    bpy.ops.pose.rigify_generate()

    # Find the generated rig
    rig = None
    for obj in bpy.data.objects:
        if obj.type == "ARMATURE" and obj.name.startswith("rig"):
            rig = obj
            break

    if rig is None:
        print("WARNING: Rigify generation may have failed, using metarig as fallback")
        rig = metarig

    # Parent mesh to rig with automatic weights
    mesh_obj.select_set(True)
    rig.select_set(True)
    bpy.context.view_layer.objects.active = rig
    try:
        bpy.ops.object.parent_set(type="ARMATURE_AUTO")
        print("Mesh parented to rig with automatic weights")
    except RuntimeError as e:
        print(f"WARNING: Auto-weights failed ({e}), using envelope weights")
        bpy.ops.object.parent_set(type="ARMATURE_ENVELOPE")

    return rig


def add_custom_bones(rig, config):
    """Add custom spring/helper bones from CHARACTER_CONFIG."""
    if config is None or "rig" not in config:
        return

    custom_bones = config.get("rig", {}).get("custom_bones", [])
    if not custom_bones:
        return

    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")

    for bone_def in custom_bones:
        bone_name = bone_def["name"]
        parent_name = bone_def.get("parent", "spine.003")

        # Find parent bone
        parent_bone = rig.data.edit_bones.get(parent_name)
        if parent_bone is None:
            # Try common Rigify names
            for prefix in ["DEF-", "ORG-", ""]:
                parent_bone = rig.data.edit_bones.get(prefix + parent_name)
                if parent_bone:
                    break

        if parent_bone is None:
            print(f"WARNING: Parent bone '{parent_name}' not found for '{bone_name}', skipping")
            continue

        # Create new bone
        new_bone = rig.data.edit_bones.new(bone_name)
        new_bone.head = parent_bone.tail
        new_bone.tail = parent_bone.tail + mathutils.Vector((0, 0, 0.1))
        new_bone.parent = parent_bone
        print(f"Added custom bone: {bone_name} -> {parent_bone.name}")

    bpy.ops.object.mode_set(mode="OBJECT")


def bake_idle_animation(rig, config):
    """Create a simple idle bobbing animation."""
    anim_config = config.get("animations", {}).get("idle", {}) if config else {}
    frames = anim_config.get("frames", 120)
    fps = anim_config.get("fps", 30)

    bpy.context.scene.render.fps = fps
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frames

    # Create action
    action = bpy.data.actions.new(name=anim_config.get("name", "idle_bobbing"))
    if rig.animation_data is None:
        rig.animation_data_create()
    rig.animation_data.action = action

    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="POSE")

    # Find the root/hips bone
    hips_bone = None
    for name in ["torso", "hips", "root", "spine", "DEF-spine"]:
        if name in rig.pose.bones:
            hips_bone = rig.pose.bones[name]
            break

    if hips_bone is None and len(rig.pose.bones) > 0:
        hips_bone = rig.pose.bones[0]

    if hips_bone:
        # Keyframe subtle up-down bobbing
        for frame in range(1, frames + 1):
            bpy.context.scene.frame_set(frame)
            # Sine wave: subtle Z translation bobbing
            phase = (frame / frames) * math.pi * 2
            bob_amount = math.sin(phase) * 0.02  # 2cm bob
            hips_bone.location.z = bob_amount
            hips_bone.keyframe_insert(data_path="location", frame=frame)

        print(f"Idle animation baked: {frames} frames at {fps} fps")
    else:
        print("WARNING: No suitable bone found for idle animation")

    bpy.ops.object.mode_set(mode="OBJECT")

    # Push to NLA
    if rig.animation_data and rig.animation_data.action:
        track = rig.animation_data.nla_tracks.new()
        track.name = "idle"
        track.strips.new(action.name, 1, action)
        rig.animation_data.action = None


def bake_reaction_animation(rig, config):
    """Create a finger-wag reaction animation."""
    anim_config = config.get("animations", {}).get("reaction", {}) if config else {}
    frames = anim_config.get("frames", 60)
    fps = anim_config.get("fps", 30)

    action = bpy.data.actions.new(name=anim_config.get("name", "finger_wag"))
    rig.animation_data.action = action

    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="POSE")

    # Find right hand/finger bone for wag
    wag_bone = None
    for name in ["hand_ik.R", "hand.R", "DEF-hand.R", "f_index.01.R"]:
        if name in rig.pose.bones:
            wag_bone = rig.pose.bones[name]
            break

    if wag_bone:
        for frame in range(1, frames + 1):
            bpy.context.scene.frame_set(frame)
            # Wag: oscillating rotation on Z axis
            if frame <= 10:
                # Raise hand
                wag_bone.rotation_euler.x = -0.3 * (frame / 10)
            elif frame <= 50:
                # Wag back and forth
                phase = ((frame - 10) / 10) * math.pi * 2
                wag_bone.rotation_euler.z = math.sin(phase) * 0.15
            else:
                # Return to rest
                t = (frame - 50) / 10
                wag_bone.rotation_euler.x = -0.3 * (1 - t)
                wag_bone.rotation_euler.z = 0

            wag_bone.keyframe_insert(data_path="rotation_euler", frame=frame)

        print(f"Reaction animation baked: {frames} frames at {fps} fps")
    else:
        print("WARNING: No suitable bone found for finger-wag animation")

    bpy.ops.object.mode_set(mode="OBJECT")

    # Push to NLA
    if rig.animation_data and rig.animation_data.action:
        track = rig.animation_data.nla_tracks.new()
        track.name = "reaction"
        track.strips.new(action.name, 1, action)
        rig.animation_data.action = None


def setup_scene_lighting(config):
    """Set up basic scene lighting based on character palette."""
    palette = config.get("palette", {}) if config else {}

    # Add key light
    bpy.ops.object.light_add(type="AREA", location=(3, -3, 5))
    key_light = bpy.context.active_object
    key_light.name = "KeyLight"
    key_light.data.energy = 500

    # Add fill light
    bpy.ops.object.light_add(type="AREA", location=(-3, -2, 3))
    fill_light = bpy.context.active_object
    fill_light.name = "FillLight"
    fill_light.data.energy = 200

    # Set world background color from palette
    bg = palette.get("background", {"r": 20, "g": 15, "b": 30})
    world = bpy.data.worlds.get("World")
    if world is None:
        world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = (bg["r"] / 255, bg["g"] / 255, bg["b"] / 255, 1.0)

    print("Scene lighting configured")


def export_glb(filepath):
    """Export scene as Draco-compressed .glb."""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format="GLB",
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_animations=True,
        export_nla_strips=True,
        export_apply=False,
    )
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"Exported: {filepath} ({size_mb:.2f} MB)")


def main():
    args = parse_args()

    # Load config if provided
    config = None
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"Loaded config: {args.config}")

    print(f"Input mesh: {args.input}")
    print(f"Output: {args.output}")

    # 1. Clear and import
    clear_scene()
    mesh_obj = import_mesh(args.input)
    print(f"Imported mesh: {mesh_obj.name}")

    # 2. Prepare mesh
    decimate_if_needed(mesh_obj, args.poly_limit)
    center_and_scale(mesh_obj)

    # 3. Rig
    enable_rigify()
    rig = create_rigify_rig(mesh_obj)
    add_custom_bones(rig, config)

    # 4. Animate
    if not args.skip_animation:
        bake_idle_animation(rig, config)
        bake_reaction_animation(rig, config)

    # 5. Scene setup
    setup_scene_lighting(config)

    # 6. Save .blend alongside output
    blend_path = os.path.splitext(args.output)[0] + ".blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved .blend: {blend_path}")

    # 7. Export .glb
    export_glb(args.output)

    print("=== AUTO-RIG COMPLETE ===")


if __name__ == "__main__":
    main()
