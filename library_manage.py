from datetime import datetime, timedelta
from copy import deepcopy


class Library:
    """図書館管理を行うシンプルなクラス実装。

    - 内部状態: books, members, borrow_records
    - 出力は日本語の CLI 互換メッセージを維持
    - テストのためにメソッドは必要に応じて値を返す
    """

    def __init__(self):
        self.books = []
        self.members = []
        self.borrow_records = []

    # --- 書籍操作 ---
    def add_book(self, book_id, title, author, copies):
        if any(b.get("book_id") == book_id for b in self.books):
            print(f"図書ID「{book_id}」の本は既に存在します。")
            return False

        book = {
            "book_id": book_id,
            "title": title,
            "author": author,
            "copies": copies,
            "available_copies": copies,
        }
        self.books.append(book)
        print(f"図書「{title}」（ID: {book_id}, 著者: {author}, 冊数: {copies}）を追加しました。")
        return True

    def list_books(self):
        if not self.books:
            print("現在、登録されている図書はありません。")
            return []

        print("--- 図書一覧 ---")
        for book in self.books:
            print(
                f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}"
            )
        return deepcopy(self.books)

    def search_book(self, book_id):
        for book in self.books:
            if book.get("book_id") == book_id:
                print(
                    f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}"
                )
                return deepcopy(book)
        print(f"図書ID「{book_id}」の本は存在しません。")
        return None

    def find_books_by_author(self, author):
        matches = []
        for book in self.books:
            a = book.get("author") or ""
            if a.lower() == (author or "").lower():
                matches.append(book)

        if not matches:
            print(f"著者「{author}」の本は見つかりませんでした。")
        else:
            print(f"--- 著者 {author} の本 ---")
            for b in matches:
                print(
                    f"ID: {b['book_id']}, タイトル: {b['title']}, 著者: {b['author']}, 在庫: {b['available_copies']}"
                )
        return deepcopy(matches)

    # --- 会員操作 ---
    def add_member(self, member_id, name):
        if any(m.get("member_id") == member_id for m in self.members):
            print(f"会員ID「{member_id}」の会員は既に存在します。")
            return False
        self.members.append({"member_id": member_id, "name": name})
        print(f"会員「{name}」（ID: {member_id}）を追加しました。")
        return True

    def list_members(self):
        if not self.members:
            print("現在、登録されている会員はいません。")
            return []
        print("--- 会員一覧 ---")
        for member in self.members:
            print(f"ID: {member['member_id']}, 名前: {member['name']}")
        return deepcopy(self.members)

    # --- 貸出/返却 ---
    def borrow_book(self, book_id, member_id, days=14):
        book = next((b for b in self.books if b.get("book_id") == book_id), None)
        if not book:
            print(f"図書ID「{book_id}」の本は存在しません。")
            return False

        member = next((m for m in self.members if m.get("member_id") == member_id), None)
        if not member:
            print(f"会員ID「{member_id}」の会員は存在しません。")
            return False

        if book.get("available_copies", 0) <= 0:
            print(f"図書「{book['title']}」は現在貸出可能な冊数がありません。")
            return False

        record_count = sum(1 for r in self.borrow_records if r.get("member_id") == member_id and not r.get("returned", False))
        if record_count >= 5:
            print(f"貸出可能数は5冊までです。")
            return False

        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=days)

        self.borrow_records.append(
            {
                "book_id": book_id,
                "member_id": member_id,
                "borrow_date": borrow_date.isoformat(),
                "due_date": due_date.isoformat(),
                "returned": False,
            }
        )
        book["available_copies"] = book.get("available_copies", 0) - 1
        print(f"図書「{book['title']}」を会員「{member['name']}」に貸し出しました。\n返却期限: {due_date.isoformat()}")
        return True

    def list_borrowed_books(self):
        print("--- 貸出中の図書一覧 ---")
        borrow_count = 0
        for record in self.borrow_records:
            if not record.get("returned", False):
                book = next((b for b in self.books if b.get("book_id") == record.get("book_id")), None)
                member = next((m for m in self.members if m.get("member_id") == record.get("member_id")), None)
                print(
                    f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}"
                )
                borrow_count += 1
        if borrow_count == 0:
            print("現在、貸出中の図書はありません。")
        return [deepcopy(r) for r in self.borrow_records if not r.get("returned", False)]

    def return_book(self, book_id, member_id):
        record = next(
            (r for r in self.borrow_records if r.get("book_id") == book_id and r.get("member_id") == member_id and not r.get("returned", False)),
            None,
        )
        if not record:
            print(f"図書ID「{book_id}」本を会員ID「{member_id}」の会員は借りていません。")
            return False

        record["returned"] = True
        book = next((b for b in self.books if b.get("book_id") == book_id), None)
        if book:
            book["available_copies"] = book.get("available_copies", 0) + 1
            print(f"図書「{book['title']}」が返却されました。")
        else:
            print(f"図書ID「{book_id}」の本は登録されていませんが、返却記録を更新しました。")
        return True

    def calculate_fines(self, per_day=100):
        """延滞料金を計算して表示する。返り値は (member_id, book_id, fine) のリスト。

        - 日付は ISO 形式で保存されていることを前提に解析します。
        - 今日の日付は実行時のローカル日付を使います。
        """
        print("--- 延滞料金一覧 ---")
        results = []
        today = datetime.now().date()
        for record in self.borrow_records:
            if not record.get("returned", False):
                due_date_str = record.get("due_date")
                try:
                    due_date = datetime.fromisoformat(due_date_str).date()
                except Exception:
                    # 不正な日付フォーマットは無視
                    continue
                overdue_days = max((today - due_date).days, 0)
                fine = overdue_days * per_day
                book = next((b for b in self.books if b.get("book_id") == record.get("book_id")), None)
                member = next((m for m in self.members if m.get("member_id") == record.get("member_id")), None)
                if book and member:
                    print(
                        f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 延滞料金: {fine}円"
                    )
                    results.append((member.get("member_id"), book.get("book_id"), fine))
        if not results:
            print("現在、貸出中の図書はありません。")
        return results


