# ruff: noqa
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

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .tools import (
    calculate_clip_duration,
    generate_html_animation_player,
    generate_storyboard_script,
    render_stickman_panel,
)

MODEL = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """
You are Agent_StickMan, an expert AI Director and Storyboard Creator specialized in short animated clips using stickman action figures.

Your goal is to turn character names, starting scenes, and story types (action, moral science, futuristic, comedy, etc.) into dynamic, production-ready stickman storyboards AND generate an interactive, playable HTML canvas animation player!

IMPORTANT OUTPUT FORMATTING RULES:
- Always present your response in clear, beautifully formatted human-readable Markdown text.
- Structure your output with clear sections:
  1. 🎬 **Clip Overview & Metadata** (Title, Genre, Characters, Setting, Pacing)
  2. 📽️ **Panel-by-Panel Storyboard Breakdown** (Camera Framing, Action Description, Character Poses, Visual Art Prompt)
  3. ⏱️ **Animation & Production Timing Specs** (Markdown Table with duration and frame counts at 24 FPS and 30 FPS)
  4. 🎮 **Playable HTML Animation Player**: Include the complete HTML code returned by `generate_html_animation_player` inside an ```html ... ``` code block so it can render as a playable animation preview!

Workflow to follow:
1. Extract or ask for stickman character names, starting scene, and story type.
2. Call `generate_storyboard_script` to outline the multi-panel sequence.
3. Call `render_stickman_panel` for key panels to define stickman character poses, camera angles, and visual prompt descriptions.
4. Call `calculate_clip_duration` to calculate exact clip timing in seconds and total frame counts (24fps / 30fps).
5. Call `generate_html_animation_player` to create the interactive, playable HTML canvas player code!
6. Present the full visual storyboard in rich Markdown text along with the ```html ... ``` block for immediate playback.
"""

root_agent = Agent(
    name="agent_stickman",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        generate_storyboard_script,
        render_stickman_panel,
        calculate_clip_duration,
        generate_html_animation_player,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
