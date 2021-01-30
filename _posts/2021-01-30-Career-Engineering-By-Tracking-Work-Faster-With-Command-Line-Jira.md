---
layout: default
title: Career Engineering: Tracking Work Faster With Command Line Jira
---

Thank you Matt Doar and Josiah Bradley for reviewing this post.

TL;DR: [go-jira](https://github.com/go-jira/jira) is super nice.

## Creating Jira tickets is necessary, slow, and annoying

Tracking my work is super important. At Linkedin, we have [one of the
largest](https://www.atlassian.com/webinars/software/how-linkedin-scaled-to-3m-jira-issues-and-500m-members)
Jira installations anywhere. We track progress with Jira tickets. We coordinate
working with other teams through Jira tickets. My manager Tom uses our Jira to
make a case for promoting us occasionally.

Jira certainly has several things I appreciate. I [can
work](https://github.com/bbkane/dotfiles/blob/dbafd0d317ed211c683782c4e8d6355e44d6b6b1/nvim/.config/nvim/init.vim#L398)
with the markup language, commenting on other's tickets works pretty well, the
Kanban board feature is spiffy, and I love the advanced search query language
(JQL) to find old tickets.

Actually creating tickets, though, can boil my brisket. In addition to the
title, description, and assignee fields, my team's Jira tickets need Epic
Links, Sprints, and Story Points fields added. That's like six fields and I'm
probably forgetting one or two of them. The Epic Link and Sprint fields require
AJAX code that take a couple of seconds to load each time, even though I
heavily re-use the same values.

It's also not like I can ignore setting up these tickets properly. As I
mentioned before, we rely on JIRA for all sorts of important purposes. Last
year I finally got annoyed enough to look for a way people could be happy
reading my tickets and I could be happy creating them and found [go-jira](https://github.com/go-jira/jira), a
command-line tool for working with Jira that lets you define templates to
shorten tasks.

## Creating Jira tickets with go-jira is fast and painless

### Install and configure

Installing go-jira is easy from MacOS: `brew install go-jira`

The next thing to do is to set up the config files and templates go-jira will
use to connect and create tickets.

#### `config.yml`

Let's go through a simplified version of my config.yml: `~/.jira.d/config.yml`

```yaml
assignee: <ldap username>
endpoint: <Jira url>
issuetype: Story
login: <ldap username>
project: <Jira project>
user: <ldap username>
custom-commands:
  - name: sprintid
    help: show sprint IDs for a ticket - `jira sprintid <ticket>`
    args:
      - name: ticket_id
        required: true
    script: |-
      {{jira}} view {{args.ticket_id}} -t debug \
      | grep sprint \
      | perl \
        -pe 's/^.*(id=[[:digit:]]+),.*(startDate=.{24}),.*(endDate=.{24}),.*$/\1\n  \2 \3/'
```

The first parts are pretty self-explanatory. endpoint is where our Jira is. The
default assignee for tickets is myself, and I have my ldap username for logging
in too.  custom-commands is the start of the real customization. It lets you
use write little shell scripts. Here's an example of using that `sprintid`
command I just defined:

```
jira sprintid custom script
$ jira login
? Jira Password [<ldap usrname>]:  ****************************
OK Found session for bkane

$ jira sprintid <ticket_id>
id=48241
  startDate=2020-11-26T08:00:21.274Z endDate=2020-12-10T08:00:00.000Z
```

And that's nice. What I really want to do, however, is make creating tickets easier.

#### the `create` template

When I run jira create, the tool opens up a YAML file that I edit. When I save
that file, the ticket is created on Jira. That YAML file is customizable with
`text/template`, so I can export the default template with `jira
export-templates -t create` and pre-fill fields that don't change for me much:


```
{{/* create template */ -}}
# ~/.jira.d/templates/create
# ... omitted fields to keep this blog post short
  # Epic Link
  # customfield_13793: PROJ-1001  # Oncall work
  # customfield_13793: PROJ-1002  # Main Project 1
  # customfield_13793: PROJ-1003  # Main Project 2

  # Sprint
  # Get sprint id from ticket: jira sprintid PROJ-????
  customfield_13792: 48241

  # Story Points
  customfield_10343: 1
```

As quarters change, my sprint epics change, and I change that commented out
list. When I create a ticket, I just uncomment the line with the epic I'm
interested in. I update the Sprint field manually with the `jira sprintid`
command shown earlier every new sprint. The easiest way I know to add more
custom fields to this template is to find or create a ticket with the field set
you're interested in via the web interface and comb through the output of `jira
view TICKET-####` to find which custom field it is.

So that's how I create tickets quickly and with a minimum of fuss these days.
