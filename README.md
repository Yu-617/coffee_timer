# ☕️ Coffee Timer

コーヒーの適切な抽出メソッドをタイマーでアシストするWebアプリケーションです。
人数や湯量を指定するだけで、最適なコーヒー豆の量を自動計算する機能も備えています。

## 📸 イメージ (Visuals)
<img width="376" height="360" alt="Screenshot 2026-02-25 at 20 26 16" src="https://github.com/user-attachments/assets/8117a19c-a391-469d-9802-c9f42b129928" />


## ✨ 主な機能 (Features)
- **自動計算機能:** 抽出したい人数や目標の湯量を入力するだけで、必要なコーヒー豆の量を瞬時に算出します。
- **抽出ナビゲーション:** [適切な抽出メソッド](https://www.youtube.com/watch?v=lJNPp-onikk&t=23s)に基づき、お湯を注ぐタイミングと量を視覚的なタイマーでアシストします。


## 🛠 技術スタック (Tech Stack)
- **Language:** Python 3.1
- **Framework:** Streamlit
- **Library:** Pandas
- **AI Assistance:** 本アプリケーションの設計およびコード生成の一部は、Google Geminiのサポートを受けて開発されました。

## 🚀 使い方 (Usage / Installation)

### Webアプリとして利用する場合（ユーザー向け）
**[Coffee Timer](https://coffeetimer.streamlit.app/)** 👈️からアプリにアクセスできます。

> **⚠️ 注意事項**
> 本リポジトリのソースコードは公開されていますが、Webアプリの利用にはパスワードロックがかかっています。環境変数（Streamlit Secrets）で管理されているため、パスワードをご存知の方のみがログイン可能です。

### ローカル環境で動かす場合（開発者向け）
ご自身のPCでコードを実行・編集したい場合は、以下の手順で環境を構築してください。

1. **リポジトリのクローン**
   ```bash
   git clone [https://github.com/Yu-617/coffee-timer.git](https://github.com/Yu-617/coffee-timer.git)
   cd coffee-timer
   ```
3. 必要なパッケージのインストール

   ```bash
   pip install -r requirements.txt
   ```
3. Secrets（パスワード）の設定
   ローカルで動かすために、パスワードを設定する秘密のファイルを作成します。
   プロジェクトのルートディレクトリに `.streamlit` フォルダを作成し、その中に `secrets.toml` というファイルを作成して以下を記述してください。
   
   ```Ini, TOML
   # .streamlit/secrets.toml
   APP_PASSWORD = "お好きなパスワード"
   ```

   ※ .streamlit フォルダは .gitignore に追加し、絶対にGitHubにプッシュしないようご注意ください。

4. アプリの起動

   ```bash
   streamlit run app.py
   ```

5. アプリの終了

   ctrl+C

## 🖋️ 作成者 (Author)
[Yu-617](https://github.com/Yu-617)
