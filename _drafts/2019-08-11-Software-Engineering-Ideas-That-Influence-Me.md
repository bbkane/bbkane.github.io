---
layout: default
title: Software Engineering Ideas That Influence Me
---

I watch a lot of conference talks on YouTube and I read a lot of software
engineering articles. Some of that media has really helped me become a better
engineer. As a relatively young engineer, I know my style will develop further and
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
  program, you should write the usage code first, so you actually have a use
  case.

### Other

- [Advanced Testing in Go (Hashimoto)](https://www.youtube.com/watch?v=8hQG7QlcLBk) ([transcript](https://about.sourcegraph.com/go/advanced-testing-in-go)): In this talk, Michael Hashimoto splits his time between talking about creating tests creating testable code. Very useful and pragmatic.
- [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell) and [Boundaries](https://www.destroyallsoftware.com/talks/boundaries): Gary Bernhart has a bunch of great videos on his [website](https://www.destroyallsoftware.com/screencasts). These two talks build off one another and talk about how you should make as much of your code as possible pure functions. This makes testing and extending it much easier.
- [CppCon 2014: Mike Acton "Data-Oriented Design and C++"](https://www.youtube.com/watch?v=rX0ItVEVjHc): This is another hugely influential talk
- [Hammock Driven Development: Rich Hickey](https://www.youtube.com/watch?v=f84n5oFoZBc)
- [Types as Sets](https://guide.elm-lang.org/appendix/types_as_sets.html): This really helped me understand how you can use types to force code that uses them to be correct.
- [John Carmack on Inlined Code](http://number-none.com/blow/john_carmack_on_inlined_code.html)

## Takeaways

- TODO: wrapping requests
- We shape our tools and our tools shape us. Don't make code so complicated it can only be navigated by IDE
- Write usage code first.
- TODO: find don't take math out of programming blog post
- TODO: embed YouTube videos and find out how to make width work on mobile devices
- TODO: add lessons to take away section. Maybe pontificate more on what's art and what's science
- Global variables are hard


https://www.evanmiller.org/mathematical-hacker.html
