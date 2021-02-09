+++
title = "Ansible User Notes"
date = 2018-02-01
updated = 2018-02-01
aliases = [ "2018/02/01/Ansible-User-Notes.html" ]
+++

Ansible has two types of users: `become_user` and `remote_user` (and the deprecated `ssh_user` and `sudo_user` that I won't cover). Here's how to use them:

`remote_user` is the account that logs into the machine (`ssh vagrant@tmp_ansible_test_vm` would have `vagrant` as the remote user). If this user is going to do perform tasks as `root` or another user, it should have sudo permissions (i.e., be added to the `wheel` group on CentOS).

If the `remote_user` is going to perform tasks as `root` or another user, set the `become:` option to `true` (at either the playbook or the task level) and the `become_user:` option to the name of the other user or `root`. If you don't specify `become_user`, the default is to switch to `root`.

### Setting `remote_user` and `become_user`

`remote_user` options can be set [in the `hosts` file](http://docs.ansible.com/ansible/latest/intro_configuration.html#remote-user) or with the following command line options (gleaned from `ansible-playbook --help`):

```
    -k, --ask-pass      ask for connection password
    --private-key=PRIVATE_KEY_FILE, --key-file=PRIVATE_KEY_FILE
                        use this file to authenticate the connection
    -u REMOTE_USER, --user=REMOTE_USER
                        connect as this user (default=None)
```

[`become_user` options](http://docs.ansible.com/ansible/latest/become.html) can be set per playbook, task, or via the following connection options (gleaned from `ansible-playbook --help`):

```
    -b, --become        run operations with become (does not imply password
                        prompting)
    --become-method=BECOME_METHOD
                        privilege escalation method to use (default=sudo),
                        valid choices: [ sudo | su | pbrun | pfexec | doas |
                        dzdo | ksu | runas | pmrun ]
    --become-user=BECOME_USER
                        run operations as this user (default=root)
    ... skipping some irrelevant ones
    -K, --ask-become-pass
                        ask for privilege escalation password
```

## Using `become_user` and `remote_user` effectively

I prefer setting `remote_user` in the hosts file and `become_user` in the command line options because it's easier to change hosts files then playbooks. Unfortunately, as of Ansible 2.4, the documented `remote_user` and `private_key_file` options don't seem to work, so I resort to the older and undocumented `ansible_ssh_user` and `ansible_ssh_private_key_file`(they [appear to be the same](https://stackoverflow.com/a/36677811/2958070)):

### Setting `remote_user` in the host file for vagrant instances:

```yaml
all:
  hosts:
    tmp-ansible-test_vm:
      ansible_host: 10.0.0.11
      ansible_ssh_user: vagrant  # remote_user / private_key_file doesn't seem to work
      ansible_ssh_private_key_file: ./.vagrant/machines/tmp_ansible_test_vm/virtualbox/private_key
```

### Setting `become_user` in descending order of precedence:

#### Command line argument (least powerful)

This also specifies some other options for good measure

```bash
ansible-playbook \
    --user=vagrant \
    --ask-pass \
    --become-user=network-automation \
    --ask-become-pass \
    --inventory 10.0.0.11, \
    install_all.yaml
```

#### Playbook level

```yaml
- hosts: all
  become: true
  become_user: network-automation  # Not recommended, see below
  ... # other stuff
```

#### Task level (most powerful)

```yaml
  - name: Push the service file
    become: true
    become_user: root
    copy:
      src: "../systemd/my_service@.service"
      dest: /etc/systemd/system/my_service@.service
```

#### My strategy for using `become_user`:

- `become_user` at the *task* level overrides `become_user` at the *playbook* level overrides `become_user` at the *command switch* level
- After initial development, don't specify `become_user` at the playbook level- this will let you set it at the command option level (different servers need different ones for the same playbook) or at the task level (which, for most purposes, *should* only need `root`)
- If you need to use root for a task, always use `become: true` and `become_user: root`. This will override whatever default `become_user` is set.

#### Getting the name of `become_user` as a variable

For some reason, this isn't normally exposed. Here's a way to get it:


```yaml
{% raw %}  - name: Get become_user in stdout (hack for Ansible not providing it as a variable)
    command: whoami
    register: whoami_output
  - set_fact:
      become_user_var: "{{ whoami_output.stdout }}"{% endraw %}
```


### Other Notes:

 - `--ask-become-pass` will break running the playbook if `remote_user` has passwordless `sudo`
 - `become_user` will fail if Ansible detects it has to do it insecurely (see [the docs](http://docs.ansible.com/ansible/latest/become.html#becoming-an-unprivileged-user)). Set the following option in `ansbible.cfg` to tell Ansible this is okay.

```ini
# This presents a window for a logged-in attacker,
# but it's a small window and I need what it enables
# See http://docs.ansible.com/ansible/latest/become.html#becoming-an-unprivileged-user
allow_world_readable_tmpfiles = True
```
