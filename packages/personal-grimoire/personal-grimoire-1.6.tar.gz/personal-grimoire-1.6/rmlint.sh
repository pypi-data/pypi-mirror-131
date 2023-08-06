#!/bin/sh

PROGRESS_CURR=0
PROGRESS_TOTAL=321

# This file was autowritten by rmlint
# rmlint was executed from: /home/jean/projects/grimoire/
# Your command line was: rmlint

RMLINT_BINARY="/usr/bin/rmlint"

# Only use sudo if we're not root yet:
# (See: https://github.com/sahib/rmlint/issues/27://github.com/sahib/rmlint/issues/271)
SUDO_COMMAND="sudo"
if [ "$(id -u)" -eq "0" ]
then
  SUDO_COMMAND=""
fi

USER='jean'
GROUP='printadmin'

# Set to true on -n
DO_DRY_RUN=

# Set to true on -p
DO_PARANOID_CHECK=

# Set to true on -r
DO_CLONE_READONLY=

# Set to true on -q
DO_SHOW_PROGRESS=true

# Set to true on -c
DO_DELETE_EMPTY_DIRS=

# Set to true on -k
DO_KEEP_DIR_TIMESTAMPS=

# Set to true on -i
DO_ASK_BEFORE_DELETE=

##################################
# GENERAL LINT HANDLER FUNCTIONS #
##################################

COL_RED='[0;31m'
COL_BLUE='[1;34m'
COL_GREEN='[0;32m'
COL_YELLOW='[0;33m'
COL_RESET='[0m'

