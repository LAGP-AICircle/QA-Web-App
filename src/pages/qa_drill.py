import streamlit as st
from typing import List, Dict
from utils.openai_utils import get_openai_client
import os
from datetime import datetime
import json

# OpenAIクライアントの初期化
if "openai_client" not in st.session_state:
    st.session_state.openai_client = get_openai_client()


def load_qa_problems() -> List[Dict]:
    """QA問題データの読み込み"""
    return [
        {
            "ref_number": "1.1",
            "ref_page": "2～4",
            "category": "テストとは何か？",
            "text": "ソフトウェアが期待通りに動かないことによる不都合を4つ答えよ。",
            "answer_count": 4,
            "correct_answers": ["経済的な損失", "時間の浪費", "信用の失墜", "傷害と死亡事故"],
            "evaluation_criteria": """
            以下の基準で回答を評価してください：
            1. 経済的損失に関する表現（金銭的損失、経済的影響なども可）
            2. 時間的損失に関する表現（時間のロス、工数の無駄なども可）
            3. 信用に関する表現（評判の低下、ブランドイメージの毀損なども可）
            4. 人的被害に関する表現（人命に関わる事故、健康被害なども可）
            """,
        },
        {
            "ref_number": "1.1",
            "ref_page": "4",
            "category": "テストとは何か？",
            "text": "テスト前実行作業を4つ答えよ。",
            "answer_count": 4,
            "correct_answers": ["テスト計画", "テスト分析", "テスト設計", "テスト実装"],
        },
        {
            "ref_number": "1.1",
            "ref_page": "5",
            "category": "テストとは何か？",
            "text": "テスト実行時の作業として、テスト実行の他にテスト工程で行うのは何か2つ答えよ。",
            "answer_count": 2,
            "correct_answers": ["実行結果のチェック", "テスト終了基準の評価"],
        },
        {
            "ref_number": "1.1.1",
            "ref_page": "9",
            "category": "テストの目的",
            "text": "テストのフェーズ、視点が異なっていると、テストの目的も異なります。主なテストの目的を9つ答えよ。",
            "answer_count": 9,
            "correct_answers": [
                "要件、ユーザーストーリー、設計、およびコードなどの作業成果物の評価",
                "明確にしたすべての要件を満たしていることの検証",
                "テスト対象が完成し、ユーザーやその他ステークホルダーの期待通りの動作内容であることの妥当性確認",
                "テスト対象の品質に対する信頼を積み重ねて、所定のレベルにあることの確証",
                "欠陥の作り込みの防止",
                "故障や欠陥の発見",
                "ステークホルダーが意志決定できる、特にテスト対象の品質レベルについての十分な情報の提供",
                "(以前に検出されなかつた故障が運用環境で発生するなどの)不適切なソフトウエア品質のリスクレベルの低減",
                "契約上、法律上、または規則上の要件や標準を遵守する、そして/またはテスト対象がそのような要件や標準に準拠していることの検証",
            ],
        },
        {
            "ref_number": "1.2.3",
            "ref_page": "21",
            "category": "エラー、欠陥、および故障",
            "text": "いくつかの原因から勘違いや思い込みが発生することにより、１つの成果物のみならず、他の欠陥を発生させることもある行為を、何と呼ぶか答えよ。",
            "answer_count": 1,
            "correct_answers": ["エラー"],
        },
        {
            "ref_number": "1.2.3",
            "ref_page": "22",
            "category": "エラー、欠陥、および故障",
            "text": "誤りによって、作業成果物やプログラムに埋め込んで実装されるものは何か答えよ。",
            "answer_count": 1,
            "correct_answers": ["欠陥"],
        },
        {
            "ref_number": "1.2.3",
            "ref_page": "22",
            "category": "エラー、欠陥、および故障",
            "text": "コンポーネントやシステムの問題により、実行されたプログラムに期待通りではない不正な結果が得られた場合、この結果のことを何と呼ぶか答えよ。",
            "answer_count": 1,
            "correct_answers": ["故障"],
        },
        {
            "ref_number": "1.3.1",
            "ref_page": "29",
            "category": "ソフトウェアテストの原則",
            "text": "テストの7原則、原則1においてテストで示すことが出来ないのは何か答えよ。",
            "answer_count": 2,
            "correct_answers": ["欠陥がないこと(もしくは故障しないこと)", "故障しない＝欠陥がない"],
        },
        {
            "ref_number": "1.3.1",
            "ref_page": "30",
            "category": "ソフトウェアテストの原則",
            "text": "テストの7原則、原則2において全数テストが不可能なためテストの現場ではソフトウェアの性質や目的、使われ方などからどのようにテストを行うか2つ答えよ。",
            "answer_count": 2,
            "correct_answers": ["重点的にテストする場所を絞る", "優先順位を決める"],
        },
        {
            "ref_number": "1.3.1",
            "ref_page": "31",
            "category": "ソフトウェアテストの原則",
            "text": "テストの7原則、原則3において欠陥を見つけるのが遅くなった際のリスクを4つ答えよ。",
            "answer_count": 4,
            "correct_answers": [
                "欠陥を特定するのに時間がかかる",
                "欠陥の修正に時間がかかってしまう",
                "間違った直し方をされる可能性がある",
                "他のソフトウェアに流用された場合は関連する箇所を探すのに時間がかかる",
            ],
        },
        {
            "ref_number": "1.3.1",
            "ref_page": "32",
            "category": "ソフトウェアテストの原則",
            "text": "テストの7原則、原則4において効率的にテストを行うために何に基づいて重点的にテストをする箇所を絞り込むのがよいか。",
            "answer_count": 1,
            "correct_answers": ["予測結果"],
        },
        {
            "ref_number": "1.3.1",
            "ref_page": "33",
            "category": "ソフトウェアテストの原則",
            "text": "テストの7原則、原則5において『殺虫剤のパラドックス』の意味として耐性の出来てしまった害虫に対して、新しい成分の殺虫剤を開発していくことに置き換えているのは何か答えよ。",
            "answer_count": 1,
            "correct_answers": ["新しい内容のテストを常に作っていくこと"],
        },
        {
            "ref_number": "1.3.1",
            "ref_page": "33",
            "category": "ソフトウェアテストの原則",
            "text": "テストの7原則、原則6において、全てのソフトウェアやソフトウェア開発ライフサイクルにないものは何か答えよ。",
            "answer_count": 1,
            "correct_answers": ["共通するテスト設計、テストの方法"],
        },
        {
            "ref_number": "1.3.1",
            "ref_page": "34",
            "category": "ソフトウェアテストの原則",
            "text": "テストの7原則、原則7において修正を行う際に確認するべき大切な作業は何か2つ答えよ。",
            "answer_count": 2,
            "correct_answers": ["性能や機能に影響はないかどうか", "システム全体に影響はないかどうか"],
        },
        {
            "ref_number": "2.1.1",
            "ref_page": "85",
            "category": "ソフトウェアテストの原則",
            "text": "ウォーターフォールモデルのどのような順番で開発が進んでいくか、上流工程から順に4工程を答えよ。",
            "answer_count": 4,
            "correct_answers": ["要件定義", "設計", "コーディング", "テスト"],
        },
        {
            "ref_number": "2.1.1",
            "ref_page": "86",
            "category": "V字モデル(シーケンシャルモデル)",
            "text": "V字モデルのテスト工程はどのように分けられるか上流工程からの工程順に4つ答えよ。",
            "answer_count": 4,
            "correct_answers": ["コンポーネントテスト", "統合テスト", "システムテスト", "受け入れテスト"],
        },
        {
            "ref_number": "2.2.3",
            "ref_page": "110",
            "category": "システムテスト テストタイプ",
            "text": "統合テストで行われるテストのタイプは、何テストが含まれるか、４つ答えよ。",
            "answer_count": 4,
            "correct_answers": ["機能テスト", "非機能テスト", "ホワイトボックステスト", "リグレッションテスト"],
        },
        {
            "ref_number": "2.3.1",
            "ref_page": "122",
            "category": "機能テスト",
            "text": "テスト工程では観点を定めてテストを行います。機能テストではどういった観点でテストを行うか答えよ。",
            "answer_count": 1,
            "correct_answers": ["機能が仕様通りに実装されているか"],
        },
        {
            "ref_number": "2.3.2",
            "ref_page": "125",
            "category": "非機能テスト",
            "text": "非機能テストの目的とは何か、答えよ。",
            "answer_count": 1,
            "correct_answers": [
                "コンポーネントやシステムの特性、例えば性能、使用性やセキュリティなどの特性を評価すること"
            ],
        },
        {
            "ref_number": "2.3.2",
            "ref_page": "126",
            "category": "非機能テスト",
            "text": "使用性テスト（usability testing）で評価するのはなにか答えよ。",
            "answer_count": 1,
            "correct_answers": [
                "特定のユーザーが特定の使用状況の下でシステムを使用する際の有効性、効率性、および満足度の度合い"
            ],
        },
        {
            "ref_number": "2.3.2",
            "ref_page": "127",
            "category": "非機能テスト",
            "text": "非機能テストはどのテストレベルで実施することが出来るか、4つのレベルを答えよ。",
            "answer_count": 4,
            "correct_answers": [
                "コンポーネントテストレベル",
                "統合テストレベル",
                "システムテストレベル",
                "受け入れテストレベル",
            ],
        },
        {
            "ref_number": "2.3.4",
            "ref_page": "132",
            "category": "変更部分のテスト",
            "text": "確認テストの実施タイミングを答えよ。",
            "answer_count": 1,
            "correct_answers": ["欠陥を修正した後"],
        },
        {
            "ref_number": "2.4",
            "ref_page": "139",
            "category": "回帰テスト",
            "text": "メンテナンステストで実施しなければならないテストの範囲を決める要因には何があるか、３つ答えよ。",
            "answer_count": 3,
            "correct_answers": ["変更のリスクの度合い", "現状システムの規模", "変更の規模"],
        },
        {
            "ref_number": "2.4.1",
            "ref_page": "140",
            "category": "メンテナンス（保守）テスト",
            "text": "保守テストを行わなければならないケースを4つ答えよ。",
            "answer_count": 4,
            "correct_answers": [
                "ソフトウェアの変更作業を行ったとき",
                "ソフトウェアの運用環境が変わったとき",
                "新しい環境への移行作業を行ったとき",
                "ソフトウェアを廃棄したとき",
            ],
        },
        {
            "ref_number": "2.4.2",
            "ref_page": "142",
            "category": "メンテナンスの影響度分析",
            "text": "影響度分析とは何か、答えよ。",
            "answer_count": 1,
            "correct_answers": [
                "さまざまなメンテナンスを行い、ソフトウェアやシステムをリリースする際には、それぞれのケースにおける作業(変更、追加、削除など)による影響を調べること"
            ],
        },
    ]


