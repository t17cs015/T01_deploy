#!/bin/sh

if [[ $# == 0 ]]; then
    $0 runserver
elif [[ $1 == "bklog" ]]; then
    $0 runserver > $(date "+%Y-%m-%S-%H:%M:%S").log
elif [[ $1 == "rmcache" ]]; then
    rm *.log
elif [[ $1 == "mig" ]]; then
    $0 makemigrations management_system && $0 migrate
elif [[ $1 == "clean" ]]; then
    rm -r db.sqlite3 
    rm -r management_system/migrations/*
elif [[ $1 == "adduser" ]]; then
    USER="admin"
    MAIL="admin@myproject.com"
    PASS="password"
    (
        echo "from django.contrib.auth import get_user_model" && \
        echo "User = get_user_model()" && \
        echo "User.objects.create_superuser('"$USER"', '"$MAIL"', '"$PASS"')" \
    ) | $0 shell
elif [[ $1 == "dbinit" ]]; then
    (
        echo "from management_system.models import Customer, Request" && \
        echo "c = Customer(" && \
        echo "email = \"t17cs015@gmail.com\"," && \
        echo "name = \"帯津勇斗\"," && \
        echo "organization_name = \"University of Yamanashi\"," && \
        echo "tell_number = \"000-000-0000\"" && \
        echo "); c.save()" && \
        echo "r = Request(" && \
        echo "scheduled_entry_datetime = \"2019-10-10 00:00:00\"," && \
        echo "scheduled_exit_datetime = \"2019-10-11 00:30:00\"," && \
        echo "purpose_admission = \"test\"," && \
        echo "request_datetime = \"1946-11-12 00:00:00\"," && \
        echo "email = c," && \
        echo "request_id = 0," && \
        echo "password = 1234" && \
        echo "); r.save()" && \
        echo "c = Customer(" && \
        echo "email = \"software17cs027@gmail.com\"," && \
        echo "name = \"keisuke sinohara\"," && \
        echo "organization_name = \"University of Yamanashi\"," && \
        echo "tell_number = \"000-000-0000\"" && \
        echo "); c.save()" && \
        echo "r = Request(" && \
        echo "scheduled_entry_datetime = \"2019-10-10 01:40:00\"," && \
        echo "scheduled_exit_datetime = \"2019-10-11 00:41:59\"," && \
        echo "purpose_admission = \"テスト\"," && \
        echo "request_datetime = \"1946-10-12 00:00:00\"," && \
        echo "email = c," && \
        echo "request_id = 1," && \
        echo "password = 1234" && \
        echo "); r.save()" && \
        echo "" \
    ) | $0 shell
elif [[ $1 == "all" ]]; then
    $0 clean
    $0 mig
    $0 adduser
    $0 dbinit
    $0
elif [[ $1 == "--help" ]]; then
    echo "使用法 : ./run.sh [オプション]..."
    echo "オプションをつけずに実行すると python3.5 manage.py runserver が実行されます。"
    echo ""
    echo "オプション"
    echo "  mig                 makemigrations と migrate を同時に実行する"
    echo "  clean               db.sqlit3 と migrations ディレクトリ以下のファイルを削除する"
    echo "  adduser             管理者ユーザーを追加する"
    echo "  dbinit              データベースにテスト用データを追加する"
    echo "  all                 強制再マイグレーションを実行し、管理者ユーザーと"
    echo "                      テスト用データをデータベースに追加しサーバーを実行する"
    echo "  その他オプション    python3.5 manage.py に与えられた引数をそのまま渡して実行する"
else
    python3.5 manage.py $@
fi

