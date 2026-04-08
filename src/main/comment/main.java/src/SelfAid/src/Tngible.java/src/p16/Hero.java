package p16;

import java.util.ArrayList; // ArrayListを使うための準備
import java.util.List;      // List（インターフェース）を使うための準備
import java.util.Map;

public class Hero {
    
    // --- 1. 設計図（フィールド） ---
    // このクラスから作られる「実体（インスタンス）」が持つデータ
    String name;

    // --- 2. コンストラクタ ---
    // new E16_2("A") とした時に、名前をセットするための特別なメソッド
    public Hero(String name) { 
        this.name = name; 
    }

    // --- 3. メソッド ---
    // 名前を取り出すための道具
    public String getName() { 
        return name; 
    }

    // --- 4. 実行用メインメソッド ---
    public static void main(String[] args) {
        
        // ① 実体（インスタンス）を2つ作成
        Hero a = new Hero("A");
        Hero b = new Hero("B");

        // ② ArrayList（可変長の配列）を用意
        // <E16_2> は「この箱には E16_2 型だけ入れるよ」という宣言
        List<Hero> list = new ArrayList<>();

        // ③ リストに詰め込む
        list.add(a);
        list.add(b);
        
        // ④ 拡張for文で1つずつ取り出して表示
        // 「listの中身を1つずつ e という変数に代入して、ループを回してね」という命令
        for (Hero e : list) {
            System.out.println(e.getName());
        }

        Hero h1=new Hero("スズキ");
        Hero h2=new Hero("斎藤");

         Map<Hero,Integer> HeroKills=new java.util.HashMap<>();
            HeroKills.put(h1, 5);
            HeroKills.put(h2, 3);

            for(Hero h : HeroKills.keySet()){
                int kills=HeroKills.get(h);
                System.out.println(h.getName()+"は"+kills+"人倒した");

            }
    }

    
}
