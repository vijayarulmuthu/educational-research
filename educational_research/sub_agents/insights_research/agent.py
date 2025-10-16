# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_newresearch_agent for finding new research lines"""

from google.adk import Agent
from google.adk.tools.google_search_tool import google_search
import google.auth
from . import prompt

import os
from dotenv import load_dotenv

# looks for a .env file in the current dir or parents
load_dotenv()

MODEL = "gemini-2.5-pro"


# Define an appropriate credential type
# CREDENTIALS_TYPE = AuthCredentialTypes.OAUTH2

# Write modes define BigQuery access control of agent:
# ALLOWED: Tools will have full write capabilites.
# BLOCKED: Default mode. Effectively makes the tool read-only.
# PROTECTED: Only allows writes on temporary data for a given BigQuery session.

insights_agent = Agent(
    model=MODEL,
    name="insights_agent",
    instruction=prompt.INSIGHTS_AGENT_PROMPT,
    output_key="recent_citing_papers",
    tools=[google_search],
)