def evaluate_answer(user_answer: str, correct_answer: str, evaluation_criteria: str = None) -> bool:
    """LLMを使用して回答を評価"""
    try:
        client = get_openai_client()
        if not client:
            st.error("OpenAIクライアントの初期化に失敗しました")
            return False

        # システムプロンプトの作成
        system_prompt = (
            "あなたはテスト技術の専門家です。ユーザーの回答が模範解答と意味的に一致しているかを判断してください。"
        )
        if evaluation_criteria:
            system_prompt += f"\n\n評価基準：\n{evaluation_criteria}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": f"ユーザーの回答: {user_answer}\n模範解答: {correct_answer}\nこれらは意味的に一致していますか？YesまたはNoで答えてください。",
                },
            ],
        )
        return response.choices[0].message.content.strip().lower() == "yes"
    except Exception as e:
        st.error(f"回答の評価中にエラーが発生しました: {str(e)}")
        return False


def check_answers(problem: Dict, user_answers: List[str]) -> tuple[bool, str]:
    """回答をチェックして結果を返す"""
    if len(user_answers) != len(problem["correct_answers"]):
        return False, "回答数が正しくありません。"

    # 完全一致チェック
    if sorted(user_answers) == sorted(problem["correct_answers"]):
        return True, "正解です！"

    # 部分一致チェック
    correct_count = 0
    evaluation_criteria = problem.get("evaluation_criteria")
    for user_ans, correct_ans in zip(sorted(user_answers), sorted(problem["correct_answers"])):
        if evaluate_answer(user_ans, correct_ans, evaluation_criteria):
            correct_count += 1

    if correct_count == len(problem["correct_answers"]):
        return True, "正解です！（意味的に一致）"
    else:
        return False, f"不正解です。（{correct_count}/{len(problem['correct_answers'])}が正解）"


