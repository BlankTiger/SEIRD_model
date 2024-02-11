venv := env_var("VIRTUAL_ENV")

default:
    @just --list

clean:
    rm -r ./SEIRD_model.egg-info
    rm -r ./build
    rm -r ./dist
    rm model.spec

build:
    #!/usr/bin/env bash
    . {{venv}}/bin/activate
    cd SEIRD_math_rs
    maturin develop -r
    cd ..
    pyinstaller --noconfirm --onefile --windowed --icon "icon.ico"  "model.pyw"

compile-requirements:
    #!/usr/bin/env bash
    . {{venv}}/bin/activate
    pip-compile -v -o requirements.txt
