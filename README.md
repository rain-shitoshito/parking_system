# parking_system
ドメイン駆動設計(DDD)を知ったのでDjangoで実現するような方法を考えた。   
Djangoの利点などを消してしまう部分も多々あるが、主に以下の部分に気を付けて作成してみた。


・コントローラ又はモデルとビジネスロジックの分離  
・バリデーションの分離（入力バリデーション・ロジックバリデーション）  
・インターセプターチックなものを作成（mixin・ロギング用デコレータ）  



## テスト
\# parking_system/account/test/（一部未作成部分あり）
```
$ python manage.py test
```

## 実行
```
$ # 1. parking_system/setting_it.pyにDB接続設定を記述
$ # 2. マイグレーション
$ python manage.py makemigrations
$ python manage.py migrate
$ # 3. 実行
$ python manage.py runserver
```