def generate_report(problems: List[Dict], results: List[Dict]) -> str:
    """採点結果のレポートを生成"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 採点結果の集計
    exact_match = 0
    semantic_match = 0
    incorrect = 0
    semantic_match_details = []
    incorrect_details = []

    report = f"""QAドリル採点結果レポート
生成日時: {now}
受験者: {st.session_state.get('logged_in_email', '未ログイン')}

=== 採点結果サマリー ===
"""

    # 各問題の結果を分析
    for i, (problem, result) in enumerate(zip(problems, results)):
        if result["is_correct"]:
            if result["message"] == "正解です！":
                exact_match += 1
            else:
                semantic_match += 1
                semantic_match_details.append((i + 1, problem, result))
        else:
            incorrect += 1
            incorrect_details.append((i + 1, problem, result))

    report += f"""【正解】完全一致：{exact_match}
【正解】AI採点による意味の一致：{semantic_match}
【不正解】どちらにも当てはまらない：{incorrect}

"""

    # 意味の一致による正解の詳細
    if semantic_match_details:
        report += "=== AI採点による意味の一致 ===\n\n"
        for problem_num, problem, result in semantic_match_details:
            report += f"""問題{problem_num}： {problem['text']}
記入：{', '.join(result['user_answers'])}
解答：{', '.join(problem['correct_answers'])}

