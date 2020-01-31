#!/bin/sh

if [[ $# == 0 ]]; then
    $0 clean
    $0 mig
    (
        echo "admin" && \
        echo "p@ssw0rd"
    ) | $0 adduser
elif [[ $1 == "mig" ]]; then
    $0 makemigrations management_system && $0 migrate
elif [[ $1 == "clean" ]]; then
    rm -r db.sqlite3 
    rm -r management_system/migrations/*
elif [[ $1 == "adduser" ]]; then
    MAIL="admin@myproject.com"
    read -p "Admistrator Name: " USER
    read -sp "Admistrator Password: " PASS
    (
        echo "from django.contrib.auth import get_user_model" && \
        echo "User = get_user_model()" && \
        echo "User.objects.create_superuser('"$USER"', '"$MAIL"', '"$PASS"')" \
    ) | $0 shell
elif [[ $1 == "rmuser" ]]; then
    read -p "Admistrator Name: " USER
    (
        echo "from django.contrib.auth import get_user_model" && \
        echo "User = get_user_model()" && \
        echo "print(User.objects.filter(is_superuser=True).filter(username='"$USER"'))" && \
        echo "User.objects.filter(is_superuser=True).filter(username='"$USER"').delete()"
    ) | $0 shell
elif [[ $1 == "--help" ]]; then
    echo "使用法 : ./run.sh [オプション]..."
    echo "オプションをつけずに実行すると python3.5 manage.py runserver が実行されます。"
    echo ""
    echo "オプション"
    echo "  mig                 makemigrations と migrate を同時に実行する"
    echo "  clean               db.sqlit3 と migrations ディレクトリ以下のファイルを削除する"
    echo "  adduser             管理者ユーザーを追加する"
    echo "  rmuser              管理者ユーザーを削除する"
    echo "  その他オプション    python3.5 manage.py に与えられた引数をそのまま渡して実行する"
else
    python3.5 manage.py $@
fi

