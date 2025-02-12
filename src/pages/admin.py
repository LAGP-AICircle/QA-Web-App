import streamlit as st
from auth import get_all_users, migrate_existing_users, save_user, is_admin, delete_user


def show_admin_page():
    """管理者ページを表示"""
    # 管理者権限チェック
    if "logged_in_email" not in st.session_state:
        st.error("ログインしてください")
        return

    if not is_admin(st.session_state.logged_in_email):
        st.error("管理者権限がありません")
        return

    st.title("管理者ページ")

    # 管理者機能のタブ
    tab1, tab2, tab3 = st.tabs(["ユーザー管理", "ユーザー追加", "データ移行"])

    # ユーザー管理タブ
    with tab1:
        st.header("登録ユーザー一覧")

        # 更新ボタン
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("一覧を更新", key="refresh_users", use_container_width=True):
                st.rerun()

        # ユーザー一覧を表示
        users = get_all_users()
        if users:
            # データフレームとして表示
            import pandas as pd

            df = pd.DataFrame(users)
            # カラム名を日本語に変更
            df.columns = ["メールアドレス", "管理者", "作成日時", "更新日時"]
            st.dataframe(df, use_container_width=True)

            # 登録ユーザー数を表示
            st.info(f"登録ユーザー数: {len(users)}名")

            # ユーザー削除セクション
            st.markdown("---")
            st.subheader("ユーザー削除")

            # 削除対象のユーザーを選択
            delete_email = st.selectbox(
                "削除するユーザーを選択",
                options=[user["email"] for user in users],
                help="削除したユーザーは元に戻せません。慎重に選択してください。",
            )

            # 削除の確認
            if delete_email == st.session_state.logged_in_email:
                st.warning("⚠️ 自分自身は削除できません")
            else:
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    delete_clicked = st.button("削除", type="primary", use_container_width=True)

                if delete_clicked:
                    # 確認ダイアログを表示（全幅で）
                    if st.session_state.get("confirm_delete") != delete_email:
                        st.session_state.confirm_delete = delete_email
                        st.warning(
                            f"本当に {delete_email} を削除しますか？\n"
                            "もう一度「削除」ボタンをクリックすると削除されます。",
                            icon="⚠️",
                        )
                    else:
                        # 2回目のクリックで削除実行
                        if delete_user(delete_email):
                            st.success(f"ユーザー {delete_email} を削除しました")
                            del st.session_state.confirm_delete
                            st.rerun()
                        else:
                            st.error("削除に失敗しました")
        else:
            st.info("登録ユーザーがいません")

    # ユーザー追加タブ
    with tab2:
        st.header("ユーザー追加")

        # 入力フォーム用のカラムを作成
        col1, col2 = st.columns([1, 1])

        with col1:
            # 成功メッセージの表示（セッション状態から）
            if st.session_state.get("user_added"):
                st.success(f"ユーザー {st.session_state.user_added} を登録しました！")
                del st.session_state.user_added

            with st.form("add_user_form"):
                new_email = st.text_input(
                    "メールアドレス", help="@lberc-g.jp または @alt-g.jp のメールアドレスを入力してください"
                )
                new_password = st.text_input("パスワード", type="password")
                confirm_password = st.text_input("パスワード（確認）", type="password")
                is_admin_user = st.checkbox(
                    "管理者権限を付与", help="管理者権限を持つユーザーは、ユーザー管理などの特別な機能を使用できます"
                )

                submitted = st.form_submit_button("ユーザーを追加", use_container_width=True)
                if submitted:
                    if not new_email or not new_password or not confirm_password:
                        st.error("すべての項目を入力してください")
                    elif new_password != confirm_password:
                        st.error("パスワードが一致しません")
                    else:
                        try:
                            save_user(new_email, new_password, is_admin_user)
                            # 成功メッセージ用のセッション状態を設定
                            st.session_state.user_added = new_email
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

        # 右側に説明を表示
        with col2:
            st.markdown(
                """
            #### 📝 ユーザー登録について
            
            1. メールアドレスは社内メールを使用してください
            2. パスワードは8文字以上を推奨します
            3. 管理者権限は必要な場合のみ付与してください
            """
            )

    # データ移行タブ
    with tab3:
        st.header("データ移行")
        st.write("credentials.jsonからSQLiteデータベースへデータを移行します。")

        if st.button("移行を実行", key="migrate_data"):
            try:
                migrate_existing_users()
                st.success("データ移行が完了しました")
            except Exception as e:
                st.error(f"データ移行中にエラーが発生しました: {str(e)}")
