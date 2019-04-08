---
layout: default
title: My Favorite Text Diagram Tools
---

I love that diagrams can make difficult concepts intuitive. I hate that
generally they're stored in opaque binary formats, which make them difficult to
version control, and that generally they're created by clicking and dragging
buttons and boxes around. Typing is generally much faster and less frustrating.


With that in in mind, here are some of my favorite diagram-to-text tools:

## [Quick Database Diagrams](https://www.quickdatabasediagrams.com/)

[Quick Database Diagrams](https://www.quickdatabasediagrams.com/) lets you
quickly prototype schemas for SQL databases. It's really helped me out at times.

![]({{ site.baseurl }}/img/2018-08-20-My-Favorite-Text-Diagram-Tools/quickdbd.png)

## [PlantUML](http://plantuml.com/)

PlantUML is a textual description to diagram generator that features several
types of diagrams. My favorites right now are the state diagram and the sequence
diagram (both images here sourced from plantuml.com).

![]({{ site.baseurl }}/img/2018-08-20-My-Favorite-Text-Diagram-Tools/plantuml-state.png)

![]({{ site.baseurl }}/img/2018-08-20-My-Favorite-Text-Diagram-Tools/sequence-diagram-dnaouh43.png)

### Using PlantUML with Visual Studio Code

There is a really nice [plugin](https://github.com/qjebbs/vscode-plantuml) for
PlantUML for VSCode. Install it with:

```
ext install plantuml
```

Use it by creating a `.wsd` file to get syntax highlighting and
(not so great, but stil useful) auto-completion.

See the commands it provides with `Cmd+P`, then typing `> PlantUML`. One very
useful command I've found is `PlantUML: Preview Current Diagram`. Just keep in
mind that it can take a few seconds to turn a change into a live preview.

### Exporting PlantUML diagrams to Confluence

This method even preserves clickable links

1. Export to SVG: `plantuml -tsvg <name>`.
2. Paste text into *HTML* macro in Confluence.

## graphviz

[graphviz](https://www.graphviz.org/) and its associated layout tools dot and
neato are tools to generate graph images from text input files. So I don't
really use them like I use the previous tools, but I figure they're worth a
mention.
