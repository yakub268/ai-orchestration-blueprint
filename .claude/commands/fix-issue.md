Analyze and fix GitHub issue: $ARGUMENTS

Follow the "Explore, Plan, Code, Commit" workflow:

## Phase 1: Explore
1. Fetch issue details using `gh issue view $ARGUMENTS`
2. Read issue comments and linked PRs
3. Search codebase for files mentioned in the issue
4. Identify all affected components

## Phase 2: Plan
Think hard about the solution approach:
- What is the root cause?
- What files need modification?
- Are there edge cases to consider?
- What tests should be added/modified?

Create a detailed implementation plan before writing code.

## Phase 3: Code
Implement the fix following these guidelines:
- Make minimal, focused changes
- Follow existing code style (check .eslintrc.js, .prettierrc)
- Add/update tests for the changes
- Update documentation if needed

## Phase 4: Commit
1. Run tests to verify the fix
2. Create a descriptive commit message following conventional commits:
   ```
   fix: <short description>
   
   Fixes #$ARGUMENTS
   
   - Bullet points explaining changes
   ```
3. Create PR with clear description linking to the issue
