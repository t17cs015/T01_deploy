#!/bin/sh

if [[ $# == 0 ]]; then
    python3.5 manage.py runserver
elif [[ $1 == "mig" ]]; then
    python3.5 manage.py makemigrations management_system && python3.5 manage.py migrate
elif [[ $1 == "clean" ]]; then
    rm -r db.sqlite3 
    management_system/migrations/*
elif [[ $1 == "all" ]]; then
    $0 clean
    $0 mig
elif [[ $1 == "--help" ]]; then
    echo "使用法 : ./run.sh [オプション]..."
    echo "オプションをつけずに実行すると python3.5 manage.py runserver が実行されます。"
    echo ""
    echo "オプション"
    echo "  mig                 makemigrations と migrate を同時に実行する"
    echo "  clean               db.sqlit3 と migrations ディレクトリ以下のファイルを削除する"
    echo "  all                 clean オプションを付けて実行した後に"
    echo "                      mig オプションを付けて実行したのと同じ結果を与える"
    echo "  その他オプション    python3.5 manage.py に与えられた引数をそのまま渡して実行する"
else
    python3.5 manage.py $@
fi


