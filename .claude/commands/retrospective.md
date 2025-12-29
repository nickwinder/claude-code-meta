# Retrospective

Reflect on the current conversation session and capture learnings into reusable artifacts.

## Purpose

At the end of a work session, use this command to:
- Reflect on what worked well and what didn't
- Extract successful approaches and common pitfalls
- Create persistent knowledge artifacts from temporary conversation context
- Build up your project's institutional knowledge over time

## Workflow

### Step 1: Gather User Input

Ask the user: **"What should I capture from this session?"**

Listen for signals like:
- "The way we debugged X"
- "That workflow for Y"
- "The pattern we used for Z"
- "How to avoid mistake X"
- "The steps we took to accomplish Y"

### Step 2: Read Conversation History

Read the entire current conversation to understand:
- What tasks were performed
- What approaches succeeded
- What mistakes were made and corrected
- What patterns emerged
- What tools/techniques were used
- What decisions were made and why

### Step 3: Analyze and Reflect

Based on the conversation and user input, identify:

**Successful Approaches:**
- What worked well?
- What techniques proved effective?
- What problem-solving patterns emerged?

**Common Pitfalls:**
- What mistakes were made?
- What didn't work initially?
- What should be avoided?

**Reusable Patterns:**
- What steps could be abstracted?
- What knowledge would help in future sessions?
- What's worth preserving for the team/project?

**Verification Strategies:**
- How did we validate success?
- What checks or tests were important?
- How can we ensure quality?

### Step 4: Determine Artifact Type(s)

Use the AskUserQuestion tool to present options:

**Question:** "What type of artifact should I create from this reflection?"

**Options:**

1. **Skill** (Recommended for complex, multi-step workflows)
   - Description: "Create a Skill that Claude can automatically discover and use. Best for complex procedures with multiple steps, scripts, or reference materials."
   - When: The learning involves a complete workflow that Claude should autonomously apply
   - Structure: Directory with SKILL.md + supporting files
   - Example: "PDF processing workflow", "Data analysis pipeline", "Code review procedure"

2. **Slash Command** (Recommended for frequent manual tasks)
   - Description: "Create a Slash Command for explicit invocation. Best for shortcuts you want to trigger manually when needed."
   - When: The learning is a prompt template or quick action you want control over
   - Structure: Single .md file
   - Example: "/deploy instructions", "/review-checklist", "/explain-architecture"

3. **CLAUDE.md Update** (Recommended for project-wide guidelines)
   - Description: "Update the project's CLAUDE.md with new instructions or context. Best for project-specific conventions, preferences, or background knowledge."
   - When: The learning applies broadly across the entire project
   - Structure: Update to .claude/CLAUDE.md
   - Example: "Our team's coding standards", "Project architecture overview", "Deployment process"

4. **Multiple Artifacts**
   - Description: "Create multiple types (e.g., both a Skill and update CLAUDE.md). Use when the learning has multiple facets."
   - When: The learning should be captured in multiple ways

**Allow multiSelect: true** so user can choose multiple options

### Step 5: Generate Artifacts

For each selected artifact type:

#### If Creating/Updating a Skill:

**Invoke the `skill-generator` skill:**

Use the Skill tool: `skill: "skill-generator"`

Provide context from the reflection:
- Project purpose and domain
- Skill name (ask user if needed, use verb-noun format)
- Description of what the skill should do
- Expected workflow steps (from successful approaches)
- Common pitfalls identified in reflection
- Verification strategies
- Concrete examples from the conversation

The skill-generator will:
- Check if skill already exists
- Generate SKILL.md with proper YAML frontmatter
- Create supporting scripts/templates/references if needed
- Validate the skill structure
- Place files in .claude/skills/[skill-name]/

**If updating an existing skill:**
1. Check if skill exists: `ls .claude/skills/[skill-name]`
2. Ask user: "Skill '[skill-name]' already exists. Should I update it or create a new one?"
3. If updating, provide the existing skill content to skill-generator along with what should be added/changed

#### If Creating/Updating a Slash Command:

**Invoke the `command-generator` skill:**

Use the Skill tool: `skill: "command-generator"`

Provide context from the reflection:
- Conversation history (for retrospective context)
- Command purpose and workflow
- Whether arguments are needed
- Expected inputs/outputs
- Successful approaches from the session
- Common pitfalls identified
- Concrete usage examples from the conversation

The command-generator will:
- Check if command already exists
- Ask user for command name and details
- Design appropriate command structure
- Determine frontmatter requirements
- Generate command markdown with proper formatting
- Validate YAML and markdown syntax
- Place file in .claude/commands/

**If updating an existing command:**
1. Check if command exists: `ls .claude/commands/[command-name].md`
2. Ask user: "Command '/[command-name]' already exists. Should I update it or create a new one?"
3. If updating, provide existing content to command-generator with changes needed

