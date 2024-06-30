
alias superuser='manage createsuperuser'
alias backup='manage dbbackup -z'
alias restore='manage dbrestore -z'

# Добавляем быструю команду для установки ncdu
ncdu () {
  BIN_PATH=$(which ncdu)
  if [ $? -ne 0 ]; then
    if [[ $(whoami) -ne 'root' ]]
    then
      echo "Нужно быть root"
      return 1
    fi

    apt update || return 1
    apt install ncdu -y
    ncdu $@
  else
    $BIN_PATH $@
  fi
}

# Добавляем быструю команду для установки mc
mc () {
  BIN_PATH=$(which mc)
  if [ $? -ne 0 ]; then
    if [[ $(whoami) -ne 'root' ]]
    then
      echo "Нужно быть root"
      return 1
    fi

    apt update || return 1
    apt install mc -y
    # Настраиваем Lynx-навигацию
    mkdir -p ~/.config/mc
    printf '%s\n' '[Panels]' 'navigate_with_arrows=true' > ~/.config/mc/ini

    mc $@
  else
    $BIN_PATH $@
  fi
}

# Добавляем быструю команду для установки ipython
ipython () {
  BIN_PATH=$(which ipython)
  if [ $? -ne 0 ]; then
    if [[ $(whoami) -ne 'root' ]]
    then
      echo "Нужно быть root"
      return 1
    fi

    pip install ipython || return 1
    ipython $@
  else
    $BIN_PATH $@
  fi
}

# Добавляем быструю команду для установки bpython
bpython () {
  BIN_PATH=$(which bpython)
  if [ $? -ne 0 ]; then
    if [[ $(whoami) -ne 'root' ]]
    then
      echo "Нужно быть root"
      return 1
    fi

    apt update || return 1
    apt install less -y
    pip install bpython || return 1
    bpython $@
  else
    $BIN_PATH $@
  fi
}
