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

"""Prompt for the academic_newresearch_agent agent."""


DATA_AGENT_PROMPT = """
Synthesize Disconnected Data: Organize and interpret data across the critical dimensions listed below. Do not just list facts; provide a comparative, balanced analysis (e.g., "School A has high academic scores but a long commute, while School B is close but has a lower teacher retention rate").

Call the Bigquery Toolset to fetch the data.  Always, use this project id: qwiklabs-gcp-02-98fba4ea0b7d
"""