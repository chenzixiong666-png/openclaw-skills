---
name: xmind-generator
description: Generate .xmind mind map files from structured data. Use when creating thinking maps, project overviews, learning outlines, or brainstorming visualizations. Supports nested hierarchies, multiple branches, and direct file generation.
---

# XMind Generator

Generate professional XMind mind map files (`.xmind`) from structured data. Perfect for visualizing complex ideas, project plans, learning materials, or team brainstorms.

## Quick Start

### Basic Usage

Provide your mind map data in JSON format:

```json
{
  "title": "Project Planning",
  "children": [
    {
      "title": "Phase 1: Planning",
      "children": [
        {"title": "Requirements"},
        {"title": "Design"},
        {"title": "Timeline"}
      ]
    },
    {
      "title": "Phase 2: Development",
      "children": [
        {"title": "Frontend"},
        {"title": "Backend"},
        {"title": "Testing"}
      ]
    }
  ]
}
```

The script will generate a ready-to-use `.xmind` file that you can open in XMind, MindNode, or other compatible software.

### Data Structure

Each node is a JSON object with:

- **`title`** (required, string): The node's text label
- **`children`** (optional, array): Sub-nodes (unlimited nesting depth)

Simple flat list:
```json
["Node 1", "Node 2", "Node 3"]
```

Mixed format (strings and objects):
```json
{
  "title": "Root",
  "children": [
    "Quick node",
    {"title": "Detailed node", "children": [...]}
  ]
}
```

## Workflow

1. **Prepare data** — Define your mind map structure in JSON
2. **Run generator** — Pass JSON to the script
3. **Output file** — Get a `.xmind` file
4. **Open & edit** — Use XMind or compatible tools to refine

## Examples

### Example 1: Product Launch Plan

```json
{
  "title": "Product Launch",
  "children": [
    {
      "title": "Marketing",
      "children": [
        {"title": "Social Media Campaign"},
        {"title": "Press Release"},
        {"title": "Influencer Outreach"}
      ]
    },
    {
      "title": "Operations",
      "children": [
        {"title": "Inventory Setup"},
        {"title": "Support Training"},
        {"title": "Payment Integration"}
      ]
    },
    {
      "title": "Technical",
      "children": [
        {"title": "Final QA"},
        {"title": "Performance Testing"},
        {"title": "Deployment"}
      ]
    }
  ]
}
```

### Example 2: Learning Outline

```json
{
  "title": "Machine Learning Fundamentals",
  "children": [
    {
      "title": "Supervised Learning",
      "children": [
        {"title": "Linear Regression"},
        {"title": "Classification"},
        {"title": "Neural Networks"}
      ]
    },
    {
      "title": "Unsupervised Learning",
      "children": [
        {"title": "Clustering"},
        {"title": "Dimensionality Reduction"}
      ]
    }
  ]
}
```

### Example 3: Team Structure

```json
{
  "title": "Engineering Department",
  "children": [
    {
      "title": "Frontend Team",
      "children": [
        {"title": "React Lead"},
        {"title": "UI/UX Designer"},
        {"title": "Junior Developer"}
      ]
    },
    {
      "title": "Backend Team",
      "children": [
        {"title": "Tech Lead"},
        {"title": "DevOps Engineer"},
        {"title": "Database Specialist"}
      ]
    }
  ]
}
```

## Output

The generated `.xmind` file:
- ✅ Opens in XMind, MindNode, Freemind, Freeplane
- ✅ Can be edited and saved in the native app
- ✅ Supports unlimited nesting depth
- ✅ Preserves structure and hierarchy

## Tips

1. **Large maps**: Even 1000+ nodes work fine; XMind handles complexity well
2. **Unicode support**: Chinese, emojis, special characters all work
3. **Edit after creation**: You can open the `.xmind` file and manually enhance styling, colors, icons in XMind
4. **Programmatic updates**: Regenerate with new JSON structure anytime

## Common Uses

- **Project planning** — Break down deliverables and timelines
- **Learning** — Organize course content or study materials
- **Brainstorming** — Capture ideas in a visual hierarchy
- **Documentation** — Create concept maps or system architecture overviews
- **Team planning** — Visualize org charts and responsibilities
- **Problem solving** — Map out solutions and dependencies

---

Need a mind map? Provide your data structure in JSON, and I'll generate the `.xmind` file for you! 🧠