# モジュールレベルで互換性を保つシンプルなインスタンス
lib = Library()

# 既存スクリプトやテストがモジュール関数を期待する可能性を考慮して、
# 下記にラッパー関数を残す（内部で lib に委譲）。

def add_book(book_id, title, author, copies):
    return lib.add_book(book_id, title, author, copies)

def list_books():
    return lib.list_books()

def search_book(book_id):
    return lib.search_book(book_id)

def find_books_by_author(author):
    return lib.find_books_by_author(author)

def add_member(member_id, name):
    return lib.add_member(member_id, name)

def list_members():
    return lib.list_members()

def borrow_book(book_id, member_id):
    return lib.borrow_book(book_id, member_id)

def list_borrowed_books():
    return lib.list_borrowed_books()

def return_book(book_id, member_id):
    return lib.return_book(book_id, member_id)

def calculate_fines():
    return lib.calculate_fines()


def find_books_by_author(author):
    """
    著者名で登録されている本を検索して一覧を返します。

    - 一致は大文字小文字を区別しません。
    - 返り値は該当する書誌情報の辞書リストです（テストや他のロジックで利用しやすいように返します）。
    - 画面表示も既存のコードスタイルに合わせて行います。
    """
    matches = []
    for book in books:  
        try:
            if book.get("author", "").lower() == author.lower():
                matches.append(book)
        except Exception:
            # 安全に動くように、想定外のデータは無視します
            continue

    if not matches:
        print(f"著者「{author}」の本は見つかりませんでした。")
    else:
        print(f"--- 著者 {author} の本 ---")
        for b in matches:
            print(f"ID: {b['book_id']}, タイトル: {b['title']}, 著者: {b['author']}, 在庫: {b['available_copies']}")

def _cli():
    """シンプルな対話式 CLI（モジュール関数ラッパーを利用）。"""
    while True:
        print("図書館管理システムメニュー:")
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書を検索 (ID)")
        print("4: 会員を追加")
        print("5: 会員一覧を表示")
        print("6: 図書を貸し出す")
        print("7: 貸出中の図書一覧を表示")
        print("8: 図書を返却")
        print("9: 延滞料金を計算")
        print("10: 終了")

        try:
            choice = int(input("操作を選択してください（1-10）: "))

            if choice == 1:
                book_id = input("図書IDを入力してください: ")
                title = input("タイトルを入力してください: ")
                author = input("著者名を入力してください: ")
                copies = int(input("冊数を入力してください: "))
                add_book(book_id, title, author, copies)

            elif choice == 2:
                list_books()

            elif choice == 3:
                book_id = input("検索する図書IDを入力してください: ")
                search_book(book_id)

            elif choice == 4:
                member_id = input("会員IDを入力してください: ")
                name = input("名前を入力してください: ")
                add_member(member_id, name)

            elif choice == 5:
                list_members()

            elif choice == 6:
                book_id = input("貸し出す図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                borrow_book(book_id, member_id)

            elif choice == 7:
                list_borrowed_books()

            elif choice == 8:
                book_id = input("返却する図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                return_book(book_id, member_id)

            elif choice == 9:
                calculate_fines()

            elif choice == 10:
                print("図書館管理システムを終了します。")
                break

            else:
                print("無効な選択です。1-10の数字を入力してください。")

        except ValueError as e:
            print(f"入力エラー: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    _cli()