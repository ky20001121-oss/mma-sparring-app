package p15;

public class E15_2 {

    // 【メインの内側】：プログラムの「実行ボタン」を押したときに動く場所
    public static void main(String[] args) {
        
        // 1. 材料を用意する（変数定義）
        String folder = "c:|user|";
        String file = "readme.text";

        // 2. 「外側」にある仕組み（concatPath）を呼び出す
        // 戻ってきた文字列を、そのまま System.out.println で表示する
        System.out.println(concatPath(folder, file));
        
    } // mainメソッドはここで終了

    // 【メインの外側】：いつでも呼び出せる「共通の道具（メソッド）」を定義する場所
    // static：インスタンスを作らずにすぐ使える
    // String：最後は必ず「文字列」を返すと宣言している
    public static String concatPath(String folder, String file) {
        
        // 3. 渡された材料（folder）の中身をチェックする
        // もし末尾が「|」で終わっていない（!）なら
        if (!folder.endsWith("|")) {
            // 間に「|」を補う
            folder = folder + "|";
        }
        
        // 4. 合体させた結果を「メイン」に持ち帰る（return）
        return folder + file;
        
    } // concatPathメソッドはここで終了

} // E15_2クラスはここで終了
