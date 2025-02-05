# thinkLLM
## 概要
このコードはOllamaを用いて思考機能を持たないLLMでも擬似的に思考を再現するためのものです。
また、GoogleのAPIを用いた簡易的なWeb検索も実装しています。
現時点では日本語での使用を想定しています。

## 使い方
1.Ollamaをインストール
https://ollama.com
2.このコードのデフォルトモデル(TinySwallow-1.5B)を使う場合、ターミナルで以下を実行
ollama run hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF
3.requirements.txtをインストール
4.main.pyを実行

また、Web検索機能を用いる場合はディレクトリ内に.envファイルを作成し、
GOOGLE_API_KEY=YOUR_KEY
CUSTOM_SEARCH_ENGINE_ID=YOUR_ID
の形でAPIキーなどを書き込んでください。

## 環境
### 開発、動作確認環境
mac mini M2 Pro 16GB RAM 512GB SSD
macOS 15.3
Python 3.12.5

### 動作環境
OllamaとPythonの必要ライブラリが動作すればWindowsでも動作すると思います。
