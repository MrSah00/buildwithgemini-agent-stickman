# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for Agent_StickMan - Stickman Storyboard Creator Agent."""

import json
import os
from typing import Any, Dict, List


def generate_storyboard_script(
    characters: List[str],
    starting_scene: str,
    story_type: str,
    num_panels: int = 4,
) -> Dict[str, Any]:
    """Generate a structured multi-panel storyboard script outline.

    Args:
        characters: Names of the stickman characters (e.g. ['Stick-Bob', 'Ninja-Dot']).
        starting_scene: Description of the opening scene/environment.
        story_type: Genre of the clip (e.g. 'action', 'moral science', 'futuristic', 'comedy').
        num_panels: Number of storyboard panels to generate (default 4).

    Returns:
        A dictionary containing the clip metadata, character list, and panel breakdown.
    """
    characters_str = ", ".join(characters)
    panels = []

    for i in range(1, num_panels + 1):
        if i == 1:
            title = f"Panel 1: Establishing Shot — {starting_scene[:30]}..."
            desc = f"Introduction of {characters_str} in {starting_scene}. Poses are established."
            camera = "Wide Shot"
        elif i == num_panels:
            title = f"Panel {i}: Climax / Resolution"
            desc = f"Final action climax for {characters_str}. Lesson or conclusion of the {story_type} narrative."
            camera = "Dynamic Low-Angle Shot"
        else:
            title = f"Panel {i}: Escalation & Action"
            desc = f"Conflict builds between {characters_str}. Dynamic motion and stickman martial/action poses."
            camera = "Medium Close-Up Shot"

        panels.append({
            "panel_number": i,
            "scene_title": title,
            "camera_framing": camera,
            "action_description": desc,
            "recommended_pacing_sec": 3.5,
        })

    return {
        "status": "success",
        "clip_title": f"{story_type.capitalize()} Clip featuring {characters_str}",
        "story_type": story_type,
        "starting_scene": starting_scene,
        "characters": characters,
        "total_panels": num_panels,
        "script_outline": panels,
    }


def render_stickman_panel(
    panel_number: int,
    scene_title: str,
    action_description: str,
    stickman_poses: List[Dict[str, str]],
    visual_prompt: str,
) -> Dict[str, Any]:
    """Prepare keyframe panel concepts and visual stickman art prompts.

    Args:
        panel_number: Sequence number of the panel (1-indexed).
        scene_title: Short title for the scene panel.
        action_description: Description of the action occurring in the frame.
        stickman_poses: List of character poses e.g. [{'character': 'Stick-Bob', 'pose': 'high kick'}, {'character': 'Ninja-Dot', 'pose': 'backflip dodge'}].
        visual_prompt: Detailed prompt for stickman image generation.

    Returns:
        A dictionary with rendered panel keyframe specs.
    """
    return {
        "status": "rendered",
        "panel_number": panel_number,
        "scene_title": scene_title,
        "action_description": action_description,
        "stickman_poses": stickman_poses,
        "visual_prompt": visual_prompt,
        "render_style": "2D Minimalist Stickman Action Vector Art, High Contrast, Dynamic Speed Lines",
    }


def calculate_clip_duration(num_panels: int, pacing: str = "normal") -> Dict[str, Any]:
    """Calculate clip duration in seconds, frame count, and timing pacing.

    Args:
        num_panels: Total number of storyboard panels.
        pacing: Action pacing - 'slow' (5s/panel), 'normal' (3.5s/panel), 'fast' (2s/panel).

    Returns:
        A dictionary with timing details and FPS calculation.
    """
    pacing_map = {
        "slow": 5.0,
        "normal": 3.5,
        "fast": 2.0,
    }
    sec_per_panel = pacing_map.get(pacing.lower(), 3.5)
    total_seconds = num_panels * sec_per_panel
    frames_24fps = int(total_seconds * 24)
    frames_30fps = int(total_seconds * 30)

    return {
        "num_panels": num_panels,
        "pacing": pacing,
        "sec_per_panel": sec_per_panel,
        "total_duration_seconds": total_seconds,
        "total_frames_24fps": frames_24fps,
        "total_frames_30fps": frames_30fps,
    }


def generate_html_animation_player(
    clip_title: str,
    characters: List[str],
    story_type: str,
    panels_data: List[Dict[str, Any]],
    output_filename: str = "stickman_storyboard.html",
) -> Dict[str, Any]:
    """Generate a self-contained HTML/JS Canvas interactive animation player for the stickman clip.

    Args:
        clip_title: Title of the animation clip.
        characters: List of character names.
        story_type: Genre or theme.
        panels_data: List of panel details with scene_title, action_description, and poses.
        output_filename: Filename for the saved HTML storyboard file.

    Returns:
        A dictionary containing the complete HTML animation player string and saved path.
    """
    char1 = characters[0] if len(characters) > 0 else "Stick-Bob"
    char2 = characters[1] if len(characters) > 1 else "Stick-Tim"
    panels_json = json.dumps(panels_data)

    html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{clip_title}</title>