#### If Updating CLAUDE.md:

**Invoke the `claudemd-generator` skill:**

Use the Skill tool: `skill: "claudemd-generator"`

Provide context from the reflection:
- What information should be added
- Why this is important for the project
- Where it fits in the project context
- Successful approaches from the session
- Project-specific conventions identified
- Team standards that emerged

The claudemd-generator will:
- Read existing .claude/CLAUDE.md
- Analyze current structure and length
- Determine appropriate section for new content
- Apply WHAT/WHY/HOW framework
- Recommend progressive disclosure if approaching 300 lines
- Update CLAUDE.md with proper formatting
- Validate markdown syntax
- Provide summary of changes made

### Step 6: Validate Generated Artifacts

For each artifact created:

**Skills:**
The skill-generator skill handles:
- Valid YAML frontmatter with `name` and `description` fields
- Correct markdown formatting
- Proper file paths in `.claude/skills/`

**Slash Commands:**
The command-generator skill handles:
- Valid YAML frontmatter (if present)
- Correct markdown formatting
- Proper file placement in `.claude/commands/`
- No naming conflicts with existing commands

**CLAUDE.md:**
The claudemd-generator skill handles:
- Valid markdown formatting
- No syntax errors
- Proper heading hierarchy
- Structure preservation
- Length warnings (300+ lines)

If any skill reports validation errors, review and address before proceeding.

### Step 7: Summary Report

Present a clear summary:

```markdown
## Retrospective Complete

### Artifacts Created/Updated:

[List each artifact with its location and purpose]

**Skills:**
- [skill-name]: [description] (`.claude/skills/[skill-name]/SKILL.md`)

**Slash Commands:**
- /[command-name]: [description] (`.claude/commands/[command-name].md`)

**CLAUDE.md Updates:**
- Section: [section-name]
- Changes: [summary of what was added]

### Key Learnings Captured:

**Successful Approaches:**
- [bullet points]

**Common Pitfalls:**
- [bullet points]

**Verification Strategies:**
- [bullet points]

### Next Steps:

- [For Skills] Claude will automatically discover and use this skill when relevant
- [For Slash Commands] Type `/[command-name]` to invoke
- [For CLAUDE.md] Changes will apply to all future conversations in this project

The knowledge from this session is now preserved and reusable!
```

## Best Practices

1. **Be specific in descriptions**: Skill/command descriptions should clearly indicate when to use them
2. **Capture context**: Include the "why" behind decisions, not just the "how"
3. **Use examples**: Concrete examples from the conversation make artifacts more useful
4. **Stay focused**: One skill/command should address one clear capability
5. **Validate thoroughly**: Always check YAML and markdown syntax before saving
6. **Preserve structure**: When updating existing files, maintain their organization
7. **Document pitfalls**: Mistakes are valuable learning - capture what didn't work

## Error Handling

**If directory doesn't exist:**
- Create it: `mkdir -p .claude/skills/[skill-name]` or `mkdir -p .claude/commands`

**If file already exists:**
- Ask user whether to update or create new with different name
- Never overwrite without explicit permission

**If validation fails:**
- Report specific errors clearly
- Attempt automatic fixes for common issues (YAML syntax)
- Ask user for guidance if automatic fix isn't possible

**If conversation history unavailable:**
- Ask user to describe what should be captured
- Work from user's verbal summary
- Note in artifact that it was created from summary, not full conversation

## Examples

### Example 1: Workflow Captured as Skill

**User:** `/retrospective`
**User Input:** "The way we processed those PDFs with form filling"

**Outcome:** Created skill `process-pdf-forms` with:
- SKILL.md with complete workflow
- Template form in `templates/`
- Validation script in `scripts/`

### Example 2: Quick Action as Slash Command

**User:** `/retrospective`
**User Input:** "That deployment checklist we created"

**Outcome:** Created `/deploy-check` command with:
- Pre-deployment validation steps
- Environment-specific notes
- Rollback procedures

### Example 3: Project Convention in CLAUDE.md

**User:** `/retrospective`
**User Input:** "Our team's API naming conventions"

**Outcome:** Updated CLAUDE.md:
- Added "API Conventions" section
- Documented naming patterns
- Included examples from conversation

### Example 4: Multiple Artifacts

**User:** `/retrospective`
**User Input:** "The entire code review process we developed"

**Outcome:** Created:
- Skill `code-review` (for automatic application)
- Slash command `/review` (for manual invocation)
- Updated CLAUDE.md with code quality standards

## Important Notes

- Always read the full conversation before analyzing
- Preserve the user's voice and preferences
- Focus on what's actually useful and reusable
- Don't over-engineer - keep artifacts simple and focused
- Test that artifact names don't conflict with existing ones
- Format all YAML and markdown correctly
- Provide clear, actionable summary at the end
