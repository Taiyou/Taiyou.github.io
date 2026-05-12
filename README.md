# researchmap 業績サイト

researchmap の公開 API から研究者プロフィールと業績情報を定期取得し、GitHub Pages 上で閲覧できる静的サイト。

## セットアップ

1. `config.example.yml` をコピーして `config.yml` を作成し、対象の researchmap permalink を記入する。
2. ローカル実行:

   ```bash
   pip install -r requirements.txt
   python scripts/fetch_researchmap.py
   python -m http.server -d docs
   ```

3. ブラウザで <http://localhost:8000> を開く。

## デプロイ

- GitHub の Settings → Pages で、Source を `Deploy from a branch`、Branch を `main` / `/docs` に設定する。
- `.github/workflows/update.yml` が毎日 02:00 JST に researchmap からデータを取得して自動コミットする。

## ファイル構成

- `config.yml` — 取得対象の研究者・業績種別の設定
- `scripts/fetch_researchmap.py` — researchmap API からデータを取得
- `scripts/normalize.py` — API レスポンスを内部スキーマへ正規化
- `docs/` — GitHub Pages の公開ルート（静的サイト）
- `docs/data/` — 取得スクリプトが生成する JSON