<style>
  body {{ margin:0; padding:15px; font-family: 'Segoe UI', Tahoma, sans-serif; background:#0f172a; color:#f8fafc; text-align:center; }}
  .player-card {{ background:#1e293b; border-radius:12px; padding:20px; max-width:680px; margin:0 auto; box-shadow:0 10px 25px rgba(0,0,0,0.5); border:1px solid #334155; }}
  h2 {{ margin:0 0 5px 0; color:#38bdf8; font-size:1.4rem; }}
  .meta {{ font-size:0.85rem; color:#94a3b8; margin-bottom:15px; }}
  canvas {{ background:#090d16; border-radius:8px; border:2px solid #3b82f6; width:100%; height:auto; display:block; margin:0 auto; }}
  .controls {{ display:flex; gap:10px; justify-content:center; align-items:center; margin-top:15px; flex-wrap:wrap; }}
  button {{ background:#2563eb; color:#fff; border:none; padding:8px 16px; border-radius:6px; font-weight:600; cursor:pointer; font-size:0.9rem; transition:background 0.2s; }}
  button:hover {{ background:#1d4ed8; }}
  .scene-info {{ background:#0f172a; border-radius:6px; padding:10px; margin-top:15px; font-size:0.9rem; color:#cbd5e1; min-height:45px; border-left:4px solid #38bdf8; text-align:left; }}
  .badge {{ background:#0284c7; padding:2px 8px; border-radius:4px; font-size:0.75rem; font-weight:bold; color:#fff; margin-right:6px; }}
</style>
</head>
<body>
<div class="player-card">
  <h2>🎬 {clip_title}</h2>
  <div class="meta"><span class="badge">{story_type.upper()}</span> Cast: {char1} vs {char2}</div>
  <canvas id="stage" width="600" height="320"></canvas>
  <div class="controls">
    <button id="btnPlay" onclick="togglePlay()">▶ Play</button>
    <button id="btnReset" onclick="resetAnim()">🔄 Restart</button>
    <button onclick="prevScene()">⏮ Prev Scene</button>
    <button onclick="nextScene()">⏭ Next Scene</button>
  </div>
  <div class="scene-info" id="sceneInfo">Loading scene...</div>
</div>

<script>
const canvas = document.getElementById('stage');
const ctx = canvas.getContext('2d');
const panels = {panels_json};

let currentScene = 0;
let isPlaying = true;
let animFrame = 0;
let t = 0;

function drawStickman(x, y, scale, headColor, bodyColor, pose, label) {{
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);

  // Label
  ctx.fillStyle = "#94a3b8";
  ctx.font = "bold 13px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(label, 0, -55);

  ctx.lineWidth = 4;
  ctx.strokeStyle = bodyColor;
  ctx.lineCap = "round";

  // Head
  ctx.beginPath();
  ctx.arc(0, -35, 12, 0, Math.PI * 2);
  ctx.fillStyle = headColor;
  ctx.fill();
  ctx.stroke();

  // Body
  ctx.beginPath();
  ctx.moveTo(0, -23);
  ctx.lineTo(0, 10);
  ctx.stroke();

  const cycle = Math.sin(t * 0.15);

  if (pose === "kick") {{
    // Arms
    ctx.beginPath();
    ctx.moveTo(0, -18); ctx.lineTo(-18, -30);
    ctx.moveTo(0, -18); ctx.lineTo(18, -10);
    ctx.stroke();
    // Legs: High kick
    ctx.beginPath();
    ctx.moveTo(0, 10); ctx.lineTo(-12, 35);
    ctx.moveTo(0, 10); ctx.lineTo(30, -15);
    ctx.stroke();
  }} else if (pose === "slash") {{
    // Arms swinging weapon / slash
    ctx.beginPath();
    ctx.moveTo(0, -18); ctx.lineTo(25, -25);
    ctx.moveTo(0, -18); ctx.lineTo(15, 0);
    ctx.stroke();
    // Glowing weapon arc
    ctx.strokeStyle = headColor;
    ctx.lineWidth = 5;
    ctx.beginPath(); ctx.moveTo(25, -25); ctx.lineTo(45, -35); ctx.stroke();
    ctx.lineWidth = 4;
    ctx.strokeStyle = bodyColor;
    // Legs
    ctx.beginPath();
    ctx.moveTo(0, 10); ctx.lineTo(-18, 35);
    ctx.moveTo(0, 10); ctx.lineTo(18, 35);
    ctx.stroke();
  }} else if (pose === "walk" || pose === "run") {{
    // Walking/Running motion
    ctx.beginPath();
    ctx.moveTo(0, -18); ctx.lineTo(-15 * cycle, 0);
    ctx.moveTo(0, -18); ctx.lineTo(15 * cycle, 0);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, 10); ctx.lineTo(18 * cycle, 35);
    ctx.moveTo(0, 10); ctx.lineTo(-18 * cycle, 35);
    ctx.stroke();
  }} else if (pose === "victory") {{
    // Both arms in air
    ctx.beginPath();
    ctx.moveTo(0, -18); ctx.lineTo(-20, -45);
    ctx.moveTo(0, -18); ctx.lineTo(20, -45);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, 10); ctx.lineTo(-12, 35);
    ctx.moveTo(0, 10); ctx.lineTo(12, 35);
    ctx.stroke();
  }} else {{ // Idle / Guard
    ctx.beginPath();
    ctx.moveTo(0, -18); ctx.lineTo(-14, 0);
    ctx.moveTo(0, -18); ctx.lineTo(14, 0);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, 10); ctx.lineTo(-12, 35);
    ctx.moveTo(0, 10); ctx.lineTo(12, 35);
    ctx.stroke();
  }}

  ctx.restore();
}}

function render() {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Background Environment
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(0, 260, canvas.width, 60); // Floor
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 2;
  for(let x=0; x<canvas.width; x+=40) {{
    ctx.beginPath(); ctx.moveTo(x, 260); ctx.lineTo(x, 320); ctx.stroke();
  }}

  const scene = panels[currentScene] || {{ scene_title: "Panel " + (currentScene+1), action_description: "Stickman scene action" }};
  document.getElementById('sceneInfo').innerHTML = "<strong>" + (scene.scene_title || "Scene " + (currentScene+1)) + "</strong><br>" + (scene.action_description || "");

  const slide = Math.sin(t * 0.05) * 30;
  const bounce = Math.abs(Math.sin(t * 0.12)) * 25;

  // Alternate dynamic positions for any panel number (Panel 1, 2, 3, 4, 5, 6...)
  const panelMode = currentScene % 4;

  if (panelMode === 0) {{
    drawStickman(160 + slide, 230, 1.2, "#38bdf8", "#ffffff", "walk", "{char1}");
    drawStickman(420 - slide, 230, 1.2, "#f43f5e", "#ffffff", "idle", "{char2}");
  }} else if (panelMode === 1) {{
    drawStickman(230, 230 - bounce, 1.2, "#38bdf8", "#38bdf8", "kick", "{char1}");
    drawStickman(370, 230, 1.2, "#f43f5e", "#ffffff", "slash", "{char2}");
  }} else if (panelMode === 2) {{
    drawStickman(220 + slide, 230, 1.2, "#38bdf8", "#ffffff", "slash", "{char1}");
    drawStickman(380 - slide, 230 - bounce, 1.2, "#f43f5e", "#f43f5e", "kick", "{char2}");
  }} else {{
    drawStickman(230, 230, 1.2, "#38bdf8", "#ffffff", "victory", "{char1}");
    drawStickman(370, 230, 1.2, "#f43f5e", "#ffffff", "idle", "{char2}");
  }}

  if (isPlaying) {{
    t++;
    if (t % 120 === 0) {{
      currentScene = (currentScene + 1) % panels.length;
    }}
    animFrame = requestAnimationFrame(render);
  }}
}}

function togglePlay() {{
  isPlaying = !isPlaying;
  document.getElementById('btnPlay').textContent = isPlaying ? "⏸ Pause" : "▶ Play";
  if (isPlaying) render();
}}

function resetAnim() {{
  currentScene = 0;
  t = 0;
  if (!isPlaying) togglePlay();
}}

function prevScene() {{
  currentScene = (currentScene - 1 + panels.length) % panels.length;
  t = 0;
  if (!isPlaying) render();
}}

function nextScene() {{
  currentScene = (currentScene + 1) % panels.length;
  t = 0;
  if (!isPlaying) render();
}}

render();
</script>
</body>
</html>"""

    # Save to disk locally if directory exists
    target_path = output_filename
    try:
        base_dir = os.path.dirname(__file__)
        static_dir = os.path.join(base_dir, "..", "frontend", "static")
        if os.path.exists(static_dir):
            target_path = os.path.join(static_dir, output_filename)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(html_code)
    except Exception:
        pass

    return {
        "status": "generated",
        "clip_title": clip_title,
        "filename": output_filename,
        "html_code": html_code,
    }
