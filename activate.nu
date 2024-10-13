# This file must be used with "source activate.nu" *from nu*
# You cannot run it directly

def deactivate [] {
    if ("_OLD_VIRTUAL_PATH" in $env) {
        $env.PATH = $env._OLD_VIRTUAL_PATH
        hide-env "_OLD_VIRTUAL_PATH"
    }
    if ("_OLD_VIRTUAL_PYTHONHOME" in $env) {
        $env.PYTHONHOME = $env._OLD_VIRTUAL_PYTHONHOME
        hide-env "_OLD_VIRTUAL_PYTHONHOME"
    }
    if ("VIRTUAL_ENV" in $env) {
        hide-env "VIRTUAL_ENV"
    }
    if ("VIRTUAL_ENV_PROMPT" in $env) {
        hide-env "VIRTUAL_ENV_PROMPT"
    }
}

# Deactivate any currently active virtual environment
deactivate

# Set VIRTUAL_ENV path
let virtual_env = (pwd | path join ".venv")
if not ($virtual_env | path exists) {
    print "Error: Virtual environment directory does not exist."
    return
}
$env.VIRTUAL_ENV = $virtual_env

# Update PATH
$env._OLD_VIRTUAL_PATH = $env.PATH
let venv_bin = ($virtual_env | path join "bin")
$env.PATH = ($env.PATH | split row (char esep) | prepend $venv_bin | str join (char esep))

# Unset PYTHONHOME if set
if ("PYTHONHOME" in $env) {
    $env._OLD_VIRTUAL_PYTHONHOME = $env.PYTHONHOME
    hide-env "PYTHONHOME"
}

# Set VIRTUAL_ENV_PROMPT
$env.VIRTUAL_ENV_PROMPT = "(.venv) "

print "Virtual environment activated. Use 'deactivate' to exit."

# No direct equivalent in nu for "hash -r" but it's not needed
# hash -r 2> /dev/null
