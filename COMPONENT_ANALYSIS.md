# A2X Marketplace Component Statistical Analysis

## Executive Summary

**Total Unique Components Found:**
- **22 Unique Agents**
- **90+ Commands** (from codescope alone)
- **66 Commands** (from cam-shift-detector)
- **4 Skills**

**Key Finding:** cam-shift-detector, revit-ai, and moderator share the **same 16-agent library**, suggesting a common "analysis & planning" framework.

---

## 📊 AGENT BREAKDOWN BY CATEGORY

### **Category 1: Code Analysis & Documentation (7 agents)**
1. `api-documenter` - API documentation generation
2. `codebase-analyzer` - Codebase structure analysis
3. `dependency-mapper` - Dependency tracking and mapping
4. `pattern-detector` - Code pattern identification
5. `test-coverage-analyzer` - Test coverage analysis
6. `tech-debt-auditor` - Technical debt identification
7. `code-walkthrough-guide` - Code walkthrough generation (2 versions)

**Use Case:** Code quality, documentation, and technical analysis

---

### **Category 2: Product & Requirements (5 agents)**
1. `requirements-analyst` - Requirements gathering and analysis
2. `epic-optimizer` - Epic planning and optimization
3. `user-researcher` - User research and insights
4. `user-journey-mapper` - User journey mapping
5. `market-researcher` - Market research and analysis

**Use Case:** Product planning, requirements engineering, user research

---

### **Category 3: Technical Planning & Review (4 agents)**
1. `technical-evaluator` - Technical decision evaluation
2. `technical-decisions-curator` - Technical decision documentation
3. `document-reviewer` - Document review and quality
4. `scope-compliance` - Scope adherence checking

**Use Case:** Technical governance and decision-making

---

### **Category 4: Data & Analysis (2 agents)**
1. `data-analyst` - Data analysis and insights
2. `trend-spotter` - Trend identification and analysis

**Use Case:** Data-driven decision making

---

### **Category 5: Specialized Workflow (4 agents)**
1. `deep-research` - Deep technical research
2. `spec-writer` - Specification writing
3. `theia-pr-walkthrough` - PR review walkthrough generation
4. `code-walkthrough-guide-improved` - Enhanced code walkthroughs

**Use Case:** Research, documentation, and PR review workflows

---

## 📋 COMMAND BREAKDOWN BY CATEGORY

### **Development Workflow (20 commands)**
- `dev.md`, `dev-story.md`
- `code-review.md`
- `create-module.md`, `edit-module.md`
- `create-workflow.md`, `edit-workflow.md`
- `create-agent.md`, `edit-agent.md`
- `workflow-init.md`, `workflow-status.md`
- `audit-workflow.md`
- `implementation-readiness.md`
- `story-context.md`, `story-ready.md`, `story-done.md`
- `convert-legacy.md`
- `correct-course.md`
- `bmad-master.md`, `bmad-builder.md`, `bmad-new-chat.md`

---

### **Documentation & Specification (15 commands)**
- `prd.md`, `create-prd.md`
- `product-brief.md`
- `tech-spec.md`, `create-tech-spec.md`
- `document-project.md`
- `index-docs.md`, `redoc.md`
- `shard-doc.md`
- `tech-writer.md`
- `module-brief.md`
- `epic-tech-context.md`
- `backlog.md`
- `create-theia-inputs.md`
- `walkthrough.md`

---

### **Design & UX (8 commands)**
- `create-ux-design.md`
- `ux-designer.md`
- `create-wireframe.md`
- `create-dataflow.md`
- `create-diagram.md`
- `create-flowchart.md`
- `create-excalidraw-*` (4 variants)

---

### **Planning & Strategy (12 commands)**
- `brainstorming.md`, `brainstorming-coach.md`
- `brainstorm-project.md`
- `design-thinking.md`, `design-thinking-coach.md`
- `innovation-strategy.md`, `innovation-strategist.md`
- `sprint-planning.md`
- `retrospective.md`
- `create-epics-and-stories.md`, `create-story.md`
- `problem-solving.md`

---

### **Research & Analysis (8 commands)**
- `research.md`
- `domain-research.md`
- `analyst.md`
- `advanced-elicitation.md`, `adv-elicit.md`
- `frame-expert.md`
- `check-implementation-readiness.md`
- `architecture.md`, `create-architecture.md`

---

