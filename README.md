# tech-article-hub 🚀

機械学習を用いた「Qiita記事のカテゴリ自動分類機能」を搭載した、モダンなWebアプリケーションです。
本プロジェクトでは、Flaskによるサーバーサイドレンダリング構成（第1章）から始まり、さらにモダンなFastAPI + リアルタイムJavaScriptによるSPA構成（第2章）へのアーキテクチャの進化を記録しています。

---

## 🌟 主な機能と特徴

1. **Flaskによるクリーンな関心の分離**
   - `auth`（ユーザー認証・会員登録）と `main`（主要機能・AI推論）を完全にディレクトリごと分割。Factoryパターンによる初期化を採用し、実務に即した高い保守性を確保しています。
2. **FastAPIを使用したREST API**
   - バックエンドをDBアクセスにAsyncSessionを使用のREST APIとして再構築。フロントエンド（Vanilla JS）と完全に分離し、モダンなWebアプリケーションの構成へと進化させました。ログイン状態は現在はLocalStorageに保存。XSSリスクを踏まえ、HttpOnly Cookie方式を検討中
3. **機械学習の「学習」と「推論」の分離（学習処理と推論処理を分離）**
   - `test_ai.py` でオフライン学習（ロジスティック回帰、データ分割方法、件数、ベースライン、評価指標を併記）を行い、モデルを `.pkl` として保存。アプリ側（`ai_model.py`）では起動時に一度だけロードして使い回す設計（シングルトンライク）にし、起動時にモデルをロードし、リクエストごとの再ロードを回避を実現しています。
4. **Dockerによる開発環境のコンテナ化**
   - `Dockerfile` および `docker-compose` を完備し、どの環境でもコマンド一発で同じ開発環境が立ち上がります。

---

## 📂 フォルダ構成

```

Markdown
## 📂 フォルダ構成

tech-article-hub/
├── .gitignore               # 機密情報や不要なファイルを隠す設定ファイル
├── Dockerfile               # アプリをコンテナ化するための設計図
├── docker-compose.yml       # コンテナの起動や環境を管理する設定ファイル
├── requirements.txt         # 依存ライブラリ一覧
│
├── app/                     # 🌶️ 【Flask版】メインディレクトリ
│   ├── app.py               # Flaskアプリの起動・初期化を行う核
│   ├── model.py             # 💾 データベースの設計図（共通のモデル定義）
│   ├── forms.py             # 📝 ユーザー入力のバリデーション（フォーム定義）
│   ├── config.py            # ⚙️ アプリの設定を管理するスクリプト
│   ├── test_views.py        # 🧪 テスト用の処理スクリプト
│   ├── instance/            # 🔒 (Git除外) ローカルDB等の置き場
│   │
│   ├── auth/                # 🔑 【認証機能の部屋】
│   │   └── views.py         # 認証関連（ログイン・会員登録等）の画面処理
│   │
│   ├── main/                # 🏠 【メイン機能 ＆ AIの部屋】
│   │   ├── views.py         # メイン関連（お気に入り一覧等）の画面処理
│   │   ├── ai_model.py      # 🤖 0.01秒でAIの脳みそをロードして動かす場所
│   │   ├── training_article.csv # 🔒 (Git除外) AI学習用のデータ
│   │   └── trained_model.pkl # 🔒 (Git除外) 正解率93%のAIの脳みそ
│   │
│   ├── migrations/          # 🗺️ データベースのマイグレーション履歴・設定
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   └── templates/           # 🎨 【画面の見た目（HTML）の部屋】
│       ├── auth/            # login.html, signup.html 置き場
│       └── main/            # index.html, favorite_list.html 置き場
│
└── app-fastapi/             # ⚡ 【FastAPI版】メインディレクトリ
├── main.py              # アプリ全体の親玉（FastAPI本体とルーター合流の核）
├── db.py                # 🔌 非同期DB接続（AsyncSession）の設定
├── tech_hub.db          # 🔒 (Git除外) ローカルSQLiteデータベース
├── init_database.py     # 🛠️ データベースの初期化スクリプト
│
├── cruds/               # 💾 【データ操作の部屋】（SQL発行・DB処理ロジック）
│   ├── user.py
│   └── favorite.py
│
├── models/              # 📐 【DBモデルの部屋】（SQLAlchemyによるテーブル定義）
│   ├── user.py
│   └── favorite.py
│
├── schemas/             # 📝 【Pydanticバリデーションの部屋】（リクエスト/レスポンス定義）
│   ├── user.py
│   └── favorite.py
│
├── routers/             # 🛣️ 【エンドポイントの部屋】（APIRouterによる機能別ルート定義）
│   ├── user.py          # ログイン・サインアップAPI
│   ├── favorite.py      # お気に入り管理API
│   ├── ai_model.py      # 🤖 AI推論API
│   ├── training_article.csv # 🔒 (Git除外) AI学習用のデータ
│   └── trained_model.pkl # 🔒 (Git除外) AIの脳みそ
│
└── frontapp/            # 🎨 【フロントエンドの部屋】（HTML + JavaScript）
├── favorite.html    # メイン（お気に入り一覧・記事検索窓）の画面
├── favorite.js      # お気に入り・検索・画面遷移・ログイン状態の制御JS
├── login.html       # ログイン画面
├── login.js         # ログインの通信・認証制御JS
├── signup.html      # サインアップ画面
└── signup.js        # サインアップの通信制御JS
```
