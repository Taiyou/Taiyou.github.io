# Hiro Taiyo Hamada website

濱田太陽の個人サイト (<https://taiyou.github.io/>)。`/publications/` は researchmap の公開 API から毎日自動更新される業績一覧。

## サイトの編集

- 本文は `site/pages/` にある。トップは `index.html`、お知らせは `_news.md`、下層ページは `research.md` などの Markdown。
- 画像は `docs/assets/img/` に置き、Markdown から `![説明](ファイル名.jpg)` で参照する。
- YouTube は `@youtube 動画ID タイトル` の1行で並べられる。
- デザインは `site/template.html` と `site/assets/site.css`。
- `site/` か `scripts/build_site.py` を main に push すると `.github/workflows/build-site.yml` が `docs/` を再生成してコミットする。手元で確認するときは次を実行する。

  ```bash
  python3 scripts/build_site.py
  python3 -m http.server -d docs
  ```

# researchmap 業績一覧

researchmap の公開 API から研究者プロフィールと業績情報を定期取得し、GitHub Pages 上で閲覧できる静的ページ。

## セットアップ

1. `config.example.yml` をコピーして `config.yml` を作成し、対象の researchmap permalink を記入する。
2. ローカル実行:

   ```bash
   pip install -r requirements.txt
   python scripts/fetch_researchmap.py
   python -m http.server -d docs
   ```

3. ブラウザで <http://localhost:8000/publications/> を開く。

## デプロイ

- GitHub の Settings → Pages で、Source を `Deploy from a branch`、Branch を `main` / `/docs` に設定する。
- `.github/workflows/update.yml` が毎日 02:00 JST に researchmap からデータを取得して自動コミットする。

## ファイル構成

- `config.yml` — 取得対象の研究者・業績種別の設定
- `scripts/fetch_researchmap.py` — researchmap API からデータを取得
- `scripts/normalize.py` — API レスポンスを内部スキーマへ正規化
- `docs/` — GitHub Pages の公開ルート（静的サイト）
- `docs/publications/` — 業績一覧ページ
- `docs/publications/data/` — 取得スクリプトが生成する JSON
