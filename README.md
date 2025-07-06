# thinkLLM
## 概要
このプロジェクトは、Ollamaを使用して思考機能を持たないLLMでも擬似的に思考を再現することを目的としています。
さらに、GoogleのAPIを利用した簡易的なWeb検索機能も実装しています。
現時点では日本語での使用を想定しています。

## 使い方
1. Ollamaをインストールします。  
   [Ollamaの公式サイト](https://ollama.com)からインストールできます。
2. デフォルトモデル（gemma3:4b）を使用する場合、ターミナルで以下を実行します。  
   ```bash
   ollama run gemma3:4b
   ```
3. `requirements.txt`に記載されたライブラリをインストールします。  
   ```bash
   pip install -r requirements.txt
   ```
4. `main.py`を実行します。  
   ```bash
   python main.py

また、Web検索機能を使用する場合は、プロジェクトディレクトリ内に`.env`ファイルを作成し、以下の形式でAPIキーなどを記述してください。  
```
GOOGLE_API_KEY=YOUR_KEY
CUSTOM_SEARCH_ENGINE_ID=YOUR_ID
```

## 環境
### 開発および動作確認環境
- Mac mini M2 Pro 16GB RAM 512GB SSD
- macOS 15.3
- Python 3.12.5

### 動作環境
OllamaとPythonの必要ライブラリが動作すれば、Windowsでも動作する可能性があります。
