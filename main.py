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
        thinking_prompt = f"質問: {user_input}\n\n質問に答えるための思考プロセスをステップ形式で日本語で記述してください。ステップの中に、質問に答えるためにネット検索が必要かどうかを判断するステップを必ず含めてください。ネット検索が必要な場合は「ネット検索が必要」という言葉を思考プロセスの中に含めてください。思考プロセスのみを記述してください。"
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

        # 2. 検索結果がある場合は、検索結果を元にもう一度思考する
        search_analysis_result = ""
        if search_results_content:
            print("検索結果を分析...")
            search_analysis_prompt = f"質問: {user_input}\n\n検索結果:\n{search_results_content}\n\n上記の質問と検索結果を踏まえ、回答を生成するための思考プロセスを日本語でステップ形式で記述してください。検索結果をどのように利用して回答を生成するかを具体的に記述してください。思考プロセスのみを記述してください。"
            search_analysis_response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': search_analysis_prompt}], stream=True)
            print("\n検索結果分析による思考プロセス:")
            for part in search_analysis_response:
                search_analysis_result += part['message']['content']
                print(part['message']['content'], end="", flush=True)
            print("\n")
        else:
            print("検索結果分析はスキップされました。")

        # 3. 思考結果と検索結果分析を用いて回答を生成
        answer_prompt_base = f"思考プロセス:\n{thinking_result}\n\n"
        if search_analysis_result:
            answer_prompt_base += f"検索結果分析による思考プロセス:\n{search_analysis_result}\n\n"
        answer_prompt = answer_prompt_base + f"ユーザーからの質問: {user_input}\n\n上記の思考プロセスと検索結果分析に基づいてユーザーに対する質問への回答を生成してください。なお、思考プロセスと検索結果分析を再度出力する必要はなく、回答のみを生成してください。回答は日本語で行なってください。"

        answer_response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': answer_prompt}], stream=True)
        print("\n回答:")
        for part in answer_response:
            print(part['message']['content'], end="", flush=True)
        print("\n---")

if __name__ == "__main__":
    main()
