public class Bankaccount {

    private String accountNumber;
    private int balance;

    public Bankaccount(String accountNumber, int balance) {
        this.accountNumber = accountNumber;
        this.balance = balance;
    }

    public String getAccountNumber() { return this.accountNumber; }
    public int getBalance() { return this.balance; }

    @Override
    public boolean equals(Object o) {
        // 1. 自分自身と同じ場所（メモリ）を指してたら即座にtrue
        if (this == o) {
            return true;
        }

        // 2. 相手がBankaccount型であるか確認
        if (o instanceof Bankaccount) {
            // 3. Object型をBankaccount型に変換（キャスト）
            Bankaccount a = (Bankaccount) o;

            // 4. お互いの口座番号から空白を削る
            String s1 = this.accountNumber.trim();
            String s2 = a.getAccountNumber().trim(); // 相手の番号を取得

            // 5. 文字列の中身を比較
            return s1.equals(s2);
        }

        // 6. 型が違うか、中身が違えばfalse
        return false;
    }

    // 問題①の「System.out.println(a)」で表示を変えるためのメソッド
    @Override
    public String toString() {
        return "¥" + this.balance + "（口座番号：" + this.accountNumber + "）";
    }
}


    

