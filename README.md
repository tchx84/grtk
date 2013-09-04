## git-redmine toolkit

grtk contains a set of convenience scripts that allows developers to
interact with redmine from CLI.

### Features
* send patches to redmine.
* fetch patches from a given issue.
* merge patches from a given issue.
* report spent time on issues.

### Installation
* $cd /some/place/
* $git clone https://github.com/tchx84/grtk.git
* $mkdir ~/.grtk/
* $cp /some/place/grtk/etc/config.example ~/.grtk/config
* $vim ~/.grtk/config #change it properly

### Make it easy to use
* $vim ~/.bashrc
* add these lines:

  alias gfetch=/some/place/grtk/fetch.py
  
  alias gmerge=/some/place/grtk/merge.py

  alias gsend=/some/place/grtk/send.py

  alias gspent=/some/place/grtk/spent.py

### Development
* if you ever find this useful, feel free to extend it and send a pull request!