print_progress_prefix() {
    if [ -n "$DO_SHOW_PROGRESS" ]; then
        PROGRESS_PERC=0
        if [ $((PROGRESS_TOTAL)) -gt 0 ]; then
            PROGRESS_PERC=$((PROGRESS_CURR * 100 / PROGRESS_TOTAL))
        fi
        printf '%s[%3d%%]%s ' "${COL_BLUE}" "$PROGRESS_PERC" "${COL_RESET}"
        if [ $# -eq "1" ]; then
            PROGRESS_CURR=$((PROGRESS_CURR+$1))
        else
            PROGRESS_CURR=$((PROGRESS_CURR+1))
        fi
    fi
}

handle_emptyfile() {
    print_progress_prefix
    echo "${COL_GREEN}Deleting empty file:${COL_RESET} $1"
    if [ -z "$DO_DRY_RUN" ]; then
        rm -f "$1"
    fi
}

handle_emptydir() {
    print_progress_prefix
    echo "${COL_GREEN}Deleting empty directory: ${COL_RESET}$1"
    if [ -z "$DO_DRY_RUN" ]; then
        rmdir "$1"
    fi
}

handle_bad_symlink() {
    print_progress_prefix
    echo "${COL_GREEN} Deleting symlink pointing nowhere: ${COL_RESET}$1"
    if [ -z "$DO_DRY_RUN" ]; then
        rm -f "$1"
    fi
}

handle_unstripped_binary() {
    print_progress_prefix
    echo "${COL_GREEN} Stripping debug symbols of: ${COL_RESET}$1"
    if [ -z "$DO_DRY_RUN" ]; then
        strip -s "$1"
    fi
}

handle_bad_user_id() {
    print_progress_prefix
    echo "${COL_GREEN}chown ${USER}${COL_RESET} $1"
    if [ -z "$DO_DRY_RUN" ]; then
        chown "$USER" "$1"
    fi
}

handle_bad_group_id() {
    print_progress_prefix
    echo "${COL_GREEN}chgrp ${GROUP}${COL_RESET} $1"
    if [ -z "$DO_DRY_RUN" ]; then
        chgrp "$GROUP" "$1"
    fi
}

handle_bad_user_and_group_id() {
    print_progress_prefix
    echo "${COL_GREEN}chown ${USER}:${GROUP}${COL_RESET} $1"
    if [ -z "$DO_DRY_RUN" ]; then
        chown "$USER:$GROUP" "$1"
    fi
}

###############################
# DUPLICATE HANDLER FUNCTIONS #
###############################

check_for_equality() {
    if [ -f "$1" ]; then
        # Use the more lightweight builtin `cmp` for regular files:
        cmp -s "$1" "$2"
        echo $?
    else
        # Fallback to `rmlint --equal` for directories:
        "$RMLINT_BINARY" -p --equal  "$1" "$2"
        echo $?
    fi
}

original_check() {
    if [ ! -e "$2" ]; then
        echo "${COL_RED}^^^^^^ Error: original has disappeared - cancelling.....${COL_RESET}"
        return 1
    fi

    if [ ! -e "$1" ]; then
        echo "${COL_RED}^^^^^^ Error: duplicate has disappeared - cancelling.....${COL_RESET}"
        return 1
    fi

    # Check they are not the exact same file (hardlinks allowed):
    if [ "$1" = "$2" ]; then
        echo "${COL_RED}^^^^^^ Error: original and duplicate point to the *same* path - cancelling.....${COL_RESET}"
        return 1
    fi

    # Do double-check if requested:
    if [ -z "$DO_PARANOID_CHECK" ]; then
        return 0
    else
        if [ "$(check_for_equality "$1" "$2")" -ne "0" ]; then
            echo "${COL_RED}^^^^^^ Error: files no longer identical - cancelling.....${COL_RESET}"
            return 1
        fi
    fi
}

cp_symlink() {
    print_progress_prefix
    echo "${COL_YELLOW}Symlinking to original: ${COL_RESET}$1"
    if original_check "$1" "$2"; then
        if [ -z "$DO_DRY_RUN" ]; then
            # replace duplicate with symlink
            rm -rf "$1"
            ln -s "$2" "$1"
            # make the symlink's mtime the same as the original
            touch -mr "$2" -h "$1"
        fi
    fi
}

cp_hardlink() {
    if [ -d "$1" ]; then
        # for duplicate dir's, can't hardlink so use symlink
        cp_symlink "$@"
        return $?
    fi
    print_progress_prefix
    echo "${COL_YELLOW}Hardlinking to original: ${COL_RESET}$1"
    if original_check "$1" "$2"; then
        if [ -z "$DO_DRY_RUN" ]; then
            # replace duplicate with hardlink
            rm -rf "$1"
            ln "$2" "$1"
        fi
    fi
}

cp_reflink() {
    if [ -d "$1" ]; then
        # for duplicate dir's, can't clone so use symlink
        cp_symlink "$@"
        return $?
    fi
    print_progress_prefix
    # reflink $1 to $2's data, preserving $1's  mtime
    echo "${COL_YELLOW}Reflinking to original: ${COL_RESET}$1"
    if original_check "$1" "$2"; then
        if [ -z "$DO_DRY_RUN" ]; then
            touch -mr "$1" "$0"
            if [ -d "$1" ]; then
                rm -rf "$1"
            fi
            cp --archive --reflink=always "$2" "$1"
            touch -mr "$0" "$1"
        fi
    fi
}

clone() {
    print_progress_prefix
    # clone $1 from $2's data
    # note: no original_check() call because rmlint --dedupe takes care of this
    echo "${COL_YELLOW}Cloning to: ${COL_RESET}$1"
    if [ -z "$DO_DRY_RUN" ]; then
        if [ -n "$DO_CLONE_READONLY" ]; then
            $SUDO_COMMAND $RMLINT_BINARY --dedupe  --dedupe-readonly "$2" "$1"
        else
            $RMLINT_BINARY --dedupe  "$2" "$1"
        fi
    fi
}

skip_hardlink() {
    print_progress_prefix
    echo "${COL_BLUE}Leaving as-is (already hardlinked to original): ${COL_RESET}$1"
}

skip_reflink() {
    print_progress_prefix
    echo "${COL_BLUE}Leaving as-is (already reflinked to original): ${COL_RESET}$1"
}

user_command() {
    print_progress_prefix

    echo "${COL_YELLOW}Executing user command: ${COL_RESET}$1"
    if [ -z "$DO_DRY_RUN" ]; then
        # You can define this function to do what you want:
        echo 'no user command defined.'
    fi
}

remove_cmd() {
    print_progress_prefix
    echo "${COL_YELLOW}Deleting: ${COL_RESET}$1"
    if original_check "$1" "$2"; then
        if [ -z "$DO_DRY_RUN" ]; then
            if [ -n "$DO_KEEP_DIR_TIMESTAMPS" ]; then
                touch -r "$(dirname "$1")" "$STAMPFILE"
            fi
            if [ -n "$DO_ASK_BEFORE_DELETE" ]; then
              rm -ri "$1"
            else
              rm -rf "$1"
            fi
            if [ -n "$DO_KEEP_DIR_TIMESTAMPS" ]; then
                # Swap back old directory timestamp:
                touch -r "$STAMPFILE" "$(dirname "$1")"
                rm "$STAMPFILE"
            fi

            if [ -n "$DO_DELETE_EMPTY_DIRS" ]; then
                DIR=$(dirname "$1")
                while [ ! "$(ls -A "$DIR")" ]; do
                    print_progress_prefix 0
                    echo "${COL_GREEN}Deleting resulting empty dir: ${COL_RESET}$DIR"
                    rmdir "$DIR"
                    DIR=$(dirname "$DIR")
                done
            fi
        fi
    fi
}

original_cmd() {
    print_progress_prefix
    echo "${COL_GREEN}Keeping:  ${COL_RESET}$1"
}

##################
# OPTION PARSING #
##################

ask() {
    cat << EOF

This script will delete certain files rmlint found.
It is highly advisable to view the script first!

Rmlint was executed in the following way:

   $ rmlint

Execute this script with -d to disable this informational message.
Type any string to continue; CTRL-C, Enter or CTRL-D to abort immediately
EOF
    read -r eof_check
    if [ -z "$eof_check" ]
    then
        # Count Ctrl-D and Enter as aborted too.
        echo "${COL_RED}Aborted on behalf of the user.${COL_RESET}"
        exit 1;
    fi
}

usage() {
    cat << EOF
usage: $0 OPTIONS

OPTIONS:

  -h   Show this message.
  -d   Do not ask before running.
  -x   Keep rmlint.sh; do not autodelete it.
  -p   Recheck that files are still identical before removing duplicates.
  -r   Allow deduplication of files on read-only btrfs snapshots. (requires sudo)
  -n   Do not perform any modifications, just print what would be done. (implies -d and -x)
  -c   Clean up empty directories while deleting duplicates.
  -q   Do not show progress.
  -k   Keep the timestamp of directories when removing duplicates.
  -i   Ask before deleting each file
EOF
}

DO_REMOVE=
DO_ASK=

while getopts "dhxnrpqcki" OPTION
do
  case $OPTION in
     h)
       usage
       exit 0
       ;;
     d)
       DO_ASK=false
       ;;
     x)
       DO_REMOVE=false
       ;;
     n)
       DO_DRY_RUN=true
       DO_REMOVE=false
       DO_ASK=false
       DO_ASK_BEFORE_DELETE=false
       ;;
     r)
       DO_CLONE_READONLY=true
       ;;
     p)
       DO_PARANOID_CHECK=true
       ;;
     c)
       DO_DELETE_EMPTY_DIRS=true
       ;;
     q)
       DO_SHOW_PROGRESS=
       ;;
     k)
       DO_KEEP_DIR_TIMESTAMPS=true
       STAMPFILE=$(mktemp 'rmlint.XXXXXXXX.stamp')
       ;;
     i)
       DO_ASK_BEFORE_DELETE=true
       ;;
     *)
       usage
       exit 1
  esac