"""

    # 不正解の詳細
    if incorrect_details:
        report += "=== 不正解 ===\n\n"
        for problem_num, problem, result in incorrect_details:
            report += f"""問題{problem_num}：{problem['text']}
記入：{', '.join(result['user_answers'])}
解答：{', '.join(problem['correct_answers'])}

"""

    # 詳細結果
    report += "=== 詳細結果 ===\n"
    for i, (problem, result) in enumerate(zip(problems, results)):
        report += f"""問題{i + 1}: {problem['text']}
参照項番: {problem['ref_number']}
参照ページ: {problem['ref_page']}
項目: {problem['category']}
結果: {'正解' if result['is_correct'] else '不正解'}
ユーザーの回答と採点: """

        for j, user_ans in enumerate(result["user_answers"]):
            report += f"\n {j+1}.{user_ans}"
            if user_ans == problem["correct_answers"][j]:
                report += "\n  採点結果：【正解】完全一致"
            elif result["is_correct"] and "意味的に一致" in result["message"]:
                report += "\n  採点結果：【正解】AI採点による意味が一致"
            else:
                report += "\n  採点結果：【不正解】"
        report += "\n\n"

    return report


def save_report(report: str) -> str:
    """レポートをファイルに保存"""
    try:
        # レポート保存用のディレクトリを作成
        reports_dir = os.path.join("reports")
        os.makedirs(reports_dir, exist_ok=True)

        # ファイル名を生成（タイムスタンプとユーザーメールを含む）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_email = st.session_state.get("logged_in_email", "anonymous")
        user_email = user_email.split("@")[0]  # メールアドレスのドメイン部分を除去
        filename = f"qa_drill_report_{user_email}_{timestamp}.txt"
        filepath = os.path.join(reports_dir, filename)

        # レポートを保存
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)

        return filepath
    except Exception as e:
        st.error(f"レポートの保存中にエラーが発生しました: {str(e)}")
        return None


def show_question(question: Dict, index: int):
    """問題の表示"""
    # 問題ヘッダー
    st.markdown(
        f"""
    ---    
    #### 【問題{index + 1}】  {question['text']}
    ---
    ###### 参照項番：{question['ref_number']}　参照ページ：{question['ref_page']}　項目：{question['category']}
    ---  
    """,
        unsafe_allow_html=False,
    )

    # 解答欄
    st.markdown("##### 解答欄：")
    user_answers = []
    for i in range(question["answer_count"]):
        key = f"q{index}_answer_{i}"
        answer = st.text_input(f"回答 {i+1}", key=key)
        if answer:
            user_answers.append(answer)

    # 採点ボタン
    if st.button(f"採点（問題{index + 1}）", key=f"grade_{index}"):
        is_correct, message = check_answers(question, user_answers)
        if is_correct:
            st.success(message)
        else:
            st.error(message)

    st.markdown("---")


def evaluate_all_answers(problems: List[Dict]) -> List[Dict]:
    """全ての回答を評価"""
    results = []
    for i, problem in enumerate(problems):
        user_answers = []
        for j in range(problem["answer_count"]):
            key = f"q{i}_answer_{j}"
            answer = st.session_state.get(key, "").strip()
            if answer:
                user_answers.append(answer)

        is_correct, message = check_answers(problem, user_answers)
        results.append({"is_correct": is_correct, "message": message, "user_answers": user_answers})

    return results


def show_qa_drill_page():
    """QAドリルページを表示"""
    # 現在のページがQAドリルでない場合は即座に終了
    if st.session_state.page != "qa_drill":
        return

    # ログインチェック
    if not st.session_state.get("password_correct", False):
        st.error("ログインが必要です")
        st.stop()

    # カスタムCSSを追加
    st.markdown(
        """
        <style>
        .small-font {
            font-size: 0.9em !important;
        }
        .small-font p {
            font-size: 0.9em !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # メインコンテンツ
    st.title("QA Training Drill")
    st.write("QA事業部のドリルです。各問題をよく読んで回答してください。")

    # 問題データの読み込み
    problems = load_qa_problems()

    # すべての問題を表示
    for i, problem in enumerate(problems):
        show_question(problem, i)

    # 回答送信ボタン
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("回答を送信", key="submit_answers", use_container_width=True):
            with st.spinner("採点中..."):
                # 全ての回答を評価
                results = evaluate_all_answers(problems)

                # レポートを生成
                report = generate_report(problems, results)

                # レポートを保存
                report_path = save_report(report)

                if report_path:
                    st.success(f"採点が完了しました！レポートが保存されました: {report_path}")
                    # レポートの内容をダウンロード可能にする
                    with open(report_path, "r", encoding="utf-8") as f:
                        report_content = f.read()
                    st.download_button(
                        label="レポートをダウンロード",
                        data=report_content,
                        file_name=os.path.basename(report_path),
                        mime="text/plain",
                    )
                else:
                    st.error("レポートの保存に失敗しました。")

    with col2:
        if st.button("回答をクリア", key="clear_answers", use_container_width=True):
            # セッション状態から回答をクリア
            keys_to_remove = [key for key in st.session_state.keys() if key.startswith("q")]
            for key in keys_to_remove:
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    show_qa_drill_page()
