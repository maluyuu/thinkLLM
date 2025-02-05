import ollama
import os
from dotenv import load_dotenv
from search_module import search_google_api, fetch_site_content

load_dotenv()

def main():
    model_name = "hf.co/SakanaAI/TinySwallow-1.5B-Instruct-GGUF" # デフォルトモデル。ユーザーに確認後に変更可能
    num_search_results = 3  # 検索結果から上位何件のサイト内容を取得するか

    while True:
        user_input = input("質問を入力してください ('終了'でプログラムを終了): ")
        if user_input.lower() == '終了':
            break

        # 1. モデルに回答方法を考えさせる (ネット検索が必要かどうかも判断させる)
        thinking_prompt = f"質問: {user_input}\n\nこの質問に答えるための思考プロセスをステップ形式で記述してください。ステップの中に、この質問に答えるためにネット検索が必要かどうかを判断するステップを必ず含めてください。ネット検索が不要と判断した場合は、ネット検索を行うステップは不要です。思考プロセスのみを記述してください。"
        thinking_response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': thinking_prompt}], stream=True)
        print("\n思考プロセス:")
        thinking_result = ""
        for part in thinking_response:
            thinking_result += part['message']['content']
            print(part['message']['content'], end="", flush=True)
        print("\n")

        # 思考プロセスからネット検索が必要かどうかを判断
        need_search = "ネット検索が必要" in thinking_result

        # ネット検索が必要な場合は検索を実行し、サイト内容を取得
        search_results_content = ""
        if need_search:
            print("ネット検索を実行...")
            search_results = search_google_api(user_input)
            if search_results:
                print("\n検索結果:")
                for i, result in enumerate(search_results[:num_search_results]): # 上位N件のみ表示
                    print(f"[{i+1}] {result['title']} - {result['url']}")
                    content = fetch_site_content(result['url'])
                    search_results_content += f"\n\n[{result['title']}]\n{content}"
            else:
                print("検索結果が見つかりませんでした。")
        else:
            print("ネット検索は不要と判断されました。")

        # 2. 思考結果と検索結果を用いて回答を生成
        answer_prompt_base = f"思考プロセス:\n{thinking_result}\n\nユーザーからの質問: {user_input}\n\n上記の思考プロセスに基づいてユーザーに対する質問への回答を生成してください。なお、思考プロセスを再度出力する必要はなく、回答のみを生成してください。"
        if search_results_content:
            answer_prompt = answer_prompt_base + f"\n\n参考資料:\n{search_results_content}"
        else:
            answer_prompt = answer_prompt_base

        answer_response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': answer_prompt}], stream=True)
        print("\n回答:")
        for part in answer_response:
            print(part['message']['content'], end="", flush=True)
        print("\n---")

if __name__ == "__main__":
    main()