### **Project Management (5 commands)**
- `pm.md` (project manager)
- `sm.md` (scrum master)
- `storyteller.md`, `storytelling.md`
- `creative-problem-solver.md`

---

### **Utilities & Misc (8 commands)**
- `architect.md`
- `sc-tidy.md`
- `party-mode.md`
- `tea.md`
- `agent-vibes.md`
- `background-music.md`
- `add.md`, `get.md`, `hide.md`
- `language.md`, `learn.md`, `effects.md`

---

## 🔍 KEY INSIGHTS

### **1. Duplication Analysis**
- **16 agents duplicated** across cam-shift-detector, revit-ai, and moderator (XPS)
- Suggests a "core analysis framework" being reused
- **Opportunity:** Create a single "analysis-toolkit" plugin instead of duplicating

### **2. Category Distribution**

| Category | Agents | Commands | Total |
|----------|--------|----------|-------|
| Code Analysis & Docs | 7 | 15 | 22 |
| Development Workflow | 0 | 20 | 20 |
| Product & Requirements | 5 | 0 | 5 |
| Planning & Strategy | 0 | 12 | 12 |
| Design & UX | 0 | 8 | 8 |
| Research & Analysis | 2 | 8 | 10 |
| Project Management | 0 | 5 | 5 |
| Technical Planning | 4 | 0 | 4 |
| Specialized Workflow | 4 | 3 | 7 |
| Utilities | 0 | 8 | 8 |

**Strongest Areas:**
1. **Development Workflow** (20 commands)
2. **Code Analysis** (22 components)
3. **Planning & Strategy** (12 commands)

**Gaps:**
- No agents for project management (only commands)
- Limited data analysis agents (only 2)
- No CI/CD or DevOps-specific agents

### **3. Naming Patterns**

**Prefixes Found:**
- `bmad-*` (4 commands) - Custom workflow system
- `create-*` (13 commands) - Creation workflows
- `edit-*` (3 commands) - Editing workflows
- `story-*` (3 commands) - Agile story management

**Agent Suffixes:**
- `-analyzer` (3 agents)
- `-mapper` (2 agents)
- `-optimizer` (1 agent)
- `-auditor` (1 agent)

---

## 💡 RECOMMENDED PLUGIN STRUCTURE

Based on statistical analysis:

### **Option 1: By Function (Recommended)**

```
plugins/
├── code-analysis-toolkit/        # 7 agents + 15 commands
├── development-workflow/          # 20 commands
├── product-planning-toolkit/      # 5 agents + 12 commands
├── design-ux-toolkit/             # 8 commands
├── research-analysis-toolkit/     # 2 agents + 8 commands
└── project-management-toolkit/    # 5 commands
```

### **Option 2: By Role**

```
plugins/
├── developer-toolkit/      # Code analysis agents + dev commands
├── product-manager-toolkit/  # Requirements agents + PM commands
├── architect-toolkit/      # Technical planning + architecture
└── researcher-toolkit/     # Research agents + analysis commands
```

### **Option 3: Consolidate Duplicates**

```
plugins/
├── core-analysis-framework/  # The 16 shared agents (consolidate duplicates)
├── maya-toolkit/            # Already created!
├── workflow-automation/     # All bmad-* and workflow commands
└── utilities/               # Misc tools
```

---

## 📈 STATISTICS SUMMARY

- **Total Locations Scanned:** 6 (local repos, XPS, Google Drive)
- **Repositories with .claude:** 20+
- **Unique Agents:** 22
- **Unique Commands:** 90+ (codescope) + 66 (cam-shift) = 150+
- **Duplication Rate:** 73% (16/22 agents appear in multiple repos)
- **Category Coverage:** 10 distinct categories

**Storage Distribution:**
- Local ~/personal/repos: 15 repos with .claude
- XPS ~/personal: 4 repos with .claude
- ~/.claude: 6 agents, 3 commands, 1 skill
- Google Drive: 20+ agents in archives

---

## 🎯 NEXT STEPS RECOMMENDATION

1. **De-duplicate first:** Create `core-analysis-framework` plugin with the 16 shared agents
2. **Keep maya-toolkit** as-is (already well-structured)
3. **Create category-based plugins** for the remaining unique components
4. **Archive** Google Drive agents separately (reference library)

This approach gives you:
- ✅ No duplication
- ✅ Clear separation of concerns
- ✅ Easy to maintain
- ✅ Discoverable by function
