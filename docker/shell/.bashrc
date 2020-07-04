# ~/.bashrc: executed by bash(1) for non-login shells.

# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
export LS_OPTIONS='--color=auto'
alias ls='ls $LS_OPTIONS'
alias lla='ls $LS_OPTIONS -A -l -h'
alias ll='ls $LS_OPTIONS -l -h'
alias la='ls $LS_OPTIONS -A'
alias l='ls $LS_OPTIONS -CF'
alias clr="clear"

# Some more alias to avoid making mistakes:
alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'

# CD
function cd {
    builtin cd "$@" && ls -ACFs
}
alias up="cd ../"
alias up2="cd ../../"
alias up3="cd ../../../"
alias up4="cd ../../../../"
alias up5="cd ../../../../../"
alias back="cd -"
alias home="cd ~"
alias root="cd /"

# Django
alias dj="python /www/manage.py"