done

if [ -z $DO_REMOVE ]
then
    echo "#${COL_YELLOW} ///${COL_RESET}This script will be deleted after it runs${COL_YELLOW}///${COL_RESET}"
fi

if [ -z $DO_ASK ]
then
  usage
  ask
fi

if [ -n "$DO_DRY_RUN" ]
then
    echo "#${COL_YELLOW} ////////////////////////////////////////////////////////////${COL_RESET}"
    echo "#${COL_YELLOW} /// ${COL_RESET} This is only a dry run; nothing will be modified! ${COL_YELLOW}///${COL_RESET}"
    echo "#${COL_YELLOW} ////////////////////////////////////////////////////////////${COL_RESET}"
fi

######### START OF AUTOGENERATED OUTPUT #########

handle_emptydir '/home/jean/projects/grimoire/grimoire/manual' # empty folder
handle_emptydir '/home/jean/projects/grimoire/grimoire/gyg/data_analysis/spark-warehouse' # empty folder
handle_emptyfile '/home/jean/projects/grimoire/grimoire/smartimmersion/test/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/search_run/application/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/search_run/domain/entries/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/smartimmersion/domain/variations_generator/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/core/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/desktop/focus/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/desktop/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/desktop/performance/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/search_run/domain/entries/path.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/smartimmersion/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/smartimmersion/domain/scoring/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/databases/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/tests/file/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/event_sourcing/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/gyg/data_analysis/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/translator/test/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/gyg/test/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/age/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/observability/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/search_run/tests/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/smartimmersion/domain/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/smartimmersion/application/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/translator/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/scripts/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/search_run/domain/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/tests/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/gyg/data_analysis/domain/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/tests/observability/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/having_time/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/having_time/test/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/desktop/test/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/anki/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/test/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/event_sourcing/test/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/grimoire/desktop/timebox/__init__.py' # empty file
handle_emptyfile '/home/jean/projects/grimoire/tests/work/__init__.py' # empty file

