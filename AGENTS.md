## Agents

### Always write unit tests
When implementing any new feature, including a db schema change, endpoint, or otherwise, always write unit tests for it (/tests directory).  Unit tests should be based entirely on the inteded functionality discussed by the user, rather than based on the implementation details.  When writing the test, if a behaviours intention is not clear, ask the user for clarification, rather than making assumptions or searching the implementation for the answer.

### Always write documentation
WHen implementing any new feature, including a db schema change, endpoint, or otherwise, always update the README.  The README should be readable by humans, but also by agents when necessary to understand the context and purpose of the project.  The README should be a good balance between concise for humans to process, but detailed enough for agents to understand the context and purpose of the project.