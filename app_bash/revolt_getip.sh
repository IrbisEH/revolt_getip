#!/usr/bin/bash

UTIL_NAME="getip"
DATA_PATH="${HOME}/revolt_config/ip_addresses.lst"

ProcessGet() {
  local search_by="$1"

  if [[ ! -f "$DATA_PATH" ]]; then
    echo "Error! Data file '${DATA_PATH}' not found."
    exit 1
  fi

  if [[ -z "$search_by" ]]; then
    cat "$DATA_PATH"
  else
    # Фильтрация файла с помощью grep
    grep -i "$search_by" "$DATA_PATH" || {
      echo "No matches found for '$search_by'."
      exit 1
    }
  fi
}

ProcessSet() {
  echo "set cmd"
}

ProcessVersion() {
  echo "${UTIL_NAME} util version: ${VERSION}"
}

ProcessHelp() {
  cat <<EOF
Usage: ${UTIL_NAME} [OPTIONS]

Options:
  -g, --get [SEARCH]   Show data, optionally filtered by SEARCH
  -s, --set            NOT IMPLEMENTED
  -h, --help           Display this help message
EOF
}

Main() {
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
      -g|--get)
        local search_arg=""
        [[ -n "$2" && "$2" != -* ]] && { search_arg="$2"; shift; }
        ProcessGet "$search_arg"
        return 0
        ;;
      -s|--set)
        return 0
        ;;
      -h|--help)
        ProcessHelp
        return 0
        ;;
      *)
        ProcessHelp
        exit 1
        ;;
    esac
    shift
  done

  ProcessHelp
  exit 1
}

Main "$@"