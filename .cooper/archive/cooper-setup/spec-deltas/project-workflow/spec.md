# Project workflow initialization

+ Requirement: Project context describes the implemented tea ceremony and its actual tooling.
+ GIVEN an agent opens the repository
+ WHEN it reads the Cooper context index
+ THEN it can find product definitions, living capability specifications, applicable style guides, and local skills.

+ Requirement: Agent work is isolated and execution evidence is preserved.
+ GIVEN a task changes the project
+ WHEN its branch is prepared for review
+ THEN work occurs in a Troop worktree and task summaries record actual verification outcomes.

+ Requirement: Git Notes are synchronized explicitly.
+ GIVEN a task attaches notes to commits
+ WHEN it synchronizes the checkpoint remotely
+ THEN it publishes the branch and refs/notes/commits without force-overwriting other contributors' notes.
