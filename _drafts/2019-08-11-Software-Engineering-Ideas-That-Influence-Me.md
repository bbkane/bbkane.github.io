---
layout: default
title: Software Engineering Ideas That Influence Me
---

I watch a lot of conference talks on YouTube and I read a lot of software
engineering articles. Some of that media has really helped me become a better
engineer. As a relative newcomer to engineering, I know my style will develop further and
my current judgment of "best practice" will change (and I can see how it's
changed historically by looking at my old code), but I plan to read/watch these
resources every year. I look forward to future me gaining new perspective on
them.

## Resources

### Casey Muratori

Casey Muratori is a game tools programmer who has a lot of ideas I really like.
In particular, he advocates eschewing object oriented programming for
imperative code with plain old data types.

- [Semantic Compression](https://caseymuratori.com/blog_0015): This post (and
  the rest of the series) have really helped me to grasp the "semantic
  compression" concept Casey uses here. I can actually trace its influence on
  my thought process through my historical code.
- [Designing and Evaluating Reusable Components (2004)](https://caseymuratori.com/blog_0024): This talk is about what makes
  an API great. One particualr thing that stands out to me is how an API needs
  to cater to beginner users with simple functions yet also cater to more
  experienced users by offering more complicated knobs to twiddle.
- [The Worst API Ever Made](https://caseymuratori.com/blog_0025): This is a
  rather hilarious post that really emphasizes how, when architecting a
  program, you should write the usage code first, so your users don't hate their experience with your API.

### Other

- [Advanced Testing in Go (Hashimoto)](https://www.youtube.com/watch?v=8hQG7QlcLBk) ([transcript](https://about.sourcegraph.com/go/advanced-testing-in-go)):
  In this talk, Michael Hashimoto splits his time between talking about
  creating tests creating testable code. Very useful and pragmatic.
- [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) and [Boundaries](https://www.destroyallsoftware.com/talks/boundaries):
  Gary Bernhart has a bunch of great videos on his
  [website](https://www.destroyallsoftware.com/screencasts). These two talks
  build off one another and talk about how you should make as much of your code
  as possible pure functions. This makes testing and extending it much easier.
- [CppCon 2014: Mike Acton "Data-Oriented Design and C++"](https://www.youtube.com/watch?v=rX0ItVEVjHc):
  This is another hugely influential talk. Mike Acton has a lot of
  efficiency-oriented ideas for designing code performantly.
- [Hammock Driven Development: Rich Hickey](https://www.youtube.com/watch?v=f84n5oFoZBc):
  Lectures like this are hard to come by. Rich Hickey gives wonderful tips on
  how to solve hard problems. The main one is that it can take a lot of time
  and conscious/unconscious thought to get an elegant solution.
- [Types as Sets](https://guide.elm-lang.org/appendix/types_as_sets.html):
  Types as Sets (unfortunately relegated to an appendix) really helped me
  understand how you can use types to force your data structures to be correct-
  to "make invalid states unrepresentable". Also see
  [this Handmade Hero QA](https://guide.handmadehero.org/code/day376/#8204)
  for a great overlapping explanation of discriminated unions in C/C++ and perhaps
  [What the Heck are Algebraic Data Types? ( for Programmers )](http://merrigrove.blogspot.com/2011/12/another-introduction-to-algebraic-data.html).
  If you're intrigued and want to really explore the math behind this, check out
  [The algebra (and calculus!) of algebraic data types](https://codewords.recurse.com/issues/three/algebra-and-calculus-of-algebraic-data-types)
  for an interesting exploration.
- [John Carmack on Inlined Code](http://number-none.com/blow/john_carmack_on_inlined_code.html):
  This John Carmack article talks about the benefits of inlining code that's
  only going to be called once. It also links to another functional programming
  article and you can follow that rabbit hole for far longer than you originally
  intended (don't ask me how I know that).
- [Google's networked API Design Guide](https://cloud.google.com/apis/design/):
  Google's REST/RPC design guide is pretty opinionated, but looks very
  reasonable to me. I haven't designed many REST APIs, and I've been using this
  guide to shape how I design a side project of mine. In particular, creating
  "collection" and "item" abstractions and building operations on top of those
  has been revelatory (it turns out it's a common pattern, but I never noticed it
  before).
- [The Mathematical Hacker](https://www.evanmiller.org/mathematical-hacker.html):
  Evan Miller argues here that math is a tool for understanding the world, and
  that programmers should use it to do a lot of the heavy lifting. It's a bit of
  a reality check to some of my "well I can add this thingie here, and won't that
  be elegant" daydreams. Code is to solve a problem, and most of the harder
  problems are best solved mathmatically and simply transcribed as code.
- [The Architecture of Open Source Applications](http://www.aosabook.org/en/index.html):
	a couple of free online books about the architecture of existing oplications.
	I've read parts of it, but I really need to read it in it's entirety.
- [Safe and Efficient, Now](http://okmij.org/ftp/Computation/lightweight-static-guarantees.html):
	This site talks about how to use the type system to protect against invalid
	data. I particularly like the "DirtyString" example - using a separate type to
	represent untrusted data, along with a function that validates it and returns a
	validated version of the type. You can design your other functions to simply
	take an instance of the validated type, and be confident that their already
	validated!
- [Using Rust For Game Development](https://www.youtube.com/watch?v=aKLntZcp27M) and [Is There More to Game Architecture than ECS?](https://www.youtube.com/watch?v=aKLntZcp27M) are examples of programming patterns that fall out of the somewhat extreme needs video game designs impose on their architects. I haven't tried these architectures but I really liked these talks.

### Examples

These are libraries that have really impressed me with their usability;
whatever they're doing, I want to emulate!

TODO: add links

- Python's pathlib library - easily my preferred way to work with paths. Most
  (all?) methods returns a new instance instead of mutating.
- Python's requests library - lots of hooks, provides easy and advanced ways to
  use it (TODO: make a blog post about this).
- SQLite3 - runs everywhere, insanely good docs, very useful
- Go's kingpin library - fluent-style; fairly terse.