original_cmd  '/home/jean/projects/grimoire/tests/__pycache__/test_main.cpython-38-pytest-5.4.3.pyc' # original
remove_cmd    '/home/jean/projects/grimoire/tests/__pycache__/test_main.cpython-38-pytest-6.1.1.pyc' '/home/jean/projects/grimoire/tests/__pycache__/test_main.cpython-38-pytest-5.4.3.pyc' # duplicate

original_cmd  '/home/jean/projects/grimoire/tests/__pycache__/test_mlflow.cpython-39-pytest-6.1.2.pyc' # original
remove_cmd    '/home/jean/projects/grimoire/tests/__pycache__/test_mlflow.cpython-39-pytest-6.1.0.pyc' '/home/jean/projects/grimoire/tests/__pycache__/test_mlflow.cpython-39-pytest-6.1.2.pyc' # duplicate

original_cmd  '/home/jean/projects/grimoire/tests/__pycache__/test_paths_correct.cpython-39-pytest-6.1.2.pyc' # original
remove_cmd    '/home/jean/projects/grimoire/tests/__pycache__/test_paths_correct.cpython-39-pytest-6.1.0.pyc' '/home/jean/projects/grimoire/tests/__pycache__/test_paths_correct.cpython-39-pytest-6.1.2.pyc' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/desktop/test/__pycache__/test_clipboard.cpython-39-pytest-6.1.2.pyc' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/desktop/test/__pycache__/test_clipboard.cpython-39-pytest-6.1.0.pyc' '/home/jean/projects/grimoire/grimoire/desktop/test/__pycache__/test_clipboard.cpython-39-pytest-6.1.2.pyc' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/reader.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/reader.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/reader.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/repl.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/repl.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/repl.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/buffers.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core/async/impl/buffers.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/buffers.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/dispatch.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core/async/impl/dispatch.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/dispatch.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/ioc_helpers.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core/async/impl/ioc_helpers.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/ioc_helpers.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/protocols.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core/async/impl/protocols.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/protocols.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core/async.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/timers.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core/async/impl/timers.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/timers.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/channels.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core/async/impl/channels.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core/async/impl/channels.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/spec/gen/alpha.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/spec/gen/alpha.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/spec/gen/alpha.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/edn.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/tools/reader/edn.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/edn.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/reader_types.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/tools/reader/reader_types.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/reader_types.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/impl/commons.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/tools/reader/impl/commons.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/impl/commons.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/impl/errors.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/tools/reader/impl/errors.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/impl/errors.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/impl/utils.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/tools/reader/impl/utils.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/impl/utils.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core3443799.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core3EDD6FD.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core3443799.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/impl/inspect.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/tools/reader/impl/inspect.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader/impl/inspect.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core5F0D069.cljs.cache.json' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core3443799.cljs.cache.json' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core5F0D069.cljs.cache.json' # duplicate
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core3EDD6FD.cljs.cache.json' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core5F0D069.cljs.cache.json' # duplicate
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/old/coreBFFBFD0.cljs.cache.json' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core5F0D069.cljs.cache.json' # duplicate
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/old/coreEE05465.cljs.cache.json' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/user/core5F0D069.cljs.cache.json' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs_http/core.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs_http/core.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs_http/core.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs_http/client.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs_http/client.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs_http/client.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs_http/util.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs_http/util.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs_http/util.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/clojure/walk.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/clojure/walk.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/clojure/walk.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/clojure/string.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/clojure/string.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/clojure/string.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/clojure/set.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/clojure/set.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/clojure/set.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/caching.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/caching.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/caching.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cognitect/transit.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cognitect/transit.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cognitect/transit.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/delimiters.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/delimiters.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/delimiters.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/eq.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/eq.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/eq.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/util.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/util.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/util.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/impl/reader.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/impl/reader.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/impl/reader.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/handlers.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/handlers.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/handlers.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/impl/decoder.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/impl/decoder.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/impl/decoder.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/impl/writer.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/impl/writer.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/impl/writer.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/types.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/com/cognitect/transit/types.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/com/cognitect/transit/types.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/async/run.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/async/run.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/async/run.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/asserts/asserts.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/asserts/asserts.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/asserts/asserts.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/entrypointregistry.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/debug/entrypointregistry.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/entrypointregistry.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/async/nexttick.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/async/nexttick.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/async/nexttick.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/logrecord.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/debug/logrecord.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/logrecord.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/debug.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/debug/debug.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/debug.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/logbuffer.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/debug/logbuffer.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/logbuffer.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/errorcontext.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/debug/errorcontext.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/errorcontext.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/crypt/crypt.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/crypt/crypt.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/crypt/crypt.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/disposable/idisposable.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/disposable/idisposable.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/disposable/idisposable.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/browserfeature.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/dom/browserfeature.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/browserfeature.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/htmlelement.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/dom/htmlelement.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/htmlelement.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/logger.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/debug/logger.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/debug/logger.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/disposable/disposable.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/disposable/disposable.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/disposable/disposable.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/asserts.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/dom/asserts.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/asserts.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/tags.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/dom/tags.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/tags.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/tagname.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/dom/tagname.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/tagname.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/eventid.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/eventid.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/eventid.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/safe.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/dom/safe.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/safe.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/event.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/event.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/event.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/browserevent.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/browserevent.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/browserevent.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/listenable.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/listenable.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/listenable.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/listener.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/listener.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/listener.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/listenermap.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/listenermap.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/listenermap.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/legacyconversions.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/html/legacyconversions.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/legacyconversions.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/eventtarget.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/eventtarget.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/eventtarget.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/eventtype.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/eventtype.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/eventtype.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/safescript.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/html/safescript.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/safescript.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/safestylesheet.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/html/safestylesheet.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/safestylesheet.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/trustedtypes.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/html/trustedtypes.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/trustedtypes.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/json/hybrid.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/json/hybrid.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/json/hybrid.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/trustedresourceurl.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/html/trustedresourceurl.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/trustedresourceurl.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/safeurl.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/html/safeurl.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/safeurl.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/labs/useragent/engine.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/labs/useragent/engine.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/labs/useragent/engine.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/uncheckedconversions.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/html/uncheckedconversions.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/uncheckedconversions.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/labs/useragent/platform.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/labs/useragent/platform.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/labs/useragent/platform.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/labs/useragent/browser.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/labs/useragent/browser.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/labs/useragent/browser.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/log/log.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/log/log.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/log/log.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/labs/useragent/util.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/labs/useragent/util.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/labs/useragent/util.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/math/coordinate.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/math/coordinate.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/math/coordinate.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/math/math.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/math/math.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/math/math.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/errorcode.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/errorcode.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/errorcode.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/eventtype.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/eventtype.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/eventtype.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/httpstatus.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/httpstatus.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/httpstatus.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/jsonp.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/jsonp.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/jsonp.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/math/integer.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/math/integer.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/math/integer.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/wrapperxmlhttpfactory.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/wrapperxmlhttpfactory.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/wrapperxmlhttpfactory.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/websocket.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/websocket.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/websocket.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/async/workqueue.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/async/workqueue.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/async/workqueue.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/xhrlike.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/xhrlike.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/xhrlike.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/mochikit/async/deferred.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/mochikit/async/deferred.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/mochikit/async/deferred.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/xmlhttpfactory.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/xmlhttpfactory.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/xmlhttpfactory.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/xmlhttp.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/xmlhttp.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/xmlhttp.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/jsloader.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/jsloader.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/jsloader.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/promise/resolver.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/promise/resolver.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/promise/resolver.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/promise/thenable.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/promise/thenable.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/promise/thenable.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/string/const.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/string/const.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/string/const.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/string/stringformat.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/string/stringformat.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/string/stringformat.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/string/typedstring.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/string/typedstring.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/string/typedstring.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/timer/timer.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/timer/timer.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/timer/timer.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/structs/map.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/structs/map.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/structs/map.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/structs/structs.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/structs/structs.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/structs/structs.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/process/env.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/process/env.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/process/env.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/useragent/product.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/useragent/product.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/useragent/product.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/no/en/core.cljc' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/no/en/core.cljc' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/no/en/core.cljc' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/useragent/useragent.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/useragent/useragent.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/useragent/useragent.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/debug.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/debug.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/debug.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/dom.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/dom.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/dom.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/core.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/core.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/core.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/batching.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/impl/batching.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/batching.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/ratom.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/ratom.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/ratom.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/component.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/impl/component.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/component.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/input.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/impl/input.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/input.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/resources/libs/my.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/resources/libs/my.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/resources/libs/my.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/template.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/impl/template.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/template.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/util.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/impl/util.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/util.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/figwheel/main/generated/dev_auto_test_runner.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/generated-input-files/gen_test_runner.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/figwheel/main/generated/dev_auto_test_runner.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/desktop/test/__pycache__/test_shortcut.cpython-39-pytest-6.1.2.pyc' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/desktop/test/__pycache__/test_shortcut.cpython-39-pytest-6.1.0.pyc' '/home/jean/projects/grimoire/grimoire/desktop/test/__pycache__/test_shortcut.cpython-39-pytest-6.1.2.pyc' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/nodetype.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/dom/nodetype.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/nodetype.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/clojure/browser/dom.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/clojure/browser/dom.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/clojure/browser/dom.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/translator/test/__pycache__/test_translator.cpython-39-pytest-6.1.2.pyc' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/translator/test/__pycache__/test_translator.cpython-39-pytest-6.1.0.pyc' '/home/jean/projects/grimoire/grimoire/translator/test/__pycache__/test_translator.cpython-39-pytest-6.1.2.pyc' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/gyg/test/__pycache__/test_databricks_notebook.cpython-39-pytest-6.1.2.pyc' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/gyg/test/__pycache__/test_databricks_notebook.cpython-39-pytest-6.1.0.pyc' '/home/jean/projects/grimoire/grimoire/gyg/test/__pycache__/test_databricks_notebook.cpython-39-pytest-6.1.2.pyc' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/protocols.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/reagent/impl/protocols.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/reagent/impl/protocols.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/browserfeature.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/browserfeature.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/browserfeature.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/tools/reader.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/tools/reader.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/spec/alpha.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/spec/alpha.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/spec/alpha.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/events.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/events/events.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/events/events.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/base.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/base.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/base.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/xhrio.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/net/xhrio.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/net/xhrio.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/safehtml.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/html/safehtml.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/html/safehtml.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/uri/utils.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/uri/utils.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/uri/utils.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/iter/iter.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/iter/iter.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/iter/iter.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/uri/uri.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/uri/uri.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/uri/uri.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljsjs/react/development/react.inc.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljsjs/react/production/react.min.inc.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljsjs/react/development/react.inc.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/string/string.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/string/string.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/string/string.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/array/array.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/array/array.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/array/array.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/dom.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/dom/dom.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/dom/dom.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core.cljs' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core.cljs' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core.cljs' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/promise/promise.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/goog/promise/promise.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/goog/promise/promise.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljsjs/react-dom/production/react-dom.min.inc.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljsjs/react-dom/development/react-dom.inc.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljsjs/react-dom/production/react-dom.min.inc.js' # duplicate

original_cmd  '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core.js' # original
remove_cmd    '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/target/public/cljs-out/dev/cljs/core.js' '/home/jean/projects/grimoire/grimoire/smartimmersion/clojure/out/cljs/core.js' # duplicate



######### END OF AUTOGENERATED OUTPUT #########

if [ $PROGRESS_CURR -le $PROGRESS_TOTAL ]; then
    print_progress_prefix
    echo "${COL_BLUE}Done!${COL_RESET}"
fi

if [ -z $DO_REMOVE ] && [ -z $DO_DRY_RUN ]
then
  echo "Deleting script " "$0"
  rm -f '/home/jean/projects/grimoire/rmlint.sh';
fi